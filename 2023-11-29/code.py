# Using 'for' statements with enumeration

import time
# make a list
some_cool_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
print()

# Instead of this:
# for i in range(len(some_cool_letters)):
#     print(some_cool_letters[i])
#     time.sleep(0.2)

# Do this:
for a_cool_letter in some_cool_letters:
    print(a_cool_letter)
    time.sleep(0.2)

# Get fancy a show the count:
# for count, a_cool_letter in enumerate(some_cool_letters):
#     print(count, a_cool_letter)
#     time.sleep(0.2)
