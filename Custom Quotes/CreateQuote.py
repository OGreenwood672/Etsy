from PIL import Image, ImageDraw, ImageFont


def MakeBase(width, height, BaseColour):
    
    return Image.new("RGB", (width, height), BaseColour)

def get_dimensions_of_text(draw, text, font):
    left, top, right, bottom = draw.textbbox((0, 0), text, font)
    return (right - left), (bottom - top)

def AddText(img, text, pos, limit, font, TextColour, size, quotee=None):

    draw = ImageDraw.Draw(img)

    text_font = ImageFont.truetype(f"./Fonts/{font}", size)
    w, _ = get_dimensions_of_text(draw, text, text_font)

    lines = [text]
    while w > limit:
        words = []
        for word in lines[-1].split():
            words.append(word)
            w, h = get_dimensions_of_text(draw, ' '.join(words), text_font)
            if w > limit:
                CurrentLine = lines.pop()
                lines.append(' '.join(words[:-1]))
                lines.append(' '.join(CurrentLine.split()[len(words) - 1:]))
                break
        w, h = get_dimensions_of_text(draw, lines[-1], text_font)

    if quotee:
        lines.extend(["", f" - {quotee}"])

    x = 0.5 * WIDTH
    y = 0.5 * HEIGHT
    dX = lambda x: - x / 2
    dH = len(lines) * size * -0.5

    if "right" in pos:
        dX = lambda x: - x
        x = (1 - BORDER) * WIDTH
    if "left" in pos:
        dX = lambda x: 0
        x = BORDER * WIDTH
    if "top" in pos:
        dH = 0
        y = BORDER * HEIGHT
    if "bottom" in pos:
        dH = len(lines) * size * -1
        y = (1 - BORDER) * HEIGHT

    for line in lines:
        w, h = get_dimensions_of_text(draw, line, text_font)
        draw.text((x + dX(w), y + dH), line, TextColour, font=text_font)
        dH += size

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


FontSize = 165

limit = WIDTH * 0.6

if __name__ == "__main__":

    name = input("Name:")
    position = input("Position: ")
    colour = eval(input("Colour: ").upper().replace(" ", "_"))
    font = fonts[int(input("Font (1-5): "))]
    quote = input("Quote: ")
    if input("Author y/n: ") == "y":
        author = input("Author: ")
    else:
        author = None

    # name = 6
    # position = "bottom left"
    # colour = ANTIQUE_STEEL
    # font = fonts[3]
    # quote = "You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose."
    # author = "Dr. Seuss"
    
    img = MakeBase(WIDTH, HEIGHT, colour)

    img = AddText(
        img,
        quote,
        position,
        limit,
        font,
        BLACK,
        FontSize,
        author
    )

    save(img, name)