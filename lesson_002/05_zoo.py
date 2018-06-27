#!/usr/bin/env python
# -*- coding: utf-8 -*-

zoo = ['lion', 'kangaroo', 'elephant', 'monkey', ]

zoo.insert(1, 'bear')
print(zoo)

birds = ['rooster', 'ostrich', 'lark', ]

zoo.extend(birds)
print(zoo)

zoo.remove('elephant')
print(zoo)

print(zoo.index('monkey')+1)

print(zoo.index('lark')+1)



# зачет!