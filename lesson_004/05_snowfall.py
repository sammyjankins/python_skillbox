# -*- coding: utf-8 -*-

import simple_draw as sd

# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

N = 20

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()

sd.resolution = (800, 800)
x_levels = []
y_levels = []
lengths = []
delta_y = []
factors = []
for _ in range(N):
    x_levels.append(sd.random_number(50, 750))
    y_levels.append(sd.random_number(650, 800))
    delta_y.append(sd.random_number(20, 60))
    lengths.append(sd.random_number(10, 100))
    factors.append(((sd.random_number(3, 8) / 10), (sd.random_number(3, 8) / 10), sd.random_number(1, 60)))

while True:
    for index in range(N):
        if y_levels[index] > 50:
            sd.snowflake(sd.get_point(x_levels[index], y_levels[index]),
                         lengths[index],
                         sd.background_color,
                         factors[index][0],
                         factors[index][1],
                         factors[index][2])
            y_levels[index] -= delta_y[index]
            x_levels[index] += sd.random_number(-50, 50)
        else:
            y_levels[index] = sd.random_number(650, 800)
            delta_y[index] = sd.random_number(20, 60)
            factors[index] = ((sd.random_number(3, 8) / 10), (sd.random_number(3, 8) / 10), sd.random_number(1, 60))
        sd.snowflake(sd.get_point(x_levels[index], y_levels[index]),
                     lengths[index],
                     sd.COLOR_WHITE,
                     factors[index][0],
                     factors[index][1],
                     factors[index][2])
    if sd.user_want_exit():
        break

sd.pause()

# подсказка: что бы убрать мигание нужно
#  - отключить clear_screen()
#  - на старом месте снежинки отрисовать её же, но цветом sd.background_color


# 4) Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg


# зачет!