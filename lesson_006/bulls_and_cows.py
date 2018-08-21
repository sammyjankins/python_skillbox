from random import randint


# загадать число
def init_number():
    output = set()
    while len(output) != 4:
        output.add(str(randint(0, 9)))  # TODO: с сетом круто придумали
    output = list(output)
    while output[0] == 0:  # TODO: а зачем перебирать, если второй элемент точно не 0, если первый 0? Лучше просто их тогда свопнуть
        output.insert(0, output.pop())
    return "".join(output)  # TODO: да можно список оставить


# проверить число
def check_numbers(game_num, user_num):
    ganados = {"bulls": 0, "cows": 0}
    for i, num in enumerate(user_num):
        if num is game_num[i]:  # TODO: ==
            ganados["bulls"] += 1
        elif game_num.find(num) is not -1:  # TODO: num in game_num
            ganados["cows"] += 1
    return ganados
