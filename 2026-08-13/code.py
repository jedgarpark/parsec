# circuit python parsec -- Fruit Jam Library: Neopixels (and buttons)
# # adafruit_fruitjam helper library based on Portal Base

import time
from adafruit_fruitjam.peripherals import Peripherals

colors = [0x880000, 0x008800, 0x0000FF]

fruitjam = Peripherals()
fruitjam.neopixels.brightness = 1
fruitjam.neopixels.fill(0x000000)  # start all off

fruitjam.neopixels[4] = 0x202020
fruitjam.neopixels.show()

while True:
    buttons = (fruitjam.button3, fruitjam.button2, fruitjam.button1)

    for i, pressed in enumerate(buttons):
        fruitjam.neopixels[i] = colors[i] if pressed else 0x000000
    fruitjam.neopixels.show()

    time.sleep(0.05)
