from random import randint
from itertools import product

# множество возможных вариантов
bunch_of_numbers = []


def check_sets(num1, num2):
    return len(set(num1) - set(num2))


# список комбинаций 4-х цифр
versions = []
last_attempt = ''


# формирование списка комбинаций 4-х цифр (bulls + cows = 4)
def init_versions(number, vers=0):
    mass = []
    for row in product(number, repeat=4):
        row = ''.join(row)
        if len(set(row)) == len(row):
            mass.append(row)
    if vers:
        versions.extend(mass)
    else:
        return mass


# анализ словаря с быками и коровами и модификация списка возможных вариантов на его основе
def get_ganados(ganados=None):
    # заполнение массива вариантов в начале игры
    global bunch_of_numbers
    if ganados is None:  # TODO: это надо унести в отдельную функцию для инициализации изначального списка
        for i in range(1022, 9877):
            number = str(i)
            if len(set(number)) == len(number):
                bunch_of_numbers.append(number)
    else:  # TODO: в этой функции пусть останется только то, что после этого else

        # Когда натыкаемся на число, дающее поголовье в количестве 4-х особей, заполняем список versions
        # комбинациями из этих 4-х чисел. Далее функция try_number замечает что он не пустой и перебирает его.
        check_sum = ganados["bulls"] + ganados["cows"]
        if check_sum == 4:
            if len(versions) == 0:
                init_versions(last_attempt, 1)

        # Заполняем новый массив вариантов из старого комбинациями, не содержащими ненужных чисел.
        elif check_sum == 0:  # TODO: всё, что в этом условии, в отдельную функцию, пусть она возвращает new_bunch
            new_bunch = []
            for number in bunch_of_numbers:
                if check_sets(number, last_attempt) == 4:  # проверяем что в очередном числе нет ни одного ненужного
                    new_bunch.append(number)
            bunch_of_numbers = new_bunch

        # Если ноль быков, то можно из списка вариантов удалить такие числа, цифры в которых стоят на тех же местах,
        # что в последней попытке. Чтобы итерация не ломалась, сначала собираем все варианты в сет. Почему в сет?
        # Потому что варианты могут повторяться, если больше одного числа из последней попытки совпадает. Когда я
        # собирал это добро в список, то потом при удалении вариантов из bunch была ошибка при попытке удаления
        # того же числа несколько раз. Потом понял, что можно было просто проверять на if number in bunch_of_numbers
        # но решил оставить решение с сетом.
        elif ganados["bulls"] == 0:  # TODO: и тут
            bad_options = set()
            for letter in last_attempt:
                for number in bunch_of_numbers:
                    if last_attempt.find(letter) == number.find(letter):
                        bad_options.add(number)
            for number in bad_options:
                bunch_of_numbers.remove(number)

        # Случай, когда поголовье не 0, но и не 4, при этои имеем хотя бы одного быка(значит в комбинации есть хотя
        #  бы одно ненужное число). Тут можно удалить из множества все комбинации из этих 4-х цифр. Немножно упростил
        #  блок и изменил функцию init_versions
        else:  # TODO: и тут
            bad_options = init_versions(last_attempt)
            for number in bad_options:
                if number in bunch_of_numbers:
                    bunch_of_numbers.remove(number)


# возвращает число из списка возможных вариантов или списка комбинаций 4 цифр
def try_number():
    global last_attempt
    if len(versions) == 0:
        last_attempt = bunch_of_numbers[randint(0, len(bunch_of_numbers) - 1)]
    else:
        last_attempt = versions.pop()
        # TODO: о есть есть два источника чисел. bunch_of_numbers и versions.
        # TODO: Но из versions вы не вычищаете значения, когда check_sum == 0 и где не 0, не 4 и хотя бы один бык
        # TODO: мб где эти два списка синхронизируются, и я не увидел. Если мне не показалось,
        # TODO: попробуйте использовать один пул значений и по ходу выполнения его сокращать
    return last_attempt
