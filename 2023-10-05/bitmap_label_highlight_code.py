# SPDX-FileCopyrightText: 2022 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# M8 mate for Adafruit Macropad RP2040 and M8 Headless
import time
import displayio
import terminalio
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
import board

display = board.DISPLAY
main_group = displayio.Group()
display.show(main_group)
title = label.Label(
    y=4,
    font=terminalio.FONT,
    color=0x0,
    text="                           ",
    background_color=0xFFFFFF,
)
layout = GridLayout(x=0, y=13, width=128, height=54, grid_size=(4, 4), cell_padding=5)
label_text = [
    "FULL", "^", " HALF ",
    "<", "v", ">",
    "CTRL ", "OPT", "EDIT",
    "SHFT", "PLAY", "OFF",
    "    ", "    ", "    "
]
labels = []
for j in range(15):
    labels.append(label.Label(terminalio.FONT, text=label_text[j], max_glyphs=10))

for index in range(15):
    x = index % 3
    y = index // 3
    layout.add_content(labels[index], grid_position=(x, y), cell_size=(1, 1))

main_group.append(title)
main_group.append(layout)

while True:
    # time.sleep(1)
    for i in range(len(labels)):
        labels[i].color = 0x0
        labels[i].background_color = 0xffff00
        time.sleep(0.25)
        labels[i].color = 0xffffff
        labels[i].background_color = 0x0
        time.sleep(0.25)
