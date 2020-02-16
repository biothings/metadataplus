"""
    Generate ImmPort Sitemap

    Use known ID file.

"""

import csv
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup


def main():

    with open(__file__[:-3] + '.txt', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        ids = [row[0] for row in reader][1:]

    xml_file = "sitemap_immport.xml"

    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for id_ in ids:
        url = ET.SubElement(urlset, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = "https://metadataplus.biothings.io/immport/" + id_

    ET.ElementTree(urlset).write(xml_file, encoding="UTF-8", xml_declaration=True)

    bs = BeautifulSoup(open(xml_file), 'xml')
    with open(xml_file, 'w', encoding='utf-8') as file:
        file.write(bs.prettify())


if __name__ == "__main__":
    main()
