import feedparser
from bs4 import BeautifulSoup
from PIL import Image
from typing import Optional, Tuple, List

# -------------------------
# RSS feeds
# -------------------------
tagesschau = feedparser.parse("https://morss.it/https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml")
bbc = feedparser.parse("https://morss.it/https://feeds.bbci.co.uk/news/world/rss.xml")
news_feed = tagesschau  # choose feed

# -------------------------
# Keyword → image mapping
# -------------------------
news_characters = {
    "trump": "donald1.webp",
    "merz": "burns3.webp",
    "usa": "Homer.jpg",
    "us": "Homer.jpg",
    "afd": "afd-schnitzel.jpg"
}

# -------------------------
# Console colors
# -------------------------
console_colors = [
    (135, 135, 135),  # gray
    (215, 89, 89),    # red
    (13, 188, 121),   # green
    (229, 229, 16),   # yellow
    (78, 142, 211),   # blue
    (195, 83, 195),   # magenta
    (17, 168, 205),   # cyan
    (229, 229, 229)   # white
]

# -------------------------
# Helper functions
# -------------------------

def get_news_text_from_feed(feed: feedparser.FeedParserDict, entry_no: int) -> str:
    """Extract text paragraphs from RSS feed content."""
    content = feed.entries[entry_no].get("content", [{}])
    if not content:
        return ""
    soup = BeautifulSoup(str(content[0]), "html.parser")
    paragraphs = soup.find_all("p")
    return "\n".join(p.get_text().strip() for p in paragraphs).strip()


def get_news_headline_from_rss(feed: feedparser.FeedParserDict, entry_no: int) -> str:
    return feed.entries[entry_no].title


def get_news_description_from_rss(feed: feedparser.FeedParserDict, entry_no: int) -> str:
    return feed.entries[entry_no].description


# -------------------------
# Keyword detection
# -------------------------
import re

def find_character_image(headline: str, description: str) -> Optional[str]:
    """Detect keyword in headline/description and return corresponding image."""
    text = f"{headline} {description}".lower()
    for keyword, image_file in news_characters.items():
        pattern = rf"\b{re.escape(keyword)}\b[.,!?]?"
        if re.search(pattern, text):
            return image_file
    return None


# -------------------------
# Image manipulation
# -------------------------

def get_resized_image_abs(img: Image.Image, new_width: int) -> Image.Image:
    w, h = img.size
    factor = new_width / w
    return img.resize((new_width, int(h * factor / 2)), Image.Resampling.LANCZOS)


def get_closest_color_from_palette(target_color: Tuple[int, int, int], colors: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    diffs = [sum(abs(tc - c) for tc, c in zip(target_color, color)) for color in colors]
    min_idx = diffs.index(min(diffs))
    return colors[min_idx]


def get_recolored_image(img: Image.Image, color_palette: List[Tuple[int, int, int]]) -> Image.Image:
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            pixels[x, y] = get_closest_color_from_palette(pixels[x, y], color_palette)
    return img


# -------------------------
# Main article processor
# -------------------------

def process_article(entry_no: int, assets_path: str = "assets", image_width: int = 200) -> dict:
    """Return all info needed for frontend rendering."""
    headline = get_news_headline_from_rss(news_feed, entry_no)
    description = get_news_description_from_rss(news_feed, entry_no)
    text = get_news_text_from_feed(news_feed, entry_no)

    image_file = find_character_image(headline, description)
    if image_file:
        image_path = f"{assets_path}/{image_file}"
        image = Image.open(image_path)
        resized = get_resized_image_abs(image, image_width)
        recolored = get_recolored_image(resized, console_colors)
        # Convert to HTML-friendly preformatted text
        ascii_html = image_to_html(recolored, text)
    else:
        ascii_html = "<pre></pre>"

    return {
        "title": headline,
        "description": description,
        "html": ascii_html
    }


# -------------------------
# Convert image + text to HTML (colored ASCII style)
# -------------------------

def image_to_html(img: Image.Image, text: str) -> str:
    """Convert image pixels to HTML spans colored like console, safe against IndexError."""
    pixels = img.load()
    w, h = img.size
    text = text.strip()
    if not text:
        text = " "  # fallback, falls leer

    # repeat text enough to cover all pixels
    repeat_count = (w * h + len(text) - 1) // len(text)  # ceil division
    text = (text * repeat_count)[: w * h]  # exactly w*h characters

    html = "<pre style='line-height:1; font-family: monospace;'>"
    counter = 0
    for y in range(h):
        line = ""
        for x in range(w):
            color = pixels[x, y]
            char = text[counter]
            line += f"<span style='color: rgb{color};'>{char}</span>"
            counter += 1
        html += line + "\n"
    html += "</pre>"
    return html

