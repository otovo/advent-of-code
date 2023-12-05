from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Valve:
    name: str
    flow_rate: int
    connected_to: list[str]


def read_input(filename: str) -> dict[str, Valve]:
    valves = {}
    with open(filename, "r") as fp:
        for line in fp:
            name = line.split()[1]
            flow_rate = int(line.split(";")[0].split("=")[1])
            neighbors = line.strip().split("lea")[1].strip().split()[3:]
            valves[name] = Valve(name, flow_rate, neighbors)

    return valves


def find_max_pressure_released(valves: dict[str, Valve]) -> int:
    start_node = valves["AA"]
    minutes_remaining = 30
    return 0


if __name__ == "__main__":
    valves = read_input("test_input.txt")
    print(valves)
