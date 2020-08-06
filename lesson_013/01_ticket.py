# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
from os import path, makedirs
from random import randint, choice

import qrcode
from PIL import Image, ImageDraw, ImageFont


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

class Ticket:
    template = 'images/ticket_template.png'
    font_path = path.normpath('Roboto-Light.ttf')

    def __init__(self, fio, from_, to, date, save_path=None):
        self.fio = fio
        self.from_ = from_
        self.to = to
        self.date = date
        self.save_path = save_path
        self.im = None
        self.draw = None

    @staticmethod
    def _valid_name(line):
        line = ''.join(line)
        return line.isalpha()

    @staticmethod
    def _valid_date(line):
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

    def _check_args(self):
        return all((self._valid_name(self.fio),
                    self._valid_name(self.from_),
                    self._valid_name(self.to),
                    self._valid_date(self.date)))

    def make_ticket(self):
        self.im = Image.open(self.template)
        self.draw = ImageDraw.Draw(self.im)
        font = ImageFont.truetype(self.font_path, 16)
        date_font = ImageFont.truetype(self.font_path, 12)
        self.draw.text((45, 123), self.fio, font=font, fill='black')
        self.draw.text((45, 193), self.from_, font=font, fill='black')
        self.draw.text((45, 257), self.to, font=font, fill='black')
        self.draw.text((288, 260), self.date, font=date_font, fill='black')
        if self.save_path is not None:
            self._save()
        self.im.show()

    def _save(self):
        try:
            makedirs(self.save_path, exist_ok=True)
            rgb_im = self.im.convert('RGB')
            rgb_im.save(path.join(self.save_path, 'ticket.jpg'))
        except Exception as exc:
            print(exc)


class FalloutTicket(Ticket):
    template = 'fallout-3preview.jpg'
    font_path = path.normpath('Overseer.ttf')
    qr_source = 'https://tinyurl.com/2fcpre6'
    color = (104, 224, 124)
    color_hex = f'#{"".join([hex(x)[2:] for x in color])}'
    bg_color_hex = '#0f350c'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_font = None

    def _make_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=3,
            border=1
        )
        qr.add_data(self.qr_source)
        qr.make()
        return qr.make_image(fill_color=self.bg_color_hex, back_color=self.color_hex, border_color=self.color_hex)

    def _draw_frame(self):
        x_left = 30
        x_right = 700
        y_top = 30
        y_bottom = 380
        y_up_mid = 190
        y_down_mid = 220

        # вертикальные
        self.draw.line([x_left, y_top, x_left, y_up_mid], fill=self.color, width=2)
        self.draw.line([x_left, y_down_mid, x_left, y_bottom], fill=self.color, width=2)
        self.draw.line([x_right, y_down_mid, x_right, 305], fill=self.color, width=2)
        self.draw.line([x_right, y_top, x_right, y_up_mid], fill=self.color, width=2)
        self.draw.line([x_right, 348, x_right, y_bottom], fill=self.color, width=2)

        # горизонтальные
        self.draw.line([x_left, y_top, 200, y_top], fill=self.color, width=2)
        self.draw.line([498, y_top, x_right, y_top], fill=self.color, width=2)
        self.draw.line([x_left, y_bottom, 349, y_bottom], fill=self.color, width=2)
        self.draw.line([379, y_bottom, 604, y_bottom], fill=self.color, width=2)
        self.draw.line([678, y_bottom, x_right, y_bottom], fill=self.color, width=2)

    def _make_fields(self):
        self.draw.text((55, 75), 'PASSENGER:', font=self.base_font, fill=self.color)
        self.draw.text((260, 75), 'DATE:', font=self.base_font, fill=self.color)
        self.draw.text((445, 75), 'SEAT:', font=self.base_font, fill=self.color)
        self.draw.text((55, 305), 'GATE:', font=self.base_font, fill=self.color)

    def _arrange_template(self):
        seat, gate = [f'{randint(1, 24)}{choice("ABCDEF")}' for _ in range(2)]
        self.draw.text((445, 105), seat, font=self.base_font, fill=self.color)
        self.draw.text((55, 335), gate, font=self.base_font, fill=self.color)

        boarding_font = ImageFont.truetype(self.font_path, 22)
        today = datetime.today()
        self.draw.text((260, 305), f'Boarding time: {today.strftime("%H:%M")}', font=boarding_font, fill=self.color)
        self.draw.text((185, 335), '*beware of ghouls in the waiting room', font=boarding_font, fill=self.color)
        self._make_fields()
        self._draw_frame()
        self.im.paste(self._make_qr(), (596, 30))

    def make_ticket(self):
        self.im = Image.open(self.template)
        self.draw = ImageDraw.Draw(self.im)
        self._arrange_template()
        self.base_font = ImageFont.truetype(self.font_path, 24)
        self.draw.text((55, 105), self.fio, font=self.base_font, fill=self.color)
        self.draw.text((260, 105), self.date, font=self.base_font, fill=self.color)

        route = f'{self.from_} >> {self.to}'
        r_font_size = 48 if len(route) <= 25 else 50 - len(route) // 2
        route_font = ImageFont.truetype(self.font_path, r_font_size)
        field_width = 25 if len(route) <= 25 else 25 + len(route) // 2
        self.draw.text((55, 193), f'{route:^{field_width}}', font=route_font, fill=self.color)
        if self.save_path is not None:
            self._save()
        self.im.show()


def process_cmd(args):
    fio, from_, to = [' '.join(line) for line in (args.fio, args.from_, args.to)]
    ticket_class = FalloutTicket if args.fallout else Ticket
    ticket = ticket_class(fio, from_, to, args.date, args.save_to)
    ticket.make_ticket()


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
