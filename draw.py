from errno import WSAEDQUOT
from PIL import Image, ImageDraw, ImageFont

def draw_text(text, color, output_path, background_path="background.png", font=ImageFont.truetype(r'arial.ttf', 12), starting_pos=(0,0)):
    img = Image.open(background_path)
    draw = ImageDraw.Draw(img)

    draw.text(starting_pos, str(text), fill=color, font=font)
    img.save(output_path)
