# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = res = (900, 600)


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:
    snow_count = 0

    def __init__(self):
        Snowflake.snow_count += 1
        self.x = sd.randint(0, res[0])
        self.y = res[1]
        self.length = sd.randint(5, 50)
        self.delta_y = sd.randint(10, 20)
        self.delta_x = self.length // 5
        self.factor_a = sd.randint(4, 7) / 10
        self.factor_b = sd.randint(2, 5) / 10
        self.factor_c = sd.randint(40, 70)
        self.color = sd.COLOR_WHITE

    def clear_previous_picture(self):
        self.color = sd.background_color
        Snowflake.draw(self)
        self.color = sd.COLOR_WHITE

    def move(self):
        self.x += self.delta_x
        self.y -= self.delta_y

    def draw(self):
        sd.snowflake(sd.get_point(self.x, self.y),
                     self.length,
                     self.color,
                     self.factor_a,
                     self.factor_b,
                     self.factor_c)

    def can_fall(self):
        return True if self.y >= 0 else False


flake = Snowflake()

while True:
    flake.clear_previous_picture()
    flake.move()
    flake.draw()
    if not flake.can_fall():
        break
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
# flakes = get_flakes(count=N)  # создать список снежинок
# while True:
#     for flake in flakes:
#         flake.clear_previous_picture()
#         flake.move()
#         flake.draw()
#     fallen_flakes = get_fallen_flakes()  # подчитать сколько снежинок уже упало
#     if fallen_flakes:
#         append_flakes(count=fallen_flakes)  # добавить еще сверху
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break

sd.pause()
