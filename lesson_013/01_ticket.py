# -*- coding: utf-8 -*-
import argparse
from os import path, makedirs

from PIL import Image, ImageDraw, ImageFont
from fallout_ticket import make_fallout_ticket


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

def make_ticket(fio, from_, to, date):
    im = Image.open('images/ticket_template.png')
    draw = ImageDraw.Draw(im)
    f_path = path.normpath('Roboto-Light.ttf')
    font = ImageFont.truetype(f_path, 16)
    date_font = ImageFont.truetype(f_path, 12)
    draw.text((45, 123), fio, font=font, fill='black')
    draw.text((45, 193), from_, font=font, fill='black')
    draw.text((45, 257), to, font=font, fill='black')
    draw.text((288, 260), date, font=date_font, fill='black')
    im.show()
    return im


# make_ticket('Dan B Cooper', 'Portland', 'Seattle', '24.11.1971')

def valid_name(line):
    line = ''.join(line)
    return line.isalpha()


def valid_date(line):
    from datetime import datetime
    try:
        day, month, year = line.split('.')
        datetime(year=int(year), month=int(month), day=int(day))
        return True
    except ValueError as exc:
        if 'unpack' in exc.args[0] or 'literal' in exc.args[0]:
            print(f'Incorrect date: please specify date following the example: 24.11.2004')
        else:
            print(f'Incorrect date: {exc}')
        return False


def check_args(args):
    return all((valid_name(args.fio),
                valid_name(args.from_),
                valid_name(args.to),
                valid_date(args.date)))


def process_cmd(args):
    if check_args(args):
        fio, from_, to = [' '.join(line) for line in (args.fio, args.from_, args.to)]
        if args.fallout:
            im = make_fallout_ticket(fio, from_, to, args.date)
        else:
            im = make_ticket(fio, from_, to, args.date)
        if args.save_to is not None:
            try:
                makedirs(args.save_to, exist_ok=True)
                rgb_im = im.convert('RGB')
                rgb_im.save(path.join(args.save_to, 'ticket.jpg'))
            except Exception as exc:
                print(exc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fio', action='store', dest='fio', nargs='+', required=True, help='Last name')
    parser.add_argument('--from', action='store', dest='from_', nargs='+', required=True, help='From where')
    parser.add_argument('--to', action='store', dest='to', nargs='+', required=True, help='To where')
    parser.add_argument('--date', action='store', dest='date', required=True, help='Example: 24.11.2004')
    parser.add_argument('--save_to', action='store', dest='save_to', required=False, help='Path to save the image')
    parser.add_argument('--fallout', action='store_true', required=False, help='Make fallout ticket')
    args = parser.parse_args()
    process_cmd(args)


if __name__ == '__main__':
    main()

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.


# варианты консольного запуска:
# python 01_ticket.py --fio Dan B Cooper --from Portland --to Seattle --date 24.11.1971
# python 01_ticket.py --fio Dan B Cooper --from Portland --to Seattle --date 24.11.1971 --save_to tickets/skillbox
# python 01_ticket.py --fio Alex Murphy --from Detroit --to Los Angeles --date 17.07.1987 --fallout
# python 01_ticket.py --fio Alex Murphy --from Detroit --to Los Angeles --date 17.07.1987 --fallout --save_to
# tickets/fallout
