from random import randint
from itertools import product

# множество возможных вариантов
bunch_of_numbers = []


def check_sets(num1, num2):
    return len(set(num1) - set(num2))


# список комбинаций 4-х цифр
versions = False
last_attempt = ''


# формирование списка комбинаций 4-х цифр (bulls + cows = 4)
def init_versions(number, vers=0):
    mass = []
    for row in product(number, repeat=4):
        row = ''.join(row)
        if len(set(row)) == len(row):
            mass.append(row)
    if vers:
        global bunch_of_numbers
        bunch_of_numbers = mass
        # TODO тут приравнял это дело, теперь все операции с одним пулом, при чек-сумме = 4
        # TODO bunch_of_numbers инициализируется версиями
        # TODO кстати, в versions всегда была бы чек-сумма 4, в целом ее имеет смысл проверять лишь на bull == 0
        # TODO так что эту проверку я дополнительно добавил в случае чек-суммы 4
    else:
        return mass


def init_ganados():
    global bunch_of_numbers
    if not bunch_of_numbers:
        for i in range(1022, 9877):
            number = str(i)
            if len(set(number)) == len(number):
                bunch_of_numbers.append(number)


# check_sum == 0
def zero_case():
    global bunch_of_numbers
    new_bunch = []
    for number in bunch_of_numbers:
        if check_sets(number, last_attempt) == 4:  # проверяем что в очередном числе нет ни одного ненужного
            new_bunch.append(number)
    return new_bunch


# check_sum 1..3, но bulls == 0
def zero_bulls_case():
    bad_options = set()
    for letter in last_attempt:
        for number in bunch_of_numbers:
            if last_attempt.find(letter) == number.find(letter):
                bad_options.add(number)
    for number in bad_options:
        bunch_of_numbers.remove(number)


# check_sum 1..3 и bulls != 0
def other_sum():
    bad_options = init_versions(last_attempt)
    for number in bad_options:
        if number in bunch_of_numbers:
            bunch_of_numbers.remove(number)


# анализ словаря с быками и коровами и модификация списка возможных вариантов на его основе
def get_ganados(ganados):
    # заполнение массива вариантов в начале игры
    global bunch_of_numbers
    check_sum = ganados["bulls"] + ganados["cows"]
    # Когда натыкаемся на число, дающее поголовье в количестве 4-х особей, заполняем bunch_of_numbers
    # комбинациями из этих 4-х чисел
    if check_sum == 4:
        global versions
        if not versions:
            init_versions(last_attempt, 1)
            versions = True
        else:
            zero_bulls_case()
    # Заполняем новый массив вариантов из старого комбинациями, не содержащими ненужных чисел
    elif check_sum == 0:
        bunch_of_numbers = zero_case()

    # Если ноль быков, то можно из списка вариантов удалить такие числа, цифры в которых стоят на тех же местах,
    # что в последней попытке.
    elif ganados["bulls"] == 0:
        zero_bulls_case()

    # Случай, когда поголовье не 0, но и не 4, при этои имеем хотя бы одного быка(значит в комбинации есть хотя
    #  бы одно ненужное число). Тут можно удалить из множества все комбинации из этих 4-х цифр.
    else:
        other_sum()
    print(len(bunch_of_numbers))


# возвращает число из списка возможных вариантов
def try_number():
    global last_attempt
    last_attempt = bunch_of_numbers.pop(randint(0, len(bunch_of_numbers) - 1))
    return last_attempt
