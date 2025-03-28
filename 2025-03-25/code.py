
import array
import time
import usb.core
import adafruit_usb_host_descriptors

# SNES-style gamepad button mapping
BUTTONS = [
    "Up", "Down", "Left", "Right",
    "A", "B", "X", "Y",
    "Start", "Select",
    "L-Shoulder", "R-Shoulder"
]

# Will store button mappings as we calibrate
BUTTON_MAPS = {}

# Set to true to print detailed information about all devices found
VERBOSE_SCAN = True

DIR_IN = 0x80
controller = None

# Initial device scan
if VERBOSE_SCAN:
    for device in usb.core.find(find_all=True):
        controller = device
        print("pid", hex(device.idProduct))
        print("vid", hex(device.idVendor))
        print("man", device.manufacturer)
        print("product", device.product)
        print("serial", device.serial_number)
        print("config[0]:")
        config_descriptor = adafruit_usb_host_descriptors.get_configuration_descriptor(
            device, 0
        )

        i = 0
        while i < len(config_descriptor):
            descriptor_len = config_descriptor[i]
            descriptor_type = config_descriptor[i + 1]
            if descriptor_type == adafruit_usb_host_descriptors.DESC_CONFIGURATION:
                config_value = config_descriptor[i + 5]
                print(f" value {config_value:d}")
            elif descriptor_type == adafruit_usb_host_descriptors.DESC_INTERFACE:
                interface_number = config_descriptor[i + 2]
                interface_class = config_descriptor[i + 5]
                interface_subclass = config_descriptor[i + 6]
                print(f" interface[{interface_number:d}]")
                print(
                    f"  class {interface_class:02x} subclass {interface_subclass:02x}"
                )
            elif descriptor_type == adafruit_usb_host_descriptors.DESC_ENDPOINT:
                endpoint_address = config_descriptor[i + 2]
                if endpoint_address & DIR_IN:
                    print(f"  IN {endpoint_address:02x}")
                else:
                    print(f"  OUT {endpoint_address:02x}")
            i += descriptor_len

# get the first device found
device = None
while device is None:
    for d in usb.core.find(find_all=True):
        device = d
        break
    time.sleep(0.1)

# set configuration so we can read data from it
device.set_configuration()
print(f"configuration set for {device.manufacturer}, {device.product}, {device.serial_number}")

# Test to see if the kernel is using the device and detach it.
if device.is_kernel_driver_active(0):
    device.detach_kernel_driver(0)

# buffer to hold 64 bytes
buf = array.array("B", [0] * 64)


def print_array(arr, max_index=None, fmt="hex"):
    """
    Print the values of an array
    :param arr: The array to print
    :param max_index: The maximum index to print. None means print all.
    :param fmt: The format to use, either "hex" or "bin"
    :return: None
    """
    out_str = ""
    if max_index is None or max_index >= len(arr):
        length = len(arr)
    else:
        length = max_index

    for i in range(length):
        if fmt == "hex":
            out_str += f"{int(arr[i]):02x} "
        elif fmt == "bin":
            out_str += f"{int(arr[i]):08b} "
    print(out_str)


def reports_equal(report_a, report_b):
    """
    Test if two reports are equal.

    :param report_a: First report data
    :param report_b: Second report data
    :return: True if the reports are equal, otherwise False.
    """
    if report_a is None and report_b is not None or report_b is None and report_a is not None:
        return False

    for i in range(min(len(report_a), len(report_b))):
        if report_a[i] != report_b[i]:
            return False
    return True


def detect_button_press(idle_report, button_report):
    """
    Detect which bits changed when a button was pressed

    :param idle_report: Report when no buttons are pressed
    :param button_report: Report when a button is pressed
    :return: List of (byte_index, bit_position) tuples that changed
    """
    changes = []

    for i in range(min(len(idle_report), len(button_report))):
        if idle_report[i] != button_report[i]:
            # Find which bits changed
            diff = idle_report[i] ^ button_report[i]
            # Identify which specific bits changed
            for bit in range(8):
                if (diff >> bit) & 1:
                    changes.append((i, bit))

    return changes


def get_controller_state():
    """
    Get the current state of the controller.
    Handles timeouts and retries.

    :return: Current controller state or None on repeated failure
    """
    for _ in range(5):  # Try up to 5 times
        try:
            count = device.read(0x81, buf, timeout=100)
            return buf[:count]
        except usb.core.USBTimeoutError:
            pass  # Try again
    return None


def calibrate_buttons():
    """
    Guide the user through pressing each button to map them
    """
    print("\n=== SNES GAMEPAD CALIBRATION ===")
    print("This will help map each button on your controller.")
    print("You'll need to press each button when prompted.")
    print("\nFirst, make sure NO buttons are pressed on the controller.")

    # Use keyboard to advance for initial step
    input("Press Enter on your KEYBOARD when the controller is in neutral position...")

    # Get several samples of the idle state to make sure it's stable
    print("Recording idle state...")
    idle_samples = []
    for _ in range(5):
        state = get_controller_state()
        if state:
            idle_samples.append(state)
        time.sleep(0.1)

    if not idle_samples:
        print("Failed to get any controller readings. Please check the connection.")
        return None

    # Check if all idle samples are the same
    for sample in idle_samples[1:]:
        if not reports_equal(sample, idle_samples[0]):
            print("Warning: Controller state is unstable at rest. Try again with no buttons pressed.")
            return None

    idle_state = idle_samples[0]
    print("Idle state recorded:")
    print_array(idle_state)

    # Cache of the last several readings to detect actual changes
    last_states = [idle_state[:] for _ in range(5)]

    # Now map each button
    for button in BUTTONS:
        # Wait for user to be ready for next button
        input(f"\nPress Enter on your KEYBOARD when ready to calibrate the {button} button...")

        print(f"Now press and hold the {button} button on your controller...")

        # Wait for a state change that persists for multiple readings
        button_state = None
        start_time = time.monotonic()
        timeout = 15  # 15 seconds to press the button

        while time.monotonic() - start_time < timeout:
            current_state = get_controller_state()
            if current_state is None:
                continue

            # Check if current state is different from idle
            if not reports_equal(current_state, idle_state):
                # Check if this change is consistent for a few readings
                consistent_change = True

                # Wait and check a few more readings to confirm
                for _ in range(3):
                    time.sleep(0.1)
                    confirm_state = get_controller_state()
                    if confirm_state is None or reports_equal(confirm_state, idle_state):
                        consistent_change = False
                        break

                if consistent_change:
                    button_state = current_state
                    break

            time.sleep(0.1)

        if button_state is None:
            print(f"No consistent change detected for {button}. Skipping.")
            continue

        print(f"{button} button detected:")
        print_array(button_state)

        # Detect what changed
        changes = detect_button_press(idle_state, button_state)
        if changes:
            BUTTON_MAPS[button] = changes
            print(f"Detected changes for {button}: {changes}")
        else:
            print(f"No bit changes detected for {button}. Skipping.")

        # Wait for button release
        print(f"Release the {button} button now...")
        start_time = time.monotonic()

        while time.monotonic() - start_time < 5:  # 5 second timeout for release
            current_state = get_controller_state()
            if current_state is None:
                continue

            # Check if returned to idle state
            if reports_equal(current_state, idle_state):
                print(f"{button} button released.")
                break

            time.sleep(0.1)
        else:
            print(f"Button release timeout for {button}. Continuing anyway.")

        # Extra delay between buttons
        time.sleep(1)

    print("\nCalibration complete!")
    print(f"Successfully mapped {len(BUTTON_MAPS)} out of {len(BUTTONS)} buttons")
    return idle_state


def identify_buttons_pressed(current_state, idle_state):
    """
    Identify which buttons are pressed based on the current state

    :param current_state: Current controller state
    :param idle_state: Idle controller state (no buttons pressed)
    :return: List of buttons that are currently pressed
    """
    pressed_buttons = []

    for button, changes in BUTTON_MAPS.items():
        # For each mapped button, check if its change pattern is present
        button_pressed = True
        for byte_idx, bit_pos in changes:
            if byte_idx >= len(current_state) or byte_idx >= len(idle_state):
                button_pressed = False
                break

            # Check if the specific bit that should change for this button has changed
            mask = 1 << bit_pos
            if ((current_state[byte_idx] ^ idle_state[byte_idx]) & mask) == 0:
                button_pressed = False
                break

        if button_pressed:
            pressed_buttons.append(button)

    return pressed_buttons


def save_button_map():
    """
    Save the button mapping to a file for future use
    """
    try:
        with open("snes_button_map.py", "w") as f:
            f.write("# SNES Gamepad Button Mapping\n\n")
            f.write("BUTTON_MAPS = {\n")
            for button, changes in BUTTON_MAPS.items():
                f.write(f"    \"{button}\": {changes},\n")
            f.write("}\n")
        print("\nButton mapping saved to 'snes_button_map.py'")
    except Exception as e:
        print(f"\nError saving button map: {e}")
        # If we can't save to a file, print the mapping in a copyable format
        print_button_map_for_config()


def print_button_map_for_config():
    """
    Print the button mapping in a format that can be copied and pasted into a configuration file
    """
    print("\n# ------ COPY FROM HERE ------")
    print("# SNES Gamepad Button Mapping")
    print("BUTTON_MAPS = {")
    for button, changes in sorted(BUTTON_MAPS.items()):
        print(f"    \"{button}\": {changes},")
    print("}")
    print("# ------ COPY TO HERE ------")
    print("\nCopy the above code and save it to a file named 'snes_button_map.py'")
    print("Place this file in the same directory as your gamepad reader script.")


def load_button_map():
    """
    Try to load a previously saved button mapping
    """
    try:
        # Try to import the saved mapping
        import snes_button_map
        global BUTTON_MAPS
        BUTTON_MAPS = snes_button_map.BUTTON_MAPS
        print("\nLoaded button mapping from 'snes_button_map.py'")
        return True
    except ImportError:
        print("\nNo saved button mapping found.")
        return False


# Main program
print("\nSNES-Style Gamepad Reader")
print("------------------------")

# Try to load a saved mapping first
if not load_button_map():
    # If no mapping exists, calibrate the controller
    while True:
        idle_state = calibrate_buttons()
        if idle_state is not None:
            break
        print("\nCalibration failed. Let's try again.")
        input("Press Enter to restart calibration...")

    # Try to save the mapping, and if it fails, print it for copying
    save_button_map()
else:
    # Get current idle state
    print("\nMake sure no buttons are pressed on the controller...")
    input("Press Enter when ready...")

    # Get several samples of the idle state
    print("Recording idle state...")
    idle_samples = []
    for _ in range(5):
        state = get_controller_state()
        if state:
            idle_samples.append(state)
        time.sleep(0.1)

    if not idle_samples:
        print("Failed to get controller readings. Please check the connection.")
        while True:
            time.sleep(1)

    # Check if all idle samples are the same
    for sample in idle_samples[1:]:
        if not reports_equal(sample, idle_samples[0]):
            print("Warning: Controller state is unstable at rest.")
            print("Try again with no buttons pressed.")
            while True:
                time.sleep(1)

    idle_state = idle_samples[0]
    print("Idle state recorded:")
    print_array(idle_state)

print("\nController ready! Press buttons to see their state.")
print("Press Ctrl+C to exit.")

prev_state = idle_state[:]
prev_buttons = []

# Main loop
try:
    while True:
        current_state = get_controller_state()
        if current_state is None:
            continue

        # Only process if state has changed
        if not reports_equal(current_state, prev_state):
            # Identify pressed buttons
            pressed_buttons = identify_buttons_pressed(current_state, idle_state)

            # Only output if the pressed buttons have changed
            if pressed_buttons != prev_buttons:
                if pressed_buttons:
                    print(f"Buttons pressed: {', '.join(pressed_buttons)}")
                else:
                    print("No buttons pressed")

                # Show raw data for debugging
                # print("Raw data: ", end="")
                # print_array(current_state)
                # print()

            prev_buttons = pressed_buttons
            prev_state = current_state[:]

        time.sleep(0.01)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    print("\nExiting program.")
