from dataclasses import dataclass
from functools import cache

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 21: Title"])


DOCUMENT_EXAMPLE = []


OFFSETS: list[tuple[int, int]] = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"


@router.post("/part-1")
async def year_2023_day_21_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
    steps: int = Body(
        ...,
        embed=True,
        examples=[6],
    ),
) -> int:
    start: Coordinate | None = None
    grid: dict[Coordinate, str] = {}

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            coordinate = Coordinate(x=x_index, y=y_index)

            if character == "S":
                start = coordinate

            grid[coordinate] = character

    assert start is not None

    visited_plots: dict[Coordinate, int] = {}

    @cache
    def count_steps(*, position: Coordinate, remaining_steps: int) -> None:
        if remaining_steps == 0:
            return

        for x_offset, y_offset in OFFSETS:
            new_position = Coordinate(x=position.x + x_offset, y=position.y + y_offset)

            if grid.get(new_position, "#") == "#":
                continue

            if (
                new_position in visited_plots
                and visited_plots[new_position] > remaining_steps
            ):
                continue

            if remaining_steps % 2 == steps % 2:
                visited_plots[new_position] = remaining_steps

            count_steps(position=new_position, remaining_steps=remaining_steps - 1)

    count_steps(position=start, remaining_steps=steps + ((steps + 1) % 2))

    return len(visited_plots)


@router.post("/part-2")
async def year_2023_day_21_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
    steps: int = Body(
        ...,
        embed=True,
        examples=[6],
    ),
) -> int:
    start: Coordinate | None = None
    grid: dict[Coordinate, str] = {}

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            coordinate = Coordinate(x=x_index, y=y_index)

            if character == "S":
                start = coordinate

            grid[coordinate] = character

    assert start is not None

    visited_plots: dict[Coordinate, int] = {start: 0}

    @cache
    def count_steps(*, position: Coordinate, remaining_steps: int) -> None:
        if remaining_steps == 0:
            return

        for x_offset, y_offset in OFFSETS:
            new_position = Coordinate(x=position.x + x_offset, y=position.y + y_offset)

            if grid.get(new_position, "#") == "#":
                continue

            if (
                new_position in visited_plots
                and visited_plots[new_position] > remaining_steps
            ):
                continue

            if remaining_steps % 2 == 0:
                visited_plots[new_position] = remaining_steps

            count_steps(position=new_position, remaining_steps=remaining_steps - 1)

    count_steps(position=start, remaining_steps=steps + 1)

    # for plot, step_count in visited_plots.items():
    #     print(f"{plot=}")
    #     print(f"{step_count=}")
    #     print()

    return len(visited_plots)
