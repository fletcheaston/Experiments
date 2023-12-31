import math
import sys
import typing
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Literal

import pytest

sys.setrecursionlimit(5_000)

TILE = Literal[".", ">", "<", "^", "v"]
TILES: set[TILE] = set(typing.get_args(TILE))


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    @cached_property
    def distance(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __lt__(self, other: "Coordinate") -> bool:
        return self.distance < other.distance

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Grid:
    start: Coordinate = field(default_factory=lambda: Coordinate(x=1, y=0))
    end: Coordinate = field(default_factory=lambda: Coordinate(x=1, y=0))

    grid: dict[Coordinate, TILE] = field(default_factory=dict)

    intersections: set[Coordinate] = field(default_factory=set)
    intersection_edges: dict[Coordinate, dict[Coordinate, set[Coordinate]]] = field(
        default_factory=dict
    )

    longest_intersections: set[Coordinate] = field(default_factory=set)
    longest_full_path: set[Coordinate] = field(default_factory=set)

    def add(self, coordinate: Coordinate, tile: TILE) -> None:
        # `end` is the largest y-coordinate in the grid
        if coordinate.y > self.end.y:
            self.end = coordinate

        # Add to internal grid
        self.grid[coordinate] = tile

    def adjacent(self, coordinate: Coordinate) -> list[Coordinate]:
        # Check right downhill
        if self.grid[coordinate] == ">":
            return [
                Coordinate(
                    x=coordinate.x + 1,
                    y=coordinate.y,
                )
            ]

        # Check left downhill
        if self.grid[coordinate] == "<":
            return [
                Coordinate(
                    x=coordinate.x - 1,
                    y=coordinate.y,
                )
            ]

        # Check down downhill
        if self.grid[coordinate] == "v":
            return [
                Coordinate(
                    x=coordinate.x,
                    y=coordinate.y + 1,
                )
            ]

        # Check up downhill
        if self.grid[coordinate] == "^":
            return [
                Coordinate(
                    x=coordinate.x,
                    y=coordinate.y - 1,
                )
            ]

        new_coordinates: list[Coordinate] = []

        for x_offset, y_offset in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            new_coordinate = Coordinate(
                x=coordinate.x + x_offset,
                y=coordinate.y + y_offset,
            )

            if new_coordinate in self.grid:
                new_coordinates.append(new_coordinate)

        return new_coordinates

    def find_intersections(self) -> None:
        # We'll consider the start and end intersections
        # Makes later algorithms easier to work with
        self.intersections.add(self.start)
        self.intersections.add(self.end)

        # Check for more than 2 adjacent nodes
        for coordinate in self.grid.keys():
            if len(self.adjacent(coordinate)) > 2:
                self.intersections.add(coordinate)

    def path_to_intersections(
        self,
        start: Coordinate,
        current: Coordinate,
        path: set[Coordinate],
    ) -> None:
        # Hit an intersection, end this path here
        if current in self.intersections:
            if start not in self.intersection_edges:
                self.intersection_edges[start] = {}

            self.intersection_edges[start][current] = path
            return

        # Check adjacent nodes
        for adjacent in self.adjacent(current):
            if adjacent not in path:
                next_path = path.copy()
                next_path.add(adjacent)

                self.path_to_intersections(start, adjacent, next_path)

    def build_intersection_edges(self) -> None:
        sorted_intersections = list(self.intersections)
        sorted_intersections.sort()

        for intersection in sorted_intersections:
            for adjacent in self.adjacent(intersection):
                self.path_to_intersections(
                    intersection, adjacent, {intersection, adjacent}
                )

    def find_longest_path(
        self,
        current: Coordinate,
        unique_path: set[Coordinate],
        full_path: set[Coordinate],
    ) -> None:
        # Base cases
        # Reached the end
        if current == self.end:
            if len(full_path) > len(self.longest_full_path):
                self.longest_intersections = unique_path
                self.longest_full_path = full_path

            return

        # Dead end
        if current not in self.intersection_edges:
            return

        # Search next nodes
        for next_node, path in self.intersection_edges[current].items():
            # Skip nodes we've already checked
            if next_node in unique_path:
                continue

            next_unqiue_path = unique_path.copy()
            next_unqiue_path.add(next_node)

            next_full_path = full_path.copy()
            next_full_path.update(path)

            self.find_longest_path(next_node, next_unqiue_path, next_full_path)

    def show(self) -> None:
        print()

        for y in range(self.start.y, self.end.y + 1):
            line = "#"

            for x in range(self.start.x, self.end.x + 1):
                coordinate = Coordinate(x=x, y=y)
                tile = self.grid.get(coordinate, "#")

                if coordinate in self.intersections:
                    line += "\033[31mX\033[0m"

                else:
                    line += tile

            line += "#"
            print(line)

    def show_path(self, path: set[Coordinate]) -> None:
        print()

        for y in range(self.start.y, self.end.y + 1):
            line = "#"

            for x in range(self.start.x, self.end.x + 1):
                coordinate = Coordinate(x=x, y=y)
                tile = self.grid.get(coordinate, "#")

                if coordinate in path:
                    line += "\033[31mX\033[0m"

                else:
                    line += tile

            line += "#"
            print(line)


def part_1(document: list[str]) -> int:
    grid = Grid()

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            if character in TILES:
                grid.add(Coordinate(x=x_index, y=y_index), character)

    grid.find_intersections()
    grid.build_intersection_edges()
    grid.find_longest_path(grid.start, {grid.start}, {grid.start})

    return len(grid.longest_full_path) - 1


def part_2(document: list[str]) -> int:
    grid = Grid()

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            if character in TILES:
                grid.add(Coordinate(x=x_index, y=y_index), ".")

    grid.find_intersections()
    grid.build_intersection_edges()
    grid.find_longest_path(grid.start, {grid.start}, {grid.start})

    return len(grid.longest_full_path) - 1


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 94),
        ("input.txt", 2094),
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
        ("example-1.txt", 154),
        # ("input.txt", 6442),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
