# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# nested group hierarchy
"""
displayio nested-groups demo for HX8357 + FT5336 TFT FeatherWing
Each group holds two shapes, so dragging a group moves both together.
Touch a group to drag its pair alone; touch empty space to drag everything.
Smoothed touch input to reduce capacitive jitter.
"""
import board
import displayio
import fourwire
import vectorio
from adafruit_hx8357 import HX8357
import adafruit_ft5336

displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10
display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs)
# rotation=90 aligns display x,y with touch x,y
display = HX8357(display_bus, width=320, height=480, rotation=90)

i2c = board.I2C()
touch = adafruit_ft5336.Adafruit_FT5336(i2c)

# --- palette ---
palette = displayio.Palette(3)
palette[0] = 0xFF3030  # circles   - red
palette[1] = 0x30FF30  # triangles - green
palette[2] = 0x3080FF  # squares   - blue

# --- parent group: moving this moves everything ---
scene = displayio.Group()
display.root_group = scene

# --- circle pair ---
circle_group = displayio.Group(x=80, y=80)
circle_group.append(
    vectorio.Circle(pixel_shader=palette, radius=25, x=-30, y=0, color_index=0)
)
circle_group.append(
    vectorio.Circle(pixel_shader=palette, radius=25, x=30, y=0, color_index=0)
)

# --- triangle pair ---
tri_group = displayio.Group(x=80, y=230)
tri_group.append(
    vectorio.Polygon(
        pixel_shader=palette,
        points=[(0, -30), (-30, 25), (30, 25)],
        x=-35, y=0, color_index=1,
    )
)
tri_group.append(
    vectorio.Polygon(
        pixel_shader=palette,
        points=[(0, -30), (-30, 25), (30, 25)],
        x=35, y=0, color_index=1,
    )
)

# --- square pair ---
sq_group = displayio.Group(x=180, y=360)
sq_group.append(
    vectorio.Rectangle(
        pixel_shader=palette, width=50, height=50, x=-60, y=-25, color_index=2
    )
)
sq_group.append(
    vectorio.Rectangle(
        pixel_shader=palette, width=50, height=50, x=10, y=-25, color_index=2
    )
)

# add all shape-groups to the parent
scene.append(circle_group)
scene.append(tri_group)
scene.append(sq_group)

# --- hit testing ---
# each entry: (group, half-width, half-height) bounding box around the pair
shapes = [
    (circle_group, 60, 30),
    (tri_group, 70, 35),
    (sq_group, 65, 30),
]

def hit_shape(tx, ty):
    """Return the shape-group under screen point (tx, ty), or None."""
    # convert screen coords into scene-relative coords
    sx = tx - scene.x
    sy = ty - scene.y
    for grp, half_w, half_h in shapes:
        if abs(sx - grp.x) <= half_w and abs(sy - grp.y) <= half_h:
            return grp
    return None

# --- smoothing / jitter control ---
SMOOTHING = 0.5   # 0.0 = no smoothing, ->1.0 = heavy lag. 0.4-0.6 is a good range.
DEADBAND = 3      # ignore moves smaller than this many pixels

# --- drag state ---
active = None            # the group we're currently dragging
last_x = last_y = 0      # previous SMOOTHED touch position, for delta movement
smooth_x = smooth_y = 0  # running filtered touch position

while True:
    if touch.touched:
        try:
            points = touch.points
            if not points:
                continue
            t = points[0]  # single-finger drag
            # correct touch axes to match displayio screen space
            raw_x = display.width - 1 - t[0]
            raw_y = display.height - 1 - t[1]
            if not (0 <= raw_x < display.width and 0 <= raw_y < display.height):
                continue

            if active is None:
                # new touch: seed the filter with the raw reading (no lag on grab)
                smooth_x, smooth_y = raw_x, raw_y
                active = hit_shape(raw_x, raw_y) or scene
                last_x, last_y = smooth_x, smooth_y
            else:
                # low-pass filter: blend new reading toward the smoothed value
                smooth_x += (raw_x - smooth_x) * (1.0 - SMOOTHING)
                smooth_y += (raw_y - smooth_y) * (1.0 - SMOOTHING)

                dx = smooth_x - last_x
                dy = smooth_y - last_y

                # deadband: only move if past the noise floor
                if abs(dx) >= DEADBAND or abs(dy) >= DEADBAND:
                    active.x += int(dx)
                    active.y += int(dy)
                    last_x, last_y = smooth_x, smooth_y
        except RuntimeError:
            pass
    else:
        active = None  # finger lifted; release
