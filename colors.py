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

console_colors = [RGB_GRAY,
              RGB_RED,
              RGB_GREEN,
              RGB_YELLOW,
              RGB_BLUE,
              RGB_MAGENTA,
              RGB_CYAN,
              RGB_WHITE]