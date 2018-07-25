# -*- coding: utf-8 -*-

# Создать пакет, в котором собрать функции отрисовки из предыдущего урока
#  - радуги
#  - стены
#  - дерева
#  - смайлика
#  - снежинок
# Каждую функцию разместить в своем модуле. Название пакета и модулей - по смыслу.
# Создать модуль с функцией отрисовки кирпичного дома с широким окном и крышей.

# С помощью созданного пакета нарисовать эпохальное полотно "Утро в деревне".
# На картине должны быть:
#  - кирпичный дом, в окошке - смайлик.
#  - слева от дома - сугроб (предположим что это ранняя весна)
#  - справа от дома - дерево (можно несколько)
#  - справа в небе - радуга, слева - солнце (весна же!)
# пример см. lesson_005/results/04_painting.jpg
# Приправить своей фантазией по вкусу (коты? коровы? люди? трактор? что придумается)

import simple_draw as sd
import we_draw.my_rainbow as rb
import we_draw.my_house as house
import we_draw.my_smile as smile
from we_draw.my_tree import draw_bunches as tree
import we_draw.my_snow as snow
import we_draw.my_sun as sun

sd.resolution = res = (1000, 600)
rainbow_colors = [sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE]
winter = snow.init_snow_params(res[0] - 100, res[1])

sd.background_color = sd.COLOR_BLUE
blink = False
tree(sd.get_point(850, 0), 90, 70)
tree(sd.get_point(950, 0), 90, 70)

while True:
    blink = not blink
    house.draw_house(500, 0, 700, 201)
    sun.draw_sun(100, 500, 50)
    rainbow_colors.insert(0, rainbow_colors.pop())
    rb.draw_rainbow(-50, 1500, -500, 600, rainbow_colors)
    smile.draw_face(570, 70, sd.COLOR_ORANGE, blink)
    snow.draw_snow(winter["x"],
                   winter["y"],
                   winter["lens"],
                   winter["delta"],
                   winter["factors"])
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

# Усложненное задание (делать по желанию)
# Анимировать картину.
# Пусть слева идет снегопад, радуга переливается цветами, смайлик моргает, солнце крутит лучами, етс.
# Задержку в анимировании все равно надо ставить, пусть даже 0.01 сек - так библиотека устойчивей работает.
