import json
import os
import smtplib
import urllib.request
import xml.etree.ElementTree as ET
from email.message import EmailMessage

url = "https://feeds.bbci.co.uk/news/rss.xml"
with urllib.request.urlopen(url) as response:
    tree = ET.parse(response)

items = tree.getroot().findall("./channel/item")[:3]
stories = []
for item in items:
    stories.append(f"- {item.find('title').text} ({item.find('link').text})")
headlines = "\n".join(stories)

prompt = (
    "Here are today's top 3 news stories with links:\n\n"
    + headlines
    + "\n\nWrite a short morning briefing. For each story, say what happened "
    "in one or two sentences, and note any possible market impact. "
    "Keep it plain and simple."
)

request = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps({
        "model": "claude-haiku-4-5",
        "max_tokens": 800,
        "messages": [{"role": "user", "content": prompt}],
    }).encode(),
    headers={
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
)
with urllib.request.urlopen(request) as response:
    result = json.load(response)
summary = result["content"][0]["text"]
print(summary)

msg = EmailMessage()
msg["Subject"] = "Your morning news recap"
msg["From"] = "walbanos@gmail.com"
msg["To"] = "walbanos@gmail.com"
msg.set_content(summary)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login("walbanos@gmail.com", os.environ["GMAIL_APP_PASSWORD"])
    server.send_message(msg)
