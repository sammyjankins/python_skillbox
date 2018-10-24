# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = res = (900, 600)
sd.background_color = sd.COLOR_BLACK


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:
    flakes = []
    level = 0    # будет сугроб

    def __init__(self):
        self.x = sd.randint(0, res[0])
        self.y = res[1]
        self.length = sd.randint(5, 50)
        self.delta_y = sd.randint(10, 20)
        self.delta_x = self.length // 5
        self.factor_a = sd.randint(4, 7) / 10
        self.factor_b = sd.randint(2, 5) / 10
        self.factor_c = sd.randint(40, 70)
        self.color = sd.COLOR_WHITE
        self.skip = False                      # чтобы не учитывалась каждый раз как только что упавшая
        Snowflake.flakes.append(self)

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
        if self.y > Snowflake.level:
            return True
        else:
            return False


# flake = Snowflake()
#
# while True:
#     flake.clear_previous_picture()
#     flake.move()
#     flake.draw()
#     if not flake.can_fall():
#         break
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break


def get_flakes(count=10):
    for _ in range(count):
        Snowflake()


def get_fallen_flakes():
    fallen_count = 0
    for flake in Snowflake.flakes:
        if not flake.skip:
            if not flake.can_fall():
                fallen_count += 1
                flake.skip = not flake.skip
    return fallen_count


get_flakes(25)

# сугроб увеличивается со временем

while True:
    for flake in Snowflake.flakes:
        if not flake.skip:
            flake.clear_previous_picture()
            flake.move()
            flake.draw()
    fallen_flakes = get_fallen_flakes()
    if fallen_flakes:
        get_flakes(count=fallen_flakes)
        Snowflake.level += fallen_flakes / 5
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()


