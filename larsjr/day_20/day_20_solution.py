import itertools
from dataclasses import dataclass


class IdentifierNotFound(Exception):
    pass


@dataclass
class Number:
    value: int
    identifier: int


def read_input(filename: str) -> list[Number]:
    numbers = []
    with open(filename) as fp:
        lines = fp.readlines()

    for i, line in enumerate(lines):
        numbers.append(Number(value=int(line.strip()), identifier=i))

    return numbers


def find_number_with_identifier(
    number_for_index: dict[int, Number], identifier: int
) -> tuple[int, Number]:
    for index, number in number_for_index.items():
        if number.identifier == identifier:
            return index, number
    raise IdentifierNotFound(identifier)


def calculate_new_index(
    current_index: int, current_value: int, length_of_numbers: int
) -> int:

    if abs(current_value) >= length_of_numbers:
        direction_to_move = int(current_value / abs(current_value))  # either -1 or 1
        # When moving the number, the number itself should be removed from the
        # list, so we work on a list that is length_of_numbers - 1 long
        current_value = (
            abs(current_value) % (length_of_numbers - 1)
        ) * direction_to_move

    new_index = current_index + current_value

    if new_index == 0:
        new_index = length_of_numbers - 1  # wrap around
    elif new_index == length_of_numbers - 1:
        new_index = 0  # wrap around

    if new_index < 0:
        new_index = (length_of_numbers - 1) + new_index

    if new_index >= length_of_numbers:
        new_index = (new_index - length_of_numbers) + 1

    return new_index


def to_list(number_for_index: dict[int, Number]) -> list[Number]:
    mixed_numbers = []
    for i in range(len(number_for_index)):
        mixed_numbers.append(number_for_index[i])

    return mixed_numbers


def mix(numbers: list[Number]) -> list[Number]:
    number_for_index = {i: n for i, n in enumerate(numbers)}

    for i in range(len(number_for_index)):
        index_of_number_to_move, number_to_move = find_number_with_identifier(
            number_for_index, i
        )

        new_index = calculate_new_index(
            index_of_number_to_move, number_to_move.value, len(number_for_index)
        )

        if new_index > index_of_number_to_move:
            for i in range(index_of_number_to_move + 1, new_index + 1):
                number_for_index[i - 1] = number_for_index[i]
        elif new_index < index_of_number_to_move:
            for i in range(index_of_number_to_move, max(new_index - 1, 1), -1):
                number_for_index[i] = number_for_index[i - 1]

        number_for_index[new_index] = number_to_move

    return to_list(number_for_index)


def find_nth_numbers_after_zero(numbers: list[int], iterations: list[int]) -> list[int]:
    counter = 0
    found_zero = False
    numbers_at_iterations = []
    for n in itertools.cycle(numbers):
        if found_zero:
            counter += 1

        if n == 0:
            found_zero = True

        if counter in iterations:
            numbers_at_iterations.append(n)

        if len(numbers_at_iterations) == len(iterations):
            break

    return numbers_at_iterations


if __name__ == "__main__":
    numbers = read_input("input.txt")
    mixed_numbers = mix(numbers)
    coordinate_elements = find_nth_numbers_after_zero(
        [n.value for n in mixed_numbers], [1000, 2000, 3000]
    )
    print(sum(coordinate_elements))
