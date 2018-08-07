from time import sleep
from skynet import try_number, get_ganados
from bulls_and_cows import check_numbers, init_number
from termcolor import cprint, colored

rounds_count = 0
hidden_number = init_number()

# создание списка вариантов
get_ganados()

cprint("** Добро пожаловать в игру \"Быки и коровы\"!", "green", "on_grey", attrs=["bold"])
cprint("** Компьютер играет сам с собой!", "green", "on_grey", attrs=["bold"])

while True:
    rounds_count += 1
    attempt = try_number()
    check_result = check_numbers(hidden_number, attempt)
    check_sum = check_result["bulls"] + check_result["cows"]
    get_ganados(check_result)
    print((colored("** Компьютер пробует число - ", "yellow", "on_grey", attrs=["bold"])), end="")
    print((colored(attempt, "yellow", "on_grey", attrs=["bold"])))
    sleep(1)
    if check_result["bulls"] is 4:
        cprint("** Это победа!", "green", "on_grey", attrs=["bold"])
        print((colored("** Количество ходов - ", "green", "on_grey", attrs=["bold"])), end="")
        print((colored(rounds_count, "green", "on_grey", attrs=["bold"])))
        break
    else:
        print((colored("** Быки - ", "yellow", "on_grey", attrs=["bold"])), end="")
        print((colored(check_result["bulls"], "yellow", "on_grey", attrs=["bold"])))
        print((colored("** Коровы - ", "yellow", "on_grey", attrs=["bold"])), end="")
        print((colored(check_result["cows"], "yellow", "on_grey", attrs=["bold"])))
    sleep(1)
