"""This example turns on the little red LED when button A is pressed."""

from adafruit_circuitplayground import cp

while True:
    if cp.button_a:
        cp.red_led = True
    else:
        cp.red_led = False

    # or, get succinct!
    #cp.red_led = cp_button_a

'''non Playground example below:'''
#
# import time
# import board
# import digitalio
#
# led = digitalio.DigitalInOut(board.D13)
# led.switch_to_output()
#
# button = digitalio.DigitalInOut(board.BUTTON_A)
# button.switch_to_input(pull=digitalio.Pull.DOWN)
#
# while True:
#     if button.value:  # button is pushed
#         led.value = True
#     else:
#         led.value = False
#
#     time.sleep(0.01)



'''Buttons light up neopixels:'''
# from adafruit_circuitplayground import cp
#
# cp.pixels.brightness = 0.3
# cp.pixels.fill((0, 0, 0))  # Turn off the NeoPixels if they're on!
#
# while True:
#     if cp.button_a:
#         cp.pixels[0:3] = [(80, 40, 0)] * 3  # light a slice of LEDs
#     else:
#         cp.pixels[0:3] = [(0, 0, 0)] * 3
#
#     if cp.button_b:
#         cp.pixels[7:10] = [(0, 20, 100)] * 3
#     else:
#         cp.pixels[7:10] = [(0, 0, 0)] * 3
#
#     if cp.button_a and cp.button_b:
#         cp.pixels.fill((100, 0, 100))
#     else:
#         cp.pixels.fill((0,0,0))
