from gpiozero import LED, Button
from signal import pause

led = LED(27)
button = Button(17)

button.when_pressed = led.toggle

pause()