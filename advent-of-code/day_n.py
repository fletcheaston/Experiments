from fastapi import APIRouter

from src.types import Lines

router = APIRouter(tags=["20XX - Day N: Title"])


@router.post("/part-1")
async def year_20xx_day_n_part_1(lines: Lines) -> int:
    """ """
    total = 0

    # Iterate over lines
    for line in lines:
        pass

    return total


@router.post("/part-2")
async def year_20xx_day_n_part_2(lines: Lines) -> int:
    """ """
    total = 0

    # Iterate over lines
    for line in lines:
        pass

    return total
