# -*- coding: utf-8 -*-

import simple_draw as sd
import snowfall

# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N)
#  нарисовать_снежинки_цветом(color)
#  сдвинуть_снежинки()
#  количество_достигших_низа_экрана()
#  добавить_снежинки(count)
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

snowfall.create_snowflakes(20)
while True:
    snowfall.move_snowflakes()
    count = snowfall.bottom_count()
    if count:
        snowfall.create_snowflakes(
            count)  # add_snowflakes решил упразднить, т.к. create_snowflakes по сути это и делает
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
# зачет!