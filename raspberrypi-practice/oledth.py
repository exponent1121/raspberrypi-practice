import time
import board
import adafruit_shtc3
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

OLED_ADDR = 0x3C        
UPDATE_SEC = 1.0      

TEMP_OK = (20.0, 26.0)
HUM_OK  = (40.0, 60.0)

def comfort_state(t, h):
    good = (TEMP_OK[0] <= t <= TEMP_OK[1]) and (HUM_OK[0] <= h <= HUM_OK[1])
    return "GOOD" if good else "BAD"

# OLED
serial = i2c(port=1, address=OLED_ADDR)
device = ssd1306(serial)

# SHTC3
i2c_bus = board.I2C()
sensor = adafruit_shtc3.SHTC3(i2c_bus)

def draw_face(draw, x, y, good=True):
    size = 48

    # 얼굴 테두리
    draw.ellipse((x, y, x+size, y+size), outline=255, fill=0)

    # 눈 위치
    ex1, ey = x + 16, y + 18
    ex2 = x + 32

    # 눈(공통)
    draw.ellipse((ex1-2, ey-2, ex1+2, ey+2), fill=255)
    draw.ellipse((ex2-2, ey-2, ex2+2, ey+2), fill=255)

    if good:
        draw.arc((x+12, y+18, x+36, y+42), start=20, end=160, fill=255)
    else:
        draw.arc((x+12, y+26, x+36, y+48), start=200, end=340, fill=255)
        # 눈물(한 방울)
        draw.ellipse((x+34, y+26, x+38, y+34), outline=255, fill=0)

TEMP_BUF = []
HUM_BUF = []
BUF_N = 5

def smooth(buf, new, n=5):
    buf.append(new)
    if len(buf) > n:
        buf.pop(0)
    return sum(buf) / len(buf)

try:
    while True:
        t = sensor.temperature
        h = sensor.relative_humidity

        t_s = smooth(TEMP_BUF, t, BUF_N)
        h_s = smooth(HUM_BUF, h, BUF_N)

        state = comfort_state(t_s, h_s)
        good = (state == "GOOD")

        reason = []
        if not (TEMP_OK[0] <= t_s <= TEMP_OK[1]):
            reason.append("TEMP")
        if not (HUM_OK[0] <= h_s <= HUM_OK[1]):
            reason.append("HUM")
        reason_txt = "OK" if not reason else " & ".join(reason)

        with canvas(device) as draw:
            draw.text((0, 0),  f"T: {t_s:4.1f}C", fill=255)
            draw.text((0, 12), f"H: {h_s:4.1f}%", fill=255)

            draw.text((0, 24), f"COMFORT: {state}", fill=255)
            draw.text((0, 36), f"CHECK: {reason_txt}", fill=255)

            draw.text((0, 52), f"T {TEMP_OK[0]}-{TEMP_OK[1]} / H {HUM_OK[0]}-{HUM_OK[1]}", fill=255)

            draw_face(draw, x=80, y=8, good=good)

        time.sleep(UPDATE_SEC)

except KeyboardInterrupt:
    pass
