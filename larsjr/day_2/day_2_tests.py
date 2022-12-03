import unittest
from parameterized import parameterized


from day_2_solution import (
    Move,
    Outcome,
    points_part_1,
    points_from_move,
    outcome_of_round,
    get_correct_move,
)


class TestDay2(unittest.TestCase):
    def test_points_from_move_rock(self):
        self.assertEqual(1, points_from_move(Move.ROCK))

    def test_points_from_move_paper(self):
        self.assertEqual(2, points_from_move(Move.PAPER))

    def test_points_from_move_scissors(self):
        self.assertEqual(3, points_from_move(Move.SCISSORS))

    @parameterized.expand(
        [
            [Move.ROCK, Move.ROCK, Outcome.DRAW],
            [Move.PAPER, Move.PAPER, Outcome.DRAW],
            [Move.SCISSORS, Move.SCISSORS, Outcome.DRAW],
            [Move.ROCK, Move.PAPER, Outcome.WIN],
            [Move.ROCK, Move.SCISSORS, Outcome.LOSS],
            [Move.PAPER, Move.ROCK, Outcome.LOSS],
            [Move.PAPER, Move.SCISSORS, Outcome.WIN],
            [Move.SCISSORS, Move.ROCK, Outcome.WIN],
            [Move.SCISSORS, Move.PAPER, Outcome.LOSS],
        ]
    )
    def test_outcome_of_round(self, opponent_move, your_move, expected):
        self.assertEqual(outcome_of_round(opponent_move, your_move), expected)

    @parameterized.expand(
        [
            [Move.ROCK, Move.ROCK, 1 + 3],
            [Move.PAPER, Move.ROCK, 1 + 0],
            [Move.SCISSORS, Move.ROCK, 1 + 6],
        ]
    )
    def test_points_from_round(self, opponent_move, your_move, expected):
        self.assertEqual(points_part_1(opponent_move, your_move), expected)

    @parameterized.expand(
        [
            [Move.ROCK, Outcome.DRAW, Move.ROCK],
            [Move.ROCK, Outcome.LOSS, Move.SCISSORS],
            [Move.ROCK, Outcome.WIN, Move.PAPER],
            [Move.PAPER, Outcome.DRAW, Move.PAPER],
            [Move.PAPER, Outcome.LOSS, Move.ROCK],
            [Move.PAPER, Outcome.WIN, Move.SCISSORS],
            [Move.SCISSORS, Outcome.DRAW, Move.SCISSORS],
            [Move.SCISSORS, Outcome.LOSS, Move.PAPER],
            [Move.SCISSORS, Outcome.WIN, Move.ROCK],
        ]
    )
    def test_get_correct_move(self, opponent_move, desired_outcome, expected_move):
        self.assertEqual(
            get_correct_move(opponent_move, desired_outcome), expected_move
        )


if __name__ == "__main__":
    unittest.main()
