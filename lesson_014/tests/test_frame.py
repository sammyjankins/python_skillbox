import unittest
from lesson_014.bowling import Frame, BadFrameError


class TestFrame(unittest.TestCase):

    def setUp(self):
        # correct frames
        self.strike = Frame('X-')
        self.dash_spare = Frame('-/')
        self.number_spare = Frame('5/')
        self.dash_frame = Frame('--')
        self.dash_number = Frame('-7')
        self.number_dash = Frame('8-')
        self.two_numbers = Frame('52')

        # incorrect frames
        self.bad_strike = Frame('-X')
        self.bad_dash_spare = Frame('/-')
        self.bad_number_spare = Frame('/9')
        self.bad_two_numbers = Frame('55')
        self.incorrect_char_frame = Frame('-0')

    def test_strike(self):
        self.strike.eval_frame()
        self.assertEqual(self.strike.points, 20)

    def test_dash_spare(self):
        self.dash_spare.eval_frame()
        self.assertEqual(self.dash_spare.points, 15)

    def test_number_spare(self):
        self.number_spare.eval_frame()
        self.assertEqual(self.number_spare.points, 15)

    def test_dash_frame(self):
        self.dash_frame.eval_frame()
        self.assertEqual(self.dash_frame.points, 0)

    def test_dash_number(self):
        self.dash_number.eval_frame()
        self.assertEqual(self.dash_number.points, 7)

    def test_number_dash(self):
        self.number_dash.eval_frame()
        self.assertEqual(self.number_dash.points, 8)

    def test_two_numbers(self):
        self.two_numbers.eval_frame()
        self.assertEqual(self.two_numbers.points, 7)

    def test_bad_strike(self):
        with self.assertRaises(BadFrameError):
            self.bad_strike.eval_frame()

    def test_bad_dash_spare(self):
        with self.assertRaises(BadFrameError):
            self.bad_dash_spare.eval_frame()

    def test_bad_number_spare(self):
        with self.assertRaises(BadFrameError):
            self.bad_number_spare.eval_frame()

    def test_bad_two_numbers(self):
        with self.assertRaises(BadFrameError):
            self.bad_two_numbers.eval_frame()

    def test_incorrect_char_frame(self):
        with self.assertRaises(BadFrameError):
            self.incorrect_char_frame.eval_frame()


if __name__ == '__main__':
    unittest.main()
