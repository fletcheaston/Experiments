from dataclasses import dataclass, field
from typing import Literal

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 16: The Floor Will Be Lava"])


DOCUMENT_EXAMPLE = [
    ".|...\\....",
    "|.-.\\.....",
    ".....|-....",
    "........|..",
    "...........",
    ".........\\",
    "..../.\\...",
    ".-.-/..|...",
    ".|....-|.\\",
    "..//.|.....",
]


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


@router.post("/part-1")
async def year_2023_day_16_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    # NOTE - Your input likely has invalid escape characters for Python to parse.

    With the beam of light completely focused **somewhere**, the reindeer leads you deeper still into the Lava Production Facility.
    At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

    Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead.
    There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

    Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing **empty space** (`.`), **mirrors** (`/` and `\`), and **splitters** (`|` and `-`).

    The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into **heat** to melt the rock in the cavern.

    You note the layout of the contraption (your puzzle input).
    For example:

    ```
    .|...\....
    |.-.\.....
    .....|-...
    ........|.
    ..........
    .........\\
    ..../.\\\..
    .-.-/..|..
    .|....-|.\\
    ..//.|....
    ```

    The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

    - If the beam encounters **empty space** (`.`), it continues in the same direction.
    - If the beam encounters a **mirror** (`/` or `\`), the beam is **reflected** 90 degrees depending on the angle of the mirror.
      For instance, a rightward-moving beam that encounters a `/` mirror would continue **upward** in the mirror's column, while a rightward-moving beam that encounters a `\` mirror would continue **downward** from the mirror's column.
    - If the beam encounters the **pointy end of a splitter** (`|` or `-`), the beam passes through the splitter as if the splitter were **empty space**.
      For instance, a rightward-moving beam that encounters a `-` splitter would continue in the same direction.
    - If the beam encounters the **flat side of a splitter** (`|` or `-`), the beam is **split into two beams** going in each of the two directions the splitter's pointy ends are pointing.
      For instance, a rightward-moving beam that encounters a `|` splitter would split into two beams: one that continues **upward** from the splitter's column and one that continues **downward** from the splitter's column.

    Beams do not interact with other beams; a tile can have many beams passing through it at the same time.
    A tile is **energized** if that tile has at least one beam pass through it, reflect in it, or split in it.

    In the above example, here is how the beam of light bounces around the contraption:

    ```
    >|<<<\....
    |v-.\^....
    .v...|->>>
    .v...v^.|.
    .v...v^...
    .v...v^..\\
    .v../2\\\..
    <->-/vv|..
    .|<<<2-|.\\
    .v//.|.v..
    ```

    Beams are only shown on empty tiles; arrows indicate the direction of the beams.
    If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead.
    Here is the same diagram but instead only showing whether a tile is **energized** (`#`) or not (`.`):

    ```
    ######....
    .#...#....
    .#...#####
    .#...##...
    .#...##...
    .#...##...
    .#..####..
    ########..
    .#######..
    .#...#.#..
    ```

    Ultimately, in this example, **`46`** tiles become **energized**.

    The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation.
    With the beam starting in the top-left heading right, **how many tiles end up being energized?**
    """
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
    """
    # NOTE - Your input likely has invalid escape characters for Python to parse.

    As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel.
    There, a collection of buttons lets you align the contraption so that the beam enters from **any edge tile** and heading away from that edge.
    (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

    So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left).
    To produce lava, you need to find the configuration that **energizes as many tiles as possible**.

    In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

    ```
    .|<2<\....
    |v-v\^....
    .v.v.|->>>
    .v.v.v^.|.
    .v.v.v^...
    .v.v.v^..\\
    .v.v/2\\\..
    <-2-/vv|..
    .|<<<2-|.\\
    .v//.|.v..
    ```

    Using this configuration, **`51`** tiles are energized:

    ```
    .#####....
    .#.#.#....
    .#.#.#####
    .#.#.##...
    .#.#.##...
    .#.#.##...
    .#.#####..
    ########..
    .#######..
    .#...#.#..
    ```

    Find the initial beam configuration that energizes the largest number of tiles; **how many tiles are energized in that configuration?**
    """
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
