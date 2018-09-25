# -*- coding: utf-8 -*-

# Игра «Быки и коровы»
# https://goo.gl/Go2mb9
#
# Правила:
# Компьютер загадывает четырехзначное число, все цифры которого различны
# (первая цифра числа отлична от нуля). Игроку необходимо разгадать задуманное число.
# Игрок вводит четырехзначное число, компьютер сообщают о количестве «быков» и «коров»
# в названном числе
# «бык» — цифра есть в записи задуманного числа и стоит в той же позиции,
#       что и в задуманном числе
# «корова» — цифра есть в записи задуманного числа, но не стоит в той же позиции,
#       что и в задуманном числе
#
# Например, если задумано число 3275 и названо число 1234,
# получаем в названном числе одного «быка» и одну «корову».
# Очевидно, что число отгадано в том случае, если имеем 4 «быка».
#
# Формат ответа компьютера
# > быки - 1, коровы - 1


# Составить модуль, реализующий функциональность игры.
# Функции реализаци игры:
#   загадать_число()
#   проверить_число(NN) - возвращает словарь {'bulls': N, 'cows': N}
# Загаданное число хранить в глобальной переменной
# Обратите внимание, что строки - это список символов
#
# В текущем модуле (lesson_006/01_mastermind.py) реализовать логику работы с пользователем:
#  начало игры,
#  ввод числа пользователем
#  вывод результата проверки
#  если игрок выйграл - показать количество ходов и вопрос "Хотите еще партию?"

from bulls_and_cows import init_number, check_numbers
from termcolor import cprint, colored

# сохранение загаданного числа в hidden_number и инициализация счетчика ходов
hidden_number = init_number()
rounds_count = 0

# TODO: сам на днях прочитал про суть оператора is и начал параноить немного, и видно не зря)

cprint("** Добро пожаловать в игру \"Быки и коровы\"!", "green", "on_grey", attrs=["bold"])
cprint("** Игра загадала число, время угадывать!", "green", "on_grey", attrs=["bold"])
while True:
    rounds_count += 1
    print((colored("** Введите 4-значное число: ", "yellow", "on_grey", attrs=["bold"])), end="")
    user_input = input()

    # проверка на корректность ввода
    while (len(user_input) != 4) or (not user_input.isdigit()):
        print((colored("** Некорректный ввод! Введите 4-значное число: ",
                       "red",
                       "on_grey",
                       attrs=["bold"])), end="")
        user_input = input()

    check_result = check_numbers(hidden_number, user_input)
    if check_result["bulls"] == 4:
        cprint("** Это победа!", "green", "on_grey", attrs=["bold"])
        print((colored("** Количество ходов - ", "green", "on_grey", attrs=["bold"])), end="")
        print((colored(rounds_count, "green", "on_grey", attrs=["bold"])))
        if rounds_count < 10:
            print((colored("** Вы наверное гений! У вас АйКью, случайно, не 160?!",
                           "green",
                           "on_grey",
                           attrs=["bold"])))
            cprint("** Если да, то не будет ли вам скучно сыграть еще одну партию(Y/N)?",
                   "green",
                   "on_grey",
                   attrs=["bold"])
        else:
            cprint("** Не хотели бы вы сыграть еще одну партию(Y/N)?", "red", "on_grey", attrs=["bold"])
        ans = input()
        if ans == 'Y':
            hidden_number = init_number()
            rounds_count = 0
        elif ans == 'N':
            break
        else:
            cprint("** Некорректный ввод!", "red", "on_grey", attrs=["bold"])
            cprint("** Истолкуем это как \"нет\", досвидания!", "green", "on_grey", attrs=["bold"])
            break
    else:
        print((colored("** Быки - ", "yellow", "on_grey", attrs=["bold"])), end="")
        print((colored(check_result["bulls"], "yellow", "on_grey", attrs=["bold"])))
        print((colored("** Коровы - ", "yellow", "on_grey", attrs=["bold"])), end="")
        print((colored(check_result["cows"], "yellow", "on_grey", attrs=["bold"])))

# Усложненное задание (делать по желанию)

# Реализовать модуль искусственного интеллекта для отгадывания числа
# Функции ИИ:
#  выдать_вариант_числа()
#  получить_количество_быков_и_коров()

# Сделать модуль авто-игры (auto_mastermind):
#   модуль движка загадывает число
#   модуль ИИ отгадывает
#   протокол вопросов-ответов выводить на консоль

# зачет! 
