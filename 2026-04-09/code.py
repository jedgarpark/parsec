import board
import busio
import time

uart = busio.UART(board.D0, board.D1, baudrate=115200)
time.sleep(1)  # give TermDriver2 time to boot and be ready

uart.write(b'\x1b[2J')      # clear screen
uart.write(b'\x1b[H')       # cursor home
time.sleep(1)

indent = 0

while True:
    msg = ' ' * indent + 'CircuitPython Parsec'
    print(msg)
    uart.write((msg + '\r\n').encode())
    time.sleep(0.25)
    indent = (indent + 4) % 24
