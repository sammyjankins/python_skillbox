# -*- coding: utf-8 -*-
from functools import reduce


# Есть функция генерации списка простых чисел


def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
    return prime_numbers


# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик
class PrimeNumbers:
    """Итератор простых чисел до N элементов"""

    def __init__(self, n):
        self.number, self.n, self.primes = 2, n, []

    def __iter__(self):
        # self.number, self.primes = 2, []
        # это уже сделано в ините, можно не дублировать.
        # да, но ведь если эту строчку удалить и пройти по объекту циклом,
        # после прохода другим циклом по тому же объекту - параметры не обнулятся.
        # Разве не следует обнулить? Или обнулить хотя бы self.number..
        # Рассуждения верные, но итераторы по своей сущности - одноразовые
        # Если бы не это - вы были бы правы)
        # да, думаю я понял. Наверное обнуление имеет смысл, только если мы с помощью
        # класса эмулируем поведение контейнера, по элементам которого можно пройтись циклом..
        return self

    def __next__(self):
        while not self.check_number():
            if self.number < self.n:
                self.number += 1
            else:
                raise StopIteration()
        return self.number

    def check_number(self):
        for prime in self.primes:
            if self.number % prime == 0:
                return False
        else:
            self.primes.append(self.number)
            return True


prime_number_iterator = PrimeNumbers(n=10000)


# если это раскомментировать, то видно что параметры prime_number_iterator
# в следующем цикле не обнуляются
# for num in prime_number_iterator:
#     if num == 251:
#         print('==================== РАЗРЫВ! ====================!\n')
#         break
#     print(num)

# for num in prime_number_iterator:
#     print(num)

# можно делать дальше

# после подтверждения части 1 преподователем, можно делать
# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


# в качестве фильтров можно передавать
def prime_numbers_generator(n, filter_type=None):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
            if not filter_type or filter_type(number):
                yield number


for number_g, number_i in zip(prime_numbers_generator(n=10000), prime_number_iterator):
    print(number_g == number_i)


def is_lucky(number):
    number = str(number)
    len_step = len(number) // 2
    return sum(map(int, number[:len_step])) == sum(map(int, number[-len_step:]))


def is_palindromic(number):
    return number == number[::-1]


def is_factorion(number):
    """ Факторион
    — натуральное число, которое равно
    сумме факториалов своих цифр.
    """

    def factorial(n):
        if n == 0:
            return 1
        return reduce(lambda x, y: x * y, range(1, n + 1))

    digits = list(map(int, str(number)))
    return sum(list(map(factorial, digits))) == number


def is_armstrong(number):
    """ Число Армстронга
    — натуральное число, которое в данной
    системе счисления равно сумме своих
    цифр, возведённых в степень, равную
    количеству его цифр.
    """
    digits = list(map(int, str(number)))

    def len_pow(digit):
        return pow(digit, len(digits))

    return sum(map(len_pow, digits)) == number


def is_automorphic(number):
    """ Автоморфное число
     — число, десятичная запись квадрата которого
     оканчивается цифрами самого этого числа.
    """
    return str(number ** 2).endswith(str(number))


def is_trimorphic(number):
    """ Триморфное число
    — натуральное число, десятичная запись куба
    которого оканчивается цифрами самого этого числа.

    Каждое автоморфное число является триморфным.
    Обратное в общем случае неверно.
    """
    return str(number ** 3).endswith(str(number))


# тяжеловесный фильтр, каждую итерацию создается новый список простых чисел, чтобы найти индекс
def is_super_prime(number):
    """ Суперпростые числа
    (также известны как простые числа высшего порядка)
     — это подмножество простых чисел, стоящих в списке
     простых чисел на позициях, являющихся простыми числами.
    """

    primes = list(prime_numbers_generator(n=number))
    return number in primes and (primes.index(number) + 1) in primes


# числа армстронга, автоморфные и факторионы показывают скудные результаты
# даже в применении по одиночке..


print('=== Счастливые палиндромные простые числа ===')
for num in prime_numbers_generator(n=10000,
                                   filter_type=lambda x: all((is_palindromic(x), is_lucky(x)))):
    print(num)
print('Хотя смысла в этом не было, ведь палиндромные все счастливые...')
print()
print('=== Счастливые суперпростые числа ===')
for num in prime_numbers_generator(n=10000,
                                   filter_type=lambda x: all((is_lucky(x), is_super_prime(x)))):
    print(num)

print('=== Палиндромные суперпростые числа ===')

for num in prime_numbers_generator(n=10000,
                                   filter_type=lambda x: all((is_palindromic(x),
                                                              is_super_prime(x)))):
    print(num)

# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.
#зачёт!