import math

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 6: Wait For It"])


@router.post("/part-1")
async def year_2023_day_6_part_1(
    times: list[int] = Body(
        ...,
        embed=True,
        examples=[[7, 15, 30]],
    ),
    distances: list[int] = Body(
        ...,
        embed=True,
        examples=[[9, 40, 200]],
    ),
) -> int:
    total: int = 1

    for time, distance in zip(times, distances):
        minimum_time = math.floor(
            (-time + math.sqrt(time**2 - 4 * -1 * -distance)) / -2 + 1
        )
        maximum_time = math.ceil(
            (-time - math.sqrt(time**2 - 4 * -1 * -distance)) / -2 - 1
        )

        total *= maximum_time - minimum_time + 1

    return total


@router.post("/part-2")
async def year_2023_day_6_part_2(
    time: int = Body(
        ...,
        embed=True,
        examples=[71530],
    ),
    distance: int = Body(
        ...,
        embed=True,
        examples=[940200],
    ),
) -> int:
    minimum_time = math.floor(
        (-time + math.sqrt(time**2 - 4 * -1 * -distance)) / -2 + 1
    )
    maximum_time = math.ceil((-time - math.sqrt(time**2 - 4 * -1 * -distance)) / -2 - 1)

    return maximum_time - minimum_time + 1
