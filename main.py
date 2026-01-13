import time
import feedparser
from bs4 import BeautifulSoup
from PIL import Image

print("Loading news feed...")

tagesschau = feedparser.parse("https://morss.it/https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml")
bbc = feedparser.parse("https://morss.it/https://feeds.bbci.co.uk/news/world/rss.xml")
news_feed = tagesschau


# news_title = news_feed.entries[0].title
# news_description = news_feed.entries[0].description
# news_content = news_feed.entries[0].content[0]
# soup = BeautifulSoup(str(news_content), "html.parser")
# news_paragraphs = soup.find_all("p")
# news_content_from_paragraphs = ""
# for p in news_paragraphs:
#     news_content_from_paragraphs += p.get_text() # nur Text aus <p> auslesen

# news_content_stripped = news_content_from_paragraphs.strip("\n                       ") # komische Absätze entfernen

def get_news_text_from_feed(feed:feedparser.FeedParserDict, entry_no:int) -> str:
    news_content = feed.entries[entry_no].content[0]
    soup = BeautifulSoup(str(news_content), "html.parser")
    news_paragraphs = soup.find_all("p")
    news_content_from_paragraphs = ""
    for p in news_paragraphs:
        news_content_from_paragraphs += p.get_text() # nur Text aus <p> auslesen

    news_content_stripped = news_content_from_paragraphs.strip("\n                       ") # komische Absätze entfernen

    return news_content_stripped

def get_news_headline_from_rss(feed:feedparser.FeedParserDict, entry_no:int) -> str:
    return feed.entries[entry_no].title

def get_news_description_from_rss(feed:feedparser.FeedParserDict, entry_no:int) -> str:
    return feed.entries[entry_no].description

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

console_colors_rgb = {
    "gray": (135, 135, 135),
    "red": (215, 89, 89),
    "green": (13, 188, 121),
    "yellow": (229, 229, 16),
    "blue": (78, 142, 211),
    "magenta": (195, 83, 195),
    "cyan": (17, 168, 205),
    "white": (229, 229, 229)
}

# console_colors_codes = {
#     "gray": 30,
#     "red": 31,
#     "green": 32,
#     "yellow": 33,
#     "blue": 34,
#     "magenta": 35,
#     "cyan": 36,
#     "white": 37
# }

console_colors_codes = {
    30: "gray",
    31: "red", 
    32: "green",
    33: "yellow",
    34: "blue",
    35: "magenta",
    36: "cyan",
    37: "white"
}

news_characters = {
    "trump ": "donald1.webp",
    "merz ": "burns3.webp",
    "usa ": "Homer.jpg",
    "afd ": "afd-schnitzel.jpg"
}

# styles
RESET   = 0
BOLD    = 1
UNDERLINE = 4
BLINK   = 5
REVERSE = 7


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

def print_text_from_image(image:Image, text:str) -> None:
    pixels = image.load()
    width, height = image.size

    text_cleaned = text.strip("\n")

    output_lines = []
    text_counter = 0
    for y in range(height):
        output_text = ""
        for x in range(width):
            source_color = pixels[x, y]
            color_name = get_key_from_value(source_color, console_colors_rgb)
            color_code = get_key_from_value(color_name, console_colors_codes)
            output_text += f"\033[{RESET};{color_code}m{text_cleaned[text_counter]}\033[0m"

            text_counter += 1
        output_lines.append(output_text)

    for line in output_lines:
        print(line) # Artikel
        time.sleep(0.05)
        
# recolored_image.save("Homer_console.jpg")
image_file = None
while not image_file:
    for entry in range(len(tagesschau.entries)):
        entry_no = entry
        text = get_news_text_from_feed(tagesschau, entry_no)
        description = get_news_description_from_rss(tagesschau, entry_no)
        headline = get_news_headline_from_rss(tagesschau, entry_no)

        tags = list(news_characters.keys())
        for tag in tags:
            if tag in headline.lower():
                image_file = news_characters[tag]
            elif tag.removesuffix(" ") + "." in headline.lower():
                image_file = news_characters[tag]
            if not image_file:
                if tag in description.lower():
                    image_file = news_characters[tag]
                elif tag.removesuffix(" ") + "." in description.lower():
                    image_file = news_characters[tag]
        if not image_file:
            continue

        image = Image.open("assets/" + image_file)
        resized_image = get_resized_image_abs(image, 250)
        recolored_image = get_recolored_image(resized_image, console_colors)

        print(f"\033[{BOLD};{YELLOW}m{headline}\033[0m") # Überschrift
        time.sleep(2)
        print(f"\033[{RESET};{YELLOW}m{description}\033[0m") # Beschreibung
        time.sleep(2)
        print_text_from_image(recolored_image, 100*text)
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("loading new article...")
        time.sleep(2)
        print("...")
        time.sleep(2)

        image_file = None