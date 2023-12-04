from fastapi import APIRouter, Body

router = APIRouter(tags=["20XX - Day N: Title"])


DOCUMENT_EXAMPLE = []


@router.post("/part-1")
async def year_20xx_day_n_part_1(
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
async def year_20xx_day_n_part_2(
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
