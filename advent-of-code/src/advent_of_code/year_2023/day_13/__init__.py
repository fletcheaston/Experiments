from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Literal

import pytest


@cache
def differences(first: str, second: str) -> int:
    diffs = 0

    for first_char, second_char in zip(first, second):
        if first_char != second_char:
            diffs += 1

    return diffs


@dataclass
class Grid:
    smudges: int
    rows: list[str] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)

    def add(self, row: str) -> None:
        self.rows.append(row)

        if not self.columns:
            self.columns = ["" for _ in range(len(row))]

        for index, character in enumerate(row):
            self.columns[index] += character

    def calculate_reflections(self, direction: Literal["rows", "columns"]) -> int:
        data: list[str] | None = None
        multiplier = 1

        if direction == "rows":
            data = self.rows.copy()
            multiplier = 100

        if direction == "columns":
            data = self.columns.copy()

        assert data is not None

        start_indexes: list[int] = []

        for index in range(len(data) - 1):
            if differences(data[index], data[index + 1]) < 2:
                start_indexes.append(index)

        for start_index in start_indexes:
            smudges_used = 0

            reflection_index = start_index + 1
            matching = True
            end_index = start_index + 1

            while matching and start_index >= 0 and end_index < len(data):
                if data[start_index] == data[end_index]:
                    start_index -= 1
                    end_index += 1

                elif (
                    differences(data[start_index], data[end_index]) == 1
                    and self.smudges - smudges_used > 0
                ):
                    smudges_used += 1
                    start_index -= 1
                    end_index += 1

                else:
                    matching = False

            if matching and smudges_used == self.smudges:
                return reflection_index * multiplier

        return 0


def part_1(document: list[str]) -> int:
    total = 0

    grid = Grid(smudges=0)

    for line in document:
        if not line:
            # Calculate reflections
            if row_count := grid.calculate_reflections("rows"):
                total += row_count
            else:
                total += grid.calculate_reflections("columns")

            # Reset grid
            grid = Grid(smudges=0)

        else:
            grid.add(line)

    # Last grid
    if row_count := grid.calculate_reflections("rows"):
        total += row_count
    else:
        total += grid.calculate_reflections("columns")

    return total


def part_2(document: list[str]) -> int:
    total = 0

    grid = Grid(smudges=1)

    for line in document:
        if not line:
            # Calculate reflections
            if row_count := grid.calculate_reflections("rows"):
                total += row_count
            else:
                total += grid.calculate_reflections("columns")

            # Reset grid
            grid = Grid(smudges=1)

        else:
            grid.add(line)

    # Last grid
    if row_count := grid.calculate_reflections("rows"):
        total += row_count
    else:
        total += grid.calculate_reflections("columns")

    return total


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 405),
        ("input.txt", 35538),
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
        ("example.txt", 400),
        ("input.txt", 30442),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
