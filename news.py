from pyscript import Element
from js import setInterval
from pyodide.http import pyfetch
from bs4 import BeautifulSoup
from PIL import Image
import io

TAGESSCHAU_RSS = "https://morss.it/https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml"

news_characters = {
    "trump ": "donald1.webp",
    "merz ": "burns3.webp",
    "usa ": "Homer.jpg",
    "us ": "Homer.jpg",
    "afd ": "afd-schnitzel.jpg"
}

current_index = 0
entries = []


async def load_feed():
    try:
        Element("status").write("Fetching RSS feed…")
        response = await pyfetch(TAGESSCHAU_RSS)
        xml = await response.text()
        Element("status").write("RSS fetched, parsing…")

        soup = BeautifulSoup(xml, "xml")
        items = soup.find_all("item")

        global entries
        entries = items

        Element("status").write(f"Loaded {len(entries)} articles")

    except Exception as e:
        Element("status").write(f"ERROR: {e}")
        raise



def extract_text(item):
    content = item.find("content:encoded")
    if not content:
        return ""

    soup = BeautifulSoup(content.text, "html.parser")
    return "\n".join(p.get_text() for p in soup.find_all("p"))


def find_character_image(title, description):
    text = (title + " " + description).lower()
    for tag, img in news_characters.items():
        if tag in text or tag.strip() + "." in text:
            return img
    return None


def show_article():
    global current_index

    if not entries:
        return

    item = entries[current_index]
    current_index = (current_index + 1) % len(entries)

    title = item.title.text
    description = item.description.text
    text = extract_text(item)

    img = find_character_image(title, description)

    html = f"""
    <div class="headline">{title}</div>
    <div class="description">{description}</div>
    <div class="article">{text[:2000]}</div>
    """

    if img:
        html = f'<img src="assets/{img}" width="300"><br>' + html

    Element("news").write(html, clear=True)


async def start():
    await load_feed()
    show_article()
    setInterval(show_article, 30000)  # every 30 seconds


import asyncio
asyncio.ensure_future(start())
