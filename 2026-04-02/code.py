#CLUE magnet polarity finder

from adafruit_clue import clue
import displayio
import terminalio
from adafruit_display_text import label
import time

THRESHOLD = 50  # µT

# Display setup
display = clue.display
group = displayio.Group()
display.root_group = group

# Big label centered on screen
text_label = label.Label(
    terminalio.FONT,
    text="---",
    color=0xFFFFFF,
    scale=5
)
text_label.anchor_point = (0.5, 0.5)
text_label.anchored_position = (display.width // 2, display.height // 2)
group.append(text_label)

while True:
    _, _, z = clue.magnetic

    if z > THRESHOLD:
        text_label.text = "NORTH"
        text_label.color = 0x0000FF  # blue
    elif z < -THRESHOLD:
        text_label.text = "SOUTH"
        text_label.color = 0xFF0000  # red
    else:
        text_label.text = "---"
        text_label.color = 0xFFFFFF

    time.sleep(0.1)
