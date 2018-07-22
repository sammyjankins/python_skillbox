# -*- coding: utf-8 -*-

import simple_draw as sd


# Написать функции рисования равносторонних геометрических фигур:
# - треугольника
# - квадрата
# - пятиугольника
# - шестиугольника
# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны

# Нарисовать все фигуры
# Выделить общую часть алгоритма рисования в отдельную функцию
# Придумать, как устранить разрыв в начальной точке фигуры

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см lesson_004/results/exercise_01_shapes.jpg


def draw_shapes(point, sides, angle_step, angle=0, length=200):
    if sides is 1:
        return point
    v1 = sd.get_vector(start_point=point, angle=angle, length=length, width=3)
    v1.draw()
    point = draw_shapes(point=v1.end_point,
                        sides=sides - 1,
                        angle_step=angle_step,
                        angle=angle + angle_step,
                        length=length)
    return point


def triangle(point, angle=0, length=200):
    sides = 3
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, angle, length)
    sd.line(point, end_point, width=3)


def square(point, angle=0, length=200):
    sides = 4
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, angle, length)
    sd.line(point, end_point, width=3)


def pentagon(point, angle=0, length=200):
    sides = 5
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, angle, length)
    sd.line(point, end_point, width=3)


def hexagon(point, angle=0, length=200):
    sides = 6
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, angle, length)
    sd.line(point, end_point, width=3)


triangle(sd.get_point(100, 400), 30, 100)
square(sd.get_point(400, 400), 30, 100)
pentagon(sd.get_point(100, 100), 30, 100)
hexagon(sd.get_point(400, 100), 30, 100)

sd.pause()

# зачет!
