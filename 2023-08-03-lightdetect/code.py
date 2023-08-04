# import time
# from adafruit_circuitplayground import cp
#
# while True:
#     print((cp.light,))
#     time.sleep(0.05)


import time
from adafruit_circuitplayground import cp

cp.pixels.auto_write = False
cp.pixels.brightness = 0.3

while True:
    peak = round(cp.light / 320 * 9)
    print((cp.light,))
    print(int(peak))

    for i in range(10):
        if i <= peak:
            cp.pixels[i] = (40, 0, 0)
        else:
            cp.pixels[i] = (0, 0, 0)
    cp.pixels.show()
    time.sleep(0.05)
