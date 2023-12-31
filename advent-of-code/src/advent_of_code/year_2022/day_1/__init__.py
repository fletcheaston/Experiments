from pathlib import Path

import pytest


def part_1(document: list[str]) -> int:
    running_total = 0
    max_total = 0

    for line in document:
        if line:
            # Add to the running total
            running_total += int(line)

        else:
            # Reset the running total
            max_total = max(max_total, running_total)
            running_total = 0

    # Make sure to catch the last running total
    max_total = max(max_total, running_total)

    return max_total


def part_2(document: list[str]) -> int:
    running_total = 0
    totals: list[int] = []

    for line in document:
        if line:
            # Add to the running total
            running_total += int(line)

        else:
            # Reset the running total
            totals.append(running_total)
            running_total = 0

    # Make sure to catch the last running total
    totals.append(running_total)

    # Sort and sum the top three values
    totals.sort(reverse=True)

    return sum(totals[:3])


@pytest.mark.parametrize(
    "filename,total",
    [
        ("example.txt", 24000),
        ("input.txt", 67450),
    ],
)
def test_part_1(filename: str, total: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == total


@pytest.mark.parametrize(
    "filename,total",
    [
        ("example.txt", 45000),
        ("input.txt", 199357),
    ],
)
def test_part_2(filename: str, total: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == total
