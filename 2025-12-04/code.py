# circuitpythong_uplot Microplot
# in community bundle
# https://circuitpython-uplot.readthedocs.io/en/latest/
#
import adafruit_display_text
import board
from circuitpython_uplot.cartesian import Cartesian
from circuitpython_uplot.plot import Plot, color

# Setting up the display
display = board.DISPLAY

# Adding the plot area
plot = Plot(0, 0, width=display.width, height=display.height, padding=20)

# plot axes type
plot.axs_params(axstype="cartesian")

# ticks
plot.tick_params(
    tickgrid=False, tickx_height=6, ticky_height=6, tickcolor=color.TEAL, showtext=True
)

x_data = [0, 1, 2, 3, 4, 5, 6]
y_data = [4, 2, 3, 6, 2, 60, 1]

Cartesian(plot, x_data, y_data, line_color=color.RED)

display.root_group = plot

while True:
    pass
