import unittest
from lesson_014.bowling import Game


class GameFrame(unittest.TestCase):

    def setUp(self):
        # correct games
        self.g1 = Game('X4/34-4X2-1/XX4/34-4')

        # incorrect games
        self.g2 = Game('1X4/34-4X2-1/XX4/34-4')
