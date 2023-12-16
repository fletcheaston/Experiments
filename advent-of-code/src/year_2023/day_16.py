from dataclasses import dataclass, field
from typing import Literal

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 16: Title"])


DOCUMENT_EXAMPLE = []


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


@dataclass(frozen=True)
class Beam:
    x_direction: Literal[-1, 0, 1]
    y_direction: Literal[-1, 0, 1]

    def __post_init__(self) -> None:
        assert abs(self.x_direction) != abs(self.y_direction)


def default_beam_grid() -> dict[Coordinate, list[Beam]]:
    return {
        Coordinate(x=0, y=0): [
            Beam(
                x_direction=1,
                y_direction=0,
            )
        ]
    }


def default_energized_grid() -> dict[Coordinate, set[Beam]]:
    return {Coordinate(x=0, y=0): set()}


@dataclass
class Grid:
    grid: dict[Coordinate, str] = field(default_factory=dict)
    beam_grid: dict[Coordinate, list[Beam]] = field(default_factory=default_beam_grid)
    energized_grid: dict[Coordinate, set[Beam]] = field(
        default_factory=default_energized_grid
    )

    max_x: int = 0
    max_y: int = 0

    def add_coordinate(self, *, x: int, y: int, character: str) -> None:
        self.max_x = max(self.max_x, x + 1)
        self.max_y = max(self.max_y, y + 1)

        self.grid[Coordinate(x=x, y=y)] = character

    def start(self, coordinate: Coordinate, beam: Beam) -> None:
        self.beam_grid = {coordinate: [beam]}
        self.energized_grid = {coordinate: set()}

    def step(self) -> None:
        new_beam_grid: dict[Coordinate, list[Beam]] = {}

        for coordinate, beams in self.beam_grid.items():
            if not beams:
                # No beams left in coordinate, just skip
                continue

            if coordinate not in self.grid:
                # Coordinate outside of the grid, beam has left the grid and can no longer return
                continue

            for beam in beams:
                if self.grid[coordinate] == ".":
                    # Move the beam in the direction it was going
                    new_coordinate = Coordinate(
                        x=coordinate.x + beam.x_direction,
                        y=coordinate.y + beam.y_direction,
                    )

                    if new_coordinate not in new_beam_grid:
                        new_beam_grid[new_coordinate] = []

                    new_beam_grid[new_coordinate].append(beam)

                elif self.grid[coordinate] == "|":
                    if beam.y_direction in [-1, 1]:
                        # Keep the beam moving
                        new_coordinate = Coordinate(
                            x=coordinate.x + beam.x_direction,
                            y=coordinate.y + beam.y_direction,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(beam)

                    elif beam.x_direction in [-1, 1]:
                        # Split the beam to go up
                        new_coordinate_up = Coordinate(
                            x=coordinate.x,
                            y=coordinate.y - 1,
                        )

                        if new_coordinate_up not in new_beam_grid:
                            new_beam_grid[new_coordinate_up] = []

                        new_beam_grid[new_coordinate_up].append(
                            Beam(
                                x_direction=0,
                                y_direction=-1,
                            )
                        )

                        # Split the beam to go down
                        new_coordinate_down = Coordinate(
                            x=coordinate.x,
                            y=coordinate.y + 1,
                        )

                        if new_coordinate_down not in new_beam_grid:
                            new_beam_grid[new_coordinate_down] = []

                        new_beam_grid[new_coordinate_down].append(
                            Beam(
                                x_direction=0,
                                y_direction=1,
                            )
                        )

                elif self.grid[coordinate] == "-":
                    if beam.x_direction in [-1, 1]:
                        # Keep the beam moving
                        new_coordinate = Coordinate(
                            x=coordinate.x + beam.x_direction,
                            y=coordinate.y + beam.y_direction,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(beam)

                    elif beam.y_direction in [-1, 1]:
                        # Split the beam to go left
                        new_coordinate_up = Coordinate(
                            x=coordinate.x - 1,
                            y=coordinate.y,
                        )

                        if new_coordinate_up not in new_beam_grid:
                            new_beam_grid[new_coordinate_up] = []

                        new_beam_grid[new_coordinate_up].append(
                            Beam(
                                x_direction=-1,
                                y_direction=0,
                            )
                        )

                        # Split the beam to go right
                        new_coordinate_down = Coordinate(
                            x=coordinate.x + 1,
                            y=coordinate.y,
                        )

                        if new_coordinate_down not in new_beam_grid:
                            new_beam_grid[new_coordinate_down] = []

                        new_beam_grid[new_coordinate_down].append(
                            Beam(
                                x_direction=1,
                                y_direction=0,
                            )
                        )

                elif self.grid[coordinate] == "/":
                    if beam.x_direction == 1:
                        # Move the beam up
                        new_coordinate = Coordinate(
                            x=coordinate.x,
                            y=coordinate.y - 1,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(
                            Beam(
                                x_direction=0,
                                y_direction=-1,
                            )
                        )

                    elif beam.x_direction == -1:
                        # Move the beam down
                        new_coordinate = Coordinate(
                            x=coordinate.x,
                            y=coordinate.y + 1,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(
                            Beam(
                                x_direction=0,
                                y_direction=1,
                            )
                        )

                    elif beam.y_direction == 1:
                        # Move the beam left
                        new_coordinate = Coordinate(
                            x=coordinate.x - 1,
                            y=coordinate.y,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(
                            Beam(
                                x_direction=-1,
                                y_direction=0,
                            )
                        )

                    elif beam.y_direction == -1:
                        # Move the beam right
                        new_coordinate = Coordinate(
                            x=coordinate.x + 1,
                            y=coordinate.y,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(
                            Beam(
                                x_direction=1,
                                y_direction=0,
                            )
                        )

                elif self.grid[coordinate] == "\\":
                    if beam.x_direction == 1:
                        # Move the beam down
                        new_coordinate = Coordinate(
                            x=coordinate.x,
                            y=coordinate.y + 1,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(
                            Beam(
                                x_direction=0,
                                y_direction=1,
                            )
                        )

                    elif beam.x_direction == -1:
                        # Move the beam up
                        new_coordinate = Coordinate(
                            x=coordinate.x,
                            y=coordinate.y - 1,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(
                            Beam(
                                x_direction=0,
                                y_direction=-1,
                            )
                        )

                    elif beam.y_direction == 1:
                        # Move the beam right
                        new_coordinate = Coordinate(
                            x=coordinate.x + 1,
                            y=coordinate.y,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(
                            Beam(
                                x_direction=1,
                                y_direction=0,
                            )
                        )

                    elif beam.y_direction == -1:
                        # Move the beam left
                        new_coordinate = Coordinate(
                            x=coordinate.x - 1,
                            y=coordinate.y,
                        )

                        if new_coordinate not in new_beam_grid:
                            new_beam_grid[new_coordinate] = []

                        new_beam_grid[new_coordinate].append(
                            Beam(
                                x_direction=-1,
                                y_direction=0,
                            )
                        )

        # If we've seen this beam at this coordinate before in the energized grid, remove it
        cleaned_beam_grid: dict[Coordinate, list[Beam]] = {}

        # self.show_energized()

        for coordinate, beams in new_beam_grid.items():
            cleaned_beam_grid[coordinate] = []

            if coordinate in self.energized_grid:
                for beam in beams:
                    if beam in self.energized_grid[coordinate]:
                        pass

                    else:
                        self.energized_grid[coordinate].add(beam)
                        cleaned_beam_grid[coordinate].append(beam)

            elif coordinate in self.grid:
                if coordinate not in self.energized_grid:
                    self.energized_grid[coordinate] = set()

                self.energized_grid[coordinate].update(set(beams))
                cleaned_beam_grid[coordinate] = beams

        self.beam_grid = cleaned_beam_grid

    def count_energized(self) -> int:
        count = 0

        for coordinate in self.grid.keys():
            if coordinate in self.energized_grid:
                count += 1

        return count

    def show(self) -> None:
        print()

        all_lines = ""

        for y in range(self.max_y):
            line = ""

            for x in range(self.max_x):
                coordinate = Coordinate(x=x, y=y)

                if coordinate in self.beam_grid:
                    line += "\033[31m#\033[0m"
                elif coordinate in self.energized_grid:
                    line += "\033[32m#\033[0m"
                else:
                    line += self.grid[coordinate]

            all_lines += line
            all_lines += "\n"

        print(all_lines)

    def show_energized(self) -> None:
        print()

        for y in range(self.max_y):
            line = ""

            for x in range(self.max_x):
                coordinate = Coordinate(x=x, y=y)

                if coordinate in self.beam_grid:
                    line += f"\033[31m{self.grid[coordinate]}\033[0m"
                elif coordinate in self.energized_grid:
                    # line += f"\033[32m#\033[0m"
                    line += f"\033[32m{self.grid[coordinate]}\033[0m"
                else:
                    line += self.grid[coordinate]

            print(line)


@router.post("/part-1")
async def year_2023_day_16_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    grid = Grid()

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            grid.add_coordinate(x=x_index, y=y_index, character=character)

    grid.start(Coordinate(x=0, y=0), Beam(x_direction=1, y_direction=0))

    while grid.beam_grid:
        grid.step()

    return grid.count_energized()


@router.post("/part-2")
async def year_2023_day_16_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    grid = Grid()

    max_x = len(document[0])
    max_y = len(document)

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            grid.add_coordinate(x=x_index, y=y_index, character=character)

    max_energized = 0

    # Start from left moving right
    for y in range(max_y):
        grid.start(Coordinate(x=0, y=y), Beam(x_direction=1, y_direction=0))

        while grid.beam_grid:
            grid.step()

        max_energized = max(max_energized, grid.count_energized())

    # Start from right moving left
    for y in range(max_y):
        grid.start(Coordinate(x=max_x, y=y), Beam(x_direction=-1, y_direction=0))

        while grid.beam_grid:
            grid.step()

        max_energized = max(max_energized, grid.count_energized())

    # Start from top moving down
    for x in range(max_x):
        grid.start(Coordinate(x=x, y=0), Beam(x_direction=0, y_direction=1))

        while grid.beam_grid:
            grid.step()

        max_energized = max(max_energized, grid.count_energized())

    # Start from bottom moving up
    for x in range(max_x):
        grid.start(Coordinate(x=x, y=max_y), Beam(x_direction=0, y_direction=-1))

        while grid.beam_grid:
            grid.step()

        max_energized = max(max_energized, grid.count_energized())

    return max_energized
