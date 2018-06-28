#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Есть словарь кодов товаров

goods = {
    'Лампа': '12345',
    'Стол': '23456',
    'Диван': '34567',
    'Стул': '45678',
}

# Есть словарь списков количества товаров на складе.

store = {
    '12345': [
        {'quantity': 27, 'price': 42},
    ],
    '23456': [
        {'quantity': 22, 'price': 510},
        {'quantity': 32, 'price': 520},
    ],
    '34567': [
        {'quantity': 2, 'price': 1200},
        {'quantity': 1, 'price': 1150},
    ],
    '45678': [
        {'quantity': 50, 'price': 100},
        {'quantity': 12, 'price': 95},
        {'quantity': 43, 'price': 97},
    ],
}

# Рассчитать на какую сумму лежит каждого товара на складе
# например для ламп

lamps_cost = store[goods['Лампа']][0]['quantity'] * store[goods['Лампа']][0]['price']
# или проще (/сложнее ?)
lamp_code = goods['Лампа']
lamps_item = store[lamp_code][0]
lamps_quantity = lamps_item['quantity']
lamps_price = lamps_item['price']
lamps_cost = lamps_quantity * lamps_price
print('Лампа -', lamps_quantity, 'шт, стоимость', lamps_cost, 'руб')

tables_code = goods['Стол']
tables_quantities = [store[tables_code][0]['quantity'],
                     store[tables_code][1]['quantity']]
tables_prices = [store[tables_code][0]['price'],
                 store[tables_code][1]['price']]
tables_cost = tables_quantities[0] * tables_prices[0] + \
              tables_quantities[1] * tables_prices[1]
print('Стол -', tables_quantities[0] + tables_quantities[1], 'шт, стоимость', tables_cost, 'руб')

sofas_code = goods['Диван']
sofas_quantities = [store[sofas_code][0]['quantity'],
                    store[sofas_code][1]['quantity']]
sofas_prices = [store[sofas_code][0]['price'],
                store[sofas_code][1]['price']]
sofas_cost = sofas_quantities[0] * sofas_prices[0] + \
             sofas_quantities[1] * sofas_prices[1]
print('Диван -', sofas_quantities[0] + sofas_quantities[1], 'шт, стоимость', sofas_cost, 'руб')

chairs_code = goods['Стул']
chairs_quantities = [store[chairs_code][0]['quantity'],
                     store[chairs_code][1]['quantity'],
                     store[chairs_code][2]['quantity']]
chairs_prices = [store[chairs_code][0]['price'],
                 store[chairs_code][1]['price'],
                 store[chairs_code][2]['price']]
chairs_cost = chairs_quantities[0] * chairs_prices[0] + \
              chairs_quantities[1] * chairs_prices[1] + \
              chairs_quantities[2] * chairs_prices[2]
print('Стул -', chairs_quantities[0] + chairs_quantities[1] + chairs_quantities[2], 'шт, стоимость', chairs_cost, 'руб')








