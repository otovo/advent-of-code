def character_to_priority(character: str):
    if character.isupper():
        return ord(character) - ord("A") + 27
    return ord(character) - ord("a") + 1


def find_common_character(compartment1: str, compartment2: str) -> str:
    return set(compartment1).intersection(set(compartment2)).pop()


def split_line(line: str) -> tuple[str, str]:
    line = line.strip()
    divide_index = int(len(line.strip()) / 2)

    compartment_1 = line[:divide_index]
    compartment_2 = line[divide_index:]

    return compartment_1, compartment_2


def find_badge(elf1: str, elf2: str, elf3: str) -> str:
    return set(elf1).intersection(elf2).intersection(elf3).pop()


def part1(lines: list[str]) -> None:
    priorities_sum = 0

    for line in lines:
        compartment_1, compartment_2 = split_line(line)
        common_character = find_common_character(compartment_1, compartment_2)
        priorities_sum += character_to_priority(common_character)

    print(f"Part one, sum of priorites: {priorities_sum}")


def part2(lines: list[str]) -> None:
    badge_priorites_sum = 0
    for i in range(0, len(lines), 3):
        elf1 = lines[i].strip()
        elf2 = lines[i + 1].strip()
        elf3 = lines[i + 2].strip()
        badge = find_badge(elf1, elf2, elf3)
        badge_priorites_sum += character_to_priority(badge)

    print(f"Part two, sum of badge priorites: {badge_priorites_sum}")


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        lines = fp.readlines()

    part1(lines)
    part2(lines)
