# -*- coding: utf-8 -*-

import simple_draw as sd


# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.


def get_polygon(n):
    def draw_shapes(point, angle=0, length=200, width=3):
        end_point = point
        for _ in range(n):
            vector = sd.get_vector(start_point=point, angle=angle, length=length, width=width)
            vector.draw()
            point = vector.end_point
            angle += 360 / n
        sd.line(point, end_point, width=width)

    return draw_shapes


for draw_shape in [get_polygon(n) for n in range(1, 8)]:
    draw_shape(point=sd.random_point(), angle=42, length=100)

sd.pause()
