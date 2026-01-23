# colors
GRAY    = 30
RED     = 31
GREEN   = 32
YELLOW  = 33
BLUE    = 34
MAGENTA = 35
CYAN    = 36
WHITE   = 37

# styles
RESET   = 0
BOLD    = 1
UNDERLINE = 4
BLINK   = 5
REVERSE = 7

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

for idx, color in enumerate(list(console_colors_codes.keys())):
    print(f"\033[{RESET};{color}mFarbe {idx+1}\033[0m")