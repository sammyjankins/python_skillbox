# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = res = (900, 600)
sd.background_color = sd.COLOR_BLACK


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку

class Snowflake:

    def __init__(self, resolution):
        self.x = sd.randint(0, resolution[0])
        self.y = resolution[1]
        self.length = sd.randint(5, 50)
        self.delta_y = sd.randint(10, 20)
        self.delta_x = self.length // 5
        self.factor_a = sd.randint(4, 7) / 10
        self.factor_b = sd.randint(2, 5) / 10
        self.factor_c = sd.randint(40, 70)
        self.color = sd.COLOR_WHITE
        self.skip = False  # чтобы не учитывалась каждый раз как только что упавшая

    def clear_previous_picture(self):
        self.color = sd.background_color
        Snowflake.draw(self)
        self.color = sd.COLOR_WHITE

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y -= delta_y

    def draw(self):
        sd.snowflake(sd.get_point(self.x, self.y),
                     self.length,
                     self.color,
                     self.factor_a,
                     self.factor_b,
                     self.factor_c)

    def can_fall(self, level):
        if self.y > level:
            return True
        else:
            return False


class SnowFall:

    def __init__(self, count=10):
        self.flakes = []
        self.level = 0
        self.generate_flakes(count)
        self.run()

    def get_fallen_flakes(self):
        fallen_count = 0
        for flake in self.flakes:
            if not flake.skip:
                if not flake.can_fall(self.level):
                    fallen_count += 1
                    flake.skip = not flake.skip
        return fallen_count

    def generate_flakes(self, count):
        for _ in range(count):
            self.flakes.append(Snowflake(res))

    def run(self):
        while True:
            for flake in self.flakes:
                if not flake.skip:
                    flake.clear_previous_picture()
                    flake.move(flake.delta_x, flake.delta_y)
                    flake.draw()
            fallen_flakes = self.get_fallen_flakes()
            if fallen_flakes:
                self.generate_flakes(count=fallen_flakes)
                self.level += fallen_flakes / 5
            sd.sleep(0.1)
            if sd.user_want_exit():
                break


snowfall = SnowFall()

sd.pause()
# зачет! 
