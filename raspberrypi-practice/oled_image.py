import time
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

OLED_ADDR = 0x3C

serial = i2c(port=1, address=OLED_ADDR)
device = ssd1306(serial)

def load_img(path, size=None):
    img = Image.open(path).convert("L")
    if size:
        img = img.resize(size)
    img = img.convert("1")
    return img

img_full1 = load_img("이미지 경로를 붙여 넣으세요", size=(device.width, device.height))
img_full2 = load_img("이미지 경로를 붙여 넣으세요", size=(device.width, device.height))

while True:
    device.display(img_full1)
    time.sleep(1)
    device.display(img_full2)
    time.sleep(1)