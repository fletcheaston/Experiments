from collections import Counter

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 14: Parabolic Reflector Dish"])


DOCUMENT_EXAMPLE = [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#....",
]


def tilt_left(line: str) -> str:
    rock_map: Counter[int, int] = Counter({0: 0})
    square_rock_map: list[int] = [-1]
    current_index = 0

    rock_line: list[str] = []

    for index, character in enumerate(line):
        if character == "#":
            current_index += 1
            rock_line.append("#")
            square_rock_map.append(index)

        elif character == ".":
            rock_line.append(".")

        elif character == "O":
            rock_map[current_index] += 1
            rock_line.append(".")

    for index, square_rock_index in enumerate(square_rock_map):
        round_rocks = rock_map[index]

        for offset in range(round_rocks):
            rock_line[square_rock_index + offset + 1] = "O"

    return "".join(rock_line)


@router.post("/part-1")
async def year_2023_day_14_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

    The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction.
    If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

    This system must be what provides the energy for the lava!
    If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

    Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish.
    The platform is covered in large rocks of various shapes.
    Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

    In short: if you move the rocks, you can focus the dish.
    The platform even has a control panel on the side that lets you **tilt** it in one of four directions!
    The rounded rocks (`O`) will roll when the platform is tilted, while the cube-shaped rocks (`#`) will stay in place.
    You note the positions of all of the empty spaces (`.`) and rocks (your puzzle input).
    For example:

    ```
    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
    ```

    Start by tilting the lever so all of the rocks will slide **north** as far as they will go:

    ```
    OOOO.#.O..
    OO..#....#
    OO..O##..O
    O..#.OO...
    ........#.
    ..#....#.#
    ..O..#.O.O
    ..O.......
    #....###..
    #....#....
    ```

    You notice that the support beams along the north side of the platform are **damaged**;
    to ensure the platform doesn't collapse, you should calculate the **total load** on the north support beams.

    The amount of load caused by a single rounded rock (`O`) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on.
    (Cube-shaped rocks (`#`) don't contribute to load.)
    So, the amount of load caused by each rock in each row is as follows:

    ```
    OOOO.#.O.. 10
    OO..#....#  9
    OO..O##..O  8
    O..#.OO...  7
    ........#.  6
    ..#....#.#  5
    ..O..#.O.O  4
    ..O.......  3
    #....###..  2
    #....#....  1
    ```

    The total load is the sum of the load caused by all of the **rounded rocks**.
    In this example, the total load is **`136`**.

    Tilt the platform so that the rounded rocks all roll north.
    Afterward, **what is the total load on the north support beams?**
    """
    total = 0

    line_size = len(document[0])
    lines: list[str] = ["" for _ in range(line_size)]

    for line in document:
        for index, character in enumerate(line):
            lines[index] += character

    for index, line in enumerate(lines):
        lines[index] = tilt_left(line)

    for row_index in range(line_size):
        line_total = 0

        for line in lines:
            if line[row_index] == "O":
                line_total += 1

        line_total *= line_size - row_index
        total += line_total

    return total


def rotate_90(raw_lines: list[str]) -> list[str]:
    # Rotates 90 degrees clockwise
    line_size = len(raw_lines[0])
    lines: list[str] = ["" for _ in range(line_size)]

    for line in raw_lines:
        for index, character in enumerate(reversed(line)):
            lines[index] += character

    return lines


def rotate_180(raw_lines: list[str]) -> list[str]:
    new_lines = raw_lines.copy()

    for _ in range(2):
        new_lines = rotate_90(new_lines)

    return new_lines


def rotate_270(raw_lines: list[str]) -> list[str]:
    new_lines = raw_lines.copy()

    for _ in range(3):
        new_lines = rotate_90(new_lines)

    return new_lines


@router.post("/part-2")
async def year_2023_day_14_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    The parabolic reflector dish deforms, but not in a way that focuses the beam.
    To do that, you'll need to move the rocks to the edges of the platform.
    Fortunately, a button on the side of the control panel labeled "**spin cycle**" attempts to do just that!

    Each **cycle** tilts the platform four times so that the rounded rocks roll **north**, then **west**, then **south**, then **east**.
    After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction.
    After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

    Here's what happens in the example above after each of the first few cycles:

    After 1 cycle:

    ```
    .....#....
    ....#...O#
    ...OO##...
    .OO#......
    .....OOO#.
    .O#...O#.#
    ....O#....
    ......OOOO
    #...O###..
    #..OO#....
    ```

    After 2 cycles:

    ```
    .....#....
    ....#...O#
    .....##...
    ..O#......
    .....OOO#.
    .O#...O#.#
    ....O#...O
    .......OOO
    #..OO###..
    #.OOO#...O
    ```

    After 3 cycles:

    ```
    .....#....
    ....#...O#
    .....##...
    ..O#......
    .....OOO#.
    .O#...O#.#
    ....O#...O
    .......OOO
    #...O###.O
    #.OOO#...O
    ```

    This process should work if you leave it running long enough, but you're still worried about the north support beams.
    To make sure they'll survive for a while, you need to calculate the **total load** on the north support beams after `1000000000` cycles.

    In the above example, after `1000000000` cycles, the total load on the north support beams is **`64`**.

    Run the spin cycle for `1000000000` cycles.
    Afterward, **what is the total load on the north support beams?**
    """
    size = 1_000_000_000

    counter = 0
    cycle_repeats: int | None = None
    cycle_counter: dict[str, int] = {}
    cycles: dict[int, list[str]] = {}

    while counter < size:
        north = [tilt_left(line) for line in rotate_90(document)]
        west = [tilt_left(line) for line in rotate_270(north)]
        south = [tilt_left(line) for line in rotate_270(west)]
        east = [tilt_left(line) for line in rotate_270(south)]

        cycled = rotate_180(east)

        cycles[counter] = cycled

        cycle_key = "".join(cycled)

        if cycle_key in cycle_counter:
            cycle_repeats = cycle_counter[cycle_key]
            break

        else:
            cycle_counter[cycle_key] = counter

        counter += 1
        document = cycled

    if cycle_repeats is None:
        last_cycle = cycles[counter - 1]
    else:
        final_cycle = (
            cycle_repeats + (size - cycle_repeats) % (counter - cycle_repeats) - 1
        )
        last_cycle = cycles[final_cycle]

    total = 0

    for index, line in enumerate(last_cycle):
        total += line.count("O") * (len(last_cycle) - index)

    return total
