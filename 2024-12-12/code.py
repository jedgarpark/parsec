# cpy Parsec triangle editor color picker

import time
import board
import displayio
import vectorio
import adafruit_touchscreen
import adafruit_display_shapes.rect

# Set up display
display = board.DISPLAY
main_group = displayio.Group()

circle_radius = 10
# Create circles with updated position for circle3 (y=180)
circle1 = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=circle_radius, x=100, y=100)
circle2 = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=circle_radius, x=200, y=100)
circle3 = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=circle_radius, x=300, y=180)  # circle3's new y position

# Set different colors for each circle
circle1.pixel_shader[0] = 0xc92f2e  
circle2.pixel_shader[0] = 0xe6bd34  
circle3.pixel_shader[0] = 0x3c6baa  

# Add the circles to the display group
main_group.append(circle1)
main_group.append(circle2)
main_group.append(circle3)

# Create triangle using circle positions as vertices
triangle_points = [(circle1.x, circle1.y), (circle2.x, circle2.y), (circle3.x, circle3.y)]
triangle = vectorio.Polygon(pixel_shader=displayio.Palette(1), points=triangle_points)
triangle.pixel_shader[0] = 0x02a599  # Default color

# Add triangle to the display group
main_group.append(triangle)

# Create center circle in the middle of the triangle
center_circle = vectorio.Circle(pixel_shader=displayio.Palette(1), radius=circle_radius, x=0, y=0)
center_circle.pixel_shader[0] = 0xFFFFFF  # White color for the center circle

# Add the center circle to the display group
main_group.append(center_circle)

# Set display root group to main group
display.root_group = main_group

# Initialize touchscreen (assumes you are using a touchscreen compatible with Adafruit's library)
touchscreen = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL, board.TOUCH_XR, board.TOUCH_YD, board.TOUCH_YU,
    calibration=((6584, 59861), (9505, 57492)),
    size=(board.DISPLAY.width, board.DISPLAY.height),
)

# Variables to track touch / drag state for each circle
is_dragging1 = False
is_dragging2 = False
is_dragging3 = False
dragged_circle = None

# Variables for color picker state
show_sliders = False
slider_x = 10
slider_y = 20  # Adjusted to the new value
slider_width = 120  # 120px wide sliders
slider_height = 30  # 30px tall sliders
red, green, blue = 0, 0, 0  # RGB initial values

# Create sliders and an "Enter" button (UI elements)
red_slider = adafruit_display_shapes.rect.Rect(x=slider_x, y=slider_y, width=slider_width, height=slider_height, fill=0xff0000)
green_slider = adafruit_display_shapes.rect.Rect(x=slider_x, y=slider_y + 40, width=slider_width, height=slider_height, fill=0x00ff00)
blue_slider = adafruit_display_shapes.rect.Rect(x=slider_x, y=slider_y + 80, width=slider_width, height=slider_height, fill=0x0000ff)
enter_button = adafruit_display_shapes.rect.Rect(x=slider_x + (slider_width // 2) - 15, y=slider_y + 120, width=30, height=30, fill=0x808080)  # Gray square button

# Add UI elements to the display group
main_group.append(red_slider)
main_group.append(green_slider)
main_group.append(blue_slider)
main_group.append(enter_button)

# Create indicator lines for each slider
red_indicator = adafruit_display_shapes.rect.Rect(x=slider_x, y=slider_y, width=2, height=slider_height, fill=0x808080)
green_indicator = adafruit_display_shapes.rect.Rect(x=slider_x, y=slider_y + 40, width=2, height=slider_height, fill=0x808080)
blue_indicator = adafruit_display_shapes.rect.Rect(x=slider_x, y=slider_y + 80, width=2, height=slider_height, fill=0x808080)

# Add indicator lines to the display group
main_group.append(red_indicator)
main_group.append(green_indicator)
main_group.append(blue_indicator)

# Hide sliders and indicators initially
red_slider.hidden = True
green_slider.hidden = True
blue_slider.hidden = True
enter_button.hidden = True
red_indicator.hidden = True
green_indicator.hidden = True
blue_indicator.hidden = True

# Function to update center circle position (centroid of the triangle)
def update_center_circle():
    cx = (circle1.x + circle2.x + circle3.x) // 3
    cy = (circle1.y + circle2.y + circle3.y) // 3
    center_circle.x = cx
    center_circle.y = cy

# Function to check if point is inside the center circle
def point_in_circle(px, py, circle):
    return (px - circle.x) ** 2 + (py - circle.y) ** 2 <= circle_radius ** 2

# Main loop
while True:
    touch_point = touchscreen.touch_point  # Get the current touch point

    if touch_point:
        touch_x, touch_y, pressure = touch_point
        
        # Check if the touch is inside the center circle (trigger for color picker)
        if point_in_circle(touch_x, touch_y, center_circle):
            show_sliders = True  # Show the sliders for color picker
            is_dragging1 = is_dragging2 = is_dragging3 = False  # Stop dragging circles
            dragged_circle = None  # Stop dragging any circle
            
        # Check if the touch is inside any of the circles and start dragging that circle
        elif (touch_x - circle1.x)**2 + (touch_y - circle1.y)**2 <= circle_radius**2:
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
            
            # Recalculate center circle position
            update_center_circle()
        
        # Check for interaction with sliders and Enter button
        if show_sliders:
            # Check if touch is on the sliders
            if slider_x <= touch_x <= slider_x + slider_width:
                if slider_y <= touch_y <= slider_y + slider_height:
                    red = int((touch_x - slider_x) / slider_width * 255)
                    red_slider.fill = (red << 16)  # Update red color
                    red_indicator.x = slider_x + int((red / 255) * slider_width)  # Update red indicator
                elif slider_y + 40 <= touch_y <= slider_y + 40 + slider_height:
                    green = int((touch_x - slider_x) / slider_width * 255)
                    green_slider.fill = (green << 8)  # Update green color
                    green_indicator.x = slider_x + int((green / 255) * slider_width)  # Update green indicator
                elif slider_y + 80 <= touch_y <= slider_y + 80 + slider_height:
                    blue = int((touch_x - slider_x) / slider_width * 255)
                    blue_slider.fill = blue  # Update blue color
                    blue_indicator.x = slider_x + int((blue / 255) * slider_width)  # Update blue indicator
                
                # Update the triangle color in real-time
                triangle.pixel_shader[0] = (red << 16) | (green << 8) | blue
            
            # Handle "Enter" button press
            if enter_button.x <= touch_x <= enter_button.x + 30 and enter_button.y <= touch_y <= enter_button.y + 30:
                # Finalize the color and hide sliders
                show_sliders = False
                red_slider.hidden = True
                green_slider.hidden = True
                blue_slider.hidden = True
                enter_button.hidden = True
                red_indicator.hidden = True
                green_indicator.hidden = True
                blue_indicator.hidden = True

    else:
        # If no touch is detected, stop dragging all circles
        is_dragging1 = False
        is_dragging2 = False
        is_dragging3 = False
        dragged_circle = None

    # Show sliders and indicators when needed
    if show_sliders:
        red_slider.hidden = False
        green_slider.hidden = False
        blue_slider.hidden = False
        enter_button.hidden = False
        red_indicator.hidden = False
        green_indicator.hidden = False
        blue_indicator.hidden = False

    time.sleep(0.01)  # Small delay for smoother interaction
