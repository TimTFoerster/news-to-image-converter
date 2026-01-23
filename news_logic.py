import feedparser
from bs4 import BeautifulSoup
from PIL import Image
import html

# ---------- FEEDS ----------

TAGESSCHAU = "https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml"

news_characters = {
    "trump ": "donald1.webp",
    "merz ": "burns3.webp",
    "usa ": "Homer.jpg",
    "us ": "Homer.jpg",
    "afd ": "afd-schnitzel.jpg"
}

# ---------- COLORS ----------

RGB_GRAY    = (135, 135, 135)
RGB_RED     = (215, 89, 89)
RGB_GREEN   = (13, 188, 121)
RGB_YELLOW  = (229, 229, 16)
RGB_BLUE    = (78, 142, 211)
RGB_MAGENTA = (195, 83, 195)
RGB_CYAN    = (17, 168, 205)
RGB_WHITE   = (229, 229, 229)

console_colors = [
    RGB_GRAY, RGB_RED, RGB_GREEN, RGB_YELLOW,
    RGB_BLUE, RGB_MAGENTA, RGB_CYAN, RGB_WHITE
]

# ---------- HELPERS ----------

def extract_text(entry) -> str:
    if hasattr(entry, "content"):
        soup = BeautifulSoup(entry.content[0].value, "html.parser")
        return "\n".join(p.get_text() for p in soup.find_all("p"))
    return entry.description


def calc_diff(c1, c2):
    return sum(abs(c1[i] - c2[i]) for i in range(3))


def closest_color(color):
    return min(console_colors, key=lambda c: calc_diff(color, c))


def recolor_image(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            pixels[x, y] = closest_color(pixels[x, y])

    return img


def image_to_colored_html(img: Image.Image, text: str) -> str:
    pixels = img.load()
    w, h = img.size
    text = html.escape(text.replace("\n", " "))
    idx = 0

    lines = []

    for y in range(h):
        line = ""
        for x in range(w):
            if idx >= len(text):
                break
            r, g, b = pixels[x, y]
            char = text[idx]
            line += (
                f'<span style="color: rgb({r},{g},{b})">'
                f'{char}</span>'
            )
            idx += 1
        lines.append(line)

    return "<br>".join(lines)


# ---------- MAIN API ----------

def get_articles():
    feed = feedparser.parse(TAGESSCHAU)
    articles = []

    for entry in feed.entries:
        title = entry.title
        description = entry.description
        text = extract_text(entry)

        image_file = None
        check = (title + " " + description).lower()

        for tag, img in news_characters.items():
            if tag in check or tag.strip() + "." in check:
                image_file = img
                break

        html_image_text = ""

        if image_file:
            img = Image.open(f"assets/{image_file}")
            img = img.resize((290, int(img.height * 300 / img.width / 2)))
            img = recolor_image(img)
            html_image_text = image_to_colored_html(img, text * 100)

        articles.append({
            "title": title,
            "description": description,
            "html": html_image_text
        })

    return articles
