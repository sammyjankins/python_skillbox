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
    def draw_shapes(point, sides, angle_step, angle=0, length=200):
        if sides is 1:
            return point
        v1 = sd.get_vector(start_point=point, angle=angle, length=length, width=3)
        v1.draw()
        return draw_shapes(point=v1.end_point,
                           sides=sides - 1,
                           angle_step=angle_step,
                           angle=angle + angle_step,
                           length=length)

    def shapes(point, angle=0, length=200):
        angle_step = 360 / n
        end_point = draw_shapes(point, n, angle_step, angle, length)
        sd.line(point, end_point, width=3)

    return shapes


for draw_shape in [get_polygon(n) for n in range(1, 8)]:
    draw_shape(point=sd.random_point(), angle=13, length=100)

sd.pause()
