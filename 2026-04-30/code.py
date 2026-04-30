import time
from noise import noise  #Community bundle @todbot's noise simplex (Perlin-esque) noise

n1_stepsize = 0.06  # 0.02 # 0.005 small move through noise space, 0.1 bigger steps but smooth, 0.5 almost random
n2_stepsize = 0.02

i = 0  # frame counter

while True:
    i += 1  # advance a frame per loop

    n1 = noise(n1_stepsize * i)  # sample 1D noise value at position 0.06 * i, walking along the noise curve
    n2 = noise(n2_stepsize * i) # second noise value sampled a different rate for varied width


    '''Convert n1 (-1.0 to 1.0) into a screen column. +1 shifts range to 0–2, * 20 scales to 0–40 columns, int() floors it to a whole number of spaces.'''
    pos = int((n1 + 1) * 20)
    width = int((n2 + 1) * 20)  # same conversion for width, returns 0-40 chars wide

    '''Print one frame: pos spaces to indent, then \ for the left wall, then width spaces for the road interior, then / for the right wall. The \\ is an escaped backslash — a single \ in the output. Note the commas add a space between each argument.'''
    print(" " * pos, "\\", ' ' * width, "/")

    time.sleep(0.05)
