# Single Projectile
#
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
screen_group = displayio.Group()

# Create white background
background = Rect(0, 0, display.width, display.height, fill=0xffffff)
screen_group.append(background)
display.root_group = screen_group

# Define colors
white = 0xffffff
black = 0x000000

# Ship properties
ship_size = 16
ship_x = display.width // 2  # center it
ship_y = display.height - ship_size
move_step = 18

# Create palette for vectorio polygon (ship)
ship_palette = displayio.Palette(2)
ship_palette[0] = white  # Background color
ship_palette[1] = black  # Ship color

# Create triangle points (pointing up)
triangle_points = [
    (0, -ship_size),      # Top point
    (-ship_size//2, ship_size//2),   # Bottom left
    (ship_size//2, ship_size//2)     # Bottom right
]

# Create the ship using vectorio.Polygon
ship = vectorio.Polygon(pixel_shader=ship_palette, points=triangle_points, x=ship_x, y=ship_y, color_index=1)
screen_group.append(ship)

# Projectile properties
projectile_radius = 4
projectile_speed = 20

# Create palette for projectiles
projectile_palette = displayio.Palette(2)
projectile_palette[0] = white  # Background color
projectile_palette[1] = black # Projectile color

# Single projectile variables
projectile = None  # Will hold the projectile circle when it exists
projectile_y = 0   # Will track the projectile's Y position

# Button state tracking
last_a_pressed = False

print("Simple single projectile ship controller ready")
print(f"Display size: {display.width}x{display.height}")
print("Use D-pad to move the ship around the screen")
print("A button: Fire projectile (only one at a time)")

while True:
    moved = False

    # Check d-pad buttons and update position
    if ctrl_pad.d_pad.UP:
        ship_y -= move_step
        moved = True
    if ctrl_pad.d_pad.DOWN:
        ship_y += move_step
        moved = True
    if ctrl_pad.d_pad.LEFT:
        ship_x -= move_step
        moved = True
    if ctrl_pad.d_pad.RIGHT:
        ship_x += move_step
        moved = True

    # Keep ship within screen bounds
    if ship_x < ship_size:
        ship_x = ship_size
    elif ship_x > display.width - ship_size:
        ship_x = display.width - ship_size
    if ship_y < ship_size:
        ship_y = ship_size
    elif ship_y > display.height - ship_size:
        ship_y = display.height - ship_size

    # Update ship position if it moved
    if moved:
        ship.x = ship_x
        ship.y = ship_y

    # A button: Fire projectile (only if no projectile exists)
    current_a_pressed = ctrl_pad.buttons.A
    if current_a_pressed and not last_a_pressed:
        if projectile is None:  # Only fire if no projectile exists
            # Create new projectile at ship position
            projectile = vectorio.Circle(
                pixel_shader=projectile_palette,
                radius=projectile_radius,
                x=ship_x,
                y=ship_y,
                color_index=1
            )
            screen_group.append(projectile)
            projectile_y = ship_y  # Remember where it started
            print("Projectile fired")

    last_a_pressed = current_a_pressed

    # Update projectile (if it exists)
    if projectile is not None:
        # Move projectile up
        projectile_y -= projectile_speed
        print(projectile_y)
        projectile.y = projectile_y

        # Remove projectile if it goes off screen
        if projectile_y < -projectile_radius:
            screen_group.remove(projectile)  # Remove from display
            projectile = None  # Clear our reference
            print("Projectile removed")

    time.sleep(0.01)
