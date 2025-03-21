import time
import board
import analogio

# Set up six analog inputs
analog_pins = [
    ("A0", analogio.AnalogIn(board.A0)),
    ("A1", analogio.AnalogIn(board.A1)),
    ("A2", analogio.AnalogIn(board.A2)),
    ("A3", analogio.AnalogIn(board.A3)),
    ("A4", analogio.AnalogIn(board.A4)),
    ("A5", analogio.AnalogIn(board.A5))
]

block = "\u2588"

def get_voltage(pin):
    # Convert the raw analog reading to voltage (0-3.3V)
    return (pin.value * 3.3) / 65536

def draw_bar_graph(readings, max_height=10, bar_width=3):
    # Clear the previous output
    print("\033[H\033[J", end="")  # ANSI escape sequences to clear screen

    # Draw the bar graph
    for i in range(max_height, 0, -1):
        line = "|"
        for name, voltage in readings:
            # Calculate how many blocks to show for this voltage
            bar_height = int((voltage / 3.3) * max_height)

            if i <= bar_height:
                # line += "█" * bar_width + " "
                line += block * bar_width + " "
            else:
                line += " " * bar_width + " "
        print(line + "|")

    # Print the pin labels
    labels = "|"
    for name, _ in readings:
        # Center the pin name in the bar width
        labels += name.center(bar_width + 1)
    print(labels + "|")

    # Print voltage values
    values = "|"
    for _, voltage in readings:
        # Format voltage to fit in bar width
        val_str = f"{voltage:.1f}".center(bar_width + 1)
        values += val_str
    print(values + "|")

# Main loop
while True:
    # Read voltage from all pins
    current_readings = [(name, get_voltage(pin)) for name, pin in analog_pins]

    # Draw the graph
    draw_bar_graph(current_readings)

    # Pause before the next reading
    time.sleep(0.15)

'''
█ U+2588 Full block
▓ U+2593 Dark shade
▒ U+2592 Medium shade
░ U+2591 Light shade
▌ U+258C Left half block
▐ U+2590 Right half block
▄ U+2584 Lower half block
▀ U+2580 Upper half block

■ U+25A0 Black square
□ U+25A1 White square
▪ U+25AA Black small square
▫ U+25AB White small square
○ U+25CB White circle
● U+25CF Black circle
◆ U+25C6 Black diamond
◇ U+25C7 White diamond
▲ U+25B2 Black up-pointing triangle
△ U+25B3 White up-pointing triangle
▼ U+25BC Black down-pointing triangle
▽ U+25BD White down-pointing triangle
◀ U+25C0 Black left-pointing triangle
▶ U+25B6 Black right-pointing triangle

─ U+2500 Horizontal line
│ U+2502 Vertical line
┌ U+250C Top-left corner
┐ U+2510 Top-right corner
└ U+2514 Bottom-left corner
┘ U+2518 Bottom-right corner
├ U+251C Vertical line and right
┤ U+2524 Vertical line and left
┬ U+252C Horizontal line and down
┴ U+2534 Horizontal line and up
┼ U+253C Vertical and horizontal line

▏ U+258F Left one eighth block
▎ U+258E Left one quarter block
▍ U+258D Left three eighths block
▌ U+258C Left half block
▋ U+258B Left five eighths block
▊ U+258A Left three quarters block
▉ U+2589 Left seven eighths block
'''
