# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Kattni Rembor for Adafruit Industries
# SPDX-FileCopyrightText: 2026 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Gamepad QT Seesaw readout on two static serial lines."""

import time
import board
from adafruit_seesaw.seesaw import Seesaw

BUTTONS = (
    (6, "X"),
    (2, "Y"),
    (5, "A"),
    (1, "B"),
    (0, "Select"),
    (16, "Start"),
)

# Button mask retruns the state of all six button pins at once over I2C transaction
button_mask = 0 
for pin, _name in BUTTONS:
    button_mask |= 1 << pin


i2c_bus = board.STEMMA_I2C()


seesaw = Seesaw(i2c_bus, addr=0x50)
seesaw.pin_mode_bulk(button_mask, seesaw.INPUT_PULLUP)

last_x = -99
last_y = -99
last_pressed = None

# Reserve the two lines we overwrite
print()
print()

while True:
    x = 1023 - seesaw.analog_read(14)                 # first get x
    y = 1023 - seesaw.analog_read(15)                 # then get y
    buttons = seesaw.digital_read_bulk(button_mask)   # then get all buttons

    # build a list of the names of buttons currently pressed:
    pressed = [name for pin, name in BUTTONS if not buttons & (1 << pin)]

    # only print new text if something has changed:
    if abs(x - last_x) > 3 or abs(y - last_y) > 3 or pressed != last_pressed:
        joy = f"thumbstick:  x={x:4d}  y={y:4d}"
        btn = "buttons:   " + (" ".join(pressed) if pressed else "-")
        print(f"\x1b[2A\x1b[2K{joy}\n\x1b[2K{btn}")
        last_x = x
        last_y = y
        last_pressed = pressed

    time.sleep(0.01)
