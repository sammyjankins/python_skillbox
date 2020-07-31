# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
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
import multiprocessing
import os

from utils import time_track, VolDataProcessor


class VolCalc(multiprocessing.Process):

    def __init__(self, file_name, collector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.collector = collector
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
        self.collector.put({'ticker': self.ticker, 'volatility': self.volatility})


class VolCalcP:

    def __init__(self, file_name):
        self.file_name = file_name
        self.vol = 0
        self.max_cost = 0
        self.min_cost = 0
        # self.data = {}

    def half_sum(self):
        return (self.max_cost + self.min_cost) / 2

    def evaluate_vol(self):
        return ((self.max_cost - self.min_cost) / self.half_sum()) * 100

    def run(self):
        ticker = self.file_name.split('_')[1][:-4]
        with open(file=self.file_name, mode='r', encoding='utf8') as file:
            transaction_prices = [float(line.split(',')[2]) for line in file if 'SECID' not in line]
            transaction_prices.sort()
            self.min_cost, self.max_cost = transaction_prices[0], transaction_prices[-1]
            volatility = self.evaluate_vol()
            return {'ticker': ticker, 'volatility': volatility}


def launch(processes=3, times=100):
    # print('============================================')
    # print(f'Процессов пула: {processes}')
    pool = multiprocessing.Pool(processes=processes)
    speed_array = []
    for _ in range(times):
        speed_array.append(restarter(pool)[1])
    average = sum(speed_array) / len(speed_array)
    return min(speed_array), max(speed_array), average


@time_track
def restarter(pool):
    directory_to_scan = 'trades'
    collector = []
    for dirpath, dirnames, filenames in os.walk(directory_to_scan):
        vols = [VolCalcP(os.path.join(directory_to_scan, file)) for file in filenames]
        collector = pool.map(VolCalcP.run, vols)
    vol_analysis = VolDataProcessor(collector)
    vol_analysis.process()
    # print(vol_analysis)


def main():
    tests = {str(amount): launch(amount) for amount in range(1, 15)}
    print('\nПолный список тестов:')
    print('+-------------+--------------+--------------+\n'
          '|  PROCESSES  |   MIN TIME   |   MAX TIME   |\n'
          '+-------------+--------------+--------------+')
    for count, time in tests.items():
        print(f'|{count:^12} - {time[0]:^12.2f} - {time[1]:^13.2f}|')
    print('+-------------+--------------+--------------+\n')

    fast = min(tests, key=lambda x: tests[x][0])
    print(f'Самый быстрый результат:\n'
          f'    Процессов: {fast}\n'
          f'    Среднее время исполнения: {tests[fast][2]}\n')
    if int(fast) == multiprocessing.cpu_count():
        print('Во время тестирования самые быстрые результаты были получены \n'
              'при количестве процессов, равном количеству ядер процессора.')


if __name__ == '__main__':
    main()

# Провел тесты дважды, и как ни странно, оба раза наибольшую эффективность проявили 9 процессов
# Скриншот: http://joxi.ru/J2bgg6QSG8bq3A
