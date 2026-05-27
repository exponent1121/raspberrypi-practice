import time
import requests
import board
import adafruit_shtc3
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

OLED_ADDR = 0x3C         
OLED_UPDATE_SEC = 1.0     
SEND_INTERVAL_SEC = 10    # 텔레그램 전송 주기

TEMP_OK = (20.0, 26.0)
HUM_OK  = (40.0, 60.0)

def is_comfy(t, h):
    return (TEMP_OK[0] <= t <= TEMP_OK[1]) and (HUM_OK[0] <= h <= HUM_OK[1])

BOT_TOKEN = "사용자 토큰 "  
CHAT_ID = "사용자 id"

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, data=payload, timeout=10)
    r.raise_for_status()


# OLED
serial = i2c(port=1, address=OLED_ADDR)
device = ssd1306(serial)

# SHTC3
i2c_bus = board.I2C()
sensor = adafruit_shtc3.SHTC3(i2c_bus)


def draw_face(draw, x, y, good=True):
    size = 48
    draw.ellipse((x, y, x+size, y+size), outline=255, fill=0)

    # 눈
    ex1, ey = x + 16, y + 18
    ex2 = x + 32
    draw.ellipse((ex1-2, ey-2, ex1+2, ey+2), fill=255)
    draw.ellipse((ex2-2, ey-2, ex2+2, ey+2), fill=255)

    if good:
        draw.arc((x+12, y+18, x+36, y+42), start=20, end=160, fill=255)
    else:
        draw.arc((x+12, y+26, x+36, y+48), start=200, end=340, fill=255)
        draw.ellipse((x+34, y+26, x+38, y+34), outline=255, fill=0)

TEMP_BUF, HUM_BUF = [], []
BUF_N = 5

def smooth(buf, new, n=5):
    buf.append(new)
    if len(buf) > n:
        buf.pop(0)
    return sum(buf) / len(buf)

last_send = 0.0
send_telegram("SHTC3 온습도 + OLED 표시 시작!")

while True:
    try:
        # 센서 읽기
        t = sensor.temperature
        h = sensor.relative_humidity

        # 안정화(원치 않으면 주석 처리 가능)
        t_s = smooth(TEMP_BUF, t, BUF_N)
        h_s = smooth(HUM_BUF, h, BUF_N)

        good = is_comfy(t_s, h_s)

        # OLED 업데이트
        with canvas(device) as draw:
            draw.text((0, 0),  f"T: {t_s:4.1f} C", fill=255)
            draw.text((0, 12), f"H: {h_s:4.1f} %", fill=255)
            draw.text((0, 24), "COMFORT: GOOD" if good else "COMFORT: BAD", fill=255)
            draw.text((0, 52), f"OK T {TEMP_OK[0]}-{TEMP_OK[1]}  H {HUM_OK[0]}-{HUM_OK[1]}", fill=255)

            draw_face(draw, x=80, y=8, good=good)

        # 텔레그램 전송(10초마다)
        now = time.time()
        if now - last_send >= SEND_INTERVAL_SEC:
            msg = (
                "온습도 측정값\n"
                f"- 온도: {t_s:.1f} °C\n"
                f"- 습도: {h_s:.1f} %\n"
                f"- 상태: {'쾌적' if good else '비쾌적'}\n"
                f"- 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            send_telegram(msg)
            last_send = now

        time.sleep(OLED_UPDATE_SEC)

    except Exception as e:
        print(f"오류 발생: {type(e).__name__}: {e}")
        time.sleep(2)
