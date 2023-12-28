from dataclasses import dataclass, field
from itertools import combinations

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 11: Cosmic Expansion"])


DOCUMENT_EXAMPLE = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]


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


@router.post("/part-1")
async def year_2023_day_11_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    You continue following signs for "Hot Springs" and eventually come across an observatory.
    The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

    He doesn't know anything about the missing machine parts; he's only visiting for this research project.
    However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

    Maybe you can help him with the analysis to speed things up?

    The researcher has collected a bunch of data and compiled the data into a single giant **image** (your puzzle input).
    The image includes **empty space** (`.`) and **galaxies** (`#`).
    For example:

    ```
    ...#......
    .......#..
    #.........
    ..........
    ......#...
    .#........
    .........#
    ..........
    .......#..
    #...#.....
    ```

    The researcher is trying to figure out the sum of the lengths of the **shortest path between every pair of galaxies**.
    However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

    Due to something involving gravitational effects, **only some space expands**.
    In fact, the result is that **any rows or columns that contain no galaxies** should all actually be twice as big.

    In the above example, three columns and two rows contain no galaxies:

    ```
       v  v  v
     ...#......
     .......#..
     #.........
    >..........<
     ......#...
     .#........
     .........#
    >..........<
     .......#..
     #...#.....
       ^  ^  ^
    ```

    These rows and columns need to be **twice as big**; the result of cosmic expansion therefore looks like this:

    ```
    ....#........
    .........#...
    #............
    .............
    .............
    ........#....
    .#...........
    ............#
    .............
    .............
    .........#...
    #....#.......
    ```

    Equipped with this expanded universe, the shortest path between every pair of galaxies can be found.
    It can help to assign every galaxy a unique number:

    ```
    ....1........
    .........2...
    3............
    .............
    .............
    ........4....
    .5...........
    ............6
    .............
    .............
    .........7...
    8....9.......
    ```

    In these 9 galaxies, there are **36 pairs**.
    Only count each pair once; order within the pair doesn't matter.
    For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one `.` or `#` at a time.
    (The shortest path between two galaxies is allowed to pass through another galaxy.)

    For example, here is one of the shortest paths between galaxies `5` and `9`:

    ```
    ....1........
    .........2...
    3............
    .............
    .............
    ........4....
    .5...........
    .##.........6
    ..##.........
    ...##........
    ....##...7...
    8....9.......
    ```

    This path has length **`9`** because it takes a minimum of **nine steps** to get from galaxy `5` to galaxy `9` (the eight locations marked `#` plus the step onto galaxy `9` itself).
    Here are some other example shortest path lengths:

    Between galaxy `1` and galaxy `7`: `15`
    Between galaxy `3` and galaxy `6`: `17`
    Between galaxy `8` and galaxy `9`: `5`

    In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is **`374`**.

    Expand the universe, then find the length of the shortest path between every pair of galaxies.
    **What is the sum of these lengths?**
    """
    grid = Grid(
        space=[list(line) for line in document],
        displacement=2,
    )

    grid.expand()

    grid.pair_galaxies()

    return grid.calculate_galaxy_combo_distances()


@router.post("/part-2")
async def year_2023_day_11_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    The galaxies are much **older** (and thus much **farther apart**) than the researcher initially estimated.

    Now, instead of the expansion you did before, make each empty row or column **one million times** larger.
    That is, each empty row should be replaced with `1000000` empty rows, and each empty column should be replaced with `1000000` empty columns.

    (In the example above, if each empty row or column were merely `10` times larger, the sum of the shortest paths between every pair of galaxies would be **`1030`**.
    If each empty row or column were merely `100` times larger, the sum of the shortest paths between every pair of galaxies would be **`8410`**.
    However, your universe will need to expand far beyond these values.)

    Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies.
    **What is the sum of these lengths?**
    """
    grid = Grid(
        space=[list(line) for line in document],
        displacement=1000000,
    )

    grid.expand()

    grid.pair_galaxies()

    return grid.calculate_galaxy_combo_distances()
