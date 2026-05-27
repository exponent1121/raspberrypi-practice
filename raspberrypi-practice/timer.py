import time
import tm1637
from gpiozero import LED, Button

TM_CLK = 24
TM_DIO = 23
BUTTON_PIN = 17
LED_PIN = 27

tm = tm1637.TM1637(clk=TM_CLK, dio=TM_DIO)
tm.brightness(7)
tm.show("PUSH")

led = LED(LED_PIN)
button = Button(BUTTON_PIN, pull_up=True)

def show_mmss(total_seconds: int):
    m = total_seconds // 60
    s = total_seconds % 60
    tm.numbers(m, s)

def blink_alarm(blink_count=10, on_time=0.25, off_time=0.25):
    for _ in range(blink_count):
        led.on()
        tm.numbers(0, 0)
        time.sleep(on_time)

        led.off()
        tm.show("    ")
        time.sleep(off_time)

    tm.numbers(0, 0)

def run_timer():
    for remaining in range(30, -1, -1):
        show_mmss(remaining)
        time.sleep(1)
    blink_alarm()


try:
    while True:
        button.wait_for_press()

        led.on()
        time.sleep(0.1)
        led.off()

        run_timer()

        button.wait_for_release()
        tm.show("PUSH")
except KeyboardInterrupt:
    pass

finally:
    led.off()