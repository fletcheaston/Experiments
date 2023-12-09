from dataclasses import dataclass

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 9: Title"])


DOCUMENT_EXAMPLE = []


@dataclass
class History:
    values: list[list[int]]

    @property
    def latest_all_zero(self) -> bool:
        return all([value == 0 for value in self.values[-1]])

    def calculate_next(self) -> None:
        next_values: list[int] = []

        for index in range(len(self.values[-1]) - 1):
            first = self.values[-1][index]
            second = self.values[-1][index + 1]

            difference = second - first

            next_values.append(difference)

        self.values.append(next_values)

    def fill_in_placeholders(self) -> None:
        # Do the first manually
        self.values[-1].append(0)

        # Do the rest in a loop
        for index in range(len(self.values) - 2, -1, -1):
            self.values[index].append(
                self.values[index + 1][-1] + self.values[index][-1]
            )


@router.post("/part-1")
async def year_2023_day_9_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for line in document:
        history = History(
            values=[[int(value.strip()) for value in line.split(" ")]],
        )

        while not history.latest_all_zero:
            history.calculate_next()

        history.fill_in_placeholders()

        total += history.values[0][-1]

    return total


@dataclass
class BackwardsHistory:
    values: list[list[int]]

    @property
    def latest_all_zero(self) -> bool:
        return all([value == 0 for value in self.values[-1]])

    def calculate_next(self) -> None:
        next_values: list[int] = []

        for index in range(len(self.values[-1]) - 1):
            first = self.values[-1][index]
            second = self.values[-1][index + 1]

            difference = second - first

            next_values.append(difference)

        self.values.append(next_values)

    def fill_in_placeholders(self) -> None:
        # Do the first manually
        self.values[-1].insert(0, 0)

        # Do the rest in a loop
        for index in range(len(self.values) - 2, -1, -1):
            self.values[index].insert(
                0, self.values[index][0] - self.values[index + 1][0]
            )


@router.post("/part-2")
async def year_2023_day_9_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for line in document:
        history = BackwardsHistory(
            values=[[int(value.strip()) for value in line.split(" ")]],
        )

        while not history.latest_all_zero:
            history.calculate_next()

        history.fill_in_placeholders()

        total += history.values[0][0]

    return total
