import math

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 8: Title"])


DOCUMENT_EXAMPLE = []


@router.post("/part-1")
async def year_2023_day_8_part_1(
    instructions: str = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    steps = 0
    current_step = "AAA"

    maps: dict[str, tuple[str, str]] = {}

    # Iterate over lines
    for line in document:
        start, rest = line.split(" = ")
        left, right = rest.replace("(", "").replace(")", "").split(", ")

        maps[start] = (left, right)

    while current_step != "ZZZ":
        instruction = instructions[steps % len(instructions)]

        if instruction == "L":
            current_step = maps[current_step][0]

        elif instruction == "R":
            current_step = maps[current_step][1]

        steps += 1

    return steps


@router.post("/part-2")
async def year_2023_day_8_part_2(
    instructions: str = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    steps: list[str] = []
    maps: dict[str, tuple[str, str]] = {}

    # Iterate over lines
    for index, line in enumerate(document):
        start, rest = line.split(" = ")
        left, right = rest.replace("(", "").replace(")", "").split(", ")

        maps[start] = (left, right)

        if start.endswith("A"):
            steps.append(start)

    steps_index = 0
    cycles = []

    while True:
        for index, previous_step in enumerate(steps):
            current_step = maps[previous_step]
            next_step = (
                current_step[0]
                if instructions[steps_index % len(instructions)] == "L"
                else current_step[1]
            )

            if next_step.endswith("Z"):
                cycles.append(steps_index + 1)

            steps[index] = next_step

        if len(cycles) == len(steps):
            break

        steps_index += 1

    return math.lcm(*cycles)
