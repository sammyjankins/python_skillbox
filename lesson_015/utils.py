import csv
from datetime import datetime, time

from termcolor import colored, cprint


def user_input_handling(message, actions):
    while True:
        try:
            answer = int(input(colored(message, 'yellow')))
            if 1 <= answer <= actions:
                return answer
            else:
                print(colored(f'You must enter digits from 1 to {actions}', 'red'))
                continue
        except ValueError:
            print(colored(f'You must enter digits from 1 to {actions}', 'red'))


def game_to_csv(save_path):
    def decorator(method):
        _progress = []

        def wrapper(self):
            _progress.append({'current_location': self.current_location,
                              'current_experience': self.player.exp,
                              'current_date': datetime.today()})

            passed_delta = datetime.today() - _progress[0]['current_date']
            minutes, seconds = divmod(passed_delta.seconds, 60)
            passed_time = time(minute=minutes, second=seconds)
            cprint(f'Прошло времени: {passed_time.strftime("%M:%S")}', color='green')

            method(self)

            if self.over:
                with open(save_path, 'w', newline='') as out_csv:
                    writer = csv.DictWriter(out_csv, delimiter=',', fieldnames=list(_progress[0].keys()))
                    writer.writeheader()
                    writer.writerows(_progress)

        return wrapper

    return decorator
