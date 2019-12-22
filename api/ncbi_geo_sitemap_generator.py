
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

xml_file_base = "sitemap{}.xml"
client = Elasticsearch('su07:9199')
index = 'ncbi_geo'

search = Search(using=client, index=index)
ids = sorted([doc.meta.id for doc in search.scan()], key=lambda esid: int(esid[3:]))


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


id_sectioned = list(chunks(ids, 50000))

for index, id_list in enumerate(id_sectioned):

    xml_file = xml_file_base.format(index)
    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for id in id_list:
        url = ET.SubElement(urlset, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = "https://discovery.biothings.io/metadata/geo/" + id

    ET.ElementTree(urlset).write(xml_file, encoding="UTF-8", xml_declaration=True)

    bs = BeautifulSoup(open(xml_file), 'xml')
    with open(xml_file, 'w', encoding='utf-8') as file:
        file.write(bs.prettify())
