import math
from pathlib import Path

import pytest


def part_1(
    instructions: str,
    document: list[str],
) -> int:
    steps = 0
    current_step = "AAA"

    maps: dict[str, tuple[str, str]] = {}

    for line in document:
        start, rest = line.split(" = ")
        left, right = rest.replace("(", "").replace(")", "").split(", ")

        maps[start] = (left, right)

    while current_step != "ZZZ":
        instruction = instructions[steps % len(instructions)]

        if instruction == "L":
            current_step = maps[current_step][0]
        elif instruction == "R":
            current_step = maps[current_step][1]
        else:
            raise AssertionError

        steps += 1

    return steps


def part_2(
    instructions: str,
    document: list[str],
) -> int:
    steps: list[str] = []
    maps: dict[str, tuple[str, str]] = {}

    for index, line in enumerate(document):
        start, rest = line.split(" = ")
        left, right = rest.replace("(", "").replace(")", "").split(", ")

        maps[start] = (left, right)

        if start.endswith("A"):
            steps.append(start)

    steps_index = 0
    cycles = []

    while True:
        for index, previous_step in enumerate(steps):
            current_step = maps[previous_step]
            instruction = instructions[steps_index % len(instructions)]

            if instruction == "L":
                next_step = current_step[0]
            elif instruction == "R":
                next_step = current_step[1]
            else:
                raise AssertionError

            if next_step.endswith("Z"):
                cycles.append(steps_index + 1)

            steps[index] = next_step

        if len(cycles) == len(steps):
            break

        steps_index += 1

    return math.lcm(*cycles)


@pytest.mark.parametrize(
    "filename,instructions,output",
    [
        ("example-1.txt", "RL", 2),
        (
            "input.txt",
            "LLRLRLLRRLRLRLLRRLRRRLRRRLRRLRRLRLRLRRRLLRLRRLRLRRRLRLLRRLRLRLLRRRLLRLRRRLRLRRLRRLRLLRRLRRLRLRLRLLRLLRRLRRLRRLRRLRRLRLLRLRLRRRLRRRLRRLRLRLRRLRRRLRLRRRLRLRLRLRRRLRRLRRLRRRLLLLRRLRRLRLRRRLRLRRRLRRLLLLRLRLRRRLRRRLRLRRLLRLRLRRRLRLRLRRRLRLLRRRLRRLRLRLRRRLRLLRRLLRRRLRRRLRRRLRRLRLRLRRRLRRRLRRRLLRRRR",
            23147,
        ),
    ],
)
def test_part_1(filename: str, instructions: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(instructions, file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,instructions,output",
    [
        ("example-2.txt", "LR", 6),
        (
            "input.txt",
            "LLRLRLLRRLRLRLLRRLRRRLRRRLRRLRRLRLRLRRRLLRLRRLRLRRRLRLLRRLRLRLLRRRLLRLRRRLRLRRLRRLRLLRRLRRLRLRLRLLRLLRRLRRLRRLRRLRRLRLLRLRLRRRLRRRLRRLRLRLRRLRRRLRLRRRLRLRLRLRRRLRRLRRLRRRLLLLRRLRRLRLRRRLRLRRRLRRLLLLRLRLRRRLRRRLRLRRLLRLRLRRRLRLRLRRRLRLLRRRLRRLRLRLRRRLRLLRRLLRRRLRRRLRRRLRRLRLRLRRRLRRRLRRRLLRRRR",
            22289513667691,
        ),
    ],
)
def test_part_2(
    filename: str,
    instructions: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(instructions, file.read().splitlines()) == output
