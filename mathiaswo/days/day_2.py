from pathlib import Path


def get_shape_score(shape: str):
    match shape:
        case "X":
            return 1
        case "Y":
            return 2
        case "Z":
            return 3
        case _:
            raise ValueError(f"Unknown shape: {shape}")


def get_round_score(round_str: str):
    match round_str:
        case "A X" | "B Y" | "C Z":
            # draw
            return 3
        case "A Z" | "B X" | "C Y":
            # opponent wins
            return 0
        case "A Y" | "B Z" | "C X":
            # I win
            return 6
        case _:
            raise ValueError(f"Unknown str: {round_str}")


def get_choice(round_str: str) -> str:
    # convert part 2 round to part 1 shape choice
    match round_str:
        case "A Y" | "B X" | "C Z":
            # choose rock
            return "X"
        case "A Z" | "B Y" | "C X":
            # choose paper
            return "Y"
        case "A X" | "B Z" | "C Y":
            # choose scissors
            return "Z"
        case _:
            raise ValueError(f"Unknown str: {round_str}")


def main(input_string: str):
    # part 1
    score = 0
    for round in input_string.split("\n"):
        score += get_round_score(round) + get_shape_score(round[-1])

    print(score)

    # part 2
    score = 0
    for line in input_string.split("\n"):
        choice = get_choice(line)
        # round on part 1 format
        round = f"{line[0]} {choice}"
        score += get_round_score(round) + get_shape_score(round[-1])

    print(score)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "input_2.txt"
    with open(input_path) as f:
        input_string = f.read().strip()
    main(input_string)
