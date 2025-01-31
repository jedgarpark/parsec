# Bicolor Matrix Backpack in cpy

import time
import board
from adafruit_ht16k33.matrix import Matrix8x8x2

i2c = board.STEMMA_I2C()
matrix = Matrix8x8x2(i2c)

# Set brightness (0.0 to 1.0)
matrix.brightness = 0.25  # 25% brightness
matrix.fill(0)
time.sleep(1)

time.sleep(1)
matrix.fill(0)

# Draw 4x4 box
for x in range(1, 5):
    for y in range(1, 5):
        matrix[x, y] = 10

# Pixels
matrix[3, 3] = 1 # red
matrix[3, 2] = 1
matrix[2, 2] = 1
matrix[2, 3] = 1

speed=0.1
WRAP = True

while True:

    matrix.shift(1, 0, WRAP)	# shift pixels left
    time.sleep(speed)
    time.sleep(speed)
    matrix.shift(0, -1, WRAP)	# shift pixels down
    time.sleep(speed)
    matrix.shift(-1, 1, WRAP)	# shift pixels
    time.sleep(speed)
    matrix.shift(-1, 1, WRAP)	# shift pixels
    time.sleep(.5)
