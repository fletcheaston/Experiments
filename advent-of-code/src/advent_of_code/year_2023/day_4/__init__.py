from pathlib import Path

import pytest


def part_1(document: list[str]) -> int:
    total = 0

    for line in document:
        rest = line.split(": ")[1]
        winning_str, my_str = rest.split(" | ")

        winning_numbers: list[int] = [
            int(num) for num in winning_str.strip().split(" ") if num
        ]
        my_numbers: list[int] = [int(num) for num in my_str.strip().split(" ") if num]

        score = 0

        for num in my_numbers:
            if num in winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score *= 2

        total += score

    return total


def part_2(document: list[str]) -> int:
    total = 0

    # Map from index to count
    copies: dict[int, int] = {index: 1 for index in range(len(document))}

    for index, line in enumerate(document):
        rest = line.split(": ")[1]
        winning_str, my_str = rest.split(" | ")

        winning_numbers: list[int] = [
            int(num) for num in winning_str.strip().split(" ") if num
        ]
        my_numbers: list[int] = [int(num) for num in my_str.strip().split(" ") if num]

        matches = 0

        for num in my_numbers:
            if num in winning_numbers:
                matches += 1
                copies[index + matches] += copies[index]

        total += copies[index]

    return total


@pytest.mark.parametrize(
    "filename,total",
    [
        ("example.txt", 13),
        ("input.txt", 15205),
    ],
)
def test_part_1(filename: str, total: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == total


@pytest.mark.parametrize(
    "filename,total",
    [
        ("example.txt", 30),
        ("input.txt", 6189740),
    ],
)
def test_part_2(filename: str, total: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == total
