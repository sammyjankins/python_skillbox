# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

y_levels = list(range(0, 601, 50))
points = []
x = 0
for x_step in range(0, 600, 100):
    step = 50
    x = x_step
    for y in y_levels:
        points.append(sd.get_point(x, y))
        x += step
        points.append(sd.get_point(x, y))
        step = -step
    sd.lines(points, sd.COLOR_ORANGE)
    points = []
    step = 50
    x += step
    for y in y_levels:
        points.append(sd.get_point(x, y))
        x -= step
        points.append(sd.get_point(x, y))
        step = -step
    sd.lines(points, sd.COLOR_ORANGE)
    points = []

sd.pause()

# зачет!