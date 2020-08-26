import unittest
from lesson_014.bowling import Game


class GameFrame(unittest.TestCase):

    def setUp(self):
        # correct games
        self.game1 = Game('X4/34-4X2-1/XX4/')
        self.game2 = Game('X4/34-4X2-1/X')
        self.game3 = Game('X--X--X--X----X')
        self.game4 = Game('X')
        self.game5 = Game('--')

        # incorrect games
        self.bad_game_1 = Game('123456789/X--')
        self.bad_game_2 = Game('X4/34-4X2-1/XX4/34-4')
        self.bad_game_3 = Game('X4934-4X2-1/XX')
        self.incorrect_sequence = Game('1X4/34-4X2-1/XX4/')

    def test_game1(self):
        self.game1.get_score()
        self.assertEqual(self.game1.frames_amount, 10)
        self.assertEqual(self.game1.score, 138)

    def test_game2(self):
        self.game2.get_score()
        self.assertEqual(self.game2.frames_amount, 8)
        self.assertEqual(self.game2.score, 103)

    def test_game3(self):
        self.game3.get_score()
        self.assertEqual(self.game3.frames_amount, 10)
        self.assertEqual(self.game3.score, 100)

    def test_game4(self):
        self.game4.get_score()
        self.assertEqual(self.game4.frames_amount, 1)
        self.assertEqual(self.game4.score, 20)

    def test_game5(self):
        self.game5.get_score()
        self.assertEqual(self.game5.frames_amount, 1)
        self.assertEqual(self.game5.score, 0)

    def test_bad_game1(self):
        with self.assertRaises(Exception):  # TODO: какое именно исключение выстрелит знать также важно
            self.bad_game_1.get_score()

    def test_bad_game2(self):
        with self.assertRaises(Exception):
            self.bad_game_2.get_score()

    def test_bad_game3(self):
        with self.assertRaises(Exception):
            self.bad_game_3.get_score()

    def test_incorrect_sequence(self):
        with self.assertRaises(Exception):
            self.incorrect_sequence.get_score()


if __name__ == '__main__':
    unittest.main()
