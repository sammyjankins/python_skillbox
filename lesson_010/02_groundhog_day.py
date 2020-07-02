# -*- coding: utf-8 -*-
from random import choice, choices, randint

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.


ENLIGHTENMENT_CARMA_LEVEL = 777


# добавил возможность потерять карму при возникновении исключения
class BadKarmaException(Exception):
    pass


class IamGodError(BadKarmaException):
    def __str__(self):
        return 'Фил возомнил себя богом, карма частично его покинула'


class DrunkError(BadKarmaException):
    def __str__(self):
        return 'Фил напился как скотина, но наутро похмелья как не бывало!\nВпрочем, как и нескольких очков кармы...'


class CarCrashError(BadKarmaException):
    def __str__(self):
        return 'Фил стал виновником ДТП, повредив несколько очков кармы'


class GluttonyError(BadKarmaException):
    def __str__(self):
        return 'Фил так объелся, что из него выпало несколько очков кармы'


class DepressionError(BadKarmaException):
    def __str__(self):
        return 'Фил впал в депрессию, карма истощается на несколько очков'


class SuicideError(BadKarmaException):
    def __str__(self):
        return 'Фил покончил с собой! Карма не оценила, частично покинув Фила'


class KarmaOverflowError(BadKarmaException):
    def __str__(self):
        return 'Фил спятил от переизбытка мудрости, растеряв всю карму!'


exceptions = [IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError]


def one_day():
    result = choices([choice(range(1, 8)), choice(exceptions)], weights=[12 / 13, 1 / 13])[0]
    if not type(result) == int:
        raise result
    return result


def check_karma_level(karma_level):
    if karma_level:
        raise KarmaOverflowError


def log_update(day, karma_level, event):
    with open('groundhog_log.txt', 'a', encoding='utf8') as log:
        log.write(f'----------------------| '
                  f'День: {day:>2}, карма: {karma_level: >2} |----------------------\n'
                  f'Событие: {event}\n\n')


# достижение просветления возможно только если количество очков кармы точно равно 777
# при вереизбытке кармы, Фил сходит с ума и карма обнуляется
if __name__ == '__main__':
    karma = 0
    days = 0
    log_update(days, karma, 'Фил угодил во временную петлю!')
    while karma != ENLIGHTENMENT_CARMA_LEVEL:
        days += 1
        try:
            karma += one_day()
            karma_overflow = karma > ENLIGHTENMENT_CARMA_LEVEL
            check_karma_level(karma_overflow)
        except KarmaOverflowError as exc:
            karma = 0
            log_update(days, karma, str(exc))
        except BadKarmaException as exc:
            karma -= randint(karma // 20, karma // 10)
            log_update(days, karma, str(exc))
    log_update(days, karma, 'Фил достиг просветления!')
# https://goo.gl/JnsDqu

# зачет! 
