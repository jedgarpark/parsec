"""seesaw scroll wheel"""

import time
import board
from adafruit_seesaw import seesaw, rotaryio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

# instantiate HID device
cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# set up i2c and seesaw encoder
i2c = board.STEMMA_I2C()
seesaw = seesaw.Seesaw(i2c, addr=0x36)  # seesaw rotary encoder
encoder = rotaryio.IncrementalEncoder(seesaw)

last_position = encoder.position


while True:
    current_position = encoder.position
    position_change = current_position - last_position

    if current_position != last_position:
        if position_change > 0:  # scroll up
            for _ in range(abs(position_change)):
                mouse.move(wheel=1)
                time.sleep(0.005)
            print("^")

        else:  # scroll down
            for _ in range(abs(position_change)):
                mouse.move(wheel=-1)
                time.sleep(0.005)
            print("v")

        last_position = current_position  # reset state variable
