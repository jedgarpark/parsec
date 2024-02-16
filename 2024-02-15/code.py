import board
import keypad
import neopixel

# create keypad object
buttons = keypad.Keys(pins = (board.BUTTON, ), value_when_pressed=False)
led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)  # LED setup
i = 0  # counter variable

while True:
    button = buttons.events.get()  # check for keypad events
    if button:  # a keypad event has occured
        if button.pressed:
            print("          pressed", i)
            led.fill(0x003300)  # light LED
        if button.released:
            print(" released")
            led.fill(0x0)  # turn off LED
            i=i+1  # increment counter
