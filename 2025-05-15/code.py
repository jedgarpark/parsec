# seesaw analog read

import time
import board
from micropython import const
from adafruit_seesaw.seesaw import Seesaw

i2c_bus = board.STEMMA_I2C()  # The built-in STEMMA QT connector on the microcontroller
seesaw = Seesaw(i2c_bus, addr=0x50)

# Print header once
print("Seesaw Analog Read")
print("------------------")

last_x = 0
last_y = 0

while True:

    x = 1023 - seesaw.analog_read(14)
    y = 1023 - seesaw.analog_read(15)

    if (abs(x - last_x) > 3) or (abs(y - last_y) > 3):
        output = f"X: {x:4d}  Y: {y:4d}          "
        print(output, end="\r")

        last_x = x
        last_y = y

    time.sleep(0.01)
