# -*- coding: utf-8 -*-

from random import randint

# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.

from random import randint, choice
from termcolor import cprint


class House:

    def __init__(self):
        self.food = 50
        self.cat_food = 0
        self.mess = 0  # поменял грязь на беспорядок, надеюсь не критично
        self.occupants = []

    def __str__(self):
        """Жителей больше одного - значит есть кот"""
        if len(self.occupants) == 1:
            return 'В доме еды осталось {}'.format(self.food)
        else:
            return 'В доме еды осталось {}, кошачьей еды - {}, уровень беспорядка - {}'.format(
                self.food, self.cat_food, self.mess)


class Man:

    names = ['Гарри', 'Джеймс', 'Генри']

    def __init__(self):
        self.name = choice(Man.names)
        self.fullness = 50
        self.house = None
        self.money = 0

    def __str__(self):
        return 'Я - {}, сытость {}, денег'.format(
            self.name, self.fullness, self.money)

    def eat(self):
        if self.house.food >= 10:
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.money += 150
        self.fullness -= 10

    # досуг: просмотр сериала, прогулка (возможность обзавестить котом), учеба, компьютерные игры

    def leisure(self):
        activity = randint(1, 4)
        if activity == 1:
            cprint('{} смотрел Коня Боджека целый день'.format(self.name), color='green')
            self.fullness -= 10
        elif activity == 2:
            cprint('{} гулял целый день'.format(self.name), color='green')
            self.fullness -= 20
            # if randint(1,2) == 1:
            #     cat = Cat()
            #     self.house.occupants.append(cat)
            #     cprint('. Пока гулял, подобрал кота и назвал его - {}'.format(self.name, cat.name), color='green')
        elif activity == 3:
            cprint('{} изучал Python целый день'.format(self.name), color='green')
            self.fullness -= 10
        elif activity == 4:
            cprint('{} играл в The Sims целый день'.format(self.name), color='green')
            self.fullness -= 10

    def shopping(self):
        if self.money >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.money -= 50
            self.house.food += 50
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        self.house.occupants.append(self)
        cprint('{} Вьехал в дом'.format(self.name), color='cyan')

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 6)
        if self.fullness < 20:
            self.eat()
        elif self.house.food < 10:
            self.shopping()
        elif self.money < 50:
            self.work()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.leisure()

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
