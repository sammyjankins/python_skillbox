# -*- coding: utf-8 -*-
import random

import simple_draw as sd

sd.resolution = (1200, 600)


def bubble(point, step, color=sd.COLOR_ORANGE):
    radius = 50
    for _ in range(3):
        radius += step
        sd.circle(center_position=point, radius=radius, width=2, color=color)


for y in range(100, 301, 100):
    for x in range(100, 1100, 100):
        point = sd.get_point(x, y)
        bubble(point, 5)


for _ in range(100):
    point = sd.random_point()
    step = random.randint(1, 15)
    bubble(point, step, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


sd.pause()

# зачет! 

