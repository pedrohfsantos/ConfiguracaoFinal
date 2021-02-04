import datetime
import xml.etree.cElementTree as ET
from tqdm.auto import tqdm
from xml.dom import minidom


class Sitemap:
    def __init__(self, log):
        self.log = log

    def gerador_sitemap_xml(urls, caminho):
        urlset = ET.Element("urlset")
        urlset.attrib["xmlns"] = "http://www.sitemaps.org/schemas/sitemap/0.9"

        for url in tqdm(urls):
            dt = datetime.datetime.now().strftime("%Y-%m-%d")
            item = ET.SubElement(urlset, "url")
            ET.SubElement(item, "loc").text = url
            ET.SubElement(item, "lastmod").text = dt
            ET.SubElement(item, "changefreq").text = "daily"
            ET.SubElement(item, "priority").text = "1.0" if url == urls[0] else "0.9"

        xmlstr = minidom.parseString(ET.tostring(urlset, encoding="utf-8")).toprettyxml(indent="   ")
        xmlstr = xmlstr.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="utf-8"?>')
        with open(f"{caminho}/sitemap.xml", "w", encoding="utf-8") as f:
            f.write(xmlstr)
