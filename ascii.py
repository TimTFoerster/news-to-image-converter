from PIL import Image

chars='$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~i!lI;:,"^`'

def load_image(source_img_path:str) -> str:
    img = Image.open(source_img_path)
    return img

def get_resized_image_rel(img:Image.Image, factor:float) -> Image:
    width, height = img.size
    new_width = int(width * factor)
    new_height = int(height * factor / 2)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def convert_image_to_ascii(img:Image.Image) -> str:
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            source_color = pixels[x, y] # read image colors
            
            pixels[x, y] = closest_color # write 
    
    filename_and_extension = source_img_path.split(".")
    filename = filename_and_extension[0]
    extension = filename_and_extension[1]
    target_img_path = filename + "_console" + "." + extension
    
    img.save(target_img_path)