from collections import defaultdict
from pprint import pprint

from bowling import Game, BadFrameError, BadGameError


class Protocol:

    def __init__(self, filename):
        self.filename = filename
        self.tour = 0
        self.results = []
        self.winner = ['', 0]
        self.rate = defaultdict(lambda: {'games': 0, 'victories': 0})

    def run(self):
        with open(self.filename, mode='r', encoding='utf8') as file:
            lines = [line[:-1] for line in file]
            for line in lines:
                self.process_line(line)

    def process_line(self, line):
        if line.startswith('winner'):
            if not self.winner[0]:
                return
            self.results.append(f'winner is {self.winner[0]}\n')
            self.rate[self.winner[0]]['victories'] += 1
            self.winner = ['', 0]
        elif line and '#' not in line:
            line = line.split()
            player, result = line
            self.rate[player]['games'] += 1
            try:
                game = Game(result)
                game.get_score()
                score = game.score
                self.results.append(f'{player:10}{result:28}{score}\n')
                if score > self.winner[1]:
                    self.winner = [player, score]
            except (BadFrameError, BadGameError) as exc:
                self.results.append(f'{player:10}{result:28}{exc}\n')
        else:
            self.results.append(f'{line}\n')


if __name__ == '__main__':
    prot = Protocol('tournament.txt')
    prot.run()
    pprint(prot.results)
