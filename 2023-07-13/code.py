# CircuitPython Circuit Playground Library
# 2 -- Tap detection with on-board LIS3DH accelerometer

import time
from adafruit_circuitplayground import cp

# Change to 1 for single-tap detection.
cp.detect_taps = 2

print("Circuit Playground tap detection demo")

while True:
    if cp.tapped:
        print("Double Tapped!")
        cp.red_led = not cp.red_led
        time.sleep(0.05)
