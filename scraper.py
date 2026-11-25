import urllib.request
import xml.etree.ElementTree as ET

url = "https://feeds.bbci.co.uk/news/rss.xml"
with urllib.request.urlopen(url) as response:
    tree = ET.parse(response)

items = tree.getroot().findall("./channel/item")[:3]
print("Top 3 news stories:")
for i, item in enumerate(items, 1):
    print(f"{i}. {item.find('title').text}")
