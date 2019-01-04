# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint, choice, sample

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

    def __init__(self, name, sim=False):
        self.name = name
        self.house = None
        self.fullness = 30
        self.sim = sim

    def __str__(self):
        return f'{self.name}, сытость - {self.fullness}'

    def bind_to_house(self, house):
        self.house = house
        self.fullness -= 10
        self.family_print(f'{self.name} вьезжает в дом', color='cyan', sim=self.sim)

    def dying(self, reason='с голоду'):
        if self.fullness <= 0:
            self.family_print(f'{self.name} умирает {reason}...', color='red', sim=self.sim)
            self.house.someone_is_dead()
            return True
        return False

    def eat(self, max_food=30, fullness_mul=1):
        food = 'Cat' if isinstance(self, Cat) else 'Man'
        meal = randint(max_food // 3, max_food)
        if self.house.food[food] >= meal:
            Occupant.eaten += meal
            self.family_print(f'{self.name} ест', color='yellow', sim=self.sim)
            self.fullness += meal * fullness_mul
            self.house.food[food] -= meal
            return True
        else:
            insert = 'кошачьей ' if food == 'Cat' else ''
            self.family_print(f'{self.name} хочет есть, но в доме {insert}нет еды', color='red', sim=self.sim)
            return False

    def act(self):
        if self.dying():
            return False
        if self.fullness < 30:
            self.eat()
            return False
        return True

    def family_print(self, words, color, sim):
        if not sim:
            cprint(f'{words}', color=color)


class Man(Occupant):

    def __init__(self, name):
        super().__init__(name)
        self.happiness = 100

    def __str__(self):
        return f'Я - {super().__str__()}, уровень счастья - {self.happiness}'

    def pet_a_cat(self):
        self.happiness += 5
        self.fullness -= 10
        self.family_print(f'{self.name} гладит кота', color='cyan', sim=self.sim)


# чтобы счастье менялось только у взрослых
class Adult(Man):

    def act(self):
        if self.house.mess > 90:
            self.happiness -= 10
        return super().act()

    def dying(self, reason='с голоду'):
        if not super().dying(reason) and self.happiness <= 10:
            reason = reason if self.fullness <= 0 else 'от депрессии'
            return super().dying(reason)
        return False


class House:
    total_money = 0

    def __init__(self):
        self.money = 100
        man_food = 50
        self.food = {'Man': man_food, 'Cat': 30}
        self.mess = 0
        self.occupants = []
        self.its_ok = True

    def __str__(self):
        return f'В доме еды осталось - {self.food["Man"]}, кошачьей еды - {self.food["Cat"]}' \
               f', денег - {self.money}, уровень беспорядка - {self.mess}'

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

    def food_incident(self):
        for key in self.food:
            self.food[key] = 0

    def money_incident(self):
        self.money = 0


class Husband(Adult, Man):

    def __init__(self, name, salary):
        super().__init__(name)
        self.wife = None
        self.salary = salary

    def to_marry(self, wife):
        self.wife = wife
        self.wife.to_marry(self)

    def act(self):
        if super().act():
            if self.happiness < 35:
                self.gaming()
            elif self.house.money < 150:
                self.work()
            else:
                dice = randint(1, 4)
                if dice == 1:
                    self.gaming()
                elif dice == 2:
                    self.pet_a_cat()
                else:
                    self.work()

    def eat(self, *args, **kwargs):
        if not super().eat(*args, **kwargs) and self.house.money < 70:
            self.work()

    def work(self):
        self.family_print(f'{self.name} сходил на работу', color='blue', sim=self.sim)
        self.house.increase_of_capital(self.salary)
        self.fullness -= 10
        self.happiness -= 5

    def gaming(self):
        self.family_print(f'{self.name} играл в Silent Hill целый день', color='green', sim=self.sim)
        self.fullness -= 10
        self.happiness += 20


class Wife(Adult, Man):
    closet = 0

    def __init__(self, name):
        super().__init__(name)
        self.husband = None

    def act(self):
        if super().act():
            if self.happiness <= 35:
                self.buy_fur_coat()
            elif self.house.food['Man'] <= 30:
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

    def out_of_money(self):
        self.family_print(f'{self.name} деньги кончились!\n{self.husband.name}, марш работать!', color='red',
                          sim=self.sim)
        self.happiness -= 10
        self.pet_a_cat()  # чтобы не словить депрессию

    def shopping(self):
        if self.house.money >= 70:
            self.family_print(f'{self.name} сходила в магазин за едой', color='magenta', sim=self.sim)
            self.house.money -= 70
            self.house.food['Man'] += 60
            self.house.food['Cat'] += 10
            self.fullness -= 10
        else:
            self.out_of_money()

    def buy_fur_coat(self):
        if self.house.money >= 350:
            self.family_print(f'{self.name} купила новую шубу', color='magenta', sim=self.sim)
            self.house.money -= 350
            self.happiness += 60
            self.fullness -= 10
            Wife.closet += 1
        else:
            self.out_of_money()

    def clean_house(self):
        if self.fullness > 20:
            if self.house.mess > 100:
                self.house.mess -= 100
            else:
                self.house.mess = 0
            self.fullness -= 10
            self.happiness -= 25
            self.family_print(f'{self.name} прибралась', color='green', sim=self.sim)
        else:
            self.eat()

    def to_marry(self, husband):
        self.husband = husband


class Child(Man):

    def act(self):
        if super().act():
            dice = randint(1, 3)
            if dice == 1:
                self.eat()
            else:
                self.sleep()

    def eat(self, max_food=10, *args, **kwargs):
        super().eat(max_food=max_food, *args, **kwargs)

    def sleep(self):
        self.fullness -= 10
        self.family_print(f'{self.name} спит', color='green', sim=self.sim)


class Cat(Occupant):

    def __str__(self):
        return f'Я - кот {super().__str__()}'

    def act(self):
        if super().act():
            dice = randint(1, 6)
            if dice == 1:
                self.eat()
            elif dice == 2:
                self.sleep()
            else:
                self.soil()

    def eat(self, max_food=10, fullness_mul=2):
        super().eat(max_food, fullness_mul)

    def sleep(self):
        self.fullness -= 10
        self.family_print(f'{self.name} спит', color='green', sim=self.sim)

    def soil(self):
        self.fullness -= 10
        self.house.mess += 5
        self.family_print(f'{self.name} дерет обои', color='yellow', sim=self.sim)


class Simulation:

    def __init__(self, money_incidents, food_incidents):
        self.money_incidents = money_incidents
        self.food_incidents = food_incidents

    def experiment(self, salary):
        cats = 1
        survived = True
        while survived:
            pass

    def cycle(self, cats, salary):
        pass


home = House()
serge = Husband(name='Сережа', salary=150)
masha = Wife(name='Маша')
kolya = Child(name='Коля')
cat = Cat(choice(CAT_NAMES))

# свадьба
serge.to_marry(masha)

# переезд

home.accept_occupant(serge)
home.accept_occupant(masha)
home.accept_occupant(kolya)
home.accept_occupant(cat)

for day in range(1, 366):
    if home.its_ok:
        cprint(f'\n================== День {day} ==================', color='red')
        serge.act()
        masha.act()
        kolya.act()
        cat.act()
        home.act()
        cprint(serge, color='cyan')
        cprint(masha, color='cyan')
        cprint(kolya, color='cyan')
        cprint(cat, color='cyan')
        cprint(home, color='cyan')

print('\nВ итоге:')
print(f'Денег заработано - {House.total_money}')
print(f'Еды съедено - {Occupant.eaten}')
print(f'Шуб куплено - {Wife.closet}')

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
