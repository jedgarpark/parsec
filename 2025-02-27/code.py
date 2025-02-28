# CPU Benchmark for Feather RP2350
import time
import random
import microcontroller
import board
import displayio
from adafruit_ili9341 import ILI9341

# Release any resources currently in use for the displays
displayio.release_displays()

# Set up SPI connection for display
spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

# Set up the display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ILI9341(display_bus, width=320, height=240)


# Define CPU speeds to test
speeds = [
    100_000_000,  # 100 MHz
    133_000_000,  # 133 MHz (typical default)
    150_000_000,  # 150 MHz
    200_000_000   # 200 MHz
]

# Function to perform an extremely intensive calculation
def intensive_calculation():
    # Define dimensions for intensive computation
    matrix_size = 40
    iterations = 3
    trig_size = 2000

    # Create the matrices
    matrix_a = [[random.random() for _ in range(matrix_size)] for _ in range(matrix_size)]
    matrix_b = [[random.random() for _ in range(matrix_size)] for _ in range(matrix_size)]
    matrix_c = [[random.random() for _ in range(matrix_size)] for _ in range(matrix_size)]
    result = [[0 for _ in range(matrix_size)] for _ in range(matrix_size)]
    trig_array = [0] * trig_size

    # Start timing
    start_time = time.monotonic()

    # Run multiple iterations
    for iteration in range(iterations):
        # Matrix multiplication
        for i in range(matrix_size):
            for j in range(matrix_size):
                for k in range(matrix_size):
                    result[i][j] += matrix_a[i][k] * matrix_b[k][j]

        # Trigonometric calculations
        for i in range(trig_size):
            # Multi-term Taylor series for sin, cos
            x = (i % 100) * 0.1
            x2 = x * x
            x3 = x2 * x
            x4 = x3 * x
            x5 = x4 * x
            x6 = x5 * x
            x7 = x6 * x
            x8 = x7 * x
            x9 = x8 * x

            # Extended sin approximation
            sin_x = x - (x3 / 6.0) + (x5 / 120.0) - (x7 / 5040.0) + (x9 / 362880.0)

            # Extended cos approximation
            cos_x = 1.0 - (x2 / 2.0) + (x4 / 24.0) - (x6 / 720.0) + (x8 / 40320.0)

            # Compute tan(x) = sin(x)/cos(x)
            tan_x = sin_x / (cos_x + 0.0000001)

            # Store result
            trig_array[i] = (sin_x * cos_x) / (abs(tan_x) + 0.0001)

        # Matrix transformation with trig results
        for i in range(matrix_size):
            for j in range(matrix_size):
                idx1 = (i * 5) % trig_size
                idx2 = (j * 7) % trig_size

                if idx1 < trig_size and idx2 < trig_size:
                    factor = (1.0 + trig_array[idx1]) / (1.0 + abs(trig_array[idx2]))
                    result[i][j] = (result[i][j] + matrix_c[i][j]) * factor

        # Prime number searching
        primes_found = 0
        for num in range(1000, 2000):
            is_prime = True
            for divisor in range(2, int(num**0.5) + 1):
                if num % divisor == 0:
                    is_prime = False
                    break
            if is_prime:
                primes_found += 1
                if primes_found < matrix_size:
                    result[primes_found][primes_found] *= 1.01

        # Swap matrices for the next iteration
        matrix_a, matrix_b, matrix_c = matrix_b, matrix_c, result

    # End timing
    end_time = time.monotonic()

    calculation_time = end_time - start_time
    return calculation_time

# Print header
print("\n" + "=" * 40)
print("RP2350 CPU BENCHMARK")
print("=" * 40)

# Store results for comparison
results = {}

# Get the current/starting frequency
current_freq = microcontroller.cpu.frequency
print(f"Starting CPU frequency: {current_freq // 1_000_000} MHz")

# Run benchmark at each speed
for speed in speeds:
    print("\n" + "-" * 40)
    print(f"Setting CPU to {speed // 1_000_000} MHz...")

    try:
        # Set the CPU speed
        microcontroller.cpu.frequency = speed

        # Significant delay to allow frequency change to take effect
        time.sleep(1.0)

        # Verify the frequency was set
        actual_freq = microcontroller.cpu.frequency
        print(f"Actual frequency: {actual_freq // 1_000_000} MHz")

        # Run the benchmark
        print("Running benchmark... (this may take a while)")

        # Run the calculation
        elapsed_time = intensive_calculation()

        # Store and print the result
        results[actual_freq] = elapsed_time
        print(f"Result: {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"Error during benchmark at {speed // 1_000_000} MHz: {e}")

    # Brief pause before next test
    time.sleep(0.5)

# Reset to the original frequency
print("\n" + "-" * 40)
print(f"Resetting CPU to original frequency: {current_freq // 1_000_000} MHz")
microcontroller.cpu.frequency = current_freq
time.sleep(0.5)

# Print summary of results
print("\n" + "=" * 40)
print("BENCHMARK RESULTS SUMMARY")
print("=" * 40)

# Sort results by frequency
sorted_results = sorted(results.items())

# If we have a baseline result to compare to
if sorted_results:
    baseline_freq, baseline_time = sorted_results[0]

    print(f"{'Frequency (MHz)':15} | {'Time (s)':10} | {'Speedup':10}")
    print("-" * 40)

    for freq, time in sorted_results:
        speedup = baseline_time / time if time > 0 else 0
        print(f"{freq // 1_000_000:15} | {time:10.2f} | {speedup:10.2f}x")

print("\nBenchmark complete!")
