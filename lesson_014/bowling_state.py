import logging


class FrameState(object):
    """State of the frame.
    Options:
    Strike - all pins are knocked down by the first throw,
    StartRegular - the pins are partially knocked down by the first throw,
    EndRegular - the pins are not completely knocked down by the second throw (open frame),
    Spare - the pins are completely knocked down by the second throw.

    Attributes:
    name - title of state
    roll - represents number of roll
    frame - equality to 1 means the beginning of a new frame
    allowed - names of states that are allowed to switch from the current state
    next_increase - multiplier that determines how many points will be added for the next roll
    second_increase - multiplier that determines how many points will be added after one roll
    """

    name = "state"
    roll = 1
    frame = 0
    allowed = ['strike', 'start_regular']
    next_increase = 0
    second_increase = 0

    # switch state if it is valid
    def switch(self, state):
        if state.name in self.allowed:
            # print('Current:', self, ' => switched to new state', state.name)
            self.__class__ = state
        else:
            raise BadFrameError('Incorrect result recording - invalid frame state switch attempt:\n'
                                f'from {self.name} -> to {state.name}')

    def __str__(self):
        return self.name


class Strike(FrameState):
    name = 'strike'
    frame = 1
    allowed = ['start_regular', 'strike']
    next_increase = 1
    second_increase = 1


class Spare(FrameState):
    name = 'spare'
    roll = 2
    allowed = ['start_regular', 'strike']
    next_increase = 1


class StartRegular(FrameState):
    name = 'start_regular'
    frame = 1
    allowed = ['end_regular', 'spare']


class EndRegular(FrameState):
    name = 'end_regular'
    roll = 2
    allowed = ['start_regular', 'strike']


class Frame(object):
    """Represents bowling frame.
    Stores the number of points at the current moment of the game, depending on the multipliers
    and the state.

    Attributes:
    state - state of frame
    number_of_frame - to count frames
    number_of_roll - to know number of roll
    points - points for frame with current multipliers
    frame_points - points for frame without multipliers
    roll_points - points for roll

    next_increase in Frame class summarizes after each change of state, and second_increase shifts
    to next_increase one roll after strike:
    next_increase - multiplier that determines how many points will be added for the next roll
    second_increase - multiplier that determines how many points will be added after one roll
    """

    def __init__(self):
        self.state = FrameState()
        self.number_of_frame = 0
        self.number_of_roll = 1
        self.points = 0
        self.frame_points = 0
        self.roll_points = 0
        self.next_increase = 0
        self.second_increase = 0

    def switch_state(self, char):
        if char == 'X':
            self.change(Strike, char)
        elif char == '/':
            self.change(Spare, char)
        elif char in '-123456789':
            if isinstance(self.state, StartRegular):
                self.change(EndRegular, char)
            else:
                self.change(StartRegular, char)
        else:
            raise BadFrameError(f'Invalid char to evaluate: {char}')
        self.number_of_roll = self.state.roll
        self.number_of_frame += self.state.frame

    def change(self, state, char):
        self.state.switch(state)
        self.eval_points_for_roll(char)
        self.next_increase += self.state.next_increase
        self.second_increase += self.state.second_increase

    def eval_points_for_roll(self, char):
        self.state_points(char=char)
        self.points = self.frame_points
        if self.next_increase:
            self.points += self.roll_points * self.next_increase
            self.next_increase = self.second_increase
        if self.second_increase:
            self.second_increase -= 1

    def state_points(self, char):

        if self.state.name == 'strike':
            self.roll_points = self.frame_points = 10

        elif self.state.name == 'spare':
            self.frame_points = 10
            self.roll_points = 10 - self.roll_points

        elif self.state.name == 'start_regular':
            self.roll_points = int(char) if char.isdigit() else 0
            self.frame_points = 0

        else:
            self.frame_points = self.roll_points
            self.roll_points = int(char) if char.isdigit() else 0
            self.frame_points += self.roll_points
            if self.frame_points > 10:
                raise BadFrameError("Incorrect result recording - no more than 10 pins can be "
                                    "knocked down")
            elif self.frame_points == 10:
                raise BadFrameError("Incorrect result recording - 10 pins per frame should be "
                                    "marked as spare '/'")


class BadFrameError(Exception):
    pass


class BadGameError(Exception):
    pass


class Game:
    score = 0
    frames_amount = 0

    def __init__(self, result_line, cons_print=False):
        self.result_line = result_line
        self.cons_print = cons_print

    def get_score(self):
        frame = Frame()
        self.run_frame_calculation(frame)
        result = f'Game result: {self.result_line} ::: {self.score} points!\n'
        played = f'{frame.number_of_frame} frame{"s" if frame.number_of_frame > 1 else ""} played'
        left = ''
        if frame.number_of_frame < 10:
            left = f', {10 - frame.number_of_frame} frame{"s" if frame.number_of_frame < 9 else ""} left!'
        self.frames_amount = frame.number_of_frame
        message = f'{result}{played}{left}'

        if self.cons_print:
            print(message)
        logging.info(message)

    def run_frame_calculation(self, frame):
        for char in self.result_line:
            frame.switch_state(char)
            if frame.number_of_frame > 10:
                raise BadGameError("Incorrect number of frames in line: you can't play more than 10 frames!")
            self.score += frame.points
            message = (f'Number of frame: {frame.number_of_frame}, roll {frame.number_of_roll}\n'
                       f'Points for roll: {frame.points} | Game points: {self.score}')

            if self.cons_print:
                print(message)
            logging.info(message)


if __name__ == "__main__":
    game = Game('XXX347/21', True)
    game1 = Game('X4/34', True)
    game2 = Game('X4/34-4X2-1/XX4/', True)
    game3 = Game('X4/34-4X2-1/X', True)
    game4 = Game('X--X--X--X----X', True)
    game5 = Game('X46-/X---/X-/X', True)

    # game.get_score()
    # game1.get_score()
    # game2.get_score()
    # game3.get_score()
    # game4.get_score()
    game5.get_score()
