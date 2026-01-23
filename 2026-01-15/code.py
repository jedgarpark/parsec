import time

import board
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from digitalio import DigitalInOut, Pull

num_leds = 10
leds = neopixel.NeoPixel(board.NEOPIXEL, num_leds, brightness=0.1)

# Set up BLE
ble = BLERadio()
hid = HIDService()
advertisement = ProvideServicesAdvertisement(hid)

# Set up button A on the CPB
button_a = DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=Pull.DOWN)

# Set up slide switch
slide_switch = DigitalInOut(board.SLIDE_SWITCH)
slide_switch.switch_to_input(pull=Pull.UP)

# Create consumer control object (for media keys)
cc = ConsumerControl(hid.devices)

# Track previous switch state
previous_switch_state = slide_switch.value

# Show initial state (orange for disconnected)
leds.fill(0)
if slide_switch.value:  # Switch to the left - normal mode
    leds[0] = 0xFFAA00
    print("Mode: Normal shutter")
else:  # Switch to the right - intervalometer mode
    leds[5:10] = [0xFFAA00] * 5
    print("Mode: Intervalometer")

print("BLE Camera Shutter")
print("Waiting for connection...")

while True:
    if not ble.connected:
        ble.start_advertising(advertisement)
        while not ble.connected:
            pass
        print("Connected!")
        # Change to blue when connected
        leds.fill(0)
        if slide_switch.value:
            leds[0] = 0x0033FF
        else:
            leds[5:10] = [0x0033FF] * 5

    # Check if switch position changed
    if slide_switch.value != previous_switch_state:
        leds.fill(0)  # Clear all LEDs
        if slide_switch.value:  # Switch to the left - normal mode
            leds[0] = 0x0033FF
            print("Mode: Normal shutter")
        else:  # Switch to the right - intervalometer mode
            leds[5:10] = [0x0033FF] * 5
            print("Mode: Intervalometer")
        previous_switch_state = slide_switch.value

    if button_a.value:  # Button pressed
        if slide_switch.value:  # Switch to the left - normal mode
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
            print("Shutter!")
            time.sleep(0.25)
        else:  # Switch to the right - intervalometer mode
            print("Intervalometer: 1 second pause, then 5 shots...")
            leds[5:10] = [0xFF0000] * 5  # Red during countdown
            time.sleep(1.0)  # 1 second pause

            for shot in range(5):
                leds[5:10] = [0xFFFFFF] * 5  # White flash
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                print(f"Shot {shot + 1}/5")
                time.sleep(0.15)  # Quick interval between shots
                leds[5:10] = [0x0033FF] * 5  # Back to connected color

            print("Intervalometer complete!")
            time.sleep(0.5)  # Debounce after sequence
