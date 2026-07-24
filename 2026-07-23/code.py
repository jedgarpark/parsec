# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
rotozoom zoom demo for HX8357 + FT5336 TFT FeatherWing.
Slide a finger up/down to scale lars.bmp up and down.

bmp should be an 8-bit (256-color) indexed BMP w magenta transparent color.
"""
import math
import board
import displayio
import fourwire
import bitmaptools
import vectorio
import adafruit_imageload
from adafruit_hx8357 import HX8357
import adafruit_ft5336

displayio.release_displays()

spi = board.SPI()
display_bus = fourwire.FourWire(spi, command=board.D10, chip_select=board.D9)
# rotation=90 aligns display x,y with touch x,y
display = HX8357(display_bus, width=320, height=480, rotation=90)

i2c = board.I2C()
touch = adafruit_ft5336.Adafruit_FT5336(i2c)

W, H = display.width, display.height  # 320 x 480

# --- load the source image into RAM (indexed BMP -> Bitmap + Palette) ---
source, palette = adafruit_imageload.load("/lars.bmp")

# find the magenta background index in the palette
MAGENTA = 0xFF00FF
bg_index = 0
for i in range(len(palette)):
    if palette[i] == MAGENTA:
        bg_index = i
        break
# make the magenta pixels transparent so the black dest shows through
palette.make_transparent(bg_index)

# --- scale limits ---
MIN_SCALE = 0.25
MAX_SCALE = 2.0

# --- destination bitmap: big enough to hold the image at max zoom ---
# at MAX_SCALE the image is that much bigger, so size dest to the largest
# dimension * MAX_SCALE so a zoomed-in image never gets clipped.
longest = max(source.width, source.height)
dest_size = int(longest * MAX_SCALE) + 2
dest = displayio.Bitmap(dest_size, dest_size, len(palette))

# center the destination bitmap on screen, sharing the source's palette
tile = displayio.TileGrid(
    dest,
    pixel_shader=palette,
    x=(W - dest_size) // 2,
    y=(H - dest_size) // 2,
)
main = displayio.Group()

# solid black background behind the (partly transparent) scaling image
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x000000
main.append(
    vectorio.Rectangle(pixel_shader=bg_palette, width=W, height=H, x=0, y=0)
)

main.append(tile)
display.root_group = main


def draw_scaled(scale):
    """Clear dest, then rotozoom the source into it at the given scale."""
    dest.fill(bg_index)  # clear to the transparent magenta index
    bitmaptools.rotozoom(
        dest,
        source,
        ox=dest_size // 2, oy=dest_size // 2,        # source center -> dest center
        px=source.width // 2, py=source.height // 2,
        angle=0.0,                                   # no rotation, just scale
        scale=scale,
        skip_index=bg_index,                         # don't copy magenta pixels
    )


# initial draw
scale = 1.0
draw_scaled(scale)

last_y = None
while True:
    if touch.touched:
        try:
            points = touch.points
            if points:
                t = points[0]
                y = H - 1 - t[1]  # corrected touch y
                if last_y is None:
                    last_y = y
                # vertical drag -> scale (drag up = bigger, down = smaller)
                dy = y - last_y
                scale -= (dy / H) * (MAX_SCALE - MIN_SCALE)
                scale = min(max(scale, MIN_SCALE), MAX_SCALE)  # clamp
                last_y = y
                draw_scaled(scale)
        except RuntimeError:
            pass
    else:
        last_y = None  # finger lifted; next touch starts fresh
