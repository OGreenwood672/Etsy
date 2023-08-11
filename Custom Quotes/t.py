from PIL import Image, ImageDraw, ImageFont


def MakeBase(width, height, BaseColour):
    
    return Image.new("RGB", (width, height), BaseColour)

def get_dimensions_of_text(draw, text, font):
    left, top, right, bottom = draw.textbbox((0, 0), text, font)
    return (right - left), (bottom - top)

def AddText(img, text, x, y, font, TextColour, size):

    draw = ImageDraw.Draw(img)

    text_font = ImageFont.truetype(f"./Fonts/{font}", size)
    w, h = get_dimensions_of_text(draw, text, text_font)
    draw.text((x - w / 2, y - h / 2), text, TextColour, font=text_font)

    return img


def save(img, name):
    #filename = f"./Results/{len(os.listdir('./Results'))}.png"
    filename = f"./Results/{name}.png"
    print("[Saved]")
    img.save(filename)


WIDTH = 2480
HEIGHT = 3508

BORDER = 0.1

BLACK = 0,0,0,0

WARM_IVORY = 239, 224, 205, 255
ANGEL_BLUE = 150, 174, 208, 255
SPRING_GREEN = 236, 235, 189, 255
SNOW_WHITE = 242, 240, 235, 255
POSIDEAN = 19, 57, 85, 255
ANTIQUE_STEEL = 177, 182, 183, 255
NEUTRAL_GREY = 130, 131, 130, 255
EMINENCE = 108, 48, 130, 255
REBECCA_PURPLE = 102, 51, 153, 255

fonts = {
    1: "GreatVibes-Regular.ttf",
    2: "Jack of Gears Regular.ttf",
    3: "PIXY.ttf",
    4: "Raleway-Heavy.ttf",
    5: "Sovranix-Medium.ttf"
}


if __name__ == "__main__":

    img = MakeBase(WIDTH, HEIGHT, SNOW_WHITE)

    quote = "This is how this font looks."

    H = HEIGHT * 0.21
    for i in range(5):

        img = AddText(
            img,
            f"{i+1}. {quote}",
            WIDTH * 0.5,
            H,
            fonts[i + 1],
            BLACK,
            150 if i else 180,
        )
        H += HEIGHT * 0.13

    save(img, 20)