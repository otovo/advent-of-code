from dataclasses import dataclass
from itertools import zip_longest
from functools import cmp_to_key


@dataclass
class Pair:
    index: int
    left: list
    right: list


def read_input(filename: str) -> list[Pair]:
    with open(filename, "r") as fp:
        lines = fp.readlines()

    pairs = []
    for pair_idx, i in enumerate(range(0, len(lines), 3), start=1):
        left = eval(lines[i].strip())
        right = eval(lines[i + 1].strip())
        pairs.append(Pair(index=pair_idx, left=left, right=right))

    return pairs


def compare(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0

    elif isinstance(left, list) and isinstance(right, list):
        for item_left, item_right in zip_longest(left, right):
            if item_left is None:
                return -1  # left list runs out first
            if item_right is None:
                return 1  # right list runs out first

            res = compare(item_left, item_right)
            if res < 0:
                return -1
            elif res > 0:
                return 1
        return 0

    elif isinstance(left, int) and (list, right):
        return compare([left], right)

    else:
        return compare(left, [right])


def find_indicies_of_right_order_packages(pairs: list[Pair]) -> list[int]:
    correct_indices = []

    for pair in pairs:
        if compare(pair.left, pair.right) < 0:
            correct_indices.append(pair.index)

    return correct_indices


def find_decoder_key(pairs) -> int:
    first_divider_package = [[2]]
    second_divider_package = [[6]]
    packets = []
    for pair in pairs:
        packets.append(pair.left)
        packets.append(pair.right)
    packets.append(first_divider_package)
    packets.append(second_divider_package)

    sorted_packets = sorted(packets, key=cmp_to_key(compare))

    index_of_first_divider_package = sorted_packets.index(first_divider_package)
    index_of_second_divider_package = sorted_packets.index(second_divider_package)

    return (index_of_first_divider_package + 1) * (index_of_second_divider_package + 1)


if __name__ == "__main__":
    pairs = read_input("input.txt")
    indices_of_right_order_packages = find_indicies_of_right_order_packages(pairs)
    print(f"Solution part 1: {sum(indices_of_right_order_packages)}")

    print(f"Solution part 2: {find_decoder_key(pairs)}")
