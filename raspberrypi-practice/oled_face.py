import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

OLED_ADDR = 0x3C

serial = i2c(port=1, address=OLED_ADDR)
device = ssd1306(serial)

def draw_face(draw, x, y, good=True):
    size = 48

    draw.ellipse((x, y, x+size, y+size), outline=255, fill=0)

    ex1, ey = x + 16, y + 18
    ex2 = x + 32

    if good:
        draw.ellipse((ex1-2, ey-2, ex1+2, ey+2), fill=255)
        draw.ellipse((ex2-2, ey-2, ex2+2, ey+2), fill=255)

    else:
        draw.line((ex1-3, ey-3, ex1+3, ey+3), fill=255)
        draw.line((ex1+3, ey-3, ex1-3, ey+3), fill=255)
        draw.line((ex2-3, ey-3, ex2+3, ey+3), fill=255)
        draw.line((ex2+3, ey-3, ex2-3, ey+3), fill=255)

        draw.arc((x+12, y+26, x+36, y+48), start=200, end=340, fill=255)

good = True

while True:
    with canvas(device) as draw:
        draw.text((0, 0), "FACE DEMO", fill=255)
        draw_face(draw, x=40, y=12, good=good)
    good = not good
    time.sleep(1)