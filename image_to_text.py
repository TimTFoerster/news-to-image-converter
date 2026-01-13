from PIL import Image, ImageOps

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

def get_resized_image(img:Image, factor:float) -> Image:
    width, height = img.size
    new_size = int(width*factor), int(height*factor)
    return ImageOps.contain(img, new_size)

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

image = Image.open("trump.webp")
resized_image = get_resized_image(image, 0.4)
recolored_image = get_recolored_image(resized_image, console_colors)
recolored_image.save("trump_console.webp")
