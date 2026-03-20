# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# NeoTrellis MIDI Velocity Meter with asyncio

import time
import asyncio
import adafruit_midi
import board
import busio
import usb_midi
from adafruit_midi.note_on import NoteOn
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis

# === USER SETTINGS ===
VELOCITY_MIN = 10
VELOCITY_MID = 40
VELOCITY_MAX = 110
FADE_DELAY = 0.5
FADE_STEP_TIME = 0.1

# === SHARED DATA ===
column_states = [[0, 0] for _ in range(8)]  # [height, timestamp]
current_column = 0

# === COLORS ===
DIM = (3, 3, 3)
VELOCITY_COLORS = [
    (0, 255, 0), (50, 255, 0), (100, 255, 0), (200, 255, 0),
    (255, 200, 0), (255, 100, 0), (255, 50, 0), (255, 0, 0)
]

# Hardware setup
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
trelli = [
    [NeoTrellis(i2c, False, addr=0x2E), NeoTrellis(i2c, False, addr=0x2F)],
    [NeoTrellis(i2c, False, addr=0x30), NeoTrellis(i2c, False, addr=0x31)],
]
trellis = MultiTrellis(trelli)
trellis.brightness = 0.3

midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], in_channel=0)

def velocity_to_height(velocity):
    velocity = max(VELOCITY_MIN, min(VELOCITY_MAX, velocity))
    if velocity <= VELOCITY_MIN:
        return 0
    elif velocity >= VELOCITY_MAX:
        return 8
    elif velocity <= VELOCITY_MID:
        range_vel = VELOCITY_MID - VELOCITY_MIN
        offset_vel = velocity - VELOCITY_MIN
        return int((offset_vel / range_vel) * 4)
    else:
        range_vel = VELOCITY_MAX - VELOCITY_MID
        offset_vel = velocity - VELOCITY_MID
        return int(4 + (offset_vel / range_vel) * 4)

def draw_column(col, height):
    for row in range(8):
        y = 7 - row
        trellis.color(col, y, VELOCITY_COLORS[y] if row < height else DIM)

# Initialize display
for y in range(8):
    for x in range(8):
        trellis.color(x, y, DIM)
trellis.sync()

async def midi_task():
    """Handle MIDI input"""
    global current_column

    while True:
        msg = midi.receive()

        if msg is not None and isinstance(msg, NoteOn) and msg.velocity > 0:
            height = velocity_to_height(msg.velocity)
            column_states[current_column] = [height, time.monotonic()]
            print(f"Note {msg.note}, Vel {msg.velocity} → Col {current_column}, H {height}")
            current_column = (current_column + 1) % 8

        await asyncio.sleep(0)  # Yield to other tasks

async def display_task():
    """Handle display updates and fading"""
    last_heights = [0] * 8

    while True:
        current_time = time.monotonic()
        needs_sync = False

        for col in range(8):
            height, timestamp = column_states[col]

            if height > 0 and timestamp > 0:
                elapsed = current_time - timestamp
                if elapsed > FADE_DELAY:
                    steps = int((elapsed - FADE_DELAY) / FADE_STEP_TIME)
                    height = max(0, height - steps)

            if height != last_heights[col]:
                draw_column(col, height)
                last_heights[col] = height
                needs_sync = True

        if needs_sync:
            trellis.sync()

        await asyncio.sleep(0.02)  # 50 Hz

async def main():
    """Run both tasks concurrently"""
    midi_job = asyncio.create_task(midi_task())
    display_job = asyncio.create_task(display_task())
    await asyncio.gather(midi_job, display_job)

print("Starting asyncio MIDI visualizer...")
asyncio.run(main())
