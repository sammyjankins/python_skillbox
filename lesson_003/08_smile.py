# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd
import random


def draw_face(x, y, color):
    left_point = sd.get_point(x, y)
    right_point = sd.get_point(x + 150, y + 120)
    sd.ellipse(left_point, right_point, color, 2)
    sd.circle(sd.get_point(x + 40, y + 70), 10, color, 2)
    sd.circle(sd.get_point(x + 110, y + 70), 10, color, 2)
    points = [sd.get_point(x + 30, y + 40),
              sd.get_point(x + 60, y + 30),
              sd.get_point(x + 90, y + 30),
              sd.get_point(x + 120, y + 40)]
    sd.lines(points, color)


for _ in range(10):
    draw_face(random.randint(50, 550), random.randint(50, 550), sd.COLOR_ORANGE)

sd.pause()

# зачет!
