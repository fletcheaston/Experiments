from fastapi import APIRouter

from . import day_1

router = APIRouter()

router.include_router(day_1.router, prefix="/day-1")
