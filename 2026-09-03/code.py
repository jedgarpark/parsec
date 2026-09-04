# Fruit Jam SD Card Contents
import os
import storage
from adafruit_fruitjam.peripherals import Peripherals

fruitjam = Peripherals()  # constructing the Fruit Jam Peripherals() object triggers SD mount

try:
    vfs = storage.getmount("/sd")
    print("SD card name:", vfs.label)
    files = os.listdir("/sd")
    print("  SD card contents:")
    for name in files:
        if not name.startswith("."):
            print(" -", name)
except OSError:
    print("No SD card detected")
