from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    name: str
    operation: Callable | None = None
    number1: str | float = ""
    number2: str | float = ""
    result: float | None = None

    def compute_result(self):
        if self.operation:
            self.result = self.operation(self.number1, self.number2)


def operation_from_str(operation: str) -> Callable:
    match operation:
        case "+":
            return lambda x, y: x + y
        case "-":
            return lambda x, y: x - y
        case "*":
            return lambda x, y: x * y
        case "/":
            return lambda x, y: x / y
        case _:
            raise ValueError("Unknown operation")


def read_input(filename: str) -> list[Monkey]:
    with open(filename, "r") as fp:
        lines = fp.readlines()

    monkeys = []
    for line in lines:
        elements = line.strip().split(":")
        monkey_name = elements[0]
        number_part = elements[1].strip().split()
        if len(number_part) == 1:
            monkeys.append(Monkey(name=monkey_name, result=float(number_part[0])))
        else:
            monkeys.append(
                Monkey(
                    name=monkey_name,
                    operation=operation_from_str(number_part[1]),
                    number1=number_part[0],
                    number2=number_part[2],
                )
            )

    return monkeys


def update_dicts(
    monkey: Monkey,
    monkeys_with_result: dict[str, Monkey],
    monkeys_without_result: dict[str, Monkey],
    awaiting: dict[str, Monkey],
) -> tuple[dict[str, Monkey], dict[str, Monkey], dict[str, Monkey]]:

    if isinstance(monkey.number1, float) and isinstance(monkey.number2, float):
        monkey.compute_result()

    if monkey.result:
        monkeys_with_result[monkey.name] = monkey
        if monkey.name in monkeys_without_result:
            del monkeys_without_result[monkey.name]

        if monkey.name in awaiting:
            monkey_to_update = awaiting.pop(monkey.name)
            if monkey_to_update.number1 == monkey.name:
                monkey_to_update.number1 = monkey.result
            if monkey_to_update.number2 == monkey.name:
                monkey_to_update.number2 = monkey.result

            monkeys_with_result, monkeys_without_result, awaiting = update_dicts(
                monkey_to_update, monkeys_with_result, monkeys_without_result, awaiting
            )

    elif monkey.name not in monkeys_without_result:
        monkeys_without_result[monkey.name] = monkey
        if isinstance(monkey.number1, str):
            if monkey_with_result := monkeys_with_result.get(monkey.number1):
                monkey.number1 = monkey_with_result.result  # type: ignore
            else:
                awaiting[monkey.number1] = monkey

        if isinstance(monkey.number2, str):
            if monkey_with_result := monkeys_with_result.get(monkey.number2):
                monkey.number2 = monkey_with_result.result  # type: ignore
            else:
                awaiting[monkey.number2] = monkey
        monkeys_with_result, monkeys_without_result, awaiting = update_dicts(
            monkey, monkeys_with_result, monkeys_without_result, awaiting
        )

    return monkeys_with_result, monkeys_without_result, awaiting


def solve_riddle(monkeys: list[Monkey]) -> int | None:
    monkeys_with_result: dict[str, Monkey] = dict()
    monkeys_without_result: dict[str, Monkey] = dict()
    awaiting: dict[str, Monkey] = dict()

    for monkey in monkeys:
        update_dicts(monkey, monkeys_with_result, monkeys_without_result, awaiting)

    if result := monkeys_with_result["root"].result:
        return int(result)
    return None


if __name__ == "__main__":
    monkeys = read_input("input.txt")
    print(f"Solution, part1: {solve_riddle(monkeys)}")
