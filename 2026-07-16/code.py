# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
rotozoom demo for HX8357 + FT5336 TFT FeatherWing.
Slide a finger on the screen to rotate .bmp by an arbitrary angle.

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

# --- destination bitmap: square, big enough to hold the image at any angle ---
# a rotating square's corners sweep out to its diagonal, so size the dest
# to the source diagonal so nothing gets clipped as it spins.
diag = int(math.sqrt(source.width ** 2 + source.height ** 2)) + 2
# dest holds the same range of palette indices as the source
dest = displayio.Bitmap(diag, diag, len(palette))

# center the destination bitmap on screen, sharing the source's palette
tile = displayio.TileGrid(
    dest,
    pixel_shader=palette,
    x=(W - diag) // 2,
    y=(H - diag) // 2,
)
main = displayio.Group()

# solid black background behind the (partly transparent) rotating image
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x000000
main.append(
    vectorio.Rectangle(pixel_shader=bg_palette, width=W, height=H, x=0, y=0)
)

main.append(tile)
display.root_group = main


def draw_rotated(angle):
    """Clear dest, then rotozoom the source into it at the given angle (radians)."""
    dest.fill(bg_index)  # clear to the transparent magenta index
    bitmaptools.rotozoom(
        dest,
        source,
        ox=diag // 2, oy=diag // 2,              # place source center at dest center
        px=source.width // 2, py=source.height // 2,
        angle=angle,
        scale=1.0,
        skip_index=bg_index,                     # don't copy magenta source pixels
    )


# initial draw
angle = 4.71239  # (radians)
draw_rotated(angle)

last_x = None
while True:
    if touch.touched:
        try:
            points = touch.points
            if points:
                t = points[0]
                x = W - 1 - t[0]  # corrected touch x
                if last_x is None:
                    last_x = x
                # map horizontal finger movement to rotation:
                # dragging across the full width = one full turn
                dx = x - last_x
                angle += (dx / W) * (2 * math.pi)
                last_x = x
                draw_rotated(angle)
        except RuntimeError:
            pass
    else:
        last_x = None  # finger lifted; next touch starts fresh
