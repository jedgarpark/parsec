# CircuitPython Circuit Playground Library
# 3 -- NeoPixels
import time
from adafruit_circuitplayground import cp
print("Circuit Playground NeoPixel demo")

while True:
    print("fill")
    cp.pixels.fill((20, 0, 5))
    time.sleep(2)
    cp.pixels.fill((0, 0, 0))
    time.sleep(2)

    print("solo")
    cp.pixels[3] = ((0, 20, 5))
    time.sleep(1)
    cp.pixels[7] = ((25, 10, 0))
    cp.pixels[9] = ((35, 5, 3))
    time.sleep(1)
    cp.pixels[3] = ((0, 0, 0))
    time.sleep(1)
    cp.pixels[7] = ((0, 0, 0))
    cp.pixels[9] = ((0, 0, 0))
    time.sleep(1)
