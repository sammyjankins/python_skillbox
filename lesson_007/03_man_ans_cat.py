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
        self.cat_bowl = 0
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
            if randint(1, 2) == 1:
                self.get_a_cat()
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
        worked = self.check_bowl()
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 6)
        if self.fullness < 20 and not worked:
            self.eat()
        elif self.house.food < 10:
            self.shopping()
        elif self.money < 50:
            self.work()
        elif self.house.mess >= 100:
            self.clean_house()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.leisure()

    def get_a_cat(self):
        cat = Cat()
        self.house.occupants.append(cat)
        cprint('. Пока гулял, подобрал кота и назвал его - {}'.format(self.name, cat.name), color='green')

    def check_bowl(self):

        """В доме есть кошачья миска, человек проверяет ее каждый день и наполняет,
        если пустая (feed_pets()). Если еда кончается, покупает (buy_cat_food()),
        либо идет на работу если нет денег (work()), в таком случае это считается
        действием, на которое тратится день."""

        if self.house.cat_bowl >= 10:
            print('{} проверил кошачью миску. В миске есть {} кошачьей еды.'.format(self.name, self.house.cat_bowl))
            return False
        else:
            return self.feed_pets()

    def feed_pets(self):
        if self.house.cat_food >= 50:
            self.house.cat_bowl += 50
            self.house.cat_food -= 50
            print('Миска пуста. {} заполнил кошачью миску до отвала. Кошачьей еды осталось {}'.format(
                self.name, self.house.cat_food))
            if self.house.cat_food == 0:
                return self.buy_cat_food()
        elif self.house.cat_food > 0:
            self.house.cat_bowl += self.house.cat_food
            self.house.cat_food = 0
            print('Миска пуста. {} заполнил кошачью миску оставшейся кошачьей едой. В миске теперь {} еды'.format(
                self.name, self.house.cat_bowl))
            return self.buy_cat_food()
        else:
            return self.buy_cat_food()

    def buy_cat_food(self):
        if self.money >= 50:
            self.money -= 50
            self.house.cat_food += 50
            print('{} купил кошачьей еды. Теперь денег {}, а кошачьей еды {}'.format(
                self.name, self.money, self.house.cat_food))
            return False
        else:
            print('На кошачью еду нет денег, {} пошел на работу'.format(self.name))
            self.work()
            return True

    def clean_house(self):
        self.house.mess -= 100
        self.fullness -= 20
        print('{} прибрался. Уровень беспорядка дома - {}, сытость - {}'.format(
            self.name, self.house.mess, self.fullness))


class Cat:
    cat_names = ['Майкл', 'Эдди', 'Роджер', 'Винсент', 'Дуглас', 'Леонард', 'Уолтер',
                 'Джозеф', 'Джаспер', 'Эндрю', 'Ричард']

    def __init__(self):
        """Когда называем кота - чистим список от его имени"""
        self.name = choice(Cat.cat_names)
        Cat.cat_names.remove(self.name)
        self.fullness = 50
        self.house = None

    def __str__(self):
        return 'Я - кот по имени {}, сытость {}'.format(
            self.name, self.fullness)

    def eat(self):
        if self.house.cat_bowl >= 10:
            cprint('Кот {} поел'.format(self.name), color='yellow')
            self.fullness += 20
            self.house.cat_bowl -= 10
        else:
            cprint('Кот {} хотел поесть, но в миске нет еды'.format(self.name), color='red')

    def sleep(self):
        self.fullness -= 10
        cprint('Кот {} проспал весь день'.format(self.name), color='red')

    def tear_wallpaper(self):
        self.fullness -= 10
        self.house.mess += 5
        cprint('Кот {} весь день драл обои'.format(self.name), color='red')

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 2)
        if self.fullness < 20:
            self.eat()
        elif dice == 1:
            self.sleep()
        elif dice == 2:
            self.tear_wallpaper()


# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
