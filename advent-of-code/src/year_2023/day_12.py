from functools import cache

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 12: Title"])


DOCUMENT_EXAMPLE = []


@cache
def count_arrangements(springs: str, counts: tuple[int]) -> int:
    # Base case
    if not springs:
        if not counts:
            return 1

        return 0

    # Recursive
    current_spring = springs[0]

    if current_spring == "#":
        if not counts or len(springs) < counts[0]:
            return 0

        if "." in springs[0 : counts[0]]:
            return 0

        if springs[counts[0] :].startswith("#"):
            return 0

        if len(springs) > counts[0]:
            if springs[counts[0]] == "?":
                return count_arrangements(
                    springs[counts[0] + 1 :].lstrip("."), counts[1:]
                )

        return count_arrangements(springs[counts[0] :].lstrip("."), counts[1:])

    elif current_spring == ".":
        return count_arrangements(springs.lstrip("."), counts)

    return count_arrangements("#" + springs[1:], counts) + count_arrangements(
        "." + springs[1:], counts
    )


@router.post("/part-1")
async def year_2023_day_12_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for index, line in enumerate(document):
        springs, count_str = line.split(" ")
        counts = [int(value) for value in count_str.split(",")]

        total += count_arrangements(springs, tuple(counts))

    return total


@router.post("/part-2")
async def year_2023_day_12_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for index, line in enumerate(document):
        springs, count_str = line.split(" ")
        counts = [int(value) for value in count_str.split(",")]

        unfolded_counts = counts * 5
        unfolded_springs = "?".join([springs] * 5)

        total += count_arrangements(unfolded_springs, tuple(unfolded_counts))

    return total
