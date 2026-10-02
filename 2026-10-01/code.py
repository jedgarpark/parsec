# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
# Surviving a disconnected TMP119 by catching the OSError

import time

import board
from adafruit_tmp117 import TMP117

i2c = board.STEMMA_I2C()
sensor = None

while True:
    if sensor is None:
        try:
            sensor = TMP117(i2c)
            print("TMP119 connected")
        except (OSError, ValueError, RuntimeError, AttributeError) as err:
            print("waiting for sensor:", err)
            time.sleep(1)
            continue

    try:
        print(f"{sensor.temperature:.2f} C")
    except OSError as err:
        print("read failed:", err)
        sensor = None

    time.sleep(0.5)
