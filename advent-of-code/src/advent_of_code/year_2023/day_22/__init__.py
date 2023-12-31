import bisect
import uuid
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

import pytest


@dataclass(frozen=True)
class GridCoordinate:
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


@dataclass
class BrickCoordinate:
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


@dataclass
class Brick:
    start: BrickCoordinate
    end: BrickCoordinate
    id: uuid.UUID | str = field(default_factory=uuid.uuid4)

    @property
    def min_x(self) -> int:
        return min(self.start.x, self.end.x)

    @property
    def max_x(self) -> int:
        return max(self.start.x, self.end.x)

    @property
    def min_y(self) -> int:
        return min(self.start.y, self.end.y)

    @property
    def max_y(self) -> int:
        return max(self.start.y, self.end.y)

    @property
    def min_z(self) -> int:
        return min(self.start.z, self.end.z)

    @property
    def max_z(self) -> int:
        return max(self.start.z, self.end.z)

    @property
    def coordinates(self) -> list[GridCoordinate]:
        for x in range(self.start.x, self.end.x + 1):
            for y in range(self.start.y, self.end.y + 1):
                for z in range(self.start.z, self.end.z + 1):
                    yield GridCoordinate(x=x, y=y, z=z)

    def lower(self) -> None:
        self.start.z -= 1
        self.end.z -= 1

    def __repr__(self) -> str:
        return (
            f"id: {self.id} | start: {self.start}, | end: {self.end} | z: {self.min_z}"
        )

    def __lt__(self, other: "Brick") -> bool:
        return self.min_z < other.min_z


@dataclass
class CubeGrid:
    bricks: list[Brick] = field(default_factory=list)
    brick_map: dict[uuid.UUID, Brick] = field(default_factory=dict)
    grid: dict[GridCoordinate, uuid.UUID] = field(default_factory=dict)
    cannot_disintegrate: set[uuid.UUID] = field(default_factory=set)

    def add(self, brick: Brick) -> None:
        # Add to grid
        for coordinate in brick.coordinates:
            self.grid[coordinate] = brick.id

        # Add to map
        self.brick_map[brick.id] = brick

        # Add to list in-order
        bisect.insort(self.bricks, brick)

    def remove(self, brick_id: uuid.UUID) -> None:
        brick = self.brick_map[brick_id]

        # Remove from grid
        for coordinate in brick.coordinates:
            del self.grid[coordinate]

        # Remove from map
        del self.brick_map[brick.id]

        # Remove from list
        self.bricks.remove(brick)

    def can_lower(self, brick: Brick) -> bool:
        if brick.min_z == 1:
            return False

        for x in range(brick.min_x, brick.max_x + 1):
            for y in range(brick.min_y, brick.max_y + 1):
                coordinate = GridCoordinate(x=x, y=y, z=brick.min_z - 1)

                if coordinate in self.grid:
                    return False

        return True

    def lower(self, brick: Brick) -> None:
        for x in range(brick.min_x, brick.max_x + 1):
            for y in range(brick.min_y, brick.max_y + 1):
                self.grid[GridCoordinate(x=x, y=y, z=brick.min_z - 1)] = brick.id

                del self.grid[GridCoordinate(x=x, y=y, z=brick.max_z)]

        brick.lower()

    def compact(self) -> int:
        brick_ids_lowered: set[uuid.UUID] = set()

        for brick in self.bricks:
            while self.can_lower(brick):
                self.lower(brick)
                brick_ids_lowered.add(brick.id)

        # Resort bricks
        self.bricks.sort()

        return len(brick_ids_lowered)

    def check_below(self, brick: Brick) -> None:
        brick_ids_below: set[uuid.UUID] = set()

        for x in range(brick.min_x, brick.max_x + 1):
            for y in range(brick.min_y, brick.max_y + 1):
                coordinate = GridCoordinate(x=x, y=y, z=brick.min_z - 1)

                if coordinate in self.grid:
                    brick_ids_below.add(self.grid[coordinate])

        if len(brick_ids_below) == 1:
            self.cannot_disintegrate.add(brick_ids_below.pop())

    def count_bricks_can_disintegrate(self) -> int:
        for brick in self.bricks:
            self.check_below(brick)

        return len(self.bricks) - len(self.cannot_disintegrate)


def part_1(document: list[str]) -> int:
    grid = CubeGrid()

    for index, line in enumerate(document):
        first, second = line.split("~")

        first_x, first_y, first_z = first.split(",")
        second_x, second_y, second_z = second.split(",")

        start = BrickCoordinate(x=int(first_x), y=int(first_y), z=int(first_z))
        end = BrickCoordinate(x=int(second_x), y=int(second_y), z=int(second_z))

        grid.add(Brick(start=start, end=end))

    grid.compact()

    return grid.count_bricks_can_disintegrate()


def part_2(document: list[str]) -> int:
    grid = CubeGrid()

    for index, line in enumerate(document):
        first, second = line.split("~")

        first_x, first_y, first_z = first.split(",")
        second_x, second_y, second_z = second.split(",")

        start = BrickCoordinate(x=int(first_x), y=int(first_y), z=int(first_z))
        end = BrickCoordinate(x=int(second_x), y=int(second_y), z=int(second_z))

        grid.add(Brick(start=start, end=end))

    grid.compact()
    grid.count_bricks_can_disintegrate()

    # Get all the bricks that would cause other bricks to fall
    brick_ids = grid.cannot_disintegrate
    count = 0

    for brick_id in brick_ids:
        new_grid = deepcopy(grid)
        new_grid.remove(brick_id)
        fall_count = new_grid.compact()
        count += fall_count

    return count


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 5),
        ("input.txt", 471),
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
        ("example-1.txt", 7),
        # ("input.txt", 68525),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
