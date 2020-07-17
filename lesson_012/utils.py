import time


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result

    return surrogate


class VolDataProcessor:

    def __init__(self, vols_list, max_tickers=3, min_tickers=3):
        self.max = []
        self.min = []
        self.zero = []
        self.vols_list = vols_list
        self.process(max_tickers, min_tickers)

    # что-то мне подсказывает, что такое использование специального метода
    # не совсем корректно...если так, жду замечания)
    def __str__(self):
        self.print_max()
        self.print_min()
        self.print_zero()
        return '-'

    def construct_zero(self):
        while True:
            if self.vols_list[0].volatility == 0:
                self.zero.append(self.vols_list.pop(0).ticker)
            else:
                break

    def construct_max(self, max_tickers):
        self.max = [self.vols_list.pop() for _ in range(max_tickers)]

    def construct_min(self, min_tickers):
        self.min = [self.vols_list.pop(0) for _ in range(min_tickers)]

    def process(self, max_tickers, min_tickers):
        self.vols_list.sort(key=lambda obj: obj.volatility)
        self.construct_zero()
        self.construct_max(max_tickers)
        self.construct_min(min_tickers)

    def print_max(self):
        print('Максимальная волатильность: ')
        print('+----------+--------------+\n|  TICKER  |      VOL     |\n+----------+--------------+')

        for value in self.max:
            print(f'|{value.ticker:^9} - {value.volatility:^10.2f} % |')
        print('+----------+--------------+\n')

    def print_min(self):
        print('Минимальная волатильность: ')
        print('+----------+--------------+\n|  TICKER  |      VOL     |\n+----------+--------------+')
        for value in self.min[::-1]:
            print(f'|{value.ticker:^9} - {value.volatility:^10.2f} % |')
        print('+----------+--------------+\n')

    def print_zero(self):
        print('Нулевая волатильность: ')
        print(', '.join([value for value in self.zero]))
