# -*- coding: utf-8 -*-
import simple_draw as sd


# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих
#   и нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg


def draw_shapes(point, sides, angle_step, color, angle=0, length=200):
    if sides is 1:
        return point
    v1 = sd.get_vector(start_point=point, angle=angle, length=length, width=3)
    v1.draw(color=color)
    point = draw_shapes(point=v1.end_point,
                        sides=sides - 1,
                        angle_step=angle_step,
                        color=color,
                        angle=angle + angle_step,
                        length=length)
    return point


def triangle(point, angle=0, length=200, color=sd.COLOR_YELLOW):
    sides = 3
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, color, angle, length)
    sd.line(point, end_point, color, width=3)


def square(point, angle=0, length=200, color=sd.COLOR_YELLOW):
    sides = 4
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, color, angle, length)
    sd.line(point, end_point, color, width=3)


def pentagon(point, angle=0, length=200, color=sd.COLOR_YELLOW):
    sides = 5
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, color, angle, length)
    sd.line(point, end_point, color, width=3)


def hexagon(point, angle=0, length=200, color=sd.COLOR_YELLOW):
    sides = 6
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, color, angle, length)
    sd.line(point, end_point, color, width=3)


colors = (sd.COLOR_RED,
          sd.COLOR_ORANGE,
          sd.COLOR_YELLOW,
          sd.COLOR_GREEN,
          sd.COLOR_CYAN,
          sd.COLOR_BLUE,
          sd.COLOR_PURPLE)

print('Возможные цвета: \n',
      '0 :  red\n',
      '1 :  orange\n',
      '2 :  yellow\n',
      '3 :  green\n',
      '4 :  cyan\n',
      '5 :  blue\n',
      '6 :  purple')

while True:
    number = int(input('Введите желаемый цвет: '))
    if 0 <= number <= 6:
        color = colors[number]
        break
    else:
        print('Вы ввели некорректный номер!')

triangle(sd.get_point(100, 400), 30, 100, color)
square(sd.get_point(400, 400), 30, 100, color)
pentagon(sd.get_point(100, 100), 30, 100, color)
hexagon(sd.get_point(400, 100), 30, 100, color)

sd.pause()
