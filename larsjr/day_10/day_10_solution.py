from dataclasses import dataclass
from enum import Enum, auto


class InstructionType(Enum):
    NOOP = auto()
    ADDX = auto()


@dataclass
class Instruction:
    instruction: InstructionType
    value: int = 0

    def __str__(self) -> str:
        t = "noop" if self.instruction == InstructionType.NOOP else "addx"
        return f"{t} {self.value}"


def read_instructions(lines) -> list[Instruction]:
    instructions = []
    for line in lines:
        if line.startswith("noop"):
            instructions.append(Instruction(instruction=InstructionType.NOOP))
        else:
            instructions.append(
                Instruction(
                    instruction=InstructionType.ADDX, value=int(line.split()[1].strip())
                )
            )
    return instructions


def compute_signal_strength_if_inspect_cycle(
    cycle, inspect_cycles, register, debug=False
):
    if cycle in inspect_cycles:
        if debug:
            print(
                f"Cycle {cycle:4}. Register = {register}. Signal strength = {cycle * register}"
            )
        return cycle * register
    return 0


def print_crt(crt: list[list[str]]) -> None:
    rows = []
    for j in range(len(crt)):
        row = ""
        for i in range(len(crt[j])):
            row += str(crt[j][i])
        rows.append(row)
    for row in rows:
        print(row)
    print("\n")


def update_crt(crt, cycle, register):
    row = (cycle - 1) // 40  # y
    column = cycle - (40 * row) - 1  # x
    sprite_positions = [register - 1, register, register + 1]
    if column in sprite_positions:
        crt[row][column] = "#"


def simulate(instructions: list[Instruction], inspect_cycles: list[int]):
    cycle = 0
    register = 1
    signal_strength_sum = 0

    crt = [["." for _ in range(40)] for _ in range(6)]
    for instruction in instructions:
        if instruction.instruction == InstructionType.NOOP:
            cycle += 1
            update_crt(crt, cycle, register)
            signal_strength_sum += compute_signal_strength_if_inspect_cycle(
                cycle, inspect_cycles, register
            )
        else:
            cycle += 1
            update_crt(crt, cycle, register)
            signal_strength_sum += compute_signal_strength_if_inspect_cycle(
                cycle, inspect_cycles, register
            )

            cycle += 1
            update_crt(crt, cycle, register)
            signal_strength_sum += compute_signal_strength_if_inspect_cycle(
                cycle, inspect_cycles, register
            )

            register += instruction.value

    return signal_strength_sum, crt


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        lines = fp.readlines()

    instructions = read_instructions(lines)
    inspect_cycles = [20, 60, 100, 140, 180, 220]
    sum_signal_strengths, crt = simulate(instructions, inspect_cycles)
    print(f"Solution part 1: {sum_signal_strengths}")
    print("Solution part 2:")
    print_crt(crt)
