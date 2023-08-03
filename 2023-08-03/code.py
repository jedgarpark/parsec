# # CircuitPython Circuit Playground Library
# # 5 -- Accelerometer
#################################################
# # Accelerometer Demo
#################################################
import time
from adafruit_circuitplayground import cp
print("Circuit Playground Accelerometer demo")

while True:
    x, y, z = cp.acceleration
    print((x, y, z))
    R = abs(int(x))
    G = abs(int(y))
    B = abs(int(z))
    cp.pixels.fill((R,G,B))
    time.sleep(0.1)
