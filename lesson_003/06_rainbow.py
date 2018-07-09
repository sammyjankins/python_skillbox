# -*- coding: utf-8 -*-

# (цикл for)

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

width = 4
step = 5
x_start = y_start = 50
x_end = y_end = 550

for color in rainbow_colors:
    sd.line(sd.get_point(x_start, y_start),
            sd.get_point(x_end, y_end),
            color,
            width)
    x_start += step
    x_end += step


step = 15
width = 20
x_left = -50
y_left = -500
x_right = 1500
y_right = 500

for color in rainbow_colors:
    sd.ellipse(sd.get_point(x_left, y_left),
               sd.get_point(x_right, y_right),
               color,
               width)
    x_left += step
    y_right -= step

sd.pause()


# зачет!