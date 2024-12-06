import time
import board
import displayio
import vectorio
import adafruit_touchscreen

# Setup display
display = board.DISPLAY

# Create a group for the circles, triangle, and other display elements
main_group = displayio.Group()

# Circle radius
circle_radius = 10

# Create three circles with different initial positions
circle1 = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=circle_radius, x=100, y=100)
circle2 = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=circle_radius, x=200, y=100)
circle3 = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=circle_radius, x=300, y=100)

# Set different colors for each circle
circle1.pixel_shader[0] = 0xFF0000  # Red
circle2.pixel_shader[0] = 0x00FF00  # Green
circle3.pixel_shader[0] = 0x0000FF  # Blue

# Add the circles to the display group
main_group.append(circle1)
main_group.append(circle2)
main_group.append(circle3)

# Create the triangle using a vectorio.Polygon, initially with the points of the circles
triangle_points = [(circle1.x, circle1.y), (circle2.x, circle2.y), (circle3.x, circle3.y)]
triangle = vectorio.Polygon(pixel_shader=displayio.Palette(1), points=triangle_points)
triangle.pixel_shader[0] = 0xFFFF00  # Yellow

# Add the triangle to the display group
main_group.append(triangle)

# Set the display root group to our main group
display.root_group = main_group

# Initialize touchscreen (assumes you are using a touchscreen compatible with Adafruit's library)
touchscreen = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL, board.TOUCH_XR, board.TOUCH_YD, board.TOUCH_YU,
    calibration=((6584, 59861), (9505, 57492)),
    size=(board.DISPLAY.width, board.DISPLAY.height),
)

# Variables to track touch and dragging state for each circle
is_dragging1 = False
is_dragging2 = False
is_dragging3 = False

# Variables to track which circle is being dragged
dragged_circle = None

while True:
    touch_point = touchscreen.touch_point  # Get the current touch point

    if touch_point:
        touch_x, touch_y, pressure = touch_point
        
        # Check if the touch is inside any of the circles and start dragging that circle
        if (touch_x - circle1.x)**2 + (touch_y - circle1.y)**2 <= circle_radius**2:
            dragged_circle = circle1
            is_dragging1 = True
        elif (touch_x - circle2.x)**2 + (touch_y - circle2.y)**2 <= circle_radius**2:
            dragged_circle = circle2
            is_dragging2 = True
        elif (touch_x - circle3.x)**2 + (touch_y - circle3.y)**2 <= circle_radius**2:
            dragged_circle = circle3
            is_dragging3 = True
        
        # If a circle is being dragged, update its position
        if dragged_circle:
            dragged_circle.x = touch_x
            dragged_circle.y = touch_y

            # Update the triangle points based on the new positions of the circles
            triangle.points = [
                (circle1.x, circle1.y),
                (circle2.x, circle2.y),
                (circle3.x, circle3.y),
            ]
    
    else:
        # If no touch is detected, stop dragging all circles
        is_dragging1 = False
        is_dragging2 = False
        is_dragging3 = False
        dragged_circle = None
    
    time.sleep(0.01)  # Small delay for smoother dragging
