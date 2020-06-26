# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.
import zipfile
from pprint import pprint


class CharStat:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
        self.file_name = filename

    def calculate_stat(self):
        if self.file_name.endswith('.zip'):
            self.unzip()
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                self.scan_file_line(line)

    def scan_file_line(self, line):
        for char in line:
            if char.isalpha():
                if char in self.stat:
                    self.stat[char] += 1
                else:
                    self.stat[char] = 1

    def print_stat(self):
        pass

    def sort_stat(self):
        pass


class AlphaSortedStat(CharStat):

    def __init__(self, reverse=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverse = reverse

    def sort_function(self, pair):
        return pair[1]


# pprint(sorted(charstat.stat.items(), key=sort_function, reverse=True))
# pprint(sorted(charstat.stat.items()))
# pprint(sorted(charstat.stat.items(), reverse=True))

# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://goo.gl/Vz4828
#   и пример https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4

if __name__ == '__main__':
    need_alpha = input('Сортировать статистику по алфавиту? (да/нет) >>>') == 'да'
    filename = 'python_snippets/voyna-i-mir.txt'
    if need_alpha:
        need_reverse = input('В порядке возрастания? (да/нет) >>>') == 'да'
        char_stat = AlphaSortedStat(file_name=filename, reverse=need_reverse)
    else:
        char_stat = CharStat(file_name=filename)
    char_stat.calculate_stat()
    char_stat.print_stat()
