import unittest

from parameterized import parameterized

from day_3_solution import character_to_priority, find_badge


class TestDay3(unittest.TestCase):
    @parameterized.expand([["a", 1], ["z", 26], ["A", 27], ["Z", 52]])
    def test_char_to_priority(self, character, expected_priority):
        self.assertEqual(character_to_priority(character), expected_priority)

    def test_find_badge(self):
        elf1 = "vJrwpWtwJgWrhcsFMMfFFhFp"
        elf2 = "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"
        elf3 = "PmmdzqPrVvPwwTWBwg"

        self.assertEqual(find_badge(elf1, elf2, elf3), "r")


if __name__ == "__main__":
    unittest.main()
