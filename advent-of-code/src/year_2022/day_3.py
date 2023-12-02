import string

from fastapi import APIRouter

from src.types import Lines
from src.utils import chunks

router = APIRouter(tags=["2022 - Day 3: Rucksack Reorganization"])

ITEM_TO_PRIORITY: dict[str, int] = {
    **{char: index + 1 for index, char in enumerate(string.ascii_lowercase)},
    **{char: index + 27 for index, char in enumerate(string.ascii_uppercase)},
}


@router.post("/part-1")
async def year_2022_day_3_part_1(lines: Lines) -> int:
    total = 0

    # Iterate over lines
    for line in lines:
        first_compartment = line[: len(line) // 2]
        second_compartment = line[len(line) // 2 :]

        # Find the one duplicate item
        duplicate_item: str | None = None

        for item in first_compartment:
            if item in second_compartment:
                duplicate_item = item

        # Total up the priority
        total += ITEM_TO_PRIORITY[duplicate_item]

    return total


@router.post("/part-2")
async def year_2022_day_3_part_2(lines: Lines) -> int:
    total = 0

    # Iterate over lines
    for line_1, line_2, line_3 in chunks(lines, 3):
        # Convert each line to a set of items and get the intersections
        duplicates = set(line_1).intersection((set(line_2))).intersection((set(line_3)))

        badge = duplicates.pop()

        # Total up the priority
        total += ITEM_TO_PRIORITY[badge]

    return total
