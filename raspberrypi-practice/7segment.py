import tm1637
from time import sleep

tm = tm1637.TM1637(clk=24, dio=23)
tm.brightness(7)

for remaining in range(30, -1, -1):
    minutes = remaining // 60
    seconds = remaining % 60

    tm.numbers(minutes, seconds)
    sleep(1)

for _ in range(2):
    tm.numbers(0, 0)
    sleep(0.3)
    tm.show("    ")
    sleep(0.3)

tm.numbers(0, 0)