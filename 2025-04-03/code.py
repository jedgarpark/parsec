# LED segments using list slices instead of loops

import time
import board
import neopixel

strip_length = 64
pixels = neopixel.NeoPixel(board.A0, strip_length, brightness=0.05, auto_write=True, pixel_order=neopixel.GRBW)

seg_length = 8

red = [0xff0000]
green = [0x00ff00]
blue = [0x0000ff]
magenta = [0xff00ff]
yellow = [0x88ff00]
cyan = [0x00ffff]
orange = [0xffa500]
purple = [0x4b0082]

while True:
    time.sleep(2)
    pixels.fill(0x000000)
    time.sleep(1)


    pixels[0:8] = red * 8
    pixels[8:16] = green * 8
    pixels[16:24] = blue * 8
    pixels[24:32] = magenta * 8
    pixels[32:40] = yellow * 8
    pixels[40:48] = cyan * 8
    pixels[48:56] = orange * 8
    pixels[56:64] = purple * 8


    # for i in range(8):
    #     pixels[i] = 0xff0000
    # time.sleep(0.5)
    # for i in range(8):
    #     pixels[i+8] = 0x00ff00
    # time.sleep(0.5)
    # for i in range(8):
    #     pixels[i+16] = 0x0000ff
    # time.sleep(0.5)
    # for i in range(8):
    #     pixels[i+24] = 0xff00ff
    # time.sleep(0.5)
    # for i in range(8):
    #     pixels[i+32] = 0x88ff00
    # time.sleep(0.5)
    # for i in range(8):
    #     pixels[i+40] = 0x00ffff
    # time.sleep(0.5)
    # for i in range(8):
    #     pixels[i+48] = 0x00ffa500
    # time.sleep(0.5)
    # for i in range(8):
    #     pixels[i+56] = 0x4b0082
    # time.sleep(0.5)

