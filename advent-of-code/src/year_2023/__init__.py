from fastapi import APIRouter

from . import (
    day_1,
    day_2,
    day_3,
    day_4,
    day_5,
    day_6,
    day_7,
    day_8,
    day_9,
    day_10,
    day_11,
    day_12,
    day_13,
    day_14,
    day_15,
    day_16,
    day_17,
    day_18,
    day_19,
    day_20,
    day_21,
    day_22,
)

router = APIRouter()

router.include_router(day_1.router, prefix="/day-1")
router.include_router(day_2.router, prefix="/day-2")
router.include_router(day_3.router, prefix="/day-3")
router.include_router(day_4.router, prefix="/day-4")
router.include_router(day_5.router, prefix="/day-5")
router.include_router(day_6.router, prefix="/day-6")
router.include_router(day_7.router, prefix="/day-7")
router.include_router(day_8.router, prefix="/day-8")
router.include_router(day_9.router, prefix="/day-9")
router.include_router(day_10.router, prefix="/day-10")
router.include_router(day_11.router, prefix="/day-11")
router.include_router(day_12.router, prefix="/day-12")
router.include_router(day_13.router, prefix="/day-13")
router.include_router(day_14.router, prefix="/day-14")
router.include_router(day_15.router, prefix="/day-15")
router.include_router(day_16.router, prefix="/day-16")
router.include_router(day_17.router, prefix="/day-17")
router.include_router(day_18.router, prefix="/day-18")
router.include_router(day_19.router, prefix="/day-19")
router.include_router(day_20.router, prefix="/day-20")
router.include_router(day_21.router, prefix="/day-21")
router.include_router(day_22.router, prefix="/day-22")
