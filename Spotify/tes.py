from PIL import Image

img = Image.open("./Albums/Touch Up/cover.png")

r = 0
g = 0
b = 0

w, h = img.size
for w_pixel in range(w):
    for h_pixel in range(h):
        rgb = img.getpixel((w_pixel, h_pixel))
        r += rgb[0]
        g += rgb[1]
        b += rgb[2]
x = w*h
r /= x
g /= x
b /= x


print(f"({r}, {g}, {b})")