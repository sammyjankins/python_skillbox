#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
shops = {
    'ашан':
        [
            {'name': 'печенье', 'price': 10.99},
            {'name': 'конфеты', 'price': 34.99},
            {'name': 'карамель', 'price': 45.99},
            {'name': 'пирожное', 'price': 67.99}
        ],
    'пятерочка':
        [
            {'name': 'печенье', 'price': 9.99},
            {'name': 'конфеты', 'price': 32.99},
            {'name': 'карамель', 'price': 46.99},
            {'name': 'пирожное', 'price': 59.99}
        ],
    'магнит':
        [
            {'name': 'печенье', 'price': 11.99},
            {'name': 'конфеты', 'price': 30.99},
            {'name': 'карамель', 'price': 41.99},
            {'name': 'пирожное', 'price': 62.99}
        ],
}

shop_names = list(shops.keys())

# sweets lists:

cookie_list = [shops[shop_names[0]][0], shops[shop_names[1]][0], shops[shop_names[2]][0]]
candy_list = [shops[shop_names[0]][1], shops[shop_names[1]][1], shops[shop_names[2]][1]]
caramel_list = [shops[shop_names[0]][2], shops[shop_names[1]][2], shops[shop_names[2]][2]]
cake_list = [shops[shop_names[0]][3], shops[shop_names[1]][3], shops[shop_names[2]][3]]

# sweets prices per shop:

cookie_prices = {cookie_list[0]['price']: shop_names[0],
                 cookie_list[1]['price']: shop_names[1],
                 cookie_list[2]['price']: shop_names[2]}
candy_prices = {candy_list[0]['price']: shop_names[0],
                candy_list[1]['price']: shop_names[1],
                candy_list[2]['price']: shop_names[2]}
caramel_prices = {caramel_list[0]['price']: shop_names[0],
                  caramel_list[1]['price']: shop_names[1],
                  caramel_list[2]['price']: shop_names[2]}
cake_prices = {cake_list[0]['price']: shop_names[0],
               cake_list[1]['price']: shop_names[1],
               cake_list[2]['price']: shop_names[2]}

# removing most expensive

del cookie_prices[max(cookie_prices)]
del candy_prices[max(candy_prices)]
del caramel_prices[max(caramel_prices)]
del cake_prices[max(cake_prices)]

cookie_prices_list = list(cookie_prices)
candy_prices_list = list(candy_prices)
caramel_prices_list = list(caramel_prices)
cake_prices_list = list(cake_prices)

# result:

sweets = {
    'печенье': [
        {'shop': cookie_prices[cookie_prices_list[0]], 'price': cookie_prices_list[0]},
        {'shop': cookie_prices[cookie_prices_list[1]], 'price': cookie_prices_list[1]},
    ],
    'конфеты': [
        {'shop': candy_prices[candy_prices_list[0]], 'price': candy_prices_list[0]},
        {'shop': candy_prices[candy_prices_list[1]], 'price': candy_prices_list[1]},
    ],
    'карамель': [
        {'shop': caramel_prices[caramel_prices_list[0]], 'price': caramel_prices_list[0]},
        {'shop': caramel_prices[caramel_prices_list[1]], 'price': caramel_prices_list[1]},
    ],
    'пирожное': [
        {'shop': cake_prices[cake_prices_list[0]], 'price': cake_prices_list[0]},
        {'shop': cake_prices[cake_prices_list[1]], 'price': cake_prices_list[1]},
    ],
}

pprint(sweets)


# зачет!
