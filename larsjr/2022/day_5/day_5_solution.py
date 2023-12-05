from dataclasses import dataclass
from collections import defaultdict
import re
import copy


@dataclass
class Command:
    move_from: int
    move_to: int
    number_to_move: int


def read_crate_line(line: str, stacks: defaultdict[int, list]):
    # a create can start every fourth character
    for stack_index, index in enumerate(range(0, len(line), 4), start=1):
        if line[index] != " ":
            # crates.append((stack, lines[0][index+1]))
            stacks[stack_index].insert(0, line[index + 1])


def read_move_line(line: str, commands: list[Command]):
    pattern = r"move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)"
    match = re.match(pattern, line)
    commands.append(
        Command(
            number_to_move=int(match.group(1)),
            move_from=int(match.group(2)),
            move_to=int(match.group(3)),
        )
    )


def read_input(filename: str):
    with open(filename, "r") as fp:
        lines = fp.readlines()

    stacks: defaultdict[int, list] = defaultdict(list)
    commands: list[Command] = []

    for line in lines:
        if len(line) <= 1:
            continue

        elif line.startswith("move"):
            read_move_line(line, commands)
        elif line[1].isdigit():
            continue
        else:
            read_crate_line(line, stacks)

    return stacks, commands


def organize_crates_9000(
    stacks: defaultdict[int, list], commands: list[Command]
) -> defaultdict[int, list]:
    for command in commands:
        for _ in range(command.number_to_move):
            crate_to_move = stacks[command.move_from].pop()
            stacks[command.move_to].append(crate_to_move)

    return stacks


def organize_crates_9001(
    stacks: defaultdict[int, list], commands: list[Command]
) -> defaultdict[int, list]:
    for command in commands:
        crates_to_move = []
        for _ in range(command.number_to_move):
            crates_to_move.append(stacks[command.move_from].pop())

        for element in reversed(crates_to_move):
            stacks[command.move_to].append(element)

    return stacks


if __name__ == "__main__":
    stacks, commands = read_input("input.txt")
    organized_crates_9000 = organize_crates_9000(copy.deepcopy(stacks), commands)

    part_1_solution = ""
    for stack_number in sorted(organized_crates_9000.keys()):
        part_1_solution += organized_crates_9000[stack_number][-1]

    print(f"Top of each stack part 1: {part_1_solution}")

    organized_crates_9001 = organize_crates_9001(copy.deepcopy(stacks), commands)
    part_2_solution = ""
    for stack_number in sorted(organized_crates_9001.keys()):
        part_2_solution += organized_crates_9001[stack_number][-1]

    print(f"Top of each stack part 2: {part_2_solution}")
