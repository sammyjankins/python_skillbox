from random import randint
from itertools import product

# множество возможных вариантов
bunch_of_numbers = []


def check_sets(num1, num2):
    return len(set(num1) - set(num2))


# список комбинаций 4-х цифр
versions = []
last_attempt = 0  # TODO: подразумевается, что тут будет строка. Лучше строкой и проинициализировать


# формирование списка комбинаций 4-х цифр (bulls + cows = 4)
def init_versions(number):
    for row in product(number, repeat=4):
        row = ''.join(row)
        if len(set(row)) is len(row):  # TODO: ==
            versions.append(row)


# анализ словаря с быками и коровами и модификация списка возможных вариантов на его основе
def get_ganados(ganados=None):
    global bunch_of_numbers
    if ganados is None:
        for i in range(1022, 9877):
            number = str(i)
            if len(set(number)) is len(number):  # TODO: ==
                bunch_of_numbers.append(number)
    else:
        check_sum = ganados["bulls"] + ganados["cows"]
        if check_sum is 4:  # TODO: ==
            if len(versions) is 0:  # TODO: ==
                init_versions(last_attempt)
            else:
                pass  # TODO: Вы что-то хотели сюда дописать, но забыли?
        elif check_sum is 0:  # TODO: ==
            new_bunch = []
            for number in bunch_of_numbers:
                if check_sets(number, last_attempt) is 4:  # TODO: ==
                    new_bunch.append(number)
            bunch_of_numbers = new_bunch
        elif ganados["bulls"] is 0:  # TODO: ==
            bad_options = set()
            for letter in last_attempt:
                for number in bunch_of_numbers:
                    if last_attempt.find(letter) is number.find(letter):  # TODO: ==
                        bad_options.add(number)
            for number in bad_options:
                bunch_of_numbers.remove(number)
        else:
            new_bunch = []
            for number in bunch_of_numbers:
                if check_sets(number, last_attempt) is not 0:  # TODO: !=
                    new_bunch.append(number)
            bunch_of_numbers = new_bunch


# возвращает число из списка возможных вариантов или списка комбинаций 4 цифр
def try_number():
    global last_attempt
    if len(versions) is 0:  # TODO: ==
        last_attempt = bunch_of_numbers[randint(0, len(bunch_of_numbers) - 1)]
    else:
        last_attempt = versions.pop()
    return last_attempt
