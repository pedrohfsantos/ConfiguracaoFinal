from Class import *
from tkinter import filedialog


log = []

links = Links(log)
sitemap = Sitemap(log)


localhost = filedialog.askdirectory(title="Please select a directory")

site = links.links_site("")
sitemap.gerador_sitemap_xml(site, localhost)