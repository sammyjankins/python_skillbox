# -*- coding: utf-8 -*-

import os
import shutil
import time
import zipfile

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.


class FileArrange:

    def __init__(self, source_name, destination_name):
        self.source_name = source_name
        self.destination_name = destination_name
        self.full_file_path = ''

    def inspect_and_sort(self):
        for dirpath, dirnames, filenames in os.walk(self.source_name):
            for file in filenames:
                self.full_file_path = os.path.join(dirpath, file)
                secs = os.path.getmtime(self.full_file_path)
                file_time = time.gmtime(secs)
                self.dir_constructor(file,
                                     file_time.tm_year,
                                     file_time.tm_mon,
                                     file_time.tm_mday)

    def dir_constructor(self, file, year, month, day):
        cpy_dir = f'{self.destination_name}/{str(year)}/{str(month)}/{str(day)}'
        cpy_dir = os.path.normpath(cpy_dir)
        result_file_path = os.path.join(cpy_dir, file)
        if not os.path.exists(cpy_dir):
            os.makedirs(cpy_dir)
        self.move_file_to_dir(result_file_path)

    def move_file_to_dir(self, result_file_path):
        shutil.copy2(self.full_file_path, result_file_path)


class ZipArrange(FileArrange):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.z_file = zipfile.ZipFile(self.source_name, 'r')

    # хоть и зачтено, но изменил метод,
    # теперь будет работать для любых файлов, а не только .png
    def inspect_and_sort(self):
        infolist = self.z_file.infolist()
        for value in infolist:
            self.full_file_path = value.filename
            if not value.is_dir():
                file = value.filename.split('/')[-1]
                file_m_date = value.date_time
                self.dir_constructor(file,
                                     file_m_date[0],
                                     file_m_date[1],
                                     file_m_date[2])

    def move_file_to_dir(self, result_file_path):
        source = self.z_file.open(self.full_file_path)
        target = open(result_file_path, "wb")
        with source, target:
            shutil.copyfileobj(source, target)


file_source = 'icons'
zip_source = 'icons.zip'
destination_path = 'icons_by_year'
zip_destination_path = 'unzipped_icons_by_year'

file_arrange = FileArrange(file_source, destination_path)
file_arrange.inspect_and_sort()
zip_arrange = ZipArrange(zip_source, zip_destination_path)
zip_arrange.inspect_and_sort()

# зачет!
# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится ктолько к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
