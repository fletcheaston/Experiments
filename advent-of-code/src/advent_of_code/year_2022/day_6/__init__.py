from pathlib import Path

import pytest


def part_1(document: str) -> int | None:
    buffer_size = 4

    for start in range(0, len(document) - buffer_size):
        if len(set(list(document[start : start + buffer_size]))) == buffer_size:
            return start + buffer_size


def part_2(
    document: str,
) -> int | None:
    buffer_size = 14

    for start in range(0, len(document) - buffer_size):
        if len(set(list(document[start : start + buffer_size]))) == buffer_size:
            return start + buffer_size


@pytest.mark.parametrize(
    "filename,output",
    [
        (
            "example.txt",
            7,
        ),
        (
            "input.txt",
            1134,
        ),
    ],
)
def test_part_1(
    filename: str,
    output: str,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()[0]) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        (
            "example.txt",
            19,
        ),
        (
            "input.txt",
            2263,
        ),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()[0]) == output
