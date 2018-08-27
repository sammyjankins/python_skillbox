from random import randint


# загадать число
def init_number():
    output = set()
    while len(output) != 4:
        output.add(str(randint(0, 9)))
    output = list(output)
    if output[0] == '0':  # TODO проверка была на равенство числу 0, а надо было на равенство символу >_<
        output[0], output[1] = output[1], output[0]
    return output


# проверить число
def check_numbers(game_num, user_num):
    ganados = {"bulls": 0, "cows": 0}
    for i, num in enumerate(user_num):
        if num == game_num[i]:
            ganados["bulls"] += 1
        elif num in game_num:
            ganados["cows"] += 1
    return ganados
