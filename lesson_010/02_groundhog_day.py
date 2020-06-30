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
class IamGodError(Exception):
    def __str__(self):
        return 'Фил возомнил себя богом, карма частично его покинула'


class DrunkError(Exception):
    def __str__(self):
        return 'Фил напился как скотина, но наутро похмелья как не бывало!\nВпрочем, как и нескольких очков кармы...'


class CarCrashError(Exception):
    def __str__(self):
        return 'Фил стал виновником ДТП, повредив несколько очков кармы'


class GluttonyError(Exception):
    def __str__(self):
        return 'Фил так объелся, что из него выпало несколько очков кармы'


class DepressionError(Exception):
    def __str__(self):
        return 'Фил впал в депрессию, карма истощается на несколько очков'


class SuicideError(Exception):
    def __str__(self):
        return 'Фил покончил с собой! Карме не оценила, чатично покинув Фила'


class KarmaOverflowError(Exception):
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


# достижение просветления возможно только если количество очков кармы точно равно 777
# при вереизбытке кармы, Фил сходит с ума и карма обнуляется
if __name__ == '__main__':
    karma = 0
    days = 0
    while karma != ENLIGHTENMENT_CARMA_LEVEL:
        days += 1
        try:
            karma += one_day()
            karma_overflow = karma > ENLIGHTENMENT_CARMA_LEVEL
            check_karma_level(karma_overflow)
        except KarmaOverflowError as exc:
            print(exc)
            karma = 0
        except Exception as exc:
            print(exc)
            karma -= randint(karma // 20, karma // 10)
        print(karma)
# https://goo.gl/JnsDqu
