from __future__ import annotations
from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    number: int
    items: list[int]
    operation: Callable
    test: Callable
    true_condition: int
    false_condidtion: int
    number_inspected_items: int = 0

    def take_turn(self, monkeys: list[Monkey]):
        while self.items:
            item = self.items.pop(0)
            self.number_inspected_items += 1
            worry_level = self.operation(item)
            worry_level = int(worry_level / 3)

            if self.test(worry_level):
                monkeys[self.true_condition].items.append(worry_level)
            else:
                monkeys[self.false_condidtion].items.append(worry_level)


def parse_monkey_number(line: str) -> int:
    return int(line.split()[1].strip().strip(":"))


def parse_starting_items(line: str) -> list[int]:
    items_part = line.split(":")[1]
    items = items_part.split(",")
    return [int(item) for item in items]


def parse_operation(line: str) -> Callable:
    operation = line.split("=")
    return eval(f"lambda old: {operation[1].strip()}")


def parse_test(line: str) -> Callable:
    divide_by = int(line.split()[-1].strip())
    return lambda x: x % divide_by == 0


def parse_condition(line: str) -> int:
    return int(line.split()[-1].strip())


def create_monkey(lines: list[str]) -> Monkey:
    monkey_number = parse_monkey_number(lines[0])
    items = parse_starting_items(lines[1])
    operation = parse_operation(lines[2])
    test = parse_test(lines[3])
    true_condition = parse_condition(lines[4])
    false_condition = parse_condition(lines[5])

    return Monkey(
        number=monkey_number,
        items=items,
        operation=operation,
        test=test,
        true_condition=true_condition,
        false_condidtion=false_condition,
    )


def parse_lines(lines: list[str]) -> list[Monkey]:
    monkeys = []

    for i, line in enumerate(lines):
        if line.startswith("Monkey"):
            monkeys.append(create_monkey(lines[i : i + 6]))

    return monkeys


def play_round(monkeys: list[Monkey]) -> None:
    for monkey in monkeys:
        monkey.take_turn(monkeys)


def find_two_most_active_afer_rounds(
    num_rounds: int, monkeys: list[Monkey]
) -> tuple[Monkey, Monkey]:
    for _ in range(num_rounds):
        play_round(monkeys)

    sorted_monkeys = sorted(monkeys, key=lambda m: m.number_inspected_items)
    return (sorted_monkeys[-1], sorted_monkeys[-2])


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        lines = fp.readlines()

    monkeys = parse_lines(lines)

    m1, m2 = find_two_most_active_afer_rounds(20, monkeys)
    print(f"Solution part 1: {m1.number_inspected_items * m2.number_inspected_items}")
