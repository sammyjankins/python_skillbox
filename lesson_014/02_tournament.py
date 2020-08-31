# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно просчитать протокол турнира по боулингу в файле tournament.txt
#
# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X
#   Давид	--8/--8/4/8/-224----
#   Павел	----15623113-95/7/26
#   Роман	7/428/--4-533/34811/
#   winner is .........
#
# Нужно сформировать выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   Давид	--8/--8/4/8/-224----    68
#   Павел	----15623113-95/7/26    69
#   Роман	7/428/--4-533/34811/    94
#   winner is Татьяна

# Код обаботки файла расположить отдельном модуле, модуль bowling использовать для получения количества очков
# одного участника. Если захочется изменить содержимое модуля bowling - тесты должны помочь.
#
# Из текущего файла сделать консольный скрипт для формирования файла с результатами турнира.
# Параметры скрипта: --input <файл протокола турнира> и --output <файл результатов турнира>

import argparse
import logging

from eval_protocol import Protocol  # TODO: на Protocol тоже нужны тесты

FORMAT = '[%(asctime)-15s] %(message)s'


def main():
    logging.basicConfig(
        format=FORMAT,
        level=logging.INFO,
        handlers=[logging.FileHandler('log_bowling.log', 'a', 'utf-8')],
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', action='store', dest='input', required=True, help='Input file path')
    parser.add_argument('--output', action='store', dest='output', required=True, help='Output file path')
    args = parser.parse_args()
    protocol = Protocol(args.input)
    protocol.run()

    write_to_file(args, protocol)
    print_rate_table(protocol)


def write_to_file(args, protocol):
    with open(args.output, mode='w', encoding='utf8') as file:
        for line in protocol.results:
            file.write(line)


def print_rate_table(protocol):
    print('+----------+------------------+--------------+\n'
          '|  Игрок   |  сыграно матчей  |  всего побед |\n'
          '+----------+------------------+--------------+')
    for player in sorted(protocol.rate,
                         key=lambda x: protocol.rate[x]['victories'],
                         reverse=True):
        print(f'|{player:^10}|'
              f'{protocol.rate[player]["games"]:^18}|'
              f'{protocol.rate[player]["victories"]:^14}|')
    print('+----------+------------------+--------------+\n')


if __name__ == '__main__':
    main()

# Усложненное задание (делать по желанию)
#
# После обработки протокола турнира вывести на консоль рейтинг игроков в виде таблицы:
#
# +----------+------------------+--------------+
# | Игрок    |  сыграно матчей  |  всего побед |
# +----------+------------------+--------------+
# | Татьяна  |        99        |      23      |
# ...
# | Алексей  |        20        |       5      |
# +----------+------------------+--------------+
