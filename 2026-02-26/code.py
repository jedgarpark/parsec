# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# NeoTrellis basic MIDI keyboard
# Each row is a different color, bottom-left is lowest note (C)

import time
import board
import busio

'''import all the midi libraries'''
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

num_switches = 64

i2c = busio.I2C(board.SCL, board.SDA)

# create the trellises
trelli = [
     [NeoTrellis(i2c, False, addr=0x2E), NeoTrellis(i2c, False, addr=0x2F)],
     [NeoTrellis(i2c, False, addr=0x30), NeoTrellis(i2c, False, addr=0x31)]
]
trellis = MultiTrellis(trelli)

# Set up MIDI
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# Set the brightness value (0 to 1.0)
trellis.brightness = 0.3

# Color definitions
OFF = (0, 0, 0)
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
# We want bottom to be lowest octave, so reverse the colors
row_colors = [PINK, PURPLE, BLUE, CYAN, GREEN, YELLOW, ORANGE, RED]
row_dim_colors = [DIM_PINK, DIM_PURPLE, DIM_BLUE, DIM_CYAN, DIM_GREEN, DIM_YELLOW, DIM_ORANGE, DIM_RED]

'''
MIDI note mapping helpers
'''
# C major scale white keys: C, D, E, F, G, A, B, C
# Starting from C3 (MIDI note 48) at bottom-left
WHITE_KEY_INTERVALS = [0, 2, 4, 5, 7, 9, 11, 12]  # Semitones from root
BASE_NOTE = 24  # C1

def xy_to_pos(x, y):
    return x + (y * 8)

def pos_to_xy(pos):
    return (pos % 8, pos // 8)

def get_midi_note(x, y):
    """Calculate MIDI note for a given x, y position
    Row 7 (bottom) = lowest octave
    Row 0 (top) = highest octave
    Each column is a white key step"""
    octave = 7 - y  # Flip so row 7 is octave 0, row 0 is octave 7
    note = BASE_NOTE + (octave * 12) + WHITE_KEY_INTERVALS[x]
    print("BASE_NOTE:", BASE_NOTE, "+ octave*12:", (octave*12), "+ WHITE_KEY_INTERVALS[x]:", WHITE_KEY_INTERVALS[x])

    return note

def initialize_display():
    """Set all LEDs to dim color based on row"""
    for y in range(8):
        for x in range(8):
            trellis.color(x, y, row_dim_colors[y])

# callback when buttons are pressed
def handle_button(x, y, edge):
    pos = xy_to_pos(x, y)
    note = get_midi_note(x, y)

    if edge == NeoTrellis.EDGE_RISING:
        # Button pressed - send MIDI note on and light up bright
        midi.send(NoteOn(note, 127))  # 127 = full velocity
        trellis.color(x, y, row_colors[y])
        print(f"Note ON: {note} (x={x}, y={y})")

    elif edge == NeoTrellis.EDGE_FALLING:
        # Button released - send MIDI note off and return to dim
        midi.send(NoteOff(note, 0))
        trellis.color(x, y, row_dim_colors[y])
        print(f"Note OFF: {note}")

initialize_display()

# Setup all buttons
for i in range(num_switches):
    xy_pos = pos_to_xy(i)
    trellis.activate_key(xy_pos[0], xy_pos[1], NeoTrellis.EDGE_RISING)
    trellis.activate_key(xy_pos[0], xy_pos[1], NeoTrellis.EDGE_FALLING)
    trellis.set_callback(xy_pos[0], xy_pos[1], handle_button)
    time.sleep(0.02)

print("NeoTrellis MIDI Keyboard Ready")
print(f"Base note: C1 (MIDI {BASE_NOTE})")


while True:
    trellis.sync()  # checks all 64 buttons for state change, triggers callback
    time.sleep(0.02)
