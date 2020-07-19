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

    def __init__(self, vols_container, max_tickers=3, min_tickers=3):
        self.max = []
        self.min = []
        self.zero = []
        self.vols_container = vols_container
        self.process(max_tickers, min_tickers)
        # TODO Основную логику программы стоит всё же запускать отдельно, не в Init-е

    # что-то мне подсказывает, что такое использование специального метода
    # не совсем корректно...если так, жду замечания)
    def __str__(self):
        self.print_max()
        self.print_min()
        self.print_zero()
        return '-'

    def construct_zero(self):
        while True:
            if self.vols_container[0].volatility == 0:
                self.zero.append(self.vols_container.pop(0).ticker)
            else:
                break

    def construct_max(self, max_tickers):
        self.max = [self.vols_container.pop() for _ in range(max_tickers)]

    def construct_min(self, min_tickers):
        # TODO Удаление элемента из начала списка ведет к сдвигу всех элементов списка
        # TODO т.е. вызывает количество операций, пропорциональное количеству элементов в списке
        # TODO в целом эффективнее было бы использовать срезы из списков, например список[-3:]
        self.min = [self.vols_container.pop(0) for _ in range(min_tickers)]

    def process(self, max_tickers, min_tickers):
        self.vols_container.sort(key=lambda obj: obj.volatility)
        self.construct_zero()
        self.construct_max(max_tickers)
        self.construct_min(min_tickers)

    def print_max(self):  # TODO Плюс на каждый метод сам по себе выделяется отдельная память
        # TODO пусть это и не так затратно, как в ситуации со списком.
        # TODO Но можно было бы объединить печать в один метод.
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


class VolQueueProcessor(VolDataProcessor):

    def process(self, max_tickers, min_tickers):
        # это вообще законно?
        # TODO В этом скорее нет необходимости, класс для тикера можно создать и вне функции/класса
        # TODO правда не уверен, что это необходимо, т.к. по сути это лишние затраты памяти
        # TODO когда для этой цели можно использовать тот же словарь или список
        class Vol:

            def __init__(self, ticker, volatility):
                self.ticker = ticker
                self.volatility = volatility

        vols_list = []
        while not self.vols_container.empty():
            vol = Vol(**self.vols_container.get())
            vols_list.append(vol)
        self.vols_container = vols_list
        super().process(max_tickers, min_tickers)
# TODO И по итогу - чем больше кода вы сможете удалить, тем лучше он будет работать :)