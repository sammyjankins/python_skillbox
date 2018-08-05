from random import randint


# загадать число
def init_number():
    output = set()
    while len(output) != 4:
        output.add(str(randint(0, 9)))
    output = list(output)
    while output[0] == 0:
        output.insert(0, output.pop())
    return "".join(output)


# проверить число
def check_numbers(game_num, user_num):
    ganados = {"bulls": 0, "cows": 0}
    for i, num in enumerate(user_num):
        if num is game_num[i]:
            ganados["bulls"] += 1
        elif game_num.find(num) is not -1:
            ganados["cows"] += 1
    return ganados
