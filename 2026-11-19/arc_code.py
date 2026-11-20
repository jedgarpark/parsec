# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# Feather RP2040 + 3.5" TFT FeatherWing: the four Arc parameters

import board
import displayio
import fourwire
import terminalio
from adafruit_display_shapes.arc import Arc
from adafruit_display_shapes.circle import Circle
from adafruit_hx8357 import HX8357

WIDTH = 480
HEIGHT = 320

GREEN = 0x00FF88
AMBER = 0xFFAA00
BLUE = 0x4488FF
PINK = 0xFF4488
GREY = 0x606060
RED = 0xFF0000

displayio.release_displays()
spi = board.SPI()
display_bus = fourwire.FourWire(spi, command=board.D10, chip_select=board.D9)
display = HX8357(display_bus, width=WIDTH, height=HEIGHT)

group = displayio.Group()


cx, cy = WIDTH//2, HEIGHT//2

group.append(Circle(cx, cy, 3, fill=GREY))  # show the center point

group.append(Arc(   x=cx, y=cy, 
                    radius=100,     # radius
                    angle=90,       # angle of arc
                    direction=45,   # start point
                    segments=36,    # smoothness
                    arc_width=6,    # thicknes
                    fill=GREEN,       # fill color
                    #outline=RED # outline color
                    )
)

display.root_group = group

while True:
    pass
