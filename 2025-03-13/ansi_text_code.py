# ANSI escape sequences in the REPL
import time
i=0

while True:
    # regular version:
    # print(i, time.monotonic())

    # Clear screen
    print("\033[H\033[J", end="")  # \033 esc, [H cursor home, [J clear screen

    print(i, time.monotonic())

    # two colors on one line
    print("\033[34m",i,"\033[31m",time.monotonic(), "\033[0m")

    # add text formatting
    print("\033[1;4;34m",i,"\033[21;24;30;41m",time.monotonic(), "\033[0m")

    i=i+1
    time.sleep(0.1)

# # Text colors
# print("Text Colors:")
# print("\033[30mBlack Text (30)\033[0m")  # esc, [<color_code>, m end color command
# print("\033[31mRed Text (31)\033[0m")
# print("\033[32mGreen Text (32)\033[0m")
# print("\033[33mYellow Text (33)\033[0m")
# print("\033[34mBlue Text (34)\033[0m")
# print("\033[35mMagenta Text (35)\033[0m")
# print("\033[36mCyan Text (36)\033[0m")
# print("\033[37mWhite Text (37)\033[0m")

# print("\033[34m Hello \033[0m")

# print("\033[1mThis text is bold\033[0m")
# print("\033[2mThis text is dimmed\033[0m")
# print("\033[3mThis text is italic or highlighted\033[0m")
# print("\033[4mThis text is underlined\033[0m")
# print("\033[7mThis text has inverted colors\033[0m")

# # Bold, underlined and red text
# print("\033[1;4;31mBold, underlined red text\033[0m")
# print("\033[1;4mBold and underlined\033[24m now just bold\033[0m now only regular")


# # Background color demo
# print("\n4. Background Colors:")
# print("\033[40m Black Background (40m) \033[0m")
# print("\033[41m Red Background (41m) \033[0m")
# print("\033[42m Green Background (42m) \033[0m")
# print("\033[43m Yellow Background (43m) \033[0m")
# print("\033[44m Blue Background (44m) \033[0m")
# print("\033[45m Magenta Background (45m) \033[0m")
# print("\033[46m Cyan Background (46m) \033[0m")
# print("\033[47m White Background (47m) \033[0m")
