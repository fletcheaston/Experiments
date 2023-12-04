from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 4: Title"])


DOCUMENT_EXAMPLE = []


@router.post("/part-1")
async def year_2023_day_4_part_1(
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


@router.post("/part-2")
async def year_2023_day_4_part_2(
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
