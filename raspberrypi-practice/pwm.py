from gpiozero import LED
from time import sleep

led = LED(27)

while True:
    led.on()
    sleep(0.008)
    led.off()
    sleep(0.002)