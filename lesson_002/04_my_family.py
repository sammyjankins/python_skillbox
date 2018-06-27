#!/usr/bin/env python3
# -*- coding: utf-8 -*-

my_family = ['Отец', 'Мать', 'Я', 'Дедушка', 'Бабушка']

my_family_height = [
    ['Андрей', 170],
    ['Ольга', 165],
    ['Олег', 170],
    ['Виктор', 165],
    ['Надежда', 150]
]

print('Рост отца', my_family_height[0][1], 'см')

print('Рост всей семьи',
      my_family_height[0][1] +
      my_family_height[1][1] +
      my_family_height[2][1] +
      my_family_height[3][1] +
      my_family_height[4][1]
      , 'см')

# зачет!