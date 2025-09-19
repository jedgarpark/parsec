# Single Projectile with Rectangle Enemy
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

# Enemy properties - ALL DEFINED HERE
enemy_width = 40  # 2x the original size
enemy_height = 24  # 2x the original size
enemy_x = 50  # Start position
enemy_y = 50  # Start a few rows down from top
enemy_step = 8  # Move 8 pixels each step (1/5 of enemy width)
enemy_direction = 1  # 1 = moving right, -1 = moving left
enemy_drop_distance = 20  # How far down it moves when changing direction
enemy_move_timer = 0  # Timer for discrete movement
enemy_move_delay = 0.3  # Pause 0.3 seconds between moves

# Create the enemy as a rectangle
enemy = Rect(enemy_x, enemy_y, enemy_width, enemy_height, fill=black)
screen_group.append(enemy)
print(f"Enemy rectangle created at position ({enemy_x}, {enemy_y}) with size {enemy_width}x{enemy_height}")
print(f"Enemy will move in steps of {enemy_step} pixels every {enemy_move_delay} seconds")

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
print("Rectangle enemy will move side to side and drop down")

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
        projectile.y = projectile_y

        # Check for collision with enemy
        # Collision occurs if projectile overlaps with enemy rectangle
        if (projectile.x + projectile_radius >= enemy_x and  # Projectile right edge >= enemy left edge
            projectile.x - projectile_radius <= enemy_x + enemy_width and  # Projectile left edge <= enemy right edge
            projectile.y + projectile_radius >= enemy_y and  # Projectile bottom edge >= enemy top edge
            projectile.y - projectile_radius <= enemy_y + enemy_height):  # Projectile top edge <= enemy bottom edge

            print("HIT")
            # Remove the projectile when it hits
            screen_group.remove(projectile)
            projectile = None

        # Remove projectile if it goes off screen (only if it wasn't already removed by collision)
        elif projectile_y < -projectile_radius:
            screen_group.remove(projectile)  # Remove from display
            projectile = None  # Clear our reference
            print("Projectile removed")

    # Update enemy movement (Space Invaders discrete steps)
    enemy_move_timer += 0.01  # Add frame time (since we sleep 0.01 each frame)

    if enemy_move_timer >= enemy_move_delay:  # Time to move?
        enemy_move_timer = 0  # Reset timer

        # Move enemy one step
        enemy_x += enemy_step * enemy_direction

        # Check if enemy hits screen edge
        if enemy_x <= 0 or enemy_x >= display.width - enemy_width:
            # Change direction and drop down
            enemy_direction *= -1  # Flip direction
            enemy_y += enemy_drop_distance  # Move down
            print(f"Enemy direction changed, now at ({enemy_x}, {enemy_y})")
        else:
            print(f"Enemy stepped to ({enemy_x}, {enemy_y})")

    # Update enemy position on display
    enemy.x = enemy_x
    enemy.y = enemy_y

    time.sleep(0.01)
