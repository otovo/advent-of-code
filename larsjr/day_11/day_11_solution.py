from __future__ import annotations
from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    number: int
    items: list[int]
    operation: Callable
    divisor: int
    true_condition: int
    false_condition: int
    number_inspected_items: int = 0

    def take_turn(self, monkeys: list[Monkey], divide_worry_level=False):
        while self.items:
            item = self.items.pop(0)
            self.number_inspected_items += 1
            worry_level = self.operation(item)
            print()
            print(worry_level)
            print()
            if divide_worry_level:
                worry_level = int(worry_level / 3)

            if str(worry_level)[-1] == 0 and len(str(worry_level)) > 3:
                worry_level = int(str(worry_level[:-1]))

            if worry_level % self.divisor == 0:  # self.check_divisibility(worry_level):
                monkeys[self.true_condition].items.append(worry_level)
            else:
                monkeys[self.false_condition].items.append(worry_level)

    @staticmethod
    def divisible_by_2(num: str):
        return int(num[-1]) % 2 == 0

    @staticmethod
    def divisible_by_3(num: str):
        return sum(int(digit) for digit in num) % 3 == 0

    @staticmethod
    def divisible_by_5(num: str):
        return num[-1] in ["0", "5"]

    @staticmethod
    def divisible_by_7(num: str):
        if len(num) < 6:
            return int(num) % 7 == 0
        while len(num) > 6:
            num = str(int(num[:-1]) - 2 * int(num[-1]))

        return int(num) % 7 == 0

    @staticmethod
    def divisible_by_11(num: str):
        s = 0
        flag = True
        for digit in num:
            if flag:
                s += int(digit)
            else:
                s -= int(digit)
            flag = not flag
        return s % 11 == 0

    @staticmethod
    def divisible_by_13(num: str):
        if len(num) < 6:
            return int(num) % 13 == 0
        while len(num) > 6:
            num = str(int(num[:-1]) + 4 * int(num[-1]))

        return int(num) % 13 == 0

    @staticmethod
    def divisible_by_17(num: str):
        if len(num) < 6:
            return int(num) % 17 == 0
        while len(num) > 6:
            num = str(int(num[:-1]) - 5 * int(num[-1]))

        return int(num) % 17 == 0

    @staticmethod
    def divisible_by_19(num: str):
        if len(num) < 6:
            return int(num) % 19 == 0
        while len(num) > 6:
            num = str(int(num[:-1]) + 2 * int(num[-1]))

        return int(num) % 19 == 0

    def check_divisibility(self, worry_level):
        worry_level = str(worry_level)
        match self.divisor:
            case 2:
                return self.divisible_by_2(worry_level)
            case 3:
                return self.divisible_by_3(worry_level)
            case 5:
                return self.divisible_by_5(worry_level)
            case 7:
                return self.divisible_by_7(worry_level)
            case 11:
                return self.divisible_by_11(worry_level)
            case 13:
                return self.divisible_by_13(worry_level)
            case 17:
                return self.divisible_by_17(worry_level)
            case 19:
                return self.divisible_by_19(worry_level)
            case _:
                return int(worry_level) % self.divisor == 0

        # if worry_level % self.divisor == 0:
        #    return True
        # return False


def parse_monkey_number(line: str) -> int:
    return int(line.split()[1].strip().strip(":"))


def parse_starting_items(line: str) -> list[int]:
    items_part = line.split(":")[1]
    items = items_part.split(",")
    return [int(item) for item in items]


def parse_operation(line: str) -> Callable:
    operation = line.split("=")
    return eval(f"lambda old: {operation[1].strip()}")


def parse_divisor(line: str) -> int:
    return int(line.split()[-1].strip())


def parse_condition(line: str) -> int:
    return int(line.split()[-1].strip())


def create_monkey(lines: list[str]) -> Monkey:
    monkey_number = parse_monkey_number(lines[0])
    items = parse_starting_items(lines[1])
    operation = parse_operation(lines[2])
    divisor = parse_divisor(lines[3])
    true_condition = parse_condition(lines[4])
    false_condition = parse_condition(lines[5])

    return Monkey(
        number=monkey_number,
        items=items,
        operation=operation,
        divisor=divisor,
        true_condition=true_condition,
        false_condition=false_condition,
    )


def parse_lines(lines: list[str]) -> list[Monkey]:
    monkeys = []

    for i, line in enumerate(lines):
        if line.startswith("Monkey"):
            monkeys.append(create_monkey(lines[i : i + 6]))

    return monkeys


def play_round(monkeys: list[Monkey], divide_worry_level: bool) -> None:
    for monkey in monkeys:
        monkey.take_turn(monkeys, divide_worry_level)


def find_two_most_active_afer_rounds(
    num_rounds: int, monkeys: list[Monkey], divide_worry_level: bool
) -> tuple[Monkey, Monkey]:
    for i in range(num_rounds):
        print(f"Playing round {i}")
        play_round(monkeys, divide_worry_level)

    sorted_monkeys = sorted(monkeys, key=lambda m: m.number_inspected_items)
    return (sorted_monkeys[-1], sorted_monkeys[-2])


if __name__ == "__main__":
    with open("test_input.txt", "r") as fp:
        lines = fp.readlines()

    monkeys = parse_lines(lines)

    m1_part1, m2_part1 = find_two_most_active_afer_rounds(
        20, monkeys[:], divide_worry_level=True
    )
    print(
        f"Solution part 1: {m1_part1.number_inspected_items * m2_part1.number_inspected_items}"
    )

    # m1_part2, m2_part2 = find_two_most_active_afer_rounds(
    #    10000, monkeys[:], divide_worry_level=False
    # )
    # print(
    #    f"Solution part 2: {m1_part2.number_inspected_items * m2_part2.number_inspected_items}"
    # )
