from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

while True:
    with canvas(device) as draw:
        draw.text((0, 0), "SSD1306 OK!", fill=255)
        draw.text((0, 16), "Hello Raspberry Pi", fill=255)
    time.sleep(1)

