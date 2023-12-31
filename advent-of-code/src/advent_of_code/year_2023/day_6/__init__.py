import math

import pytest


def part_1(times: list[int], distances: list[int]) -> int:
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


def part_2(time: int, distance: int) -> int:
    minimum_time = math.floor(
        (-time + math.sqrt(time**2 - 4 * -1 * -distance)) / -2 + 1
    )
    maximum_time = math.ceil((-time - math.sqrt(time**2 - 4 * -1 * -distance)) / -2 - 1)

    return maximum_time - minimum_time + 1


@pytest.mark.parametrize(
    "times,distances,output",
    [
        ([7, 15, 30], [9, 40, 200], 288),
        ([47, 98, 66, 98], [400, 1213, 1011, 1540], 1660968),
    ],
)
def test_part_1(times: list[int], distances: list[int], output: int) -> None:
    assert part_1(times, distances) == output


@pytest.mark.parametrize(
    "time,distance,output",
    [
        (71530, 940200, 71503),
        (47986698, 400121310111540, 26499773),
    ],
)
def test_part_2(time: int, distance: int, output: int) -> None:
    assert part_2(time, distance) == output
