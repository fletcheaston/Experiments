from dataclasses import dataclass, field

import numpy as np
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 18: Title"])


DOCUMENT_EXAMPLE = []


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"


OFFSET: dict[str, tuple[int, int]] = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}

DIRECTION_OFFSETS: list[tuple[int, int]] = [
    (1, 0),
    (-1, 0),
    (0, -1),
    (0, 1),
]


@dataclass
class Grid:
    current: Coordinate
    path: list[Coordinate]

    min_x: int = 0
    max_x: int = 0

    min_y: int = 0
    max_y: int = 0

    path_set: set[Coordinate] = field(default_factory=set)
    grid: dict[Coordinate, str] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return (self.max_x - self.min_x) * (self.max_y - self.min_y)

    def move(self, x: int, y: int) -> None:
        self.min_x = min(self.min_x, self.current.x + x)
        self.max_x = max(self.max_x, self.current.x + x + 1)

        self.min_y = min(self.min_y, self.current.y + y)
        self.max_y = max(self.max_y, self.current.y + y + 1)

        self.current = Coordinate(
            x=self.current.x + x,
            y=self.current.y + y,
        )
        self.path.append(self.current)
        self.path_set.add(self.current)

    def set_grid(self) -> None:
        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                coordinate = Coordinate(x=x, y=y)

                if coordinate in self.path_set:
                    self.grid[coordinate] = "\033[31m#\033[0m"

                else:
                    self.grid[coordinate] = "."

    def flood_fill(self) -> None:
        # Go around borders first, collect all "."
        points: set[Coordinate] = set()

        for x in [self.min_x, self.max_x - 1]:
            for y in range(self.min_y, self.max_y):
                coordinate = Coordinate(x=x, y=y)

                if self.grid[coordinate] == ".":
                    points.add(coordinate)
                    self.grid[coordinate] = "O"

        for y in [self.min_y, self.max_y - 1]:
            for x in range(self.min_x, self.max_x):
                coordinate = Coordinate(x=x, y=y)

                if self.grid[coordinate] == ".":
                    points.add(coordinate)
                    self.grid[coordinate] = "O"

        visited: set[Coordinate] = set()

        while points:
            # Get a point
            point = points.pop()
            visited.add(point)

            # Get all the points around that are "."
            for offset_x, offset_y in DIRECTION_OFFSETS:
                new_point = Coordinate(x=point.x + offset_x, y=point.y + offset_y)

                # Skip points that aren't in the grid
                if new_point not in self.grid:
                    continue

                # Skip points we've already checked
                if new_point in visited:
                    continue

                if self.grid[new_point] == ".":
                    self.grid[new_point] = "O"
                    points.add(new_point)

    def count(self, character: str) -> int:
        total = 0

        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                if self.grid[Coordinate(x=x, y=y)] == character:
                    total += 1

        return total

    def show(self) -> None:
        print()

        output = ""

        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                output += self.grid[Coordinate(x=x, y=y)]

            output += "\n"

        print(output)


@router.post("/part-1")
async def year_2023_day_18_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    grid = Grid(
        current=Coordinate(x=0, y=0),
        path=[Coordinate(x=0, y=0)],
    )

    for line in document:
        direction, distance, _ = line.split(" ")

        for _ in range(int(distance)):
            grid.move(*OFFSET[direction])

    grid.set_grid()

    grid.flood_fill()

    return grid.size - grid.count("O")


@dataclass
class BigGrid:
    current: Coordinate
    path: list[Coordinate]

    perimiter: int = 0

    @property
    def enclosed_area(self) -> int:
        x_coordinates = [position.x for position in self.path[:-1]]
        y_coordinates = [position.y for position in self.path[:-1]]

        # Calculates the area within
        area = abs(np.trapz(y_coordinates, x=x_coordinates))

        return area + self.perimiter + 1

    def move(self, x: int, y: int) -> None:
        # One of these is always zero, just add both
        self.perimiter += (abs(x) + abs(y)) / 2

        self.current = Coordinate(
            x=self.current.x + x,
            y=self.current.y + y,
        )
        self.path.append(self.current)


@router.post("/part-2")
async def year_2023_day_18_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    grid = BigGrid(
        current=Coordinate(x=0, y=0),
        path=[Coordinate(x=0, y=0)],
    )

    direction_map: dict[str, str] = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }

    for line in document:
        _, __, color = line.split(" ")

        # Convert from hex to decimal
        distance = int(color[2:7], 16)
        direction = direction_map[color[7]]

        x_offset, y_offset = OFFSET[direction]

        grid.move(x_offset * distance, y_offset * distance)

    return grid.enclosed_area
