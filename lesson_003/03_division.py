# -*- coding: utf-8 -*-

# (цикл while)

# даны целые положительные числа a и b (a > b)
# Определить результат целочисленного деления a на b,
# __НЕ__ используя стандартную операцию целочисленного деления (// и %)

a, b = 179, 37

result = 0
while a >= b:
    a -= b
    result += 1

print(result)

# зачет!
