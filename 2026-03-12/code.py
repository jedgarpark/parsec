# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# NeoTrellis MIDI Visualizer
# Lights up buttons when MIDI notes are received

import time

import adafruit_midi
import board
import busio
import usb_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis

num_switches = 64

i2c = busio.I2C(board.SCL, board.SDA)

# create the trellises
trelli = [
    [NeoTrellis(i2c, False, addr=0x2E), NeoTrellis(i2c, False, addr=0x2F)],
    [NeoTrellis(i2c, False, addr=0x30), NeoTrellis(i2c, False, addr=0x31)],
]
trellis = MultiTrellis(trelli)

# Set up MIDI input
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], in_channel=0)

# Set the brightness value (0 to 1.0)
trellis.brightness = 1.0

# Color definitions
RED = (255, 0, 0)
ORANGE = (255, 40, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
PINK = (255, 20, 100)

# Dim versions (about 10% brightness)
DIM_RED = (25, 0, 0)
DIM_ORANGE = (25, 4, 0)
DIM_YELLOW = (25, 15, 0)
DIM_GREEN = (0, 25, 0)
DIM_CYAN = (0, 25, 25)
DIM_BLUE = (0, 0, 25)
DIM_PURPLE = (18, 0, 25)
DIM_PINK = (25, 2, 10)

# Each row gets a different color (row 0 = top, row 7 = bottom)
# Bottom row = lowest octave (RED), Top row = highest octave (PINK)
row_colors = [PINK, PURPLE, BLUE, CYAN, GREEN, YELLOW, ORANGE, RED]
row_dim_colors = [
    DIM_PINK,
    DIM_PURPLE,
    DIM_BLUE,
    DIM_CYAN,
    DIM_GREEN,
    DIM_YELLOW,
    DIM_ORANGE,
    DIM_RED,
]

# MIDI note mapping - all chromatic notes
BASE_NOTE = 24  # C1 (MIDI note 24) at bottom-left


def xy_to_pos(x, y): # convert x,y coordinate to 0-63
    return x + (y * 8)


def pos_to_xy(pos):  # convert 0-63 to x,y coordinate
    return (pos % 8, pos // 8)


def note_to_xy(note):
    """Convert MIDI note to x, y position on grid
    Maps all chromatic notes starting from BASE_NOTE (24)
    Each button represents one semitone
    Notes below 24 map to bottom-left (7, 0)
    Notes above 87 map to top-right (0, 7)"""

    # Clamp notes below range to bottom-left
    if note < BASE_NOTE:
        return (0, 7)  # Bottom-left

    # Clamp notes above range to top-right
    if note >= BASE_NOTE + 64:
        return (7, 0)  # Top-right

    # Simple chromatic mapping - each button is one semitone
    note_offset = note - BASE_NOTE  # 0-63

    x = note_offset % 8  # Column (0-7)
    y = 7 - (note_offset // 8)  # Row, inverted so bottom is lowest

    return (x, y)


def initialize_display():
    """Set all LEDs to dim color based on row"""
    for y in range(8):
        for x in range(8):
            trellis.color(x, y, row_dim_colors[y])

initialize_display()

# We don't need button callbacks for visualization, but we still need to set up the keys
for i in range(num_switches):
    xy_pos = pos_to_xy(i)
    # No callbacks needed for visualizer mode
    time.sleep(0.02)

print("NeoTrellis MIDI Visualizer Ready!")
print(f"Listening for MIDI notes {BASE_NOTE} to {BASE_NOTE + 63} (C1 to B6)")


while True:
    # Check for incoming MIDI messages
    msg = midi.receive()

    if msg is not None:
        if isinstance(msg, NoteOn) and msg.velocity > 0:
            # Note On message
            xy = note_to_xy(msg.note)
            if xy is not None:
                x, y = xy
                trellis.color(x, y, row_colors[y])
                print(f"Note ON: {msg.note} → ({x}, {y})")

        elif isinstance(msg, NoteOff) or (
            isinstance(msg, NoteOn) and msg.velocity == 0
        ):
            # Note Off message (or Note On with velocity 0, which is also Note Off)
            xy = note_to_xy(msg.note)
            if xy is not None:
                x, y = xy
                trellis.color(x, y, row_dim_colors[y])
                print(f"Note OFF: {msg.note} → ({x}, {y})")

    # sync the trellis to update LEDs
    trellis.sync()
    time.sleep(0.02)
