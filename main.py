import time
import os
import feedparser
from bs4 import BeautifulSoup
from PIL import Image

# Constants
DELAY = 0.5
DELAY_LONG = 1.5
DELAY_LINE = 0.05

NORMAL_IMAGE = 0
SATIRE_IMAGE = 1

# colors
GRAY    = 30
RED     = 31
GREEN   = 32
YELLOW  = 33
BLUE    = 34
MAGENTA = 35
CYAN    = 36
WHITE   = 37

# colors in RGB
RGB_GRAY    = (135, 135, 135)
RGB_RED     = (215, 89, 89)
RGB_GREEN   = (13, 188, 121)
RGB_YELLOW  = (229, 229, 16)
RGB_BLUE    = (78, 142, 211)
RGB_MAGENTA = (195, 83, 195)
RGB_CYAN    = (17, 168, 205)
RGB_WHITE   = (229, 229, 229)

# styles
RESET   = 0
BOLD    = 1
UNDERLINE = 4
BLINK   = 5
REVERSE = 7

# Links
TAGESSCHAU = "https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml"
TAGESSCHAU_MORSS = "https://morss.it/https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml"
BBC = "https://morss.it/https://feeds.bbci.co.uk/news/world/rss.xml"

console_colors_rgb = {
    "gray": RGB_GRAY,
    "red": RGB_RED,
    "green": RGB_GREEN,
    "yellow": RGB_YELLOW,
    "blue": RGB_BLUE,
    "magenta": RGB_MAGENTA,
    "cyan": RGB_CYAN,
    "white": RGB_WHITE
}

console_colors_codes = {
    GRAY: "gray",
    RED: "red", 
    GREEN: "green",
    YELLOW: "yellow",
    BLUE: "blue",
    MAGENTA: "magenta",
    CYAN: "cyan",
    WHITE: "white"
}

news_characters_comic = {
    "Trump": "donald1.webp",
    "Merz": "burns2.jpg",
    "deutsch": "sandalen.jpeg",
    "Deutschland": "merkel-hand.jpeg",
    "USA": "Homer.jpg",
    "US": "Homer.jpg",
    "AfD": "bafv.jpg"
}

news_characters = {
    "Trump": "trump.webp",
    "Merz": "merz.jpg",
    "deutsch": "deutschland.jpg",
    "Deutschland": "merkel.webp",
    "USA": "trump3.webp",
    "US": "trump3.webp",
    "AfD": "afd.jpg"
}

news_keywords = {
    "Deutschland": ["Deutschland", "deutsch", "deutsche", "deutschen", "deutscher", "Deutsche", "Deutschen", "Deutscher", "Deutsch"],
    "Merz": ["Merz", "Bundeskanzler"],
    "USA": ["USA", "US", "Amerikaner"],
    "Trump": ["Trump", "US-Präsident"],
    "AfD": ["AfD"],
    "Weidel": ["Weidel"], 
    "CSU": ["Söder", "CSU", "Bayern", "Bayerisch", "Bayerische", "Bayerischer", "bayerisch", "bayerische", "bayerischer"]
}

news_images = {
    "Trump": ["trump.webp", "donald1.webp"],
    "Merz": ["merz.jpg", "burns2.jpg"],
    "Deutschland": ["merkel.webp", "merkel-hand.jpeg"],
    "USA": ["trump3.webp", "Homer.jpg"],
    "AfD": ["afd.jpg", "darth.jpg"],
    "Weidel": ["Aliceweidel.webp", "Aliceweidel.webp"], # 2. Bild suchen
    "CSU": ["maggus.jpg", "maggus-essen2.jpg"]
}

# x = os.get_terminal_size().lines
terminal_width = os.get_terminal_size().columns

def get_articles(source:str):
    print("Loading news feed...")
    feed = feedparser.parse(source)
    articles = []

    for entry in feed.entries:
        title = entry.title
        description = entry.description
        text = str(entry.content[0])
        text_stripped = extract_text_from_feed(text)

        articles.append({
            "title": title,
            "description": description,
            "text": text_stripped
        })

    return articles

def extract_text_from_feed(text:str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    news_paragraphs = soup.find_all("p")
    news_content_from_paragraphs = ""
    for p in news_paragraphs:
        news_content_from_paragraphs += p.get_text() # nur Text aus <p> auslesen
    news_content_stripped = news_content_from_paragraphs.strip("\n                       ") # komische Absätze entfernen

    return news_content_stripped

color_codes = [num for num in range(30, 38)]
style_codes = [0, 1, 4, 7]
console_colors = [RGB_GRAY,
              RGB_RED,
              RGB_GREEN,
              RGB_YELLOW,
              RGB_BLUE,
              RGB_MAGENTA,
              RGB_CYAN,
              RGB_WHITE]

def calc_absolute_diff_of_colors(color1:tuple[int], color2:tuple[int]) -> int:
    total_diff = []
    for i in range(3):
        diff = abs(color1[i] - color2[i])
        total_diff.append(diff)
    return tuple(total_diff)

def get_closest_color_from_palette(target_color:tuple[int], colors:list[tuple[int]]) -> tuple:
    diffs_from_colors = [calc_absolute_diff_of_colors(target_color, color) for color in colors]
    min_diff = 3*255
    for idx, diff in enumerate(diffs_from_colors):
        total_diff = (diff[0] + diff[1] + diff[2])
        if total_diff < min_diff:
            min_diff = total_diff
            idx_min_diff = idx
    closest_color = colors[idx_min_diff]
    return closest_color

def get_resized_image_rel(img:Image, factor:float) -> Image:
    width, height = img.size
    new_width = int(width * factor)
    new_height = int(height * factor / 2)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def get_resized_image_abs(img:Image, new_width:int) -> Image:
    width, height = img.size
    factor = new_width / width
    new_height = int(height * factor / 2)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def get_recolored_image(img:Image, color_palette:list[tuple[int]]) -> Image:
    width, height = img.size
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            source_color = pixels[x, y] # read image colors
            if type(source_color) != tuple:
                continue
            closest_color = get_closest_color_from_palette(source_color, color_palette) # convert to console color palette
            pixels[x, y] = closest_color # write
    return img

def convert_colors_to_console_colors_from_path(source_img_path:str) -> str:
    img = Image.open(source_img_path)
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            source_color = pixels[x, y] # read image colors
            closest_color = get_closest_color_from_palette(source_color, console_colors) # convert to console color palette
            pixels[x, y] = closest_color # write 
    
    filename_and_extension = source_img_path.split(".")
    filename = filename_and_extension[0]
    extension = filename_and_extension[1]
    target_img_path = filename + "_console" + "." + extension
    
    img.save(target_img_path)

def get_key_from_value(value, dictionary:dict) -> str:
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    key_idx = values.index(value)
    return keys[key_idx]

def duplicate_text_for_image(width:int, height:int, text:str) -> str:
    chars_needed = width * height
    output_text = text
    while len(output_text) < chars_needed:
        output_text += text
    return output_text

def print_text_from_image(image:Image, text:str) -> None:
    pixels = image.load()
    width, height = image.size

    text_cleaned = text.strip("\n")
    text_long_enough = duplicate_text_for_image(width, height, text_cleaned)

    output_lines = []
    text_counter = 0
    for y in range(height):
        output_text = ""
        for x in range(width):
            source_color = pixels[x, y]
            color_name = get_key_from_value(source_color, console_colors_rgb)
            color_code = get_key_from_value(color_name, console_colors_codes)
            output_text += f"\033[{RESET};{color_code}m{text_long_enough[text_counter]}\033[0m"

            text_counter += 1
        output_lines.append(output_text)

    for line in output_lines:
        # for character in line:
        #     print(character, end="")
        #     time.sleep(0.01)
        print(line) # Artikel
        time.sleep(DELAY_LINE)

def get_image_category_from_text(description:str, headline:str, keywords_dict:dict) -> str:
    image_category = None

    for key, keyword_list in keywords_dict.items():
        for keyword in keyword_list:
            if keyword in headline:
                image_category = key
            elif keyword in description:
                image_category = key

    return image_category


image_file = None
while not image_file:

    news_articles = get_articles(TAGESSCHAU)
    for news_article in news_articles:
        headline = news_article["title"]
        description = news_article["description"]
        text = news_article["text"]

        image_category = get_image_category_from_text(description, headline, news_keywords)
        if not image_category:
            continue
        image_file = news_images[image_category][NORMAL_IMAGE]

        image = Image.open("assets/" + image_file)
        resized_image = get_resized_image_abs(image, terminal_width) # 300
        recolored_image = get_recolored_image(resized_image, console_colors)
        # recolored_image.save("Homer_console.jpg")

        print(f"\033[{BOLD};{YELLOW}m{headline}\033[0m") # Überschrift
        time.sleep(DELAY)
        print(f"\033[{RESET};{YELLOW}m{description}\033[0m") # Beschreibung
        time.sleep(DELAY_LONG)
        print_text_from_image(recolored_image, 100*text)
        image_category = get_image_category_from_text(description, headline, news_keywords)
        image_file = news_images[image_category][SATIRE_IMAGE]
        image = Image.open("assets/" + image_file)
        resized_image = get_resized_image_abs(image, terminal_width)
        recolored_image = get_recolored_image(resized_image, console_colors)
        time.sleep(DELAY)
        print("...")
        print_text_from_image(recolored_image, 100*text)
        time.sleep(DELAY)
        print("...")
        time.sleep(DELAY)
        print("loading new article...")
        time.sleep(DELAY)
        print("...")
        time.sleep(DELAY)

        image_file = None