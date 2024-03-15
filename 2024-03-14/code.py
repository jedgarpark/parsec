# jpeg loader slideshow by John Park
# based on color summarizer by @todbot / Tod Kurt
#https://gist.github.com/todbot/0bf32a6bf8dd21983a32bafc173b3223#file-code_color_palette_finder-py

import time
import board
import displayio
import jpegio
from adafruit_hx8357 import HX8357
import gc

displayio.release_displays()
# name your jpeg files whatever you like, just update the names here
jpeg_fnames = (  # these are hardcoded, you could do a file operation to grab all from a folder
    "/imgs/1.jpg",
    "/imgs/2.jpg",
    "/imgs/3.jpg",
    "/imgs/4.jpg",
    "/imgs/5.jpg",
    "/imgs/6.jpg",
    "/imgs/7.jpg",
    "/imgs/8.jpg"
)

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = HX8357(display_bus, width=480, height=320, rotation=0)

main_group = displayio.Group()
display.root_group = main_group

# start out with a blank screen, we'll replace later
bitmap = displayio.Bitmap(320, 480, 65535)
pixel_shader = displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565_SWAPPED)
tile_grid = displayio.TileGrid(bitmap, pixel_shader=pixel_shader)
main_group.append(tile_grid)

def load_jpeg_to_bitmap(jpeg_fname):
    """Load a JPEG into a displayio.Bitmap"""
    decoder = jpegio.JpegDecoder()  # instaniate the jpeg decoder
    width, height = decoder.open(jpeg_fname)  # open it, find the w,h
    bitmap = displayio.Bitmap(width, height, 65535)  # create a blank bitmap (RGB565_SWAPPED is 16-bit)
    decoder.decode(bitmap)  # decode the jpeg into the blank bitmap
    return bitmap

def slide_show(time_delay=1):
    for jpeg_fname in jpeg_fnames:
        print("----\njpeg file:", jpeg_fname)
        bitmap = load_jpeg_to_bitmap(jpeg_fname)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=pixel_shader)
        main_group[0] = tile_grid
        gc.collect()
        time.sleep(time_delay)

while True:
    slide_show(time_delay=3)
