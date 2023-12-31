import functools
from pathlib import Path

import pytest

from src.advent_of_code.utils import reduce_lfind, reduce_rfind


def part_1(document: list[str]) -> int:
    total = 0

    for line in document:
        # Remove all non-numeric characters from the string
        numerics = [character for character in line if character.isnumeric()]

        # Combine first and last digits, add to total
        total += int(f"{numerics[0]}{numerics[-1]}")

    return total


VALID_DIGIT_TO_NUM: dict[str, int] = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

VALID_DIGITS = VALID_DIGIT_TO_NUM.keys()


def part_2(document: list[str]) -> int:
    total = 0

    for line in document:
        # Find the earliest "digit"
        first_digit = functools.reduce(
            lambda a, b: reduce_lfind(a, b, line), VALID_DIGITS
        )
        last_digit = functools.reduce(
            lambda a, b: reduce_rfind(a, b, line), VALID_DIGITS
        )

        first = VALID_DIGIT_TO_NUM[first_digit]
        last = VALID_DIGIT_TO_NUM[last_digit]

        # Combine first and last digits, add to total
        total += int(f"{first}{last}")

    return total


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 142),
        ("input.txt", 54338),
    ],
)
def test_part_1(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-2.txt", 281),
        ("input.txt", 53389),
    ],
)
def test_part_2(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
