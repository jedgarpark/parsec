import time
import board
import adafruit_aw9523

i2c = board.STEMMA_I2C()
aw = adafruit_aw9523.AW9523(i2c)
print("Found AW9523")

# Specify which pin to fade (pin 1)
pin_to_fade = 1
speed = 0.02

aw.set_constant_current(pin_to_fade, 0)
# Set all pins to outputs and LED (constant current) mode
aw.LED_modes = 0xFFFF
aw.directions = 0xFFFF


while True:
    # Fade up
    for brightness in range(256):
        aw.set_constant_current(pin_to_fade, brightness)
        time.sleep(speed)
    time.sleep(0.5)

    # Fade down
    for brightness in range(255, -1, -1):
        aw.set_constant_current(pin_to_fade, brightness)
        time.sleep(speed)
    time.sleep(0.5)
