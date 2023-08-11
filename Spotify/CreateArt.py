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

def GetDefaultColour(cover):
    r = g = b = 0
    w, h = cover.size
    for w_pixel in range(w):
        for h_pixel in range(h):
            rgb = cover.getpixel((w_pixel, h_pixel))
            r += rgb[0]
            g += rgb[1]
            b += rgb[2]
    area = w*h
    r /= area
    g /= area
    b /= area
    return int(r), int(g), int(b), 255


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

def AddAlbumInfo(img, info, isDark, option=3):

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

    FontType = "Bold" if isDark else "Regular"
    ColumnSize = 80 - len(info["tracks"])
    SpecialSize = 53 - len(info["tracks"])

    if option == 3:
        draw = ImageDraw.Draw(img)
        maxw = 0
        for track in info["tracks"]:
            text_font = ImageFont.truetype(f"Fonts\Panton-{FontType}.otf", ColumnSize)
            w, _ = get_dimensions_of_text(draw, track["name"], text_font)
            if w > maxw: maxw = w
        if maxw > WIDTH * 0.365:
            option = 2
        else: option = 1
    
    if option == 1:
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
                FontType,
                BLACK,
                ColumnSize
            )
    else:
        for index, track in enumerate(info["tracks"]):

            img = AddText(
                img,
                f"{index + 1}. {track['name']}",
                WIDTH * 0.05,
                HEIGHT * 0.78 + HEIGHT * (0.203 / len(info["tracks"])) * index,
                "Bold",
                BLACK,
                SpecialSize
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
PINK = 255,204,255,255
DEFAULT = -1
COMPLEMENTARY = -2

BLACK = 0,0,0,0

DarkColours = [RED]

COLUMNS = 1
SPECIAL = 2
AUTO = 3

# content = "Albums"
# name = "Good & Evil"
# colour = WHITE
# format = AUTO

import GetInfo

if __name__ == "__main__":

    content, name = GetInfo.main()
    colour = eval(input("Choose colour: ").upper())
    format = eval(input("Would you like the format COLUMNS or SPECIAL: ").upper())

    info = load(content, name)

    cover = GetCover(content, name)
    if colour == DEFAULT:
        colour = GetDefaultColour(cover)
    elif colour == COMPLEMENTARY:
        r, g, b, a = GetDefaultColour(cover)
        colour = 255 - r, 255 - g, 255 - b, a

    img = MakeBase(WIDTH, HEIGHT, colour)
    
    img = AddCoverArt(img, cover, WIDTH * 0.82, WIDTH * 0.82, WIDTH * 0.5, WIDTH * 0.5)

    img = AddAlbumInfo(img, info, colour in DarkColours, format)

    save(img, content, name)