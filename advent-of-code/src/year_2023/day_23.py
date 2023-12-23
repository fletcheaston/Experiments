import collections
import sys
import typing
from dataclasses import dataclass, field
from typing import Literal

from fastapi import APIRouter, Body

sys.setrecursionlimit(5_000)

router = APIRouter(tags=["2023 - Day 23: Title"])


DOCUMENT_EXAMPLE = []


TILE = Literal[".", ">", "<", "^", "v"]
TILES: set[TILE] = set(typing.get_args(TILE))


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


EDGE = tuple[Coordinate, Coordinate]


@dataclass
class Grid:
    start: Coordinate = field(default_factory=lambda: Coordinate(x=1, y=0))
    end: Coordinate = field(default_factory=lambda: Coordinate(x=1, y=0))

    grid: dict[Coordinate, TILE] = field(default_factory=dict)

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
                x=coordinate.x + x_offset, y=coordinate.y + y_offset
            )

            if new_coordinate in self.grid:
                new_coordinates.append(new_coordinate)

        return new_coordinates

    def longest_path(self) -> int:
        to_check = collections.deque([(self.start, set())])
        accumulated_steps: dict[Coordinate, int] = {self.start: 0}

        while to_check:
            coordinate, path = to_check.pop()

            if coordinate == self.end:
                continue

            for adj_coordinate in self.adjacent(coordinate):
                new_cost = accumulated_steps[coordinate] + 1

                if adj_coordinate in path:
                    continue

                if (
                    adj_coordinate not in accumulated_steps
                    or new_cost > accumulated_steps[adj_coordinate]
                ):
                    accumulated_steps[adj_coordinate] = new_cost

                    new_path = path.copy()
                    new_path.add(adj_coordinate)

                    to_check.appendleft((adj_coordinate, new_path))

        return accumulated_steps[self.end]


# Start at 10:50
@router.post("/part-1")
async def year_2023_day_23_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    grid = Grid()

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            if character in TILES:
                grid.add(Coordinate(x=x_index, y=y_index), character)

    return grid.longest_path()


@router.post("/part-2")
async def year_2023_day_23_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    for line in document:
        pass

    return total
