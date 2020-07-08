# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>  # Итератор или генератор? выбирайте что вам более понятно
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234


# Решение с помощью итератора
class LogParser:

    def __init__(self, log_file_name):
        self.log_file_name = log_file_name
        self.log_file = None
        self.min_stat = None
        self.next_minute = None

    def __iter__(self):
        self.min_stat = None
        self.next_minute = None
        self.log_file = open(self.log_file_name, mode='r', encoding='utf8')
        return self

    def __next__(self):
        if self.next_minute:
            self.min_stat = self.next_minute
        for line in self.log_file:
            line = line[:-1]
            if self.check_line(line):
                continue
            else:
                for key, value in self.min_stat.items():
                    return key, value
        else:
            if self.next_minute:
                return self.next_minute.popitem()
            self.log_file.close()
            raise StopIteration()

    def check_line(self, line):
        if line.endswith('NOK'):
            minute = line.split('.')[0][1:-3]
            if self.min_stat is not None:
                if minute not in self.min_stat:
                    self.next_minute = {minute: 1}
                    return False
                else:
                    self.min_stat[minute] += 1
                    return True
            else:
                self.min_stat = {minute: 1}
                return True
        return True


# Решение с помощью генератора
def grouped_events_gen(file_name):
    min_stat = None
    with open(file_name, mode='r', encoding='utf8') as file:
        for line in file:
            line = line[:-1]
            minute = line.split('.')[0][1:-3]
            if line.endswith('NOK'):
                min_stat = yield from check_line(min_stat, minute)
        else:
            yield min_stat.popitem()


def check_line(min_stat, minute):
    if min_stat:
        if minute not in min_stat:
            yield min_stat.popitem()
            min_stat = {minute: 1}
        else:
            min_stat[minute] += 1
    else:
        min_stat = {minute: 1}
    return min_stat


# Это для инетатора
# grouped_events = LogParser('events.txt')

# А это для генератора
grouped_events = grouped_events_gen('events.txt')

for group_time, event_count in grouped_events:
    print(f'[{group_time}] {event_count}')

# Генераторами получилось лаконичнее.
# И внезапно, с помощью фичи пайчарма "extract method", узнал про такую возможность,
# как "yield from"
