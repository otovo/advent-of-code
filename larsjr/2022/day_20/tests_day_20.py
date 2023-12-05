import unittest
from day_20_solution import calculate_new_index


class NewIndexTests(unittest.TestCase):
    def test_calculate_new_index_positive_no_wrap(self):
        new_index = calculate_new_index(0, 2, 8)
        self.assertEqual(2, new_index)

    def test_calculate_new_index_negative_no_wrap(self):
        new_index = calculate_new_index(3, -2, 7)
        self.assertEqual(1, new_index)

    def test_calculate_new_index_negative_ends_up_on_first_position_should_wrap(self):
        new_index = calculate_new_index(2, -2, 7)
        self.assertEqual(6, new_index)

    def test_calculate_new_index_postive_ends_up_on_last_position_should_wrap(self):
        # [1, 2, 3, -2, -3, 0, 4]
        new_index = calculate_new_index(4, 2, 7)
        self.assertEqual(0, new_index)

    def test_calculate_new_index_negative_wraps_around(self):
        # [1, -3, 2, 3, -2, 0, 4
        new_index = calculate_new_index(1, -3, 7)
        self.assertEqual(4, new_index)

    def test_calculate_new_index_positive_wraps_around(self):
        # [1, 2, -3, 0, 3, *4*, -2] should become
        # [1, 2, -3, 4, 0, 3, -2]
        new_index = calculate_new_index(5, 4, 7)
        self.assertEqual(3, new_index)

    def test_calculate_new_index_negative_wraps_multiple(self):
        # [*-8*, 0, 1 ,2, 3] should become
        # [0, 1, 2, 3, -8]
        new_index = calculate_new_index(0, -8, 5)
        self.assertEqual(4, new_index)

    def test_calculate_new_index_negative_same_as_length_of_numbers(self):
        # [*-5*, 0, 1, 2, 3] should become ?
        # [0, 1, 2, *-5*,  3]
        new_index = calculate_new_index(0, -5, 5)
        self.assertEqual(3, new_index)

    def test_calculate_new_index_negative(self):
        # [0, *-8*, 1, 2, 3] -> [0, *-8*, 1, 2, 3]
        # [0, *-9*, 1, 2, 3] -> [0, 1, 2, 3, *-9*]
        new_index_1 = calculate_new_index(1, -8, 5)
        self.assertEqual(1, new_index_1)

        new_index_2 = calculate_new_index(1, -9, 5)
        self.assertEqual(4, new_index_2)


if __name__ == "__main__":
    unittest.main()
