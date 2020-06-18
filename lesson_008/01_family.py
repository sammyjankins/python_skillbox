# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint, sample, shuffle

CAT_NAMES = ['Майкл', 'Эдди', 'Роджер', 'Винсент', 'Дуглас', 'Леонард', 'Уолтер',
             'Джозеф', 'Джаспер', 'Эндрю', 'Ричард', 'Гарри', 'Джеймс', 'Генри', 'Фрэнк']


# Класс жителя дома, здесь будут скомпилированы некоторые атрибуты и методы, справедливые как для
# людей, так и для котов
class Occupant:

    def __init__(self, name, show=True):
        self.name = name
        self.house = None
        self.fullness = 30
        self.show = show
        self.is_dead = False

    def __str__(self):
        return f'{self.name}, сытость - {self.fullness}'

    def bind_to_house(self, house):
        self.house = house
        self.fullness -= 10
        self.family_print(text='въезжает в дом', color='cyan')

    def dying(self):
        if self.fullness <= 0:
            self.family_print(text=f'помер с голоду', color='red')
            self.is_dead = True
            self.house.someone_is_dead()
        return self.is_dead

    # нерациональным путем пытался определить тип еды по классу инстанса, залезая для этого в mro...
    # в итоге убрал часть функциональности в холодильник дома
    def eat(self, max_food=30, fullness_mul=1):
        portion = randint(max_food // 3, max_food)
        if self.house.use_fridge(portion, self):
            self.fullness += portion * fullness_mul
            self.family_print(text='поел', color='yellow')
            return True
        else:
            return False

    def act(self):
        if self.dying():
            return False
        if self.fullness < 30:
            self.eat()
            return False
        return True

    def family_print(self, text, color):
        if self.show:
            cprint(f'{self.name} {text}', color=color)


class Human(Occupant):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.happiness = 100

    def __str__(self):
        return f'Я - {super().__str__()}, уровень счастья - {self.happiness}'

    def eat(self, max_food=30, fullness_mul=1):
        if not super().eat(max_food, fullness_mul):
            self.family_print(text=f'хочет есть, но в доме нет еды', color='red')
            return False
        return True


# чтобы счастье менялось только у взрослых
class Adult(Human):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spouse = None

    def act(self):
        if self.house.mess > 90:
            self.happiness -= 10
        return super().act()

    def dying(self):
        if not super().dying():
            if self.happiness <= 10:
                self.family_print(text=f'помер от депрессии', color='red')
                self.house.someone_is_dead()
                self.is_dead = True
        return self.is_dead

    def pet_a_cat(self):
        self.happiness += 5
        self.fullness -= 10
        self.family_print(f'гладит кота', color='blue')

    # свадьба
    def wedding(self, spouse=None):
        if not self.spouse:
            self.spouse = spouse
            spouse.wedding(spouse=self)


class House:

    def __init__(self, show=True):
        self.show = show
        self.money = 100
        self.food = {Human: 50,
                     Cat: 30}
        self.mess = 0
        self.occupants = []
        self.its_ok = True
        self.cats = 0

    def __str__(self):
        return f'''В доме еды осталось - {self.food[Human]}, кошачьей еды - {self.food[Cat]},
денег - {self.money}, уровень беспорядка - {self.mess}'''

    def accept_occupants(self, *occupants):
        for occupant in occupants:
            if isinstance(occupant, Occupant):
                self.occupants.append(occupant)
                if isinstance(occupant, Cat):
                    self.cats += 1
                occupant.bind_to_house(self)

    def someone_is_dead(self):
        self.its_ok = False

    def act(self):
        self.mess += 5

    def increase_of_capital(self, amount):
        self.money += amount

    def food_incident(self):
        for food_type in self.food:
            self.food[food_type] = 0
        if self.show:
            cprint('Из холодильника внезапно пропала вся еда', color='red')

    def money_incident(self):
        self.money = 0
        if self.show:
            cprint('Из дома внезапно пропали все деньги', color='red')

    def use_fridge(self, portion, occupant):
        for food_type in self.food:
            if isinstance(occupant, food_type):
                if self.food[food_type] >= portion:
                    self.food[food_type] -= portion
                    return True
        return False


# думаю вызвался бы инит Adult. Но на этот раз множественное наследование убрал, Adult наследуется от Human (ранее Man)
class Husband(Adult):

    def __init__(self, salary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.salary = salary

    def __str__(self):
        return f'{super().__str__()}, моя зп - {self.salary}'

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
        self.family_print(f'сходил на работу', color='blue')
        self.house.increase_of_capital(self.salary)
        self.fullness -= 10
        self.happiness -= 5

    def gaming(self):
        self.family_print(f'играл в DOOM целый день', color='green')
        self.fullness -= 10
        self.happiness += 20


class Wife(Adult):

    def act(self):
        if super().act():
            if self.happiness <= 35:
                self.buy_fur_coat()
            elif self.house.food[Human] <= 30:
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
        self.family_print(f'деньги кончились!\n{self.spouse.name}, марш работать!', color='red')
        self.happiness -= 10
        self.pet_a_cat()  # чтобы не словить депрессию

    def shopping(self):
        man_food_price = 20 * (len(self.house.occupants) - self.house.cats)
        cat_food_price = 10 * self.house.cats
        food_price = man_food_price + cat_food_price
        if self.house.money >= food_price:
            self.family_print(f'сходила в магазин за едой', color='magenta')
            self.house.money -= food_price
            self.house.food[Human] += man_food_price
            self.house.food[Cat] += cat_food_price
            self.fullness -= 10
        else:
            self.out_of_money()

    def buy_fur_coat(self):
        if self.house.money >= 350:
            self.family_print(f'купила новую шубу', color='magenta')
            self.house.money -= 350
            self.happiness += 60
            self.fullness -= 10
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
            self.family_print(f'прибралась', color='green')
        else:
            self.eat()


class Child(Human):

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
        self.family_print(f'спит', color='green')


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
                self.spoil()

    def eat(self, max_food=10, fullness_mul=2):
        if not super().eat(max_food, fullness_mul):
            self.family_print(text=f'хочет есть, но в доме нет кошачьей еды', color='red')
            return False
        return True

    def sleep(self):
        self.fullness -= 10
        self.family_print(f'спит', color='green')

    def spoil(self):
        self.fullness -= 10
        self.house.mess += 5
        self.family_print(f'дерет обои', color='yellow')


class Simulation:

    def __init__(self, money_incidents=1, food_incidents=1):
        self.money_incidents = money_incidents
        self.food_incidents = food_incidents

    def experiment(self, salary):
        cats = 0
        while True:
            cats += 1
            survivals = 0
            for _ in range(3):
                if self.cycle(money_incidents=self.money_incidents,
                              food_incidents=self.food_incidents,
                              cats=cats,
                              salary=salary,
                              show=False):
                    survivals += 1
            if survivals < 2:
                return cats

    # если sim == True, вывода на экран не будет
    def cycle(self, money_incidents=1, food_incidents=1, cats=1, salary=150, show=True):
        home = House(show)
        serge = Husband(name='Сережа', salary=salary, show=show)
        masha = Wife(name='Маша', show=show)
        kolya = Child(name='Коля', show=show)

        # свадьба
        serge.wedding(masha)

        # переезд
        home.accept_occupants(serge, masha, kolya)

        # чтобы не было котов с одинаковыми именами
        names = CAT_NAMES.copy()
        shuffle(names)
        for cat in range(cats):
            home.accept_occupants(Cat(name=names.pop(), show=show))

        year = range(1, 366)
        incidents = {'food': sample(year, food_incidents), 'money': sample(year, money_incidents)}

        for day in year:
            if home.its_ok:
                if show:
                    cprint(f'\n================== День {day} ==================', color='red')
                for accident in incidents:
                    if day in incidents[accident]:
                        home.food_incident() if accident == 'food' else home.money_incident()
                home.act()
                for occupant in home.occupants:
                    occupant.act()
                if show:
                    for occupant in home.occupants:
                        cprint(occupant, color='cyan')
                    cprint(home, color='cyan')

        return home.its_ok


for food_incidents in range(6):
    for money_incidents in range(6):
        cprint('Внезапных исчезновений еды: ', end='', color='cyan')
        cprint(food_incidents, color='red')
        cprint('Внезапных исчезновений денег: ', end='', color='cyan')
        cprint(money_incidents, color='red')
        life = Simulation(food_incidents, money_incidents)
        for salary in range(50, 401, 50):
            cprint('При зарплате ', end='', color='magenta')
            cprint(salary, color='green', end='')
            cprint(' максимально можно прокормить ', end='', color='magenta')
            cprint(life.experiment(salary=salary), color='yellow', end='')
            cprint(' котов', color='magenta')

life = Simulation(1, 1)
life.cycle(show=True)
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
