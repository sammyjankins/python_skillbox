# -*- coding: utf-8 -*-

# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...


import room_1
import room_2


def print_roommates(module):
    print("В комнате", module.__name__, "живут:", end=" ")
    for i, mate in enumerate(module.folks):
        if i + 1 < len(module.folks):
            print(mate, end=", "),
        else:
            print(mate, end="\n")


print_roommates(room_1)
print_roommates(room_2)
