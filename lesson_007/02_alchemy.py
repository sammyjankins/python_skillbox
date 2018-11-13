# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())


class Water:

    def __str__(self):
        return 'Вода'

    def __add__(self, other):
        if isinstance(other, Air):
            return Storm(part1=self, part2=other)
        elif isinstance(other, Fire):
            return Steam(part1=self, part2=other)
        elif isinstance(other, Soil):
            return Dirt(part1=self, part2=other)
        elif isinstance(other, Wood):
            return Boat(part1=self, part2=other)
        else:
            return None


class Air:

    def __str__(self):
        return 'Воздух'

    def __add__(self, other):
        if isinstance(other, Water):
            return Storm(part1=self, part2=other)
        elif isinstance(other, Fire):
            return Lightning(part1=self, part2=other)
        elif isinstance(other, Soil):
            return Dust(part1=self, part2=other)
        elif isinstance(other, Wood):
            return Defoliation(part1=self, part2=other)
        else:
            return None


class Fire:

    def __str__(self):
        return 'Огонь'

    def __add__(self, other):
        if isinstance(other, Water):
            return Steam(part1=self, part2=other)
        elif isinstance(other, Air):
            return Lightning(part1=self, part2=other)
        elif isinstance(other, Soil):
            return Lava(part1=self, part2=other)
        elif isinstance(other, Wood):
            return Charcoal(part1=self, part2=other)
        else:
            return None


class Soil:

    def __str__(self):
        return 'Земля'

    def __add__(self, other):
        if isinstance(other, Water):
            return Dirt(part1=self, part2=other)
        elif isinstance(other, Air):
            return Dust(part1=self, part2=other)
        elif isinstance(other, Fire):
            return Lava(part1=self, part2=other)
        elif isinstance(other, Wood):
            return Forest(part1=self, part2=other)
        else:
            return None


class Wood:

    def __str__(self):
        return 'Дерево'

    def __add__(self, other):
        if isinstance(other, Water):
            return Boat(part1=self, part2=other)
        elif isinstance(other, Air):
            return Defoliation(part1=self, part2=other)
        elif isinstance(other, Fire):
            return Charcoal(part1=self, part2=other)
        elif isinstance(other, Soil):
            return Forest(part1=self, part2=other)
        else:
            return None


class Boat:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Лодка'


class Defoliation:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Листопад'


class Charcoal:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Уголь'


class Forest:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Лес'


class Storm:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Шторм'


class Steam:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Пар'


class Lightning:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Молния'


class Lava:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Лава'


class Dust:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Пыль'


class Dirt:

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return 'Грязь'


print(Water(), '+', Air(), '=', Water() + Air())
print(Water(), '+', Fire(), '=', Water() + Fire())
print(Water(), '+', Soil(), '=', Water() + Soil())
print(Fire(), '+', Air(), '=', Fire() + Air())
print(Soil(), '+', Air(), '=', Soil() + Air())
print(Fire(), '+', Soil(), '=', Fire() + Soil())
print('\n=============== Плюс дерево ===============\n')
print(Water(), '+', Wood(), '=', Water() + Wood())
print(Fire(), '+', Wood(), '=', Fire() + Wood())
print(Soil(), '+', Wood(), '=', Soil() + Wood())
print(Wood(), '+', Air(), '=', Wood() + Air())

# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
# зачет!