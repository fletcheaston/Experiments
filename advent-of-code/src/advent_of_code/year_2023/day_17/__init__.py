from dataclasses import dataclass, field
from heapq import heappop, heappush
from pathlib import Path

import pytest


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __lt__(self, other: "Coordinate") -> bool:
        if self.x != other.x:
            return self.x < other.x

        return self.y < other.y


OFFSETS: list[Coordinate] = [
    Coordinate(x=0, y=-1),  # Up
    Coordinate(x=0, y=1),  # Down
    Coordinate(x=1, y=0),  # Right
    Coordinate(x=-1, y=0),  # Left
]


def do_180(coordinate: Coordinate) -> Coordinate:
    return Coordinate(x=-coordinate.x, y=-coordinate.y)


Edge = tuple[Coordinate, Coordinate | None, int]


@dataclass
class Grid:
    grid: dict[Coordinate, int]

    minimum_distance: int
    maximum_distance: int

    edges: dict[Edge, list[Edge]] = field(default_factory=dict)

    max_x: int = 0
    max_y: int = 0

    def add_coordinate(self, coordinate: Coordinate, cost: int) -> None:
        self.max_x = max(self.max_x, coordinate.x + 1)
        self.max_y = max(self.max_y, coordinate.y + 1)
        self.grid[coordinate] = cost

    def run(self) -> int:
        start = (Coordinate(x=0, y=0), None, 0)

        # Build up our cost path
        queue: list[tuple[int, Edge]] = [(0, start)]
        checked: set[Edge] = {start}

        while True:
            current_cost, (point, backwards_offset, distance) = heappop(queue)

            if (
                self.minimum_distance <= distance <= self.maximum_distance
                and point.x == self.max_x - 1
                and point.y == self.max_y - 1
            ):
                return current_cost

            edges: list[Edge] = []

            if backwards_offset is None:
                for next_offset in OFFSETS:
                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    edges.append((next_point, next_offset, 1))

            elif distance < self.minimum_distance:
                # Gotta keep moving in the same direction
                next_point = Coordinate(
                    x=point.x + backwards_offset.x,
                    y=point.y + backwards_offset.y,
                )

                if next_point not in self.grid:
                    continue

                edges.append((next_point, backwards_offset, distance + 1))

            elif distance < self.maximum_distance:
                # Can turn now
                for next_offset in OFFSETS:
                    if next_offset == do_180(backwards_offset):
                        # No 180 degree turns
                        continue

                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    if next_offset == backwards_offset:
                        edges.append((next_point, next_offset, distance + 1))

                    else:
                        edges.append((next_point, next_offset, 1))

            else:
                # Over the maximum, gotta turn
                for next_offset in OFFSETS:
                    if next_offset == do_180(backwards_offset):
                        # No 180 degree turns
                        continue

                    if next_offset == backwards_offset:
                        # No going straight
                        continue

                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    edges.append((next_point, next_offset, 1))

            for edge in edges:
                if edge in checked:
                    continue

                checked.add(edge)
                current_point = edge[0]

                next_cost = current_cost + self.grid[current_point]
                heappush(
                    queue,
                    (next_cost, edge),
                )


def part_1(document: list[str]) -> int:
    grid = Grid(
        grid={},
        minimum_distance=0,
        maximum_distance=3,
    )

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            grid.add_coordinate(Coordinate(x=x_index, y=y_index), cost=int(character))

    return grid.run()


def part_2(document: list[str]) -> int:
    grid = Grid(
        grid={},
        minimum_distance=4,
        maximum_distance=10,
    )

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            grid.add_coordinate(Coordinate(x=x_index, y=y_index), cost=int(character))

    return grid.run()


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 102),
        ("example-2.txt", 12),
        ("example-3.txt", 8),
        ("input.txt", 785),
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
        ("example-1.txt", 94),
        ("example-4.txt", 71),
        ("input.txt", 922),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
