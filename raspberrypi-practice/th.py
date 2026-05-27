import time
import board
import adafruit_shtc3

i2c = board.I2C()
sensor = adafruit_shtc3.SHTC3(i2c)

while True:
    t = sensor.temperature
    h = sensor.relative_humidity
    print(f"T={t:.2f}C  H={h:.2f}%")
    time.sleep(1)