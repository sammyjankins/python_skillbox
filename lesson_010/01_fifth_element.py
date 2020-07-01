# -*- coding: utf-8 -*-

# Умножить константу BRUCE_WILLIS на пятый элемент строки, введенный пользователем

BRUCE_WILLIS = 42

input_data = None
while True:
    try:
        input_data = input('Если хочешь что-нибудь сделать, сделай это сам: ')
        leeloo = int(input_data[4])
        result = BRUCE_WILLIS * leeloo
    except ValueError:
        print(f"- Вы люди такие странные! '{input_data[4]}' - ведь не число!")
    except IndexError:
        print(f"- Я была рождена, чтобы считать до 5, а не до {len(input_data)}...")
    except Exception:
        print(f"- БАДА БУМ!")
    else:
        print(f"- Leeloo Dallas! Multi-pass № {result}!")
        break

# зачет!

# Ообернуть код и обработать исключительные ситуации для произвольных входных параметров
# - ValueError - невозможно преобразовать к числу
# - IndexError - выход за границы списка
# - остальные исключения
# для каждого типа исключений написать на консоль соотв. сообщение
