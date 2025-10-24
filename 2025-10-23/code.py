# Spyce Invaders
# With 11x5 alien grid
#
import time
import board
import displayio
import framebufferio
import vectorio
import adafruit_wii_classic
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.line import Line
import sharpdisplay
import math

# Release any existing displays
displayio.release_displays()

# Initialize Sharp Memory Display
bus = board.SPI()
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, board.D4, 400, 240)
display = framebufferio.FramebufferDisplay(framebuffer, auto_refresh=True)

# Show splash screen
splash_group = displayio.Group()
try:
    splash_bitmap = displayio.OnDiskBitmap("spyce_splash.bmp")
    splash_tile = displayio.TileGrid(
        splash_bitmap, pixel_shader=splash_bitmap.pixel_shader
    )
    splash_group.append(splash_tile)
    display.root_group = splash_group
    time.sleep(4)
    print("Starting game!")
except Exception as e:
    print(f"Could not load splash screen: {e}")
    print("Starting game without splash...")
    time.sleep(1)

# Initialize I2C and controller
i2c = board.STEMMA_I2C()
ctrl_pad = adafruit_wii_classic.Wii_Classic(i2c)

# Create main group for display
screen_group = displayio.Group()

# Create white background
background = Rect(0, 0, display.width, display.height, fill=0xFFFFFF)
screen_group.append(background)
display.root_group = screen_group

# Define colors
white = 0xFFFFFF
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
    (0, -ship_size),  # Top point
    (-ship_size // 2, ship_size // 2),  # Bottom left
    (ship_size // 2, ship_size // 2),  # Bottom right
]

# Create the ship using vectorio.Polygon
ship = vectorio.Polygon(
    pixel_shader=ship_palette, points=triangle_points, x=ship_x, y=ship_y, color_index=1
)
screen_group.append(ship)

# Alien grid properties
alien_width = 18  
alien_height = 13  
alien_cols = 11
alien_rows = 5
alien_spacing_x = 9  
alien_spacing_y = 9  
alien_step = 8  # How far the whole grid moves each step
alien_direction = 1  # 1 = moving right, -1 = moving left
alien_drop_distance = 12  # How far down grid moves when changing direction
alien_move_timer = 0
alien_move_delay = 0.3

# Starting position for top-left alien
alien_start_x = 20
alien_start_y = 30

# Create alien grid - list of dictionaries with rect and alive status
aliens = []
for row in range(alien_rows):
    for col in range(alien_cols):
        x = alien_start_x + col * (alien_width + alien_spacing_x)
        y = alien_start_y + row * (alien_height + alien_spacing_y)
        alien_rect = Rect(x, y, alien_width, alien_height, fill=black)
        screen_group.append(alien_rect)
        aliens.append({"rect": alien_rect, "alive": True, "col": col, "row": row})

print(f"Created {alien_cols}x{alien_rows} alien grid ({len(aliens)} total aliens)")

# Explosion state
explosion_lines = []
explosion_timer = 0
explosion_duration = 0.01

# Projectile properties
projectile_radius = 4
projectile_speed = 20

# Create palette for projectiles
projectile_palette = displayio.Palette(2)
projectile_palette[0] = white  # Background color
projectile_palette[1] = black  # Projectile color

# Single projectile variables
projectile = None
projectile_y = 0

# Button state tracking
last_a_pressed = False


def create_explosion(center_x, center_y):
    """Create 10 explosion lines radiating from center"""
    global explosion_lines
    explosion_lines = []

    explosion_center_x = center_x + alien_width // 2
    explosion_center_y = center_y + alien_height // 2

    for i in range(10):
        angle = (i * 36) * (math.pi / 180)
        line_length = 15

        end_x = explosion_center_x + int(line_length * math.cos(angle))
        end_y = explosion_center_y + int(line_length * math.sin(angle))

        line = Line(explosion_center_x, explosion_center_y, end_x, end_y, color=black)
        explosion_lines.append(line)
        screen_group.append(line)


def clear_explosion():
    """Remove all explosion lines"""
    global explosion_lines
    for line in explosion_lines:
        screen_group.remove(line)
    explosion_lines = []


def count_alive_aliens():
    """Count how many aliens are still alive"""
    return sum(1 for alien in aliens if alien["alive"])


print("Spyce Invaders ready!")
print(f"Display size: {display.width}x{display.height}")
print("Use D-pad to move the ship around the screen")
print("A button: Fire projectile")
print(f"Destroy all {len(aliens)} aliens!")

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
        if projectile is None:
            projectile = vectorio.Circle(
                pixel_shader=projectile_palette,
                radius=projectile_radius,
                x=ship_x,
                y=ship_y,
                color_index=1,
            )
            screen_group.append(projectile)
            projectile_y = ship_y
            print("Projectile fired")

    last_a_pressed = current_a_pressed

    # Update projectile (if it exists)
    if projectile is not None:
        # Move projectile up
        projectile_y -= projectile_speed
        projectile.y = projectile_y

        # Check for collision with any alive alien
        collision_occurred = False
        for alien in aliens:
            if alien["alive"]:
                alien_rect = alien["rect"]
                if (
                    projectile.x + projectile_radius >= alien_rect.x
                    and projectile.x - projectile_radius <= alien_rect.x + alien_width
                    and projectile.y + projectile_radius >= alien_rect.y
                    and projectile.y - projectile_radius <= alien_rect.y + alien_height
                ):
                    # Alien hit!
                    screen_group.remove(alien_rect)
                    alien["alive"] = False
                    create_explosion(alien_rect.x, alien_rect.y)
                    explosion_timer = 0

                    # Remove the projectile
                    screen_group.remove(projectile)
                    projectile = None
                    collision_occurred = True

                    alive_count = count_alive_aliens()
                    print(f"HIT! {alive_count} aliens remaining")

                    if alive_count == 0:
                        print("ALL ALIENS DESTROYED! YOU WIN!")

                    break

        # Remove projectile if it goes off screen
        if not collision_occurred and projectile_y < -projectile_radius:
            screen_group.remove(projectile)
            projectile = None

    # Handle explosion timing
    if explosion_lines:
        explosion_timer += 0.01
        if explosion_timer >= explosion_duration:
            clear_explosion()
            explosion_timer = 0  # Reset timer after clearing

    # Update alien grid movement (all aliens move together)
    alien_move_timer += 0.01

    if alien_move_timer >= alien_move_delay:
        alien_move_timer = 0

        # Calculate new positions for edge detection
        leftmost_x = float("inf")
        rightmost_x = 0

        for alien in aliens:
            if alien["alive"]:
                if alien["rect"].x < leftmost_x:
                    leftmost_x = alien["rect"].x
                if alien["rect"].x > rightmost_x:
                    rightmost_x = alien["rect"].x

        # Check if grid hits screen edge
        should_drop = False
        if alien_direction == 1 and rightmost_x + alien_width >= display.width:
            alien_direction = -1
            should_drop = True
        elif alien_direction == -1 and leftmost_x <= 0:
            alien_direction = 1
            should_drop = True

        # Move all aliens
        for alien in aliens:
            if alien["alive"]:
                if should_drop:
                    alien["rect"].y += alien_drop_distance
                alien["rect"].x += alien_step * alien_direction

    time.sleep(0.01)
