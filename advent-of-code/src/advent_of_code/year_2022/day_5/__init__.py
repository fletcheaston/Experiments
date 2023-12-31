import re
from pathlib import Path

import pytest


def part_1(
    document: list[str],
    stacks: dict[str, list[str]],
) -> str:
    for line in document:
        match = re.search(r"move (\d+) from (\d+) to (\d+)", line)

        count, start, end = match.groups()

        for _ in range(int(count)):
            # Remove from start
            crate = stacks[start].pop(0)
            stacks[end].insert(0, crate)

    # A few extra checks to preserve ordering
    stack_keys = [int(key) for key in stacks.keys()]
    stack_keys.sort()

    # Pull the top crate from each stack and create a message
    message = ""

    for key in stack_keys:
        crate = stacks[str(key)][0]
        message += crate

    return message


def part_2(
    document: list[str],
    stacks: dict[str, list[str]],
) -> str:
    for line in document:
        match = re.search(r"move (\d+) from (\d+) to (\d+)", line)

        count, start, end = match.groups()

        # Pull off the top `count` crates
        crates = stacks[start][: int(count)]
        stacks[start] = stacks[start][int(count) :]

        # Add crates to the new stack
        stacks[end] = crates + stacks[end]

    # A few extra checks to preserve ordering
    stack_keys = [int(key) for key in stacks.keys()]
    stack_keys.sort()

    # Pull the top crate from each stack and create a message
    message = ""

    for key in stack_keys:
        crate = stacks[str(key)][0]
        message += crate

    return message


@pytest.mark.parametrize(
    "filename,stacks,output",
    [
        (
            "example.txt",
            {
                "1": ["N", "Z"],
                "2": ["D", "C", "M"],
                "3": ["P"],
            },
            "CMZ",
        ),
        (
            "input.txt",
            {
                "1": ["D", "H", "R", "Z", "S", "P", "W", "Q"],
                "2": ["F", "H", "Q", "W", "R", "B", "V"],
                "3": ["H", "S", "V", "C"],
                "4": ["G", "F", "H"],
                "5": ["Z", "B", "J", "G", "P"],
                "6": ["L", "F", "W", "H", "J", "T", "Q"],
                "7": ["N", "J", "V", "L", "D", "W", "T", "Z"],
                "8": ["F", "H", "G", "J", "C", "Z", "T", "D"],
                "9": ["H", "B", "M", "V", "P", "W"],
            },
            "ZWHVFWQWW",
        ),
    ],
)
def test_part_1(
    filename: str,
    stacks: dict[str, list[str]],
    output: str,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines(), stacks) == output


@pytest.mark.parametrize(
    "filename,stacks,output",
    [
        (
            "example.txt",
            {
                "1": ["N", "Z"],
                "2": ["D", "C", "M"],
                "3": ["P"],
            },
            "MCD",
        ),
        (
            "input.txt",
            {
                "1": ["D", "H", "R", "Z", "S", "P", "W", "Q"],
                "2": ["F", "H", "Q", "W", "R", "B", "V"],
                "3": ["H", "S", "V", "C"],
                "4": ["G", "F", "H"],
                "5": ["Z", "B", "J", "G", "P"],
                "6": ["L", "F", "W", "H", "J", "T", "Q"],
                "7": ["N", "J", "V", "L", "D", "W", "T", "Z"],
                "8": ["F", "H", "G", "J", "C", "Z", "T", "D"],
                "9": ["H", "B", "M", "V", "P", "W"],
            },
            "HZFZCCWWV",
        ),
    ],
)
def test_part_2(
    filename: str,
    stacks: dict[str, list[str]],
    output: str,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines(), stacks) == output
