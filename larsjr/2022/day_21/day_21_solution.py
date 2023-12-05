from dataclasses import dataclass
from typing import Callable
from sympy.parsing.sympy_parser import parse_expr
from sympy import Eq, solveset


@dataclass
class Monkey:
    name: str
    operation: Callable | None = None
    operation_str: str | None = None
    number1: str | float = ""
    number2: str | float = ""
    result: float | None = None

    def compute_result(self):
        if self.operation:
            self.result = self.operation(self.number1, self.number2)

    def get_equation(self) -> str:
        if isinstance(self.number1, float):
            return self.replace_operation_with_number(0, self.number1)
        else:
            return self.replace_operation_with_number(2, self.number2)  # type: ignore

    def replace_operation_with_number(
        self, index_to_replace: int, replace_with: float
    ) -> str:
        elements = self.operation_str.split()  # type: ignore
        elements[index_to_replace] = f"{replace_with}"
        return f"({' '.join(elements)})"

    def get_number_that_is_str(self) -> str:
        if isinstance(self.number1, str):
            return self.number1
        elif isinstance(self.number2, str):
            return self.number2

        raise ValueError("Either number1 or number2 should be a str")

    def get_number_that_is_float(self) -> float:
        if isinstance(self.number1, float):
            return self.number1
        elif isinstance(self.number2, float):
            return self.number2

        raise ValueError("Either number1 or number2 should be a float")


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
                    operation_str=elements[1].strip(),
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


def solve_riddle2(monkeys: list[Monkey]) -> int:
    monkeys_with_result: dict[str, Monkey] = dict()
    monkeys_without_result: dict[str, Monkey] = dict()
    awaiting: dict[str, Monkey] = dict()

    # Find one of root's numbers
    for monkey in monkeys:
        update_dicts(monkey, monkeys_with_result, monkeys_without_result, awaiting)

    # Expand the expression of root that is not a number to an equation
    # of humn
    name_that_is_me = "humn"
    current_monkey_without_result = monkeys_without_result["root"]
    element_to_replace = current_monkey_without_result.get_number_that_is_str()
    equation = element_to_replace
    while element_to_replace != name_that_is_me:
        current_monkey_without_result = monkeys_without_result[element_to_replace]
        current_equation = current_monkey_without_result.get_equation()
        equation = equation.replace(element_to_replace, current_equation)
        element_to_replace = current_monkey_without_result.get_number_that_is_str()

    # Solve equation with sympy, feels a bit like cheating ;)
    left_hand_side = parse_expr(equation)
    right_hand_side = monkeys_without_result["root"].get_number_that_is_float()
    solution = solveset(Eq(left_hand_side, right_hand_side), "humn")
    return int(solution.args[0])


if __name__ == "__main__":
    input_file = "input.txt"
    monkeys = read_input(input_file)
    print(f"Solution, part1: {solve_riddle(monkeys)}")

    monkeys = read_input(input_file)
    for monkey in monkeys:
        if monkey.name == "humn":
            monkey.number1 = "humn"
            monkey.number2 = 0
            monkey.result = None

    print(f"Solution, part 2: {solve_riddle2(monkeys)}")
