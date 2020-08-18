import logging


class Frame(object):
    valid_symbols = '123456789-/X'

    def __init__(self, frame_line):
        self.frame_line = frame_line
        self.points = 0

    def __str__(self):
        return self.frame_line

    def eval_frame(self):
        self.validate_frame()
        if self.frame_line.startswith('X'):
            self.points += 20
        elif self.frame_line.endswith('/'):
            self.points += 15
        elif '-' in self.frame_line:
            fr_copy = self.frame_line.replace('-', '')
            self.points += len(fr_copy) and int(fr_copy) or len(fr_copy)
        elif self.frame_line.isdigit():
            points = sum((int(x) for x in self.frame_line))
            if points <= 9:
                self.points += points
            else:
                raise Exception(f'{points} - incorrect frame score')

    def validate_frame(self):
        # Проверка фрейма на валидность символов
        validity = {x: x in self.valid_symbols for x in self.frame_line}
        if not all(validity.values()):
            raise BadFrameError(
                f'Invalid characters in frame: {", ".join([char for char in validity if not validity[char]])}')
        if self.frame_line.startswith('/'):
            raise BadFrameError('A frame cannot start with "/"')
        if self.frame_line.endswith('X'):
            raise BadFrameError('A frame cannot ends with "X"')


class Game(object):

    def __init__(self, game_result):
        self.score = 0
        self.frames_amount = 0
        self.pairs = []
        self.game_result = game_result
        self._game_result = ''

    def get_score(self):
        self._game_result = self.game_result.replace('X', 'X-')
        if len(self._game_result) % 2:
            raise Exception('Incorrect frame sequence')
        self.eval_pairs()
        frames = (Frame(frame_line) for frame_line in self.pairs)
        for frame in frames:
            frame.eval_frame()
            self.score += frame.points
        message = f'Game result: {self.game_result} ::: {self.score} points!'
        print(message)
        logging.info(message)

    def eval_pairs(self):
        v_pairs = [self._game_result[i: i + 2] for i in range(0, len(self._game_result) - 1, 2)]
        self.pairs.extend(v_pairs)
        logging.debug(str(self.pairs))
        self.frames_amount += len(self.pairs)
        if self.frames_amount > 10:
            raise Exception("Incorrect number of frames in line: you can't play more than 10 frames!")
        played = f'{self.frames_amount} frame{"s" if self.frames_amount > 1 else ""} played'
        left = ''
        if self.frames_amount < 10:
            left = f', {10 - self.frames_amount} frame{"s" if self.frames_amount < 9 else ""} left!'
        message = f'{played}{left}'
        print(message)
        logging.info(message)


class BadFrameError(Exception):
    pass


if __name__ == '__main__':
    game1 = Game('X4/34-4X2-1/XX4/')
    game2 = Game('X4/34-4X2-1/X')
    game3 = Game('X--X--X--X----X')
    game4 = Game('X---/X---/X-/X')
    game5 = Game('aX')

    game1.get_score()
    game2.get_score()
    game3.get_score()
    game4.get_score()
    try:
        game5.get_score()
    except Exception as exc:
        logging.exception(exc)
