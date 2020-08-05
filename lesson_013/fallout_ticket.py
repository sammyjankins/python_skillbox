# -*- coding: utf-8 -*-

import os
import qrcode
from random import choice, randint
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def make_qr(info, color_hex, bg_color_hex):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=3,
        border=1
    )
    qr.add_data(info)
    qr.make()
    return qr.make_image(fill_color=bg_color_hex, back_color=color_hex, border_color=color_hex)


def draw_frame(draw_obj, color):
    x_left = 30
    x_right = 700
    y_top = 30
    y_bottom = 380
    y_up_mid = 190
    y_down_mid = 220

    # вертикальные
    draw_obj.line([x_left, y_top, x_left, y_up_mid], fill=color, width=2)
    draw_obj.line([x_left, y_down_mid, x_left, y_bottom], fill=color, width=2)
    draw_obj.line([x_right, y_down_mid, x_right, 305], fill=color, width=2)
    draw_obj.line([x_right, y_top, x_right, y_up_mid], fill=color, width=2)
    draw_obj.line([x_right, 348, x_right, y_bottom], fill=color, width=2)

    # горизонтальные
    draw_obj.line([x_left, y_top, 200, y_top], fill=color, width=2)
    draw_obj.line([498, y_top, x_right, y_top], fill=color, width=2)
    draw_obj.line([x_left, y_bottom, 349, y_bottom], fill=color, width=2)
    draw_obj.line([379, y_bottom, 604, y_bottom], fill=color, width=2)
    draw_obj.line([678, y_bottom, x_right, y_bottom], fill=color, width=2)


def make_fields(f_path, draw_obj, color):
    font = ImageFont.truetype(f_path, 24)
    draw_obj.text((55, 75), 'PASSENGER:', font=font, fill=color)
    draw_obj.text((260, 75), 'DATE:', font=font, fill=color)
    draw_obj.text((445, 75), 'SEAT:', font=font, fill=color)
    draw_obj.text((55, 305), 'GATE:', font=font, fill=color)


def make_fallout_ticket(fio, from_, to, date):
    color = (104, 224, 124)
    color_hex = f'#{"".join([hex(x)[2:] for x in color])}'
    bg_color_hex = '#0f350c'

    im = Image.open('python_snippets/fallout-3preview.jpg')
    qr_source = 'https://tinyurl.com/2fcpre6'

    draw = ImageDraw.Draw(im)
    f_path = os.path.normpath('python_snippets/Overseer.ttf')

    make_fields(f_path, draw, color)
    draw_frame(draw, color)
    im.paste(make_qr(qr_source, color_hex, bg_color_hex), (596, 30))

    font = ImageFont.truetype(f_path, 24)
    draw.text((55, 105), fio, font=font, fill=color)
    draw.text((260, 105), date, font=font, fill=color)

    seat, gate = [f'{randint(1, 24)}{choice("ABCDEF")}' for _ in range(2)]
    draw.text((445, 105), seat, font=font, fill=color)
    draw.text((55, 335), gate, font=font, fill=color)

    boarding_font = ImageFont.truetype(f_path, 22)
    today = datetime.today()
    draw.text((260, 305), f'Boarding time: {today.strftime("%H:%M")}', font=boarding_font, fill=color)
    draw.text((185, 335), '*beware of ghouls in the waiting room', font=boarding_font, fill=color)

    route = f'{from_} >> {to}'
    r_font_size = 48 if len(route) <= 25 else 50 - len(route) // 2
    route_font = ImageFont.truetype(f_path, r_font_size)
    field_width = 25 if len(route) <= 25 else 25 + len(route) // 2
    draw.text((55, 193), f'{route:^{field_width}}', font=route_font, fill=color)
    im.show()
    return im


def main():
    img = make_fallout_ticket('Alex Murphy', 'Detroit', 'Los Angeles', '17.07.1987')
    img.show()


if __name__ == '__main__':
    main()
