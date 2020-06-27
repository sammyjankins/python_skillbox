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


class CharStat:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}

    def unzip(self):
        z_file = zipfile.ZipFile(self.file_name, 'r')
        for filename in z_file.namelist():
            z_file.extract(filename)
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
        print('''+---------+----------+\n|  буква  | частота  |\n+---------+----------+''')
        stat_sum = 0
        for letter, count in self.sort_stat():
            print(f'|{letter:^9}|{count:^10}|')
            stat_sum += count
        print(f'''+---------+----------+\n|  итого  |{stat_sum:^10}|\n+---------+----------+''')

    def sort_function(self, pair):
        return pair[1]

    def sort_stat(self):
        return sorted(self.stat.items(), key=self.sort_function, reverse=True)


class AlphaSortedStat(CharStat):

    def __init__(self, reverse=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reverse = reverse

    def sort_stat(self):
        return sorted(self.stat.items(), reverse=self.reverse)


filename = 'python_snippets/voyna-i-mir.txt'


# зачет!

# def sort_function(pair):
#     return pair[1]


# charstat = CharStat(file_name=filename)
# charstat.calculate_stat()
# charstat.print_stat()

# stat = AlphaSortedStat(file_name=filename)
# stat.calculate_stat()
# stat.print_stat()

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

def check_user_input(text):
    user_input = input(text)
    while user_input not in ('да', 'нет'):
        user_input = input('Необходимо ввести: да/нет >>> ')
    return user_input == 'да'


if __name__ == '__main__':
    need_alpha_sort = check_user_input('Сортировать статистику по алфавиту? (да/нет) >>> ')
    # filename = 'python_snippets/voyna-i-mir.txt'
    filename = 'python_snippets/voyna-i-mir.txt.zip'
    if need_alpha_sort:
        need_reverse = check_user_input('В порядке возрастания? (да/нет) >>> ')
        char_stat = AlphaSortedStat(file_name=filename, reverse=not need_reverse)
    else:
        char_stat = CharStat(file_name=filename)
    char_stat.calculate_stat()
    char_stat.print_stat()
