import io

from fastapi import APIRouter, UploadFile

router = APIRouter(tags=["20XX - Day N: Title"])


@router.post("/part-1")
async def year_20xx_day_n_part_1(document: UploadFile) -> int:
    """ """
    total = 0

    # Iterate over lines
    with document.file as file:
        for line in io.TextIOWrapper(file, encoding="utf-8"):
            pass

    return total


@router.post("/part-2")
async def year_20xx_day_n_part_2(document: UploadFile) -> int:
    """ """
    total = 0

    # Iterate over lines
    with document.file as file:
        for line in io.TextIOWrapper(file, encoding="utf-8"):
            pass

    return total
