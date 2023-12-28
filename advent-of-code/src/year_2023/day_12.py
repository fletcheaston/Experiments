from functools import cache

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 12: Hot Springs"])


DOCUMENT_EXAMPLE = [
    "#.#.### 1,1,3",
    ".#...#....###. 1,1,3",
    ".#.###.#.###### 1,3,1,6",
    "####.#...#... 4,1,1",
    "#....######..#####. 1,6,5",
    ".###.##....# 3,2,1",
]


@cache
def count_arrangements(springs: str, counts: tuple[int]) -> int:
    # Base cases
    # Valid arranements only exist for no springs and no counts left
    if not springs:
        if not counts:
            return 1

        return 0

    current_spring = springs[0]

    if current_spring == "#":
        # Not enough space, invalid arrangement
        if not counts or len(springs) < counts[0]:
            return 0

        # Not enough sprints for first value, invalid arrangement
        if "." in springs[0 : counts[0]]:
            return 0

        # Too many springs for first value, invalid arrangement
        if springs[counts[0] :].startswith("#"):
            return 0

        if len(springs) > counts[0]:
            # Recursive case 1
            # Try the next arrangement with the next springs/counts
            if springs[counts[0]] == "?":
                return count_arrangements(
                    springs[counts[0] + 1 :].lstrip("."),
                    counts[1:],
                )

        # Recursive case 2
        # We have enough springs to try more arrangements
        return count_arrangements(springs[counts[0] :].lstrip("."), counts[1:])

    elif current_spring == ".":
        # Recursive case 3
        # Continue with the empty space
        return count_arrangements(springs.lstrip("."), counts)

    # Recursive case 4
    # Unknown, try both # and .
    total = count_arrangements("#" + springs[1:], counts)
    total += count_arrangements("." + springs[1:], counts)
    return total


@router.post("/part-1")
async def year_2023_day_12_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

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

    for index, line in enumerate(document):
        springs, count_str = line.split(" ")
        counts = [int(value) for value in count_str.split(",")]

        unfolded_counts = counts * 5
        unfolded_springs = "?".join([springs] * 5)

        total += count_arrangements(unfolded_springs, tuple(unfolded_counts))

    return total
