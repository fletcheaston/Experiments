from fastapi import APIRouter

from . import year_2023

router = APIRouter()

router.include_router(year_2023.router, prefix="/2023")
