from PIL import Image, ImageDraw, ImageFont
import json
from requests import get
from math import ceil

def load(content, name):
    with open(f"./{content}/{name}/info.json") as f:
        return json.load(f)
    
def GetCover(content, name):
    return Image.open(f"./{content}/{name}/cover.png")

def resize(img, width, height):

    current_width, current_height = img.size
    while current_width > width and current_height > height:
        current_width *= 0.98
        current_height *= 0.98
    
    while current_width < width and current_height < height:
        current_width *= 1.02
        current_height *= 1.02

    img = img.resize((int(current_width), int(current_height)))

    return img

def get_dimensions_of_text(draw, text, font):
    left, top, right, bottom = draw.textbbox((0, 0), text, font)
    return (right - left), (bottom - top)

def MakeBase(width, height, BaseColour):
    
    return Image.new("RGB", (width, height), BaseColour)

def AddCoverArt(img, cover, width, height, x, y):
    cover = resize(cover, width, height)

    CurrentWidth, CurrentHeight = cover.size
    left = int(x - CurrentWidth / 2)
    top = int(y - CurrentHeight / 2)

    img.paste(cover, (left, top))
    return img

def AddText(img, text, x, y, FontType, TextColour, size, capwidth=False):

    draw = ImageDraw.Draw(img)

    text_font = ImageFont.truetype(f"Fonts\Panton-{FontType}.otf", size)
    w, h = get_dimensions_of_text(draw, text, text_font)
    while capwidth and w > WIDTH * 0.85:
        size *= 0.95
        text_font = ImageFont.truetype(f"Fonts\Panton-{FontType}.otf", int(size))
        w, h = get_dimensions_of_text(draw, text, text_font)
        
    draw.text((x, y - h / 2), text, TextColour, font=text_font)

    return img

def AddAlbumInfo(img, info, isDark):

    img = AddText(
        img,
        info["name"],
        WIDTH * 0.073,
        HEIGHT * 0.68,
        "Bold",
        BLACK,
        200,
        capwidth=True
    )

    img = AddText(
        img,
        info["artist"],
        WIDTH * 0.078,
        HEIGHT * 0.738,
        "Bold" if isDark else "Regular",
        BLACK,
        105
    )

    LeftMargin = 0
    for index, track in enumerate(info["tracks"]):
        pos = index
        if (index >= len(info["tracks"]) / 2):
            index -= ceil(len(info["tracks"]) / 2)
            LeftMargin = WIDTH * 0.4

        img = AddText(
            img,
            f"{pos + 1}. {track['name']}",
            LeftMargin + WIDTH * 0.08,
            HEIGHT * 0.78 + HEIGHT * (0.203 / (ceil(len(info["tracks"]) / 2))) * index,
            "Bold" if isDark else "Regular",
            BLACK,
            80 - len(info["tracks"])
        )


    return img

def save(img, content, name):
    filename = f"./{content}/{name}/design.png"
    print(f"Saving {name}")
    img.save(filename)


WIDTH = 2480
HEIGHT = 3508

CREAM = 249,226,177,255
WHITE = 255,255,255,255
RED = 160,00,0,255

BLACK = 0,0,0,0

DarkColours = [RED]

content = "Albums"
name = "Speak Your Mind (Deluxe)"
colour = CREAM

import GetInfo

if __name__ == "__main__":

    # content, name = GetInfo.main()
    # colour = eval(input("Choose colour: ").upper())

    info = load(content, name)

    img = MakeBase(WIDTH, HEIGHT, colour)

    cover = GetCover(content, name)
    
    img = AddCoverArt(img, cover, WIDTH * 0.82, WIDTH * 0.82, WIDTH * 0.5, WIDTH * 0.5)

    img = AddAlbumInfo(img, info, colour in DarkColours)

    save(img, content, name)