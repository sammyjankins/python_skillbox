# -*- coding: utf-8 -*-

import simple_draw as sd


# Запросить у пользователя желаемую фигуру посредством выбора из существующих
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg


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


my_point = sd.get_point(300, 300)

print('Возможные фигуры: \n',
      '0 :  треугольник\n',
      '1 :  квадрат\n',
      '2 :  пятиугольник\n',
      '3 :  шестиугольник\n', )

while True:
    number = int(input('Введите желаемую фигуру: '))
    if 0 <= number <= 3:
        if number is 0:
            triangle(my_point, 30, 100)
            break
        elif number is 1:
            square(my_point, 30, 100)
            break
        elif number is 2:
            pentagon(my_point, 30, 100)
            break
        elif number is 3:
            hexagon(my_point, 30, 100)
            break
    else:
        print('Вы ввели некорректный номер!')

sd.pause()
