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

# TODO здесь ваш код...

# Усложненное задание (делать по желанию)

# Реализовать модуль искусственного интеллекта для отгадывания числа
# Функции ИИ:
#  выдать_вариант_числа()
#  получить_количество_быков_и_коров()

# Сделать модуль авто-игры (auto_mastermind):
#   модуль движка загадывает число
#   модуль ИИ отгадывает
#   протокол вопросов-ответов выводить на консоль
