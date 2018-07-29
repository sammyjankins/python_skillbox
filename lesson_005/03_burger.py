# -*- coding: utf-8 -*-

# Создать модуль my_burger. В нем определить функции добавления инградиентов:
#  - булочки
#  - котлеты
#  - огурчика
#  - помидорчика
#  - майонеза
#  - сыра
# В каждой функции выводить на консоль что-то вроде "А теперь добавим ..."

# В этом модуле создать рецепт двойного чизбургера (https://goo.gl/zA3goZ)
# с помощью фукций из my_burger и вывести на консоль.

# Создать рецепт своего бургера, по вашему вкусу.
# Если не хватает инградиентов - создать соответствующие функции в модуле my_burger

import my_burger


def double_cheeseburger():
    print("\n*** РЕЦЕПТ ДВОЙНОГО ЧИЗБУРГЕРА ***\n")
    my_burger.add_bun(half=1)
    my_burger.add_mayo()
    my_burger.add_cutlet()
    my_burger.add_cheese()
    my_burger.add_pickle()
    my_burger.add_tomato()
    my_burger.add_bun()
    my_burger.eat()


def jack_daniels_burger():
    print("\n*** РЕЦЕПТ БУРГЕРА \"ДЖЕК ДЭНИЭЛС\" ***\n")
    burger_name = "бургером \"Джек Дэниэлс\""
    my_burger.add_bun(half=1)
    my_burger.add_onion()
    my_burger.add_tomato()
    my_burger.add_pickle()
    my_burger.add_cutlet()
    my_burger.add_cheese()
    my_burger.add_jack_sauce()
    my_burger.add_bacon()
    my_burger.add_bun()
    my_burger.eat(burger_name)
    pass  # TODO: зачем?


double_cheeseburger()
jack_daniels_burger()
