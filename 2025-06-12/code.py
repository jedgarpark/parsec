# Read Built in SD card reader

import os

# Check SD card and print contents
try:
    files = os.listdir("/sd")
    print("SD card contents:")
    for file in sorted(files, key=str.lower):  # sort alphabetically, case insensitive
        if not file.startswith('.'):  # filter out dot files
            print(" ", file)
except OSError:
    print("SD card not mounted or not present")
