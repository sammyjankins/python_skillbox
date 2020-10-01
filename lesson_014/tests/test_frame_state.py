import unittest
from lesson_014.bowling_state import Frame, BadFrameError


class TestFrame(unittest.TestCase):

    def setUp(self):
        self.frame = Frame()

    # correct single frames
    def test_strike(self):
        self.frame.switch_state('X')
        self.assertEqual(self.frame.points, 10)
        self.assertEqual(self.frame.frame_points, 10)
        self.assertEqual(self.frame.roll_points, 10)
        self.assertEqual(self.frame.state.name, 'strike')

    def test_start_regular(self):
        self.frame.switch_state('4')
        self.assertEqual(self.frame.points, 0)
        self.assertEqual(self.frame.frame_points, 0)
        self.assertEqual(self.frame.roll_points, 4)
        self.assertEqual(self.frame.state.name, 'start_regular')

    def test_spare(self):
        spare_sequence = '1/'
        for char in spare_sequence:
            self.frame.switch_state(char)
        self.assertEqual(self.frame.points, 10)
        self.assertEqual(self.frame.frame_points, 10)
        self.assertEqual(self.frame.roll_points, 9)
        self.assertEqual(self.frame.state.name, 'spare')

    def test_dash_frame(self):
        spare_sequence = '--'
        for char in spare_sequence:
            self.frame.switch_state(char)
        self.assertEqual(self.frame.points, 0)
        self.assertEqual(self.frame.frame_points, 0)
        self.assertEqual(self.frame.roll_points, 0)
        self.assertEqual(self.frame.state.name, 'end_regular')

    def test_end_regular(self):
        spare_sequence = '35'
        for char in spare_sequence:
            self.frame.switch_state(char)
        self.assertEqual(self.frame.points, 8)
        self.assertEqual(self.frame.frame_points, 8)
        self.assertEqual(self.frame.roll_points, 5)
        self.assertEqual(self.frame.state.name, 'end_regular')

    def test_dash_end_frame(self):
        spare_sequence = '-5'
        for char in spare_sequence:
            self.frame.switch_state(char)
        self.assertEqual(self.frame.points, 5)
        self.assertEqual(self.frame.frame_points, 5)
        self.assertEqual(self.frame.roll_points, 5)
        self.assertEqual(self.frame.state.name, 'end_regular')

    def test_start_dash_frame(self):
        spare_sequence = '7-'
        for char in spare_sequence:
            self.frame.switch_state(char)
        self.assertEqual(self.frame.points, 7)
        self.assertEqual(self.frame.frame_points, 7)
        self.assertEqual(self.frame.roll_points, 0)
        self.assertEqual(self.frame.state.name, 'end_regular')

    # incorrect frames
    def test_wrong_spare_1(self):
        spare_sequence = '/'
        with self.assertRaises(BadFrameError):
            for char in spare_sequence:
                self.frame.switch_state(char)

    def test_wrong_spare_2(self):
        spare_sequence = 'X/'
        with self.assertRaises(BadFrameError):
            for char in spare_sequence:
                self.frame.switch_state(char)

    def test_wrong_end_frame_1(self):
        spare_sequence = '-X'
        with self.assertRaises(BadFrameError):
            for char in spare_sequence:
                self.frame.switch_state(char)

    def test_wrong_end_frame_2(self):
        spare_sequence = '19'
        with self.assertRaises(BadFrameError):
            for char in spare_sequence:
                self.frame.switch_state(char)

    def test_wrong_end_frame_3(self):
        spare_sequence = '69'
        with self.assertRaises(BadFrameError):
            for char in spare_sequence:
                self.frame.switch_state(char)

    def test_wrong_char(self):
        spare_sequence = '-0'
        with self.assertRaises(BadFrameError):
            for char in spare_sequence:
                self.frame.switch_state(char)


if __name__ == '__main__':
    unittest.main()
