from fastapi import APIRouter

from . import year_2022, year_2023

router = APIRouter()

router.include_router(year_2023.router, prefix="/2023")
router.include_router(year_2022.router, prefix="/2022")
