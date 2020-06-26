# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import zipfile


class LogParser:

    def __init__(self, log_file_name, out_file_name):
        self.log_file_name = log_file_name
        self.out_file_name = out_file_name
        self.min_stat = {}

    def unzip(self):
        z_file = zipfile.ZipFile(self.log_file_name, 'r')
        for filename in z_file.namelist():
            z_file.extract(filename)
        self.log_file_name = filename

    def count_events(self):
        with open(self.log_file_name, mode='r', encoding='utf8') as log:
            for line in log:
                line = line[:-1]
                if line.endswith('NOK'):
                    minute = line.split('.')[0][:-3]
                    self.stat_update(minute)

    def stat_update(self, minute):
        if minute not in self.min_stat:
            if self.min_stat:
                self.save_stat_line()
                self.min_stat.clear()
            self.min_stat[minute] = 1
        else:
            self.min_stat[minute] += 1

    def save_stat_line(self):
        with open(self.out_file_name, 'a', encoding='utf8') as stat_file:
            for key, value in self.min_stat.items():
                stat_file.write(f'{key}] {value}\n')
        # for key, value in self.min_stat.items():
        #     print(f'{key}] {value}')


logparser = LogParser('events.txt', 'out.txt')
logparser.count_events()

# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
