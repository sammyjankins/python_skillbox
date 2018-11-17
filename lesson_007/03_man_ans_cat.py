# -*- coding: utf-8 -*-

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

man_names = ['Гарри', 'Джеймс', 'Генри']
cat_names = ['Майкл', 'Эдди', 'Роджер', 'Винсент', 'Дуглас', 'Леонард', 'Уолтер',
             'Джозеф', 'Джаспер', 'Эндрю', 'Ричард']


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

    def accept_occupant(self, occupant):
        if isinstance(occupant, Man) or isinstance(occupant, Cat):
            self.occupants.append(occupant)
            occupant.bind_to_house(self)


class Man:

    def __init__(self, names):
        self.name = choice(names)
        self.fullness = 50
        self.house = None
        self.money = 0
        self.is_alive = True

    def __str__(self):
        return 'Я - {}, сытость {}, денег {}'.format(
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
            cprint('{} гулял целый день'.format(self.name), color='magenta')
            self.fullness -= 10
            if len(self.house.occupants) < 4 and randint(1, 2) == 1:
                self.get_a_cat()
        elif activity == 3:
            cprint('{} изучал Python целый день'.format(self.name), color='blue')
            self.fullness -= 10
        else:
            cprint('{} играл в The Sims целый день'.format(self.name), color='green')
            self.fullness -= 10

    def shopping(self):
        if self.money >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.money -= 50
            self.house.food += 50
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def bind_to_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} Вьехал в дом'.format(self.name), color='cyan')

    def act(self):
        did_work_or_eat = False
        if len(self.house.occupants) > 1:
            did_work_or_eat = self.check_bowl()
        if self.fullness <= 0:
            cprint('Сильный и независимый {} умер...'.format(self.name), color='red')
            self.is_alive = False
            return
        dice = randint(1, 6)
        if not did_work_or_eat:
            if self.fullness < 20:
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
        available_names = []
        for occupant in self.house.occupants:
            available_names.append(occupant.name)
        cat = Cat(choice(list(set(cat_names) - set(available_names))))
        cprint('Пока гулял, подобрал кота и назвал его - {}'.format(cat.name), color='green')
        self.house.accept_occupant(cat)

    def check_bowl(self):

        """В доме есть кошачья миска, человек проверяет ее каждый день и наполняет,
        если пустая (feed_pets()). Если еда кончается, покупает (buy_cat_food()),
        либо идет на работу если нет денег (work()), в таком случае это считается
        действием, на которое тратится день.

        UPD: при растущем количестве котов, проверяем, что в миске еды хватает на всех"""

        if self.house.cat_bowl >= 10 * (len(self.house.occupants) - 1):
            cprint('{} проверил кошачью миску. В миске есть {} кошачьей еды.'.format(self.name, self.house.cat_bowl),
                   color='green')
            return False
        else:
            return self.feed_pets()

    def feed_pets(self):
        if self.house.cat_food >= 50:
            self.house.cat_bowl += 50
            self.house.cat_food -= 50
            cprint('Миска пуста. {} заполнил кошачью миску до отвала. Кошачьей еды осталось {}'.format(
                self.name, self.house.cat_food), color='yellow')
            if self.house.cat_food == 0:
                return self.buy_cat_food()
        elif self.house.cat_food > 0:
            self.house.cat_bowl += self.house.cat_food
            self.house.cat_food = 0
            cprint('Миска пуста. {} заполнил кошачью миску оставшейся кошачьей едой. В миске теперь {} еды'.format(
                self.name, self.house.cat_bowl), color='yellow')
            return self.buy_cat_food()
        else:
            return self.buy_cat_food()

    def buy_cat_food(self):
        if self.money >= 50:
            self.money -= 50
            self.house.cat_food += 50
            cprint('{} купил кошачьей еды. Теперь денег {}, а кошачьей еды {}'.format(
                self.name, self.money, self.house.cat_food), color='magenta')
            return False
        else:
            if self.fullness > 10:
                cprint('На кошачью еду нет денег, {} пошел на работу'.format(self.name), color='red')
                self.work()
                return True
            else:
                self.eat()
                return True

    def clean_house(self):

        """ Важно прислушиваться к своему организму.
        Если чувствуешь, что уборка не по силам - скушай
        больше каши и приберись завтра со свежими силами """

        if self.fullness > 20:
            self.house.mess -= 100
            self.fullness -= 20
            cprint('{} прибрался. Уровень беспорядка дома - {}, сытость - {}'.format(
                self.name, self.house.mess, self.fullness), color='cyan')
        else:
            self.eat()


class Cat:

    def __init__(self, name):
        """Когда называем кота - чистим список от его имени"""
        self.name = name
        self.fullness = 50
        self.house = None
        self.is_alive = True

    def __str__(self):
        return 'Я - кот по имени {}, сытость {}'.format(
            self.name, self.fullness)

    def eat(self):
        if self.house.cat_bowl >= 10:
            cprint('Кот {} поел'.format(self.name), color='yellow')
            self.fullness += 20
            self.house.cat_bowl -= 10
        else:
            self.fullness -= 10
            cprint('Кот {} хотел поесть, но в миске нет еды'.format(self.name), color='red')

    def sleep(self):
        self.fullness -= 10
        cprint('Кот {} проспал весь день'.format(self.name), color='cyan')

    def tear_wallpaper(self):
        self.fullness -= 10
        self.house.mess += 5
        cprint('Кот {} весь день драл обои'.format(self.name), color='red')

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            self.is_alive = False
            return
        dice = randint(1, 2)
        if self.fullness < 20:
            self.eat()
        elif dice == 1:
            self.sleep()
        elif dice == 2:
            self.tear_wallpaper()

    def bind_to_house(self, house):
        self.house = house
        cprint('{} поселился в доме!'.format(self.name), color='cyan')


my_sweet_home = House()
human = Man(man_names)
my_sweet_home.accept_occupant(human)
its_ok = True  # если дома все живы, то it's ok
for day in range(1, 366):
    if its_ok:
        print('================ день {} =================='.format(day))
        for person in my_sweet_home.occupants:
            person.act()
        print('--- в конце дня ---')
        for person in my_sweet_home.occupants:
            print(person)
            if not person.is_alive:
                its_ok = False
        print(my_sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
