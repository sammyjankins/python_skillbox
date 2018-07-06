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

product_quantity = 0
product_price = 0
for product in goods:
    for type_of_product in store[goods[product]]:
        product_quantity += type_of_product['quantity']
        product_price += type_of_product['price'] * type_of_product['quantity']
    print(product, '-', product_quantity, 'щт, стоимость', product_price, 'руб')
    product_quantity, product_price = 0, 0


# зачет!






