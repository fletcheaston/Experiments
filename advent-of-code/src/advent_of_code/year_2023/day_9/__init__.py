from dataclasses import dataclass
from pathlib import Path

import pytest


@dataclass
class History:
    values: list[list[int]]

    @property
    def latest_all_zero(self) -> bool:
        return all([value == 0 for value in self.values[-1]])

    def calculate_next(self) -> None:
        next_values: list[int] = []

        for index in range(len(self.values[-1]) - 1):
            first = self.values[-1][index]
            second = self.values[-1][index + 1]

            difference = second - first

            next_values.append(difference)

        self.values.append(next_values)

    def fill_in_forwards(self) -> None:
        # Do the first manually
        self.values[-1].append(0)

        # Do the rest in a loop
        for index in range(len(self.values) - 2, -1, -1):
            self.values[index].append(
                self.values[index + 1][-1] + self.values[index][-1]
            )

    def fill_in_backwards(self) -> None:
        # Do the first manually
        self.values[-1].insert(0, 0)

        # Do the rest in a loop
        for index in range(len(self.values) - 2, -1, -1):
            self.values[index].insert(
                0, self.values[index][0] - self.values[index + 1][0]
            )


def part_1(document: list[str]) -> int:
    total = 0

    for line in document:
        history = History(
            values=[[int(value.strip()) for value in line.split(" ")]],
        )

        while not history.latest_all_zero:
            history.calculate_next()

        history.fill_in_forwards()

        total += history.values[0][-1]

    return total


def part_2(document: list[str]) -> int:
    total = 0

    for line in document:
        history = History(
            values=[[int(value.strip()) for value in line.split(" ")]],
        )

        while not history.latest_all_zero:
            history.calculate_next()

        history.fill_in_backwards()

        total += history.values[0][0]

    return total


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 114),
        ("input.txt", 1647269739),
    ],
)
def test_part_1(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 2),
        ("input.txt", 864),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
