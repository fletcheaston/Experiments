from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

import pytest

OFFSETS: list[tuple[int, int]] = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"


@dataclass
class Grid:
    grid: dict[Coordinate, str] = field(default_factory=dict)
    max_x: int = 0
    max_y: int = 0

    def add(self, coordinate: Coordinate, value: str) -> None:
        self.max_x = max(self.max_x, coordinate.x)
        self.max_y = max(self.max_y, coordinate.y)

        self.grid[coordinate] = value

    def get(self, coordinate: Coordinate, default=None) -> str | None:
        return self.grid.get(coordinate, default)


def part_1(
    document: list[str],
    steps: int,
) -> int:
    start: Coordinate | None = None
    grid = Grid()

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            coordinate = Coordinate(x=x_index, y=y_index)

            if character == "S":
                start = coordinate

            grid.add(coordinate, character)

    assert start is not None

    visited_plots: dict[Coordinate, int] = {}

    @cache
    def count_steps(*, position: Coordinate, remaining_steps: int) -> None:
        if remaining_steps == 0:
            return

        for x_offset, y_offset in OFFSETS:
            new_position = Coordinate(x=position.x + x_offset, y=position.y + y_offset)

            if grid.get(new_position, "#") == "#":
                continue

            if (
                new_position in visited_plots
                and visited_plots[new_position] > remaining_steps
            ):
                continue

            if remaining_steps % 2 == 0:
                visited_plots[new_position] = remaining_steps

            count_steps(position=new_position, remaining_steps=remaining_steps - 1)

    count_steps(position=start, remaining_steps=steps + 1)

    return len(visited_plots)


@pytest.mark.parametrize(
    "filename,steps,output",
    [
        ("example.txt", 6, 16),
        ("example.txt", 7, 21),
        ("example.txt", 64, 42),
        ("input.txt", 64, 3758),
        # ("input-p2-l.txt", 65, 3848),
        # ("input-p2-l.txt", 64, 3758),
        # ("input-p2-r.txt", 65, 3848),
        # ("input-p2-r.txt", 64, 3758),
        # ("input-p2-t.txt", 65, 3848),
        # ("input-p2-t.txt", 64, 3758),
        # ("input-p2-b.txt", 65, 3848),
        # ("input-p2-b.txt", 64, 3758),
        # ("input-p2-tl.txt", 65, 3848),
        # ("input-p2-tl.txt", 64, 3758),
        # ("input-p2-tr.txt", 65, 3848),
        # ("input-p2-tr.txt", 64, 3758),
        # ("input-p2-bl.txt", 65, 3848),
        # ("input-p2-bl.txt", 64, 3758),
        # ("input-p2-br.txt", 65, 3848),
        # ("input-p2-br.txt", 64, 3758),
    ],
)
def test_part_1(
    filename: str,
    steps: int,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines(), steps) == output
