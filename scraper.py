import os
import smtplib
import urllib.request
import xml.etree.ElementTree as ET
from email.message import EmailMessage

url = "https://feeds.bbci.co.uk/news/rss.xml"
with urllib.request.urlopen(url) as response:
    tree = ET.parse(response)

items = tree.getroot().findall("./channel/item")[:3]
lines = []
for i, item in enumerate(items, 1):
    lines.append(f"{i}. {item.find('title').text}")
    lines.append(f"   {item.find('link').text}")
body = "Top 3 news stories:\n\n" + "\n".join(lines)
print(body)

msg = EmailMessage()
msg["Subject"] = "Your morning news recap"
msg["From"] = "walbanos@gmail.com"
msg["To"] = "walbanos@gmail.com"
msg.set_content(body)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login("walbanos@gmail.com", os.environ["GMAIL_APP_PASSWORD"])
    server.send_message(msg)
