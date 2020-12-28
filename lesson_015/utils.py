from termcolor import colored


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