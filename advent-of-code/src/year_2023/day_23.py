import typing
from dataclasses import dataclass, field
from typing import Literal

from fastapi import APIRouter, Body

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
    edges: dict[EDGE, str] = field(default_factory=dict)

    def add(self, coordinate: Coordinate, tile: TILE) -> None:
        # `end` is the largest y-coordinate in the grid
        if coordinate.y > self.end.y:
            self.end = coordinate

        # Add to internal grid
        self.grid[coordinate] = tile

    def build_edges(self) -> None:
        for coordinate, tile in self.grid.items():
            # Check left
            left_coordinate = Coordinate(
                x=coordinate.x - 1,
                y=coordinate.y,
            )

            if (
                tile != ">"
                and left_coordinate in self.grid
                and self.grid[left_coordinate] != ">"
            ):
                self.edges[(coordinate, left_coordinate)] = "left"

            # Check right
            right_coordinate = Coordinate(
                x=coordinate.x + 1,
                y=coordinate.y,
            )

            if (
                tile != "<"
                and right_coordinate in self.grid
                and self.grid[right_coordinate] != "<"
            ):
                self.edges[(coordinate, right_coordinate)] = "right"

            # Check up
            up_coordinate = Coordinate(
                x=coordinate.x,
                y=coordinate.y - 1,
            )

            if (
                tile != "v"
                and up_coordinate in self.grid
                and self.grid[up_coordinate] != "v"
            ):
                self.edges[(coordinate, up_coordinate)] = "up"

            # Check down
            down_coordinate = Coordinate(
                x=coordinate.x,
                y=coordinate.y + 1,
            )

            if (
                tile != "^"
                and down_coordinate in self.grid
                and self.grid[down_coordinate] != "^"
            ):
                self.edges[(coordinate, down_coordinate)] = "down"

    def __repr__(self) -> str:
        return f"{self.start=}, {self.end=}"


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

    grid.build_edges()

    print()
    for coordinate in grid.grid.items():
        print(f"{coordinate=}")

    print()
    for edge in grid.edges.items():
        print(f"{edge=}")

    return 0


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
