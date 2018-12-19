# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint, choice

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.

CAT_NAMES = ['Майкл', 'Эдди', 'Роджер', 'Винсент', 'Дуглас', 'Леонард', 'Уолтер',
             'Джозеф', 'Джаспер', 'Эндрю', 'Ричард', 'Гарри', 'Джеймс', 'Генри', 'Фрэнк']


# Класс жителя дома, здесь будут скомпилированы некоторые атрибуты и методы, справедливые как для
# людей, так и для котов
class Occupant:
    eaten = 0

    def __init__(self, name):
        self.name = name
        self.house = None
        self.fullness = 30

    def __str__(self):
        return '{}, сытость - {}'.format(
            self.name, self.fullness)

    def bind_to_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} вьезжает в дом'.format(self.name), color='cyan')

    def dying(self, reason='с голоду'):
        cprint('{} умирает {}...'.format(self.name, reason), color='red')
        self.house.someone_is_dead()
        return True

    def eat(self, kind_of_food='man_food', max_food=30, fullness_mul=1):
        if self.house.food[kind_of_food] >= max_food:
            meal = randint(max_food // 3, max_food)
            Occupant.eaten += meal
            cprint('{} ест'.format(self.name), color='yellow')
            self.fullness += meal * fullness_mul
            self.house.food[kind_of_food] -= meal
            return True
        else:
            insert = ''
            if kind_of_food == 'cat_food':
                insert = 'кошачьей '
            cprint('{} хочет есть, но в доме {}нет еды'.format(self.name, insert), color='red')
            return False

    def act(self):
        if self.dying():
            return False
        if self.fullness < 30:
            self.eat()
            return False
        return True


class Man(Occupant):

    def __init__(self, name):
        super().__init__(name)
        self.happiness = 100

    def __str__(self):
        return 'Я - ' + super().__str__() + ', уровень счастья - {}'.format(self.happiness)

    def dying(self, reason='с голоду'):
        if self.fullness <= 0 or self.happiness <= 10:
            reason = reason if self.fullness <= 0 else 'от депрессии'
            return super().dying(reason)
        return False

    def act(self):
        if self.house.mess > 90:
            self.happiness -= 10
        return super().act()

    def pet_a_cat(self):
        self.happiness += 5
        self.fullness -= 10
        print('{} гладит кота'.format(self.name))


class House:
    total_money = 0

    def __init__(self):
        self.money = 100
        self.food = {'man_food': 50, 'cat_food': 30}
        self.mess = 0
        self.occupants = []
        self.its_ok = True

    def __str__(self):
        return 'В доме еды осталось - {}, кошачьей еды - {}, денег - {}, уровень беспорядка - {}'.format(
            self.food['man_food'], self.food['cat_food'], self.money, self.mess)

    def accept_occupant(self, occupant):
        if isinstance(occupant, (Man, Cat)):
            self.occupants.append(occupant)
            occupant.bind_to_house(self)

    def someone_is_dead(self):
        self.its_ok = False

    def act(self):
        self.mess += 5

    def increase_of_capital(self, amount):
        self.money += amount
        House.total_money += amount


class Husband(Man):

    def __init__(self, name):
        super().__init__(name)
        self.wife = None

    def __str__(self):
        return super().__str__()

    def to_marry(self, wife):
        self.wife = wife
        self.wife.to_marry(self)

    def act(self):
        if super().act():
            if self.happiness < 30:
                self.gaming()
            elif self.house.money < 100:
                self.work()
            else:
                dice = randint(1, 4)
                if dice == 1:
                    self.gaming()
                elif dice == 2:
                    self.pet_a_cat()
                else:
                    self.work()

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.house.increase_of_capital(150)
        self.fullness -= 10
        self.happiness -= 5

    def gaming(self):
        cprint('{} играл в Silent Hill целый день'.format(self.name), color='green')
        self.fullness -= 10
        self.happiness += 20


class Wife(Man):
    closet = 0

    def __init__(self, name):
        super().__init__(name)
        self.husband = None

    def __str__(self):
        return super().__str__()

    def act(self):
        if super().act():
            if self.house.food['man_food'] <= 30:
                self.shopping()
            elif self.house.mess > 100:
                self.clean_house()
            else:
                dice = randint(1, 6)
                if dice == 1:
                    self.shopping()
                elif dice == 2:
                    self.clean_house()
                elif dice == 3:
                    self.pet_a_cat()
                else:
                    self.buy_fur_coat()

    def eat(self, *args, **kwargs):
        if not super().eat(*args, **kwargs):
            self.shopping()

    def shopping(self):
        if self.house.money >= 50:
            cprint('{} сходила в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.food['man_food'] += 40
            self.house.food['cat_food'] += 10
            self.fullness -= 10
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')
            cprint('{}, марш работать!'.format(self.husband.name))
            self.happiness -= 10

    def buy_fur_coat(self):
        if self.house.money >= 350:
            cprint('{} купила новую шубу'.format(self.name), color='magenta')
            self.house.money -= 350
            self.happiness += 60
            self.fullness -= 10
            Wife.closet += 1
        else:
            cprint('{} - не хватает денег на шубу!'.format(self.name), color='red')
            cprint('{}, марш работать!'.format(self.husband.name))
            self.happiness -= 10

    def clean_house(self):
        if self.fullness > 20:
            if self.house.mess > 100:
                self.house.mess -= 100
            else:
                self.house.mess = 0
            self.fullness -= 10
            self.happiness -= 25
            cprint('{} прибралась'.format(
                self.name), color='green')
        else:
            self.eat()

    def to_marry(self, husband):
        self.husband = husband


class Cat(Occupant):

    def __str__(self):
        return 'Я - кот ' + super().__str__()

    def act(self):
        if super().act():
            dice = randint(1, 6)
            if dice == 1:
                self.eat()
            elif dice == 2:
                self.sleep()
            else:
                self.soil()

    def eat(self, kind_of_food='cat_food', max_food=10, fullness_mul=2):
        super().eat(kind_of_food, max_food, fullness_mul)

    def sleep(self):
        self.fullness -= 10
        cprint('{} спит'.format(self.name), color='green')

    def soil(self):
        self.fullness -= 10
        self.house.mess += 5
        cprint('{} дерет обои'.format(self.name), color='yellow')

    def dying(self, reason='с голоду'):
        if self.fullness <= 0:
            return super().dying()
        return False


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')
cat = Cat(choice(CAT_NAMES))

# свадьба
serge.to_marry(masha)

# переезд

home.accept_occupant(serge)
home.accept_occupant(masha)
home.accept_occupant(cat)

for day in range(1, 366):
    if home.its_ok:
        cprint('\n================== День {} =================='.format(day), color='red')
        serge.act()
        masha.act()
        cat.act()
        home.act()
        cprint(serge, color='cyan')
        cprint(masha, color='cyan')
        cprint(cat, color='cyan')
        cprint(home, color='cyan')

print('\nВ итоге:')
print('Денег заработано - {}'.format(House.total_money))
print('Еды съедено - {}'.format(Occupant.eaten))
print('Шуб куплено - {}'.format(Wife.closet))

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов
#
#
# class Cat:
#
#     def __init__(self):
#         pass
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass
#
#     def soil(self):
#         pass
#

######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)
#
# class Child:
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return super().__str__()
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass


# TODO после реализации второй части - отдать на проверку учителем две ветки


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.

#
# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')

# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')
