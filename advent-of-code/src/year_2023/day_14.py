from collections import Counter

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 14: Title"])


DOCUMENT_EXAMPLE = []


def tilt(line: str) -> str:
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

    # Iterate over lines
    for line in document:
        for index, character in enumerate(line):
            lines[index] += character

    for index, line in enumerate(lines):
        lines[index] = tilt(line)

    for row_index in range(line_size):
        line_total = 0

        for line in lines:
            if line[row_index] == "O":
                line_total += 1

        line_total *= line_size - row_index
        total += line_total

    return total


@router.post("/part-2")
async def year_2023_day_14_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for line in document:
        pass

    return total
