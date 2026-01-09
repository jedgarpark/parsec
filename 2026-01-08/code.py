import time
import board
import neopixel
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from digitalio import DigitalInOut, Pull

# Set up BLE
ble = BLERadio()
hid = HIDService()
advertisement = ProvideServicesAdvertisement(hid)

# Set up button A on the CPB
button_a = DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=Pull.DOWN)

# Set up NeoPixels (CPB has 10 NeoPixels)
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.3)

# Create consumer control object (for media keys)
cc = ConsumerControl(hid.devices)

print("BLE Camera Shutter")
print("Waiting for connection...")

while True:
    if not ble.connected:
        pixels.fill((0, 0, 255))  # Blue while waiting
        ble.start_advertising(advertisement)
        while not ble.connected:
            pass
        pixels.fill((0, 255, 0))  # Green when connected
        print("Connected!")
        time.sleep(0.5)
        pixels.fill((0, 0, 0))  # Turn off
    
    if button_a.value:  # Button pressed
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)  # Trigger shutter
        
        # Flash white
        pixels.fill((255, 255, 255))
        time.sleep(0.1)
        pixels.fill((0, 0, 0))
        
        print("Shutter!")
        time.sleep(0.4)  # Debounce


#non neo-pixel version
# import time
# import board
# from adafruit_hid.consumer_control import ConsumerControl
# from adafruit_hid.consumer_control_code import ConsumerControlCode
# from adafruit_ble import BLERadio
# from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
# from adafruit_ble.services.standard.hid import HIDService
# from digitalio import DigitalInOut, Pull

# # Set up BLE
# ble = BLERadio()
# hid = HIDService()
# advertisement = ProvideServicesAdvertisement(hid)

# # Set up button A on the CPB
# button_a = DigitalInOut(board.BUTTON_A)
# button_a.switch_to_input(pull=Pull.DOWN)

# # Create consumer control object (for media keys)
# cc = ConsumerControl(hid.devices)

# print("BLE Camera Shutter")
# print("Waiting for connection...")

# while True:
#     if not ble.connected:
#         ble.start_advertising(advertisement)
#         while not ble.connected:
#             pass
#         print("Connected!")

#     if button_a.value:  # Button pressed
#         cc.send(ConsumerControlCode.VOLUME_INCREMENT)  # Trigger shutter
#         print("Shutter!")
#         time.sleep(0.5)  # Debounce
