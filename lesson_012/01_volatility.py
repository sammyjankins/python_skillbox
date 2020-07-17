# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от полусуммы крайних значений цены за торговую сессию:
#   полусумма = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / полусумма) * 100%
# Например для бумаги №1:
#   half_sum = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / half_sum) * 100 = 8.7%
# Для бумаги №2:
#   half_sum = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / half_sum) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>

from utils import time_track
import os


class VolCalc:

    def __init__(self, file_name):
        self.file_name = file_name
        self.vol = 0
        self.max_cost = 0
        self.min_cost = 0
        self.volatility = 0
        self.ticker = ''

    def half_sum(self):
        return (self.max_cost + self.min_cost) / 2

    def evaluate_vol(self):
        return ((self.max_cost - self.min_cost) / self.half_sum()) * 100

    def run(self):
        self.ticker = self.file_name.split('_')[1][:-4]
        with open(file=self.file_name, mode='r', encoding='utf8') as file:
            transaction_prices = [float(line.split(',')[2]) for line in file if 'SECID' not in line]
            transaction_prices.sort()
            self.min_cost, self.max_cost = transaction_prices[0], transaction_prices[-1]
            self.volatility = self.evaluate_vol()


@time_track
def main():
    directory_to_scan = 'trades'
    for dirpath, dirnames, filenames in os.walk(directory_to_scan):
        vols = [VolCalc(os.path.join(directory_to_scan, file)) for file in filenames]
        for vol in vols:
            vol.run()

        # формируем списки для принта:
        # TODO Обработку данных хорошо было бы вынести в отдельную функцию (её можно даже в отдельный модуль кинуть
        # TODO чтобы потом использовать во 2 и 3 частях)
        vols.sort(key=lambda obj: obj.volatility)
        zero_vols = []
        while True:
            if vols[0].volatility == 0:
                zero_vols.append(vols.pop(0).ticker)
            else:
                break
        max_vols = [vols.pop() for _ in range(3)]
        min_vols = [vols.pop(0) for _ in range(3)]

        # принтуем отформатированные списки:
        print('Максимальная волатильность: ')
        print('+----------+--------------+\n|  TICKER  |      VOL     |\n+----------+--------------+')

        for value in max_vols:
            print(f'|{value.ticker:^9} - {value.volatility:^10.2f} % |')
        print('+----------+--------------+\n')

        print('Минимальная волатильность: ')
        print('+----------+--------------+\n|  TICKER  |      VOL     |\n+----------+--------------+')
        for value in min_vols[::-1]:
            print(f'|{value.ticker:^9} - {value.volatility:^10.2f} % |')
        print('+----------+--------------+\n')

        print('Нулевая волатильность: ')
        print(', '.join([value for value in zero_vols]))
        print()


if __name__ == '__main__':
    main()
