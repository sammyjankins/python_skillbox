# -*- coding: utf-8 -*-
import zipfile


# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.


class LogScanner:

    def __init__(self, log_to_scan, log_bad_file, log_good_file):
        self.in_file = log_to_scan
        self.out_bad = log_bad_file
        self.out_good = log_good_file
        self.line = None
        self.exception = None

    def unzip(self):
        z_file = zipfile.ZipFile(self.in_file, 'r')
        for filename in z_file.namelist():
            z_file.extract(filename)
        self.in_file = filename

    def check_line(self):
        line_data = self.line.split()
        if len(line_data) != 3:
            raise ValueError(f'Строка "{self.line}" содержит мерее 3-х полей')
        if not line_data[0].isalpha():
            raise NotNameError(line_data[0])
        if any(('@' not in line_data[1], '.' not in line_data[1])):
            raise NotEmailError(line_data[1])
        if any((not line_data[2].isdigit(), not (10 <= int(line_data[2]) <= 99))):
            raise ValueError(f'{line_data[2]} - недопустимое значение возраста')

    def scan(self):
        if self.in_file.endswith('.zip'):
            self.unzip()
        is_good_line = None
        with open(self.in_file, mode='r', encoding='utf8') as log:
            for line in log:
                self.line = line[:-1]
                try:
                    self.check_line()
                    is_good_line = True
                except Exception as exc:
                    self.exception = str(exc)
                    is_good_line = False
                finally:
                    self.save_line_to_file(is_good_line)

    def save_line_to_file(self, is_good_line=True):
        with open(self.out_good if is_good_line else self.out_bad, mode='a', encoding='utf8') as out_file:
            result = f'\n{self.line}' + f' [Exception: {self.exception}]' * (not is_good_line)
            out_file.write(result)


class NotNameError(Exception):

    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        return f'{self.name} - имя содержит недопустимые символы'


class NotEmailError(Exception):

    def __init__(self, email=None):
        self.email = email

    def __str__(self):
        return f'{self.email} - некорректное поле e-mail'


file = 'registrations.txt'

log_scanner = LogScanner(file, log_bad_file='registrations_bad.log', log_good_file='registrations_good.log')
log_scanner.scan()
