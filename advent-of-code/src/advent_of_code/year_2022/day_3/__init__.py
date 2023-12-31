import string
from pathlib import Path

import pytest

from src.advent_of_code.utils import chunks

ITEM_TO_PRIORITY: dict[str, int] = {
    **{char: index + 1 for index, char in enumerate(string.ascii_lowercase)},
    **{char: index + 27 for index, char in enumerate(string.ascii_uppercase)},
}


def part_1(document: list[str]) -> int:
    total = 0

    for line in document:
        first_compartment = line[: len(line) // 2]
        second_compartment = line[len(line) // 2 :]

        # Find the one duplicate item
        duplicate_item: str | None = None

        for item in first_compartment:
            if item in second_compartment:
                duplicate_item = item

        # Total up the priority
        total += ITEM_TO_PRIORITY[duplicate_item]

    return total


def part_2(document: list[str]) -> int:
    total = 0

    for line_1, line_2, line_3 in chunks(document, 3):
        # Convert each line to a set of items and get the intersections
        duplicates = set(line_1).intersection((set(line_2))).intersection((set(line_3)))

        badge = duplicates.pop()

        # Total up the priority
        total += ITEM_TO_PRIORITY[badge]

    return total


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 157),
        ("input.txt", 7903),
    ],
)
def test_part_1(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 70),
        ("input.txt", 2548),
    ],
)
def test_part_2(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
