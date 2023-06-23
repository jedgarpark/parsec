# using function lists
import board
import time
from random import randint
from adafruit_neokey.neokey1x4 import NeoKey1x4

i2c = board.STEMMA_I2C()

# --- NeoKey 1x4 Setup --- #
neokey = NeoKey1x4(i2c, addr=0x31)
amber = 0x300800
blue = 0x002040
red = 0x900000
yellow = 0x202000
white = 0x222222
neokey.pixels.fill(amber)

keys = [  # neokey (adjust if multiple sets), key number,
    (neokey, 0),
    (neokey, 1),
    (neokey, 2),
    (neokey, 3,),
]

#  states for key presses
key_states = [False, False, False, False]

# define four different functions
def function_a():
    print("this is function A")
    neokey.pixels.fill(red)
    for i in range(7):
        print(" "*i, i)

def function_b():
    print("this is function B")
    neokey.pixels.fill(yellow)
    print(" random number:", randint(50, 300))

def function_c():
    print("this is function C")
    print(" it makes things blue")
    neokey.pixels.fill(blue)

def function_d():
    print("this is function D")
    time.sleep(.25)
    print("  it ")
    time.sleep(.25)
    print("  is ")
    time.sleep(.25)
    print("  slow. ")
    neokey.pixels.fill(white)

def function_e():
    print("this is function E")
    print(" it happens when any key is released!")
    neokey.pixels.fill(amber)

# create a function list
function_list = ( function_a, function_b, function_c, function_d, function_e )

while True:
    # check NeoKeys
    for k in range(len(keys)):
        neokey, key_number= keys[k]
        if neokey[key_number] and not key_states[key_number]:
            # this will run the function with this index from the list
            function_list[key_number]()
            key_states[key_number] = True

        if not neokey[key_number] and key_states[key_number]:
            function_list[4]()
            key_states[key_number] = False
