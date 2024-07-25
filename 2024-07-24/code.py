import time
import board
import touchio


time.sleep(2.0)

touchA = touchio.TouchIn(board.A3)
touch_min = touchA.raw_value
print("\nthe initial raw value is", touch_min)
time.sleep(1.0)

while True:
    proximity_val = (touchA.raw_value - touch_min)
    print((proximity_val,))
    time.sleep(0.1)
