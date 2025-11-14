# Spyce Invaders
# collision and game over state
#
import math
import time

import adafruit_wii_classic
import board
import displayio
import framebufferio
import microcontroller
import sharpdisplay
import terminalio
import vectorio
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

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
    print("Showing splash screen...")
    time.sleep(1)
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

# Create black background (inverted from white)
background = Rect(0, 0, display.width, display.height, fill=0x000000)
screen_group.append(background)
display.root_group = screen_group

# Define colors
white = 0xFFFFFF
black = 0x000000

# Score tracking
score = 0
score_per_alien = 10

# Create score label at top of screen (white text on black background)
score_text = label.Label(
    terminalio.FONT, text=f"SCORE: {score}", color=white, x=10, y=17, scale=3
)
screen_group.append(score_text)

# Ship properties
ship_size = 16
ship_x = display.width // 2  # center it
ship_y = display.height - ship_size
move_step = 18

# Create palette for vectorio polygon (ship) - white ship on black background
ship_palette = displayio.Palette(2)
ship_palette[0] = black  # Background color
ship_palette[1] = white  # Ship color

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

# Load alien sprite bitmap from file (single frame, no animation)
try:
    alien_bitmap = displayio.OnDiskBitmap("alien_1a.bmp")
    alien_palette = alien_bitmap.pixel_shader
    print("Alien sprite loaded successfully")

    # Get alien dimensions from bitmap
    alien_width = alien_bitmap.width
    alien_height = alien_bitmap.height
    print(f"Alien sprite size: {alien_width}x{alien_height}")

except Exception as e:
    print(f"Could not load alien sprite: {e}")
    print("Falling back to rectangles")
    alien_bitmap = None
    alien_width = 18
    alien_height = 13

# Alien grid properties
alien_cols = 7  # Reduced from 11
alien_rows = 2
alien_spacing_x = 9
alien_spacing_y = 16
alien_step = 8
alien_direction = 1
alien_drop_distance = 12
alien_move_timer = 0
alien_move_delay = 0.05

# Starting position for top-left alien
alien_start_x = 20
alien_start_y = 150

# Create alien grid
aliens = []
for row in range(alien_rows):
    for col in range(alien_cols):
        x = alien_start_x + col * (alien_width + alien_spacing_x)
        y = alien_start_y + row * (alien_height + alien_spacing_y)

        if alien_bitmap is not None:
            # Use sprite bitmap (single frame, no animation)
            alien_tile = displayio.TileGrid(
                alien_bitmap, pixel_shader=alien_palette, x=x, y=y
            )
            screen_group.append(alien_tile)
            aliens.append({"tile": alien_tile, "alive": True, "col": col, "row": row})
        else:
            # Fallback to rectangle
            alien_rect = Rect(x, y, alien_width, alien_height, fill=black)
            screen_group.append(alien_rect)
            aliens.append({"rect": alien_rect, "alive": True, "col": col, "row": row})

print(f"Created {alien_cols}x{alien_rows} alien grid ({len(aliens)} total aliens)")

# Explosion state
explosion_lines = []
explosion_timer = 0
explosion_duration = 0.3

# Game state        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
game_over = False
game_over_text = None

# Projectile properties
projectile_radius = 4
projectile_speed = 20

# Create palette for projectiles - white projectiles on black background
projectile_palette = displayio.Palette(2)
projectile_palette[0] = black  # Background color
projectile_palette[1] = white  # Projectile color

# Single projectile variables
projectile = None
projectile_y = 0

# Button state tracking
last_a_pressed = False
last_start_pressed = False
last_select_pressed = False


def reset_game():
    """Reset the game to initial state"""
    global \
        score, \
        alien_direction, \
        aliens, \
        projectile, \
        explosion_lines, \
        game_over, \
        game_over_text

    print("GAME RESET!")

    # Clear game over state
    game_over = False
    if game_over_text is not None:
        try:
            screen_group.remove(game_over_text)
        except ValueError:
            pass
        game_over_text = None

    # Reset score
    score = 0
    score_text.text = f"SCORE: {score}"

    # Clear projectile if it exists
    if projectile is not None:
        try:
            screen_group.remove(projectile)
        except ValueError:
            pass  # Already removed
        projectile = None

    # Clear any explosions
    clear_explosion()

    # Remove all existing aliens (only if still alive/in display)
    for alien in aliens:
        if alien["alive"]:  # Only try to remove if still alive
            try:
                if "tile" in alien:
                    screen_group.remove(alien["tile"])
                elif "rect" in alien:
                    screen_group.remove(alien["rect"])
            except ValueError:
                pass  # Already removed somehow

    # Recreate alien grid
    aliens = []
    alien_direction = 1  # Reset direction to moving right

    for row in range(alien_rows):
        for col in range(alien_cols):
            x = alien_start_x + col * (alien_width + alien_spacing_x)
            y = alien_start_y + row * (alien_height + alien_spacing_y)

            if alien_bitmap is not None:
                # Use sprite bitmap (single frame, no animation)
                alien_tile = displayio.TileGrid(
                    alien_bitmap, pixel_shader=alien_palette, x=x, y=y
                )
                screen_group.append(alien_tile)
                aliens.append(
                    {"tile": alien_tile, "alive": True, "col": col, "row": row}
                )
            else:
                # Fallback to rectangle
                alien_rect = Rect(x, y, alien_width, alien_height, fill=black)
                screen_group.append(alien_rect)
                aliens.append(
                    {"rect": alien_rect, "alive": True, "col": col, "row": row}
                )

    print(
        f"Recreated {alien_cols}x{alien_rows} alien grid ({len(aliens)} total aliens)"
    )


def create_explosion(center_x, center_y):
    """Create 10 explosion lines radiating from center"""
    global explosion_lines, explosion_timer

    # Clear any existing explosion first
    clear_explosion()

    explosion_lines = []
    explosion_timer = 0  # Reset timer

    explosion_center_x = center_x + alien_width // 2
    explosion_center_y = center_y + alien_height // 2

    for i in range(10):
        angle = (i * 36) * (math.pi / 180)
        line_length = 15

        end_x = explosion_center_x + int(line_length * math.cos(angle))
        end_y = explosion_center_y + int(line_length * math.sin(angle))

        line = Line(explosion_center_x, explosion_center_y, end_x, end_y, color=white)
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


def check_alien_collision_with_ship():  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    """Check if any alien overlaps with the player ship"""
    # Ship bounding box (approximate triangle as a box)
    ship_left = ship_x - ship_size // 2
    ship_right = ship_x + ship_size // 2
    ship_top = ship_y - ship_size
    ship_bottom = ship_y + ship_size // 2

    for alien in aliens:
        if alien["alive"]:
            alien_obj = alien.get("tile") or alien.get("rect")

            # Check bounding box collision
            if (
                alien_obj.x < ship_right
                and alien_obj.x + alien_width > ship_left
                and alien_obj.y < ship_bottom
                and alien_obj.y + alien_height > ship_top
            ):
                return True

    return False


def trigger_game_over():  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    """Handle game over state"""
    global game_over, game_over_text

    game_over = True
    print(f"GAME OVER! Final Score: {score}")

    # Create game over text   # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    game_over_text = label.Label(
        terminalio.FONT,
        text="GAME OVER",
        color=white,
        x=display.width // 2 - 60,  # Center approximately
        y=50,
        scale=3,
    )
    screen_group.append(game_over_text)


print("Spyce Invaders ready!")
print(f"Display size: {display.width}x{display.height}")
print("Use D-pad to move the ship around the screen")
print("A button: Fire projectile")
print(f"Destroy all {len(aliens)} aliens!")

while True:
    # Skip gameplay updates if game over
    if game_over:   # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # Check for START button to restart
        current_start_pressed = ctrl_pad.buttons.START
        current_select_pressed = ctrl_pad.buttons.SELECT

        # START + SELECT = hard reset
        if current_start_pressed and current_select_pressed:
            print("START + SELECT pressed - Resetting CircuitPython board...")
            time.sleep(0.5)
            microcontroller.reset()

        # START alone = restart game
        if current_start_pressed:
            reset_game()

        time.sleep(0.01)
        continue  # Skip rest of game loop

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

    # Check for START + SELECT combo to reset board
    current_start_pressed = ctrl_pad.buttons.START
    current_select_pressed = ctrl_pad.buttons.SELECT

    # If both START and SELECT are pressed together, do a hard reset
    if current_start_pressed and current_select_pressed:
        print("START + SELECT pressed - Resetting CircuitPython board...")
        time.sleep(0.5)  # Brief delay so user sees the message
        microcontroller.reset()

    # Start button alone: Reset game
    if current_start_pressed and not last_start_pressed and not current_select_pressed:
        reset_game()

    last_start_pressed = current_start_pressed
    last_select_pressed = current_select_pressed

    # Update projectile (if it exists)
    if projectile is not None:
        # Move projectile up
        projectile_y -= projectile_speed
        projectile.y = projectile_y

        # Check for collision with any alive alien
        collision_occurred = False
        for alien in aliens:
            if alien["alive"]:
                # Handle both sprite and rect versions
                if "tile" in alien:
                    alien_obj = alien["tile"]
                else:
                    alien_obj = alien["rect"]

                if (
                    projectile.x + projectile_radius >= alien_obj.x
                    and projectile.x - projectile_radius <= alien_obj.x + alien_width
                    and projectile.y + projectile_radius >= alien_obj.y
                    and projectile.y - projectile_radius <= alien_obj.y + alien_height
                ):
                    # Alien hit!
                    screen_group.remove(alien_obj)
                    alien["alive"] = False

                    # Update score
                    score += score_per_alien
                    score_text.text = f"SCORE: {score}"

                    # Create explosion (this will clear any existing explosion first)
                    create_explosion(alien_obj.x, alien_obj.y)

                    # Remove the projectile
                    screen_group.remove(projectile)
                    projectile = None
                    collision_occurred = True

                    alive_count = count_alive_aliens()
                    print(f"HIT! Score: {score}, {alive_count} aliens remaining")

                    if alive_count == 0:
                        print(f"ALL ALIENS DESTROYED! FINAL SCORE: {score}")

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
            explosion_timer = 0

    # Update alien grid movement (all aliens move together)
    alien_move_timer += 0.01

    if alien_move_timer >= alien_move_delay:
        alien_move_timer = 0

        # Calculate new positions for edge detection - only check alive aliens once
        leftmost_x = float("inf")
        rightmost_x = 0

        # Single pass through aliens to find edges
        for alien in aliens:
            if alien["alive"]:
                alien_obj = alien.get("tile") or alien.get("rect")
                if alien_obj.x < leftmost_x:
                    leftmost_x = alien_obj.x
                if alien_obj.x > rightmost_x:
                    rightmost_x = alien_obj.x

        # Check if grid hits screen edge
        should_drop = False
        if alien_direction == 1 and rightmost_x + alien_width >= display.width:
            alien_direction = -1
            should_drop = True
        elif alien_direction == -1 and leftmost_x <= 0:
            alien_direction = 1
            should_drop = True

        # Move all aliens (no animation updates)
        for alien in aliens:
            if alien["alive"]:
                alien_obj = alien.get("tile") or alien.get("rect")

                # Move alien
                if should_drop:
                    alien_obj.y += alien_drop_distance
                alien_obj.x += alien_step * alien_direction

        # Check for collision with player ship after moving
        if check_alien_collision_with_ship():
            trigger_game_over()

    time.sleep(0.0167)  # ~60 FPS instead of 100 FPS
