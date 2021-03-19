import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw


def overlay_img_with_xml(image_path: Path, xml_path: Path, output_path: Path):
    output_path.mkdir(exist_ok=True)
    polygons = get_polygons_from_xml(xml_path=xml_path)
    colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
              (255, 255, 255)]
    with Image.open(str(image_path)) as f:
        for i, polygon in enumerate(polygons):
            img = ImageDraw.Draw(f)
            color = colors[i % len(colors)]
            img.line(polygon, fill=color, width=5)
        f.save(output_path / 'output.png')


def get_polygons_from_xml(xml_path: Path):
    ns = '{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}'
    # load xml
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    page_part = root[1]
    polygons = []
    # parse out the polygons
    for text_region in page_part:
        for text_line in text_region.findall(ns + 'TextLine'):
            polygon_text = text_line.find(ns + 'Coords').attrib['points']
            polygons.append([tuple(map(int, pr.split(','))) for pr in polygon_text.split(' ')])

    return polygons


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image_path', type=Path, required=True, help='Path to the image')
    parser.add_argument('-x', '--xml_path', type=Path, required=True, help='Path to the page xml')
    parser.add_argument('-o', '--output_path', type=Path, required=True, help='Path to the output folder')

    args = parser.parse_args()

    overlay_img_with_xml(**args.__dict__)
