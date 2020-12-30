# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
import json
import random
import re
from decimal import Decimal, getcontext
from pprint import pprint

from termcolor import cprint, colored

from lesson_015.utils import user_input_handling

remaining_time = '123456.0987654321'
# если изначально не писать число в виде строки - теряется точность!
field_names = ['current_location', 'current_experience', 'current_date']
getcontext().prec = len(remaining_time) + 1


# возможно будет декоратор для подготовки csv
def dec():
    pass


class Monster:
    monster_names = dict()

    def __init__(self, event_name):
        self.event_name = event_name
        self.name = ''
        self.exp = None
        self.time = None

    def __repr__(self):
        return f'{self.name}(exp={self.exp}, time={self.time})'

    def __str__(self):
        return f'{self.event_name}: {self.name}, время на победу - {self.time}'

    @classmethod
    def init_names(cls):
        """Заполнение атрибута класса именами из json файла для дальнейшей рандомной генерации в методе init_mob.
        (привет Diablo 2, все имена выдуманы автором кода по собственной инициативе и, как ни удивительно,
        не имеют отношения к реальным личностям)"""
        if len(cls.monster_names) == 0:
            with open('names_data.json', mode='r', encoding='utf8') as json_file:
                cls.monster_names = json.load(json_file)

    def init_mob(self):
        mob_parameters = self.event_name.split('_')
        self.exp, self.time = [Decimal(re.search(r'(\d+)', value).group()) for value in mob_parameters[1:]]
        self.name = f'{random.choice(self.monster_names["adjective"])} {random.choice(self.monster_names["noun"])}'


class Location:

    def __init__(self, name):
        self.name = name
        self.exp = None
        self.time = None
        self.options = []
        self.mobs = []
        self.locations = []
        self.evaluated = False

    def __str__(self):
        return self.name

    def init_loc(self):
        loc_time = self.name.split('_')
        time = re.search(r'(\d+.?\d+)', loc_time[-1])
        self.time = Decimal(time.group() if time else 0)  # потому что time пожет оказаться None

    def show_content(self):
        for event in self.mobs + self.locations:
            if isinstance(event, Location):
                cprint(f'— Вход в локацию: {event}', color='cyan')
            else:
                cprint(f'- Монстр ({event.event_name}) по кличке {event.name}', color='magenta')
        cprint('\nВыберите действие:', color='yellow')
        self.eval_options()

    def eval_options(self):
        """Действия, которые возможно совершить в течение хода зависят от заполненности контейнеров с переходами
        на локации и монстрами"""
        self.options = ['Атаковать монстра' * bool(self.mobs),
                        'Перейти в другую локацию' * bool(self.locations),
                        'Сдаться и выйти из игры']
        self.options = {i + 1: option for i, option in enumerate(filter(lambda x: x, self.options))}


class Player:

    def __init__(self):
        self.exp = Decimal()
        self.time = Decimal(remaining_time)
        self.win = False

    def action(self, time, exp=0):
        self.time -= time
        if exp:
            self.exp += exp

    def __str__(self):
        return f'У вас {self.exp} опыта и {self.time} секунд до наводнения\n'


class Game:

    def __init__(self):
        self.game_map = dict()
        self.current_location = None
        self.player = None
        self.round = 0

    def main(self):
        self.player = Player()
        self.init_game_values()

        while True:
            self.round += 1
            cprint('=' * 55, color='blue')
            cprint(f'{f" " * 23}Ход - {self.round}', color='blue')
            cprint('=' * 55, color='blue')
            print()
            self.eval_level_content()
            self.print_current_stat()
            self.current_location.show_content()
            try:
                self.print_options()
            except GameOverException as e:
                print(e.message)
                break

    def init_game_values(self):
        """Инициализация карты и текущей локации перед первым ходом"""
        Monster.init_names()
        with open('rpg.json', mode='r', encoding='utf8') as map_data:
            self.game_map = json.load(map_data)
        for key in self.game_map.keys():
            location = Location(key)
            location.init_loc()
            self.game_map = self.game_map[location.name]
            self.current_location = location

    def eval_level_content(self):
        if not self.current_location.evaluated:
            for i, event in enumerate(self.game_map):
                if isinstance(event, str):
                    monster = Monster(event)
                    monster.init_mob()
                    self.current_location.mobs.append(monster)
                else:
                    for key in event:
                        location = Location(key)
                        location.init_loc()
                        self.current_location.locations.append(location)
            self.current_location.evaluated = True

    def print_current_stat(self):
        cprint(f'Вы находитесь в {self.current_location}', color='yellow')
        cprint(self.player, color='green')
        cprint('Внутри вы видите:', color='yellow')

    def print_options(self):
        general_options = {
            'Атаковать монстра': {'color': 'magenta',
                                  'action': self.attack_mob},
            'Перейти в другую локацию': {'color': 'cyan',
                                         'action': self.go_to_level},
            'Сдаться и выйти из игры': {'color': 'red',
                                        'action': self.give_up},
        }
        level_options = ''.join([colored(f'{key}. {value}\n', general_options[value]['color'])
                                 for key, value in self.current_location.options.items()])
        print(level_options)
        ans = user_input_handling(colored('>> ', color='yellow'),
                                  len(self.current_location.options))
        general_options[self.current_location.options[ans]]['action']()

    def go_to_level(self):
        next_location = self.action(self.current_location.locations,
                                    'cyan',
                                    'Выберите локацию:',
                                    'Переход на локацию')
        self.update_map(next_location)

    def update_map(self, next_location):
        """Апдейт карты при выборе перехода на другую локацию, либо попытка открыть люк"""
        self.current_location = next_location
        if self.current_location.name.startswith('Hatch'):
            self.try_open_hatch()
        else:
            for event in self.game_map:
                if isinstance(event, str):
                    continue
                elif next_location.name not in event:
                    continue
                else:
                    self.game_map = event[next_location.name]

    def try_open_hatch(self):
        if self.player.exp >= 280:
            self.player.win = True
            raise GameOverException(text=colored('Вам удалось открыть люк!', color='green'),
                                    player=self.player)
        else:
            cprint('Вы пытаетесь открыть люк, но он не поддается...', color='red')
            return

    def attack_mob(self):
        defeated_mob = self.action(self.current_location.mobs,
                                   'magenta',
                                   'Выберите монстра:',
                                   'Атака на монстра')
        print(f'Вы победили - {defeated_mob}')

    def action(self, collection, color, text1, text2):
        """Выполнение действия над объектом, в зависимости от переданного в параменты контейнера (в котором хранятся,
        соответственно, Монстры или Локации) и текста. Если в контейнере один объект, действие выполняется над ним
        автоматически."""
        if len(collection) > 1:
            cprint(text1, color='yellow')
            for i, obj in enumerate(collection):
                cprint(f'{i + 1}. {obj}', color=color)
            ans = user_input_handling(colored('>> ', color='yellow'),
                                      len(collection))
            obj = collection.pop(ans - 1)
        else:
            obj = collection.pop()
        cprint(f'{text2} {obj}', color=color)
        self.player.action(time=obj.time, exp=obj.exp)
        if self.player.time <= 0:
            raise GameOverException(text=colored('Произошло наводнение, вы не успели спастить!', color='red'),
                                    player=self.player)
        cprint(self.player, color='green')
        return obj

    def give_up(self):
        raise GameOverException(text=colored('Вы приняли решение покинуть игру.', color='red'), player=self.player)


class GameOverException(Exception):
    win_msg = colored("Вы победили!", "green")
    lose_msg = colored("Вы проиграли!", "red")

    def __init__(self, text, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = (f'\n{text}\n'
                        f'{self.win_msg if player.win else self.lose_msg}\n'
                        f'{colored(f"Опыт к концу игры: {player.exp}", "yellow")}')


game = Game()
game.main()

# Учитывая время и опыт, не забывайте о точности вычислений!

if __name__ == '__main__':
    path_to_save = 'dungeon.csv'
