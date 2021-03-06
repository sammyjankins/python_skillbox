# -*- coding: utf-8 -*-

# (if/elif/else)

# Заданы размеры A, B - размеры конверта и x, y листа бумаги (все размеры
# могут быть в диапазоне от 1 до 1000)
#
# Определить, поместится ли бумага в конверте (стороны листа параллельны сторонам конверта)
#
# Результат проверки вывести на консоль (ДА/НЕТ)
# Использовать только операторы if/elif/else, можно вложенные

A, B = 10, 7
x, y = 8, 9

print()
print('Конверт (', A, 'на', B, ') и лист:')

if x <= A and y <= B:
    print('Размеры -', x, 'на', y, '- ДА')
elif y <= A and x <= B:
    print('Размеры -', x, 'на', y, '- ДА')
else:
    print('Размеры -', x, 'на', y, '- НЕТ')

# (усложненное задание, решать по желанию)
# Заданы размеры А, В прямоугольного отверстия и размеры х, у, z кирпича (все размеры
# могут быть в диапазоне от 1 до 1000)
#
# Определить, пройдет ли кирпич через отверстие (грани кирпича параллельны сторонам отверстия)

A, B = 8, 9

print()
print('Отверстие (', A, 'на', B, ') и кирпич:')

# x, y, z = 11, 2, 10
# x, y, z = 10, 11, 2
# x, y, z = 10, 2, 11
# x, y, z = 2, 10, 11
# x, y, z = 2, 11, 10
# x, y, z = 3, 6, 5
# x, y, z = 6, 3, 5
# x, y, z = 6, 5, 3
# x, y, z = 5, 6, 3
# x, y, z = 5, 3, 6
# x, y, z = 11, 3, 6
# x, y, z = 11, 6, 3
# x, y, z = 6, 11, 3
# x, y, z = 6, 3, 11
# x, y, z = 3, 6, 11
# x, y, z = 3, 11, 6
# просто раскоментировать нужную строку и проверить свой код

x, y, z = 3, 5, 6

if x <= A and y <= B:
    print('Размеры -', x, 'на', y, 'на', z, '- ДА')
elif y <= A and x <= B:
    print('Размеры -', x, 'на', y, 'на', z, '- ДА')
elif y <= A and z <= B:
    print('Размеры -', x, 'на', y, 'на', z, '- ДА')
elif z <= A and y <= B:
    print('Размеры -', x, 'на', y, 'на', z, '- ДА')
elif z <= A and x <= B:
    print('Размеры -', x, 'на', y, 'на', z, '- ДА')
elif x <= A and z <= B:
    print('Размеры -', x, 'на', y, 'на', z, '- ДА')
else:
    print('Размеры -', x, 'на', y, 'на', z, '- НЕТ')


# зачет!
