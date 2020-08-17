# -*- coding: utf-8 -*-

# Вас взяли на работу в молодой стартап. Идея стартапа - предоставлять сервис расчета результатов игр.
# Начать решили с боулинга, упрощенной версии.
#
# Правила такие.
#
# Всего 10 кеглей. Игра состоит из 10 фреймов. В одном фрейме до 2х бросков, цель - сбить все кегли.
# Результаты фрейма записываются символами:
#   «Х» – «strike», все 10 кеглей сбиты первым броском
#   «<число>/», например «4/» - «spare», в первый бросок сбиты 4 кегли, во второй – остальные
#   «<число><число>», например, «34» – в первый бросок сбито 3, во второй – 4 кегли.
#   вместо <число> может стоять прочерк «-», например «-4» - ни одной кегли не было сбито за первый бросок
# Результат игры – строка с записью результатов фреймов. Символов-разделителей между фреймами нет.
# Например, для игры из 4 фреймов запись результатов может выглядеть так:
#   «Х4/34-4»
# Предлагается упрощенный способ подсчета количества очков:
#   «Х» – strike всегда 20 очков
#   «4/» - spare всегда 15 очков
#   «34» – сумма 3+4=7
#   «-4» - сумма 0+4=4
# То есть для игры «Х4/34-4» сумма очков равна 20+15+7+4=46
#
# Надо написать python-модуль (назвать bowling), предоставляющий API расчета количества очков:
# функцию get_score, принимающую параметр game_result. Функция должна выбрасывать исключения,
# когда game_result содержит некорректные данные. Использовать стандартные исключения по максимуму,
# если не хватает - создать свои.
#
# Обязательно написать тесты на этот модуль. Расположить в папке tests.

# Из текущего файла сделать консольную утилиту для определения количества очков, с помощью пакета argparse
# Скрипт должен принимать параметр --result и печатать на консоль:
#   Количество очков для результатов ХХХ - УУУ.


# При написании кода помнить, что заказчик может захотеть доработок и новых возможностей...
# И, возможно, вам пригодится паттерн проектирования "Состояние",
#   см https://clck.ru/Fudd8 и https://refactoring.guru/ru/design-patterns/state


class Frame(object):
    valid_symbols = '123456789-/X'

    def __init__(self, frame_line):
        self.frame_line = frame_line
        self.points = 0

    def __str__(self):
        return self.frame_line

    def eval_frame(self):
        self.validate_frame()
        if self.frame_line.startswith('X'):
            self.points += 20
        elif self.frame_line.endswith('/'):
            self.points += 15
        elif '-' in self.frame_line:
            self.points += int(self.frame_line.replace('-', ''))
        elif self.frame_line.isdigit():
            points = sum((int(x) for x in self.frame_line))
            if points <= 9:
                self.points += points
            else:
                raise Exception(f'{points} - incorrect frame score')

    def validate_frame(self):
        # Проверка фрейма на валидность символов
        validity = {x: x in self.valid_symbols for x in self.frame_line}
        if not all(validity.values()):
            raise BadFrameError(
                f'Invalid characters in frame: {", ".join([char for char in validity if not validity[char]])}')
        if self.frame_line.startswith('/'):
            raise BadFrameError('A frame cannot start with "/"')


class Game(object):

    def __init__(self, game_result):
        self.score = 0
        self.frames_amount = 0
        self.pairs = []
        self.game_result = game_result

    def get_score(self):
        self.game_result = self.game_result.replace('X', 'X-')
        if len(self.game_result) % 2:
            raise Exception('Incorrect frame sequence')
        self.eval_pairs()
        self.frames_amount += len(self.pairs)
        frames = (Frame(frame_line) for frame_line in self.pairs)
        for frame in frames:
            frame.eval_frame()
            self.score += frame.points
        if self.frames_amount < 10:
            ending = "ов" if self.frames_amount in (1, 2, 3, 4, 5) else "а"
            print(f'Осталось сыграть еще {10 - self.frames_amount} фрейм{ending if self.frames_amount != 9 else ""}')
        print(f'Результаты игры {self.game_result} ::: {self.score} очков!\n')

    def eval_pairs(self):
        v_pairs = [self.game_result[i: i + 2] for i in range(0, len(self.game_result) - 1, 2)]
        self.pairs.extend(v_pairs)


class BadFrameError(Exception):
    pass


result1 = 'X4/34-4'
result2 = 'X4/34-4X2-1/X'

game = Game(result1)
game.get_score()

game1 = Game(result2)
game1.get_score()
