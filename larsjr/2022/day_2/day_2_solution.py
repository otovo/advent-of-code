from enum import IntEnum, Enum, auto


class Move(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    WIN = auto()
    LOSS = auto()
    DRAW = auto()


def get_move_from_letter(letter: str) -> Move:
    if letter in ["A", "X"]:
        return Move.ROCK
    elif letter in ["B", "Y"]:
        return Move.PAPER
    elif letter in ["C", "Z"]:
        return Move.SCISSORS
    else:
        raise ValueError(f"Unknown letter: {letter}")


def get_outcome_from_letter(letter: str) -> Outcome:
    match letter:
        case "X":
            return Outcome.LOSS
        case "Y":
            return Outcome.DRAW
        case "Z":
            return Outcome.WIN
        case _:
            raise ValueError(f"Unknown letter: {letter}")


def points_from_move(move) -> int:
    return int(move)


def points_from_outcome_of_round(result_of_round: Outcome) -> int:
    match result_of_round:
        case Outcome.WIN:
            return 6
        case Outcome.LOSS:
            return 0
        case _:
            return 3


def outcome_of_round(opponent_move, your_move) -> Outcome:
    if opponent_move == Move.ROCK:
        match your_move:
            case Move.PAPER:
                return Outcome.WIN
            case Move.SCISSORS:
                return Outcome.LOSS
    elif opponent_move == Move.PAPER:
        match your_move:
            case Move.ROCK:
                return Outcome.LOSS
            case Move.SCISSORS:
                return Outcome.WIN
    else:  # opponent move is Scissors
        match your_move:
            case Move.ROCK:
                return Outcome.WIN
            case Move.PAPER:
                return Outcome.LOSS

    return Outcome.DRAW


def get_correct_move(opponent_move: Move, desired_outcome: Outcome) -> Move:
    if opponent_move == Move.ROCK:
        match desired_outcome:
            case Outcome.LOSS:
                return Move.SCISSORS
            case Outcome.WIN:
                return Move.PAPER
    elif opponent_move == Move.PAPER:
        match desired_outcome:
            case Outcome.LOSS:
                return Move.ROCK
            case Outcome.WIN:
                return Move.SCISSORS
    elif opponent_move == Move.SCISSORS:
        match desired_outcome:
            case Outcome.LOSS:
                return Move.PAPER
            case Outcome.WIN:
                return Move.ROCK

    return opponent_move


def points_part_1(opponent_move: Move, your_move: Move) -> int:
    result_of_round = outcome_of_round(opponent_move, your_move)
    return points_from_move(your_move) + points_from_outcome_of_round(result_of_round)


def points_part_2(opponent_move: Move, desired_outcome: Outcome) -> int:
    your_move = get_correct_move(opponent_move, desired_outcome)
    return points_from_move(your_move) + points_from_outcome_of_round(desired_outcome)


if __name__ == "__main__":
    rounds = []
    with open("input.txt", "r") as fp:
        for line in fp:
            elements = line.split()
            rounds.append((elements[0].strip(), elements[1].strip()))

    # Part 1
    points_1 = 0
    for opponent_move, your_move in rounds:

        points_1 += points_part_1(
            get_move_from_letter(opponent_move), get_move_from_letter(your_move)
        )

    print(f"Result part 1: {points_1}")

    # Part 2
    points_2 = 0
    for opponent_move, desired_outcome in rounds:
        points_2 += points_part_2(
            get_move_from_letter(opponent_move),
            get_outcome_from_letter(desired_outcome),
        )

    print(f"Result part 2: {points_2}")
