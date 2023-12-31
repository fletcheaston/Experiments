from pathlib import Path

import pytest


def part_1(document: list[str]) -> int:
    total = 0

    for line in document:
        assignment_left, assignment_right = line.split(",")

        # Parse the left assignment
        assignment_left_start = int(assignment_left.split("-")[0])
        assignment_left_end = int(assignment_left.split("-")[1])

        assignment_left_all = set(range(assignment_left_start, assignment_left_end + 1))

        # Parse the right assignment
        assignment_right_start = int(assignment_right.split("-")[0])
        assignment_right_end = int(assignment_right.split("-")[1])

        assignment_right_all = set(
            range(assignment_right_start, assignment_right_end + 1)
        )

        # Check for assignment containment
        if assignment_left_all.issubset(
            assignment_right_all
        ) or assignment_right_all.issubset(assignment_left_all):
            total += 1

    return total


def part_2(document: list[str]) -> int:
    total = 0

    for line in document:
        assignment_left, assignment_right = line.split(",")

        # Parse the left assignment
        assignment_left_start = int(assignment_left.split("-")[0])
        assignment_left_end = int(assignment_left.split("-")[1])

        assignment_left_all = set(range(assignment_left_start, assignment_left_end + 1))

        # Parse the right assignment
        assignment_right_start = int(assignment_right.split("-")[0])
        assignment_right_end = int(assignment_right.split("-")[1])

        assignment_right_all = set(
            range(assignment_right_start, assignment_right_end + 1)
        )

        # Check for assignment containment
        if assignment_left_all.intersection(assignment_right_all):
            total += 1

    return total


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 2),
        ("input.txt", 530),
    ],
)
def test_part_1(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 4),
        ("input.txt", 903),
    ],
)
def test_part_2(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
