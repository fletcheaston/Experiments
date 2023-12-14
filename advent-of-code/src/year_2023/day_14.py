from collections import Counter

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 14: Title"])


DOCUMENT_EXAMPLE = []


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


def transpose_90(raw_lines: list[str]) -> list[str]:
    # Rotates 90 degrees clockwise
    line_size = len(raw_lines[0])
    lines: list[str] = ["" for _ in range(line_size)]

    for line in raw_lines:
        for index, character in enumerate(reversed(line)):
            lines[index] += character

    return lines


def transpose_180(raw_lines: list[str]) -> list[str]:
    new_lines = raw_lines.copy()

    for _ in range(2):
        new_lines = transpose_90(new_lines)

    return new_lines


def transpose_270(raw_lines: list[str]) -> list[str]:
    new_lines = raw_lines.copy()

    for _ in range(3):
        new_lines = transpose_90(new_lines)

    return new_lines


@router.post("/part-2")
async def year_2023_day_14_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    size = 1_000_000_000

    counter = 0
    cycle_repeats: int | None = None
    cycle_counter: dict[str, int] = {}
    cycles: dict[int, list[str]] = {}

    while counter < size:
        north = [tilt_left(line) for line in transpose_90(document)]
        west = [tilt_left(line) for line in transpose_270(north)]
        south = [tilt_left(line) for line in transpose_270(west)]
        east = [tilt_left(line) for line in transpose_270(south)]

        cycled = transpose_180(east)

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
