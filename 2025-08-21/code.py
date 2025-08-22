import time
import board
import displayio
import framebufferio
import vectorio
import adafruit_wii_classic
from adafruit_display_shapes.rect import Rect
import sharpdisplay

# Release any existing displays
displayio.release_displays()

# Initialize Sharp Memory Display
bus = board.SPI()
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, board.D4, 400, 240)
display = framebufferio.FramebufferDisplay(framebuffer, auto_refresh=True)

# Initialize I2C and controller
i2c = board.STEMMA_I2C()
ctrl_pad = adafruit_wii_classic.Wii_Classic(i2c)

# Create main group for display
group = displayio.Group()

# Create white background
background = Rect(0, 0, display.width, display.height, fill=0xffffff)
group.append(background)

display.root_group = group

# Define colors
white = 0xffffff
black = 0x000000

# Dot properties
dot_radius = 16
dot_x = display.width // 2  # center it
dot_y = display.height // 2  # center it
move_step = 32  # Smaller pixel steps = smoother movement

# Create palette for vectorio circle
palette = displayio.Palette(2)
palette[0] = white  # Background color
palette[1] = black  # Circle color

# Create the dot using vectorio.Circle
dot = vectorio.Circle(pixel_shader=palette, radius=dot_radius, x=dot_x, y=dot_y, color_index=1)

group.append(dot)

# Dot size state
original_radius = dot_radius
large_radius = dot_radius * 2

last_a_press = 0
last_b_press = 0

print("Sharp display dot controller ready")
print(f"Display size: {display.width}x{display.height}")
print("Use D-pad to move the dot around the screen")
print("A button: Hold to double dot size")
print("B button: Reset to center")

while True:
    moved = False  # move state to gang up x&y movement

    # Check d-pad buttons and update position
    if ctrl_pad.d_pad.UP:
        dot_y -= move_step
        moved = True
    if ctrl_pad.d_pad.DOWN:
        dot_y += move_step
        moved = True
    if ctrl_pad.d_pad.LEFT:
        dot_x -= move_step
        moved = True
    if ctrl_pad.d_pad.RIGHT:
        dot_x += move_step
        moved = True

    # Update dot position if it moved
    if moved:
        dot.x = dot_x
        dot.y = dot_y

    # A button: Hold to double dot size, release to return to original size
    if ctrl_pad.buttons.A:
        # Make dot larger while A is held
        if dot.radius != large_radius:
            dot.radius = large_radius
            print("Dot size: Large")
    else:
        # Return to original size when A is released
        if dot.radius != original_radius:
            dot.radius = original_radius
            print("Dot size: Normal")

    # B button: Reset to center
    if ctrl_pad.buttons.B:
        dot_x = display.width // 2
        dot_y = display.height // 2
        dot.x = dot_x
        dot.y = dot_y
        print("Dot reset to center")

    time.sleep(0.01)
