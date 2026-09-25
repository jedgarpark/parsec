# SPDX-FileCopyrightText: 2026 JP for Adafruit Industries
# SPDX-License-Identifier: MIT
#  random.choice()

# pick one element from a list at random
import time
import random

my_list = ['A', 'B', 'C', 'D']

i=1

while True:
    my_random_pick = random.choice(my_list)

    print(f"random pick {i}: {my_random_pick}")
    i=i+1
    time.sleep(1)
