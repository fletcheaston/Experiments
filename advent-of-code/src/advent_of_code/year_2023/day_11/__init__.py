from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path

import pytest


@dataclass
class Grid:
    space: list[list[str]]
    displacement: int
    galaxies: list[tuple[int, int]] = field(default_factory=list)
    galaxy_combos: list[tuple[tuple[int, int], tuple[int, int]]] = field(
        default_factory=list
    )

    rows_displaced: list[int] = field(default_factory=list)
    columns_displaced: list[int] = field(default_factory=list)

    def expand(self) -> None:
        # Expand the rows
        for index, row in enumerate(self.space):
            if all([char == "." for char in row]):
                self.rows_displaced.append(index)

        # Expand the columns
        for x_index in range(len(self.space[0])):
            if all(
                [
                    self.space[y_index][x_index] == "."
                    for y_index in range(len(self.space))
                ]
            ):
                self.columns_displaced.append(x_index)

    def pair_galaxies(self) -> None:
        for y_index, row in enumerate(self.space):
            for x_index, character in enumerate(row):
                if character == "#":
                    self.galaxies.append((x_index, y_index))

        for galaxy_combo in combinations(self.galaxies, 2):
            self.galaxy_combos.append(galaxy_combo)

    def calculate_galaxy_combo_distances(self) -> int:
        total_distance = 0

        for galaxy_a, galaxy_b in self.galaxy_combos:
            x_displacements = 0
            y_displacements = 0

            for column in self.columns_displaced:
                if (
                    galaxy_a[0] > column > galaxy_b[0]
                    or galaxy_a[0] < column < galaxy_b[0]
                ):
                    x_displacements += self.displacement - 1

            for row in self.rows_displaced:
                if galaxy_a[1] > row > galaxy_b[1] or galaxy_a[1] < row < galaxy_b[1]:
                    y_displacements += self.displacement - 1

            distance = (
                abs(galaxy_a[0] - galaxy_b[0])
                + x_displacements
                + abs(galaxy_a[1] - galaxy_b[1])
                + y_displacements
            )

            total_distance += distance

        return total_distance


def part_1(document: list[str]) -> int:
    grid = Grid(
        space=[list(line) for line in document],
        displacement=2,
    )

    grid.expand()

    grid.pair_galaxies()

    return grid.calculate_galaxy_combo_distances()


def part_2(document: list[str]) -> int:
    grid = Grid(
        space=[list(line) for line in document],
        displacement=1000000,
    )

    grid.expand()

    grid.pair_galaxies()

    return grid.calculate_galaxy_combo_distances()


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 374),
        ("input.txt", 9550717),
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
        ("example.txt", 82000210),
        ("input.txt", 648458253817),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        with open(Path(__file__).with_name(filename), "r") as file:
            assert part_2(file.read().splitlines()) == output
