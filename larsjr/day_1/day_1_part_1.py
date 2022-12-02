from __future__ import annotations
from collections import defaultdict


def get_calories_by_elf(input_file: str) -> dict[int, int]:
    elfs_and_calories: dict[int, int] = defaultdict(int)

    with open(input_file, "r") as fp:
        lines = fp.readlines()

    elf_index = 0
    for line in lines:
        if len(line.strip()) == 0:
            elf_index += 1
            continue

        elfs_and_calories[elf_index] += int(line.strip())

    return elfs_and_calories


if __name__ == "__main__":

    elfs_and_calories = get_calories_by_elf("elfs_and_calories.txt")

    print(max(elfs_and_calories.values()))
