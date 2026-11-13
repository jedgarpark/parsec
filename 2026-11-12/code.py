# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# Feather RP2040 + 3.5" TFT FeatherWing: static sparkline, zero at the bottom

import board
import displayio
import fourwire
import terminalio
from adafruit_display_shapes.sparkline import Sparkline
from adafruit_display_text import label
from adafruit_hx8357 import HX8357

WIDTH = 480
HEIGHT = 320

DATA = [22, 5,  48, 22, 48, 20, 60, 41, 50]

Y_MIN = 0
Y_MAX = max(DATA) * 1.1   # a little headroom so the peak isn't clipped

displayio.release_displays()
spi = board.SPI()
display_bus = fourwire.FourWire(spi, command=board.D10, chip_select=board.D9)
display = HX8357(display_bus, width=WIDTH, height=HEIGHT)

group = displayio.Group()

group.append(label.Label(terminalio.FONT, text="sparkline", scale=3, x=20, y=40))
group.append(label.Label(terminalio.FONT, text=str(DATA), scale=2, x=20, y=90))

spark = Sparkline(
    width=WIDTH - 40,
    height=170,
    max_items=len(DATA),
    x=20,
    y=120,
    color=0x00FF88,
    y_min=Y_MIN,
    y_max=Y_MAX,
)
group.append(spark)

for value in DATA:
    spark.add_value(value)


display.root_group = group

while True:
    pass
