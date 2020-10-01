import unittest
import logging

from lesson_014.eval_protocol import Protocol

logging.disable(level=logging.ERROR)


# тесты для реализации на паттерне "состояние"
class TestProtocol(unittest.TestCase):

    def setUp(self):
        filename = ''
        self.test_line_tour_1 = '### Tour 1'
        self.test_line_tour_2 = '### Tour 1'

        self.test_line_game_1 = 'Антон	1/6/1/--327-18812381'
        self.test_line_game_2 = 'Елена	3532X332/3/64--62X'
        self.test_line_game_3 = 'Татьяна	8/--35-47/371/518-4/'
        self.test_line_game_4 = 'Татьяна	42X--3/4/2-8171171/'
        self.test_line_game_5 = 'Антон	--36--4524636-71--31'
        self.test_line_game_6 = 'Давид	121/9/365/5/9/525326'

        self.test_line_winner = 'winner is .........'
        self.test_line_empty = ''

        self.protocol = Protocol(filename)

    def test_tour_title(self):
        self.protocol.process_line(self.test_line_tour_1)
        self.assertEqual(self.protocol.results[0], f'{self.test_line_tour_1}\n')

    def test_game(self):
        self.protocol.process_line(self.test_line_game_1)
        self.assertEqual(self.protocol.results[0], 'Антон     1/6/1/--327-18812381        81\n')
        self.assertEqual(self.protocol.winner[0], 'Антон')
        self.assertEqual(self.protocol.winner[1], 81)
        self.assertEqual(self.protocol.rate['Антон']['games'], 1)
        self.assertEqual(self.protocol.rate['Антон']['victories'], 0)

    def test_bad_game(self):
        self.protocol.process_line(self.test_line_game_2)
        self.assertEqual(self.protocol.results[0],
                         "Елена     3532X332/3/64--62X          Incorrect result recording - 10 pins per frame should be marked as spare '/'\n")
        self.assertEqual(self.protocol.winner[0], '')
        self.assertEqual(self.protocol.winner[1], 0)
        self.assertEqual(self.protocol.rate['Елена']['games'], 1)
        self.assertEqual(self.protocol.rate['Елена']['victories'], 0)

    def test_game_two_players(self):
        self.protocol.process_line(self.test_line_game_1)
        self.protocol.process_line(self.test_line_game_4)
        self.assertEqual(self.protocol.winner[0], 'Антон')
        self.assertEqual(self.protocol.winner[1], 81)
        self.assertEqual(self.protocol.rate['Антон']['games'], 1)
        self.assertEqual(self.protocol.rate['Антон']['victories'], 0)
        self.assertEqual(self.protocol.rate['Татьяна']['games'], 1)
        self.assertEqual(self.protocol.rate['Татьяна']['victories'], 0)

    def test_winner(self):
        self.protocol.process_line(self.test_line_game_1)
        self.protocol.process_line(self.test_line_game_4)
        self.protocol.process_line(self.test_line_winner)
        self.assertEqual(self.protocol.winner[0], '')
        self.assertEqual(self.protocol.winner[1], 0)
        self.assertEqual(self.protocol.rate['Антон']['games'], 1)
        self.assertEqual(self.protocol.rate['Антон']['victories'], 1)
        self.assertEqual(self.protocol.rate['Татьяна']['games'], 1)
        self.assertEqual(self.protocol.rate['Татьяна']['victories'], 0)

    def test_two_tours(self):
        tours = [
            self.test_line_tour_1,
            self.test_line_game_1,
            self.test_line_game_2,
            self.test_line_game_3,
            self.test_line_winner,
            self.test_line_empty,
            self.test_line_tour_2,
            self.test_line_game_4,
            self.test_line_game_5,
            self.test_line_game_6,
            self.test_line_winner,
            self.test_line_empty,
        ]

        for line in tours:
            self.protocol.process_line(line)
        self.assertEqual(self.protocol.rate['Антон']['games'], 2)
        self.assertEqual(self.protocol.rate['Антон']['victories'], 1)
        self.assertEqual(self.protocol.rate['Елена']['games'], 1)
        self.assertEqual(self.protocol.rate['Елена']['victories'], 0)
        self.assertEqual(self.protocol.rate['Татьяна']['games'], 2)
        self.assertEqual(self.protocol.rate['Татьяна']['victories'], 0)
        self.assertEqual(self.protocol.rate['Давид']['games'], 1)
        self.assertEqual(self.protocol.rate['Давид']['victories'], 1)
