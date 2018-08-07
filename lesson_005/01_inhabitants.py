# -*- coding: utf-8 -*-

# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...


import room_1
import room_2


def print_roommates(module):
    print("В комнате", module.__name__, "живут:", end=" ")
    print(", ".join(module.folks))

print_roommates(room_1)
print_roommates(room_2)

# зачет! 
