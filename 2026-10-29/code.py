# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# PyPortal: capacitive touch as a progress bar on D3

import time

import board
import displayio
import terminalio
import touchio
from adafruit_display_text import label
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)

display = board.DISPLAY

touch = touchio.TouchIn(board.D3)
baseline = touch.raw_value  # get a starting value
# touch.threshold = touch.raw_value + 250
span = max(200, touch.threshold - baseline) * 3

splash = displayio.Group()
display.root_group = splash

width = display.width - 40
height = 20
x = 20
y = 90

bar = HorizontalProgressBar(
    (x, y),
    (width, height),
    fill_color=0x101820,
    outline_color=0x606870,
    bar_color=0x00FF88,
    direction=HorizontalFillDirection.LEFT_TO_RIGHT,
)
splash.append(bar)

readout = label.Label(terminalio.FONT, text="", scale=2, x=x, y=50)
splash.append(readout)

while True:
    raw = touch.raw_value
    delta = max(0, raw - baseline)
    bar.value = min(100, int(delta / span * 100))
    readout.text = f"+{delta}"
    time.sleep(0.03)
