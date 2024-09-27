# bootloader without board access
# hold an external button at power-up to enter bootloader
import time
import board
import microcontroller
from digitalio import DigitalInOut, Pull

button = DigitalInOut(board.A0)
button.pull = Pull.UP

if button.value == False:  # pressed
    time.sleep(1)
    if button.value == False:  # it's still pressed, let's do this!
        print("\n going into bootloader")
        time.sleep(1)
        microcontroller.on_next_reset(microcontroller.RunMode.UF2)
        microcontroller.reset()

while True:
    if button.value == False:  # pressed
            print("button is pressed! we're just innocent men.")
            time.sleep(0.2)
    else:
        print("button not pressed. we're just normal men.")
        time.sleep(1)
