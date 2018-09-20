from time import sleep
from skynet import try_number, get_ganados, init_ganados
from bulls_and_cows import check_numbers, init_number
from termcolor import cprint, colored

rounds_count = 0
hidden_number = init_number()

cprint("** Добро пожаловать в игру \"Быки и коровы\"!", "green", "on_grey", attrs=["bold"])
cprint("** Компьютер играет сам с собой!", "green", "on_grey", attrs=["bold"])

init_ganados()

while True:
    rounds_count += 1
    attempt = try_number()
    check_result = check_numbers(hidden_number, attempt)
    get_ganados(check_result)
    print((colored("** Компьютер пробует число - ", "yellow", "on_grey", attrs=["bold"])), end="")
    print((colored(attempt, "yellow", "on_grey", attrs=["bold"])))
    sleep(0.1)
    if check_result["bulls"] == 4:
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
