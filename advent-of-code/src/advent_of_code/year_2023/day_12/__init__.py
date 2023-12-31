from functools import cache
from pathlib import Path

import pytest


@cache
def count_arrangements(springs: str, counts: tuple[int]) -> int:
    # Base cases
    # Valid arranements only exist for no springs and no counts left
    if not springs:
        if not counts:
            return 1

        return 0

    current_spring = springs[0]

    if current_spring == "#":
        # Not enough space, invalid arrangement
        if not counts or len(springs) < counts[0]:
            return 0

        # Not enough sprints for first value, invalid arrangement
        if "." in springs[0 : counts[0]]:
            return 0

        # Too many springs for first value, invalid arrangement
        if springs[counts[0] :].startswith("#"):
            return 0

        if len(springs) > counts[0]:
            # Recursive case 1
            # Try the next arrangement with the next springs/counts
            if springs[counts[0]] == "?":
                return count_arrangements(
                    springs[counts[0] + 1 :].lstrip("."),
                    counts[1:],
                )

        # Recursive case 2
        # We have enough springs to try more arrangements
        return count_arrangements(springs[counts[0] :].lstrip("."), counts[1:])

    elif current_spring == ".":
        # Recursive case 3
        # Continue with the empty space
        return count_arrangements(springs.lstrip("."), counts)

    # Recursive case 4
    # Unknown, try both # and .
    total = count_arrangements("#" + springs[1:], counts)
    total += count_arrangements("." + springs[1:], counts)
    return total


def part_1(document: list[str]) -> int:
    total = 0

    for index, line in enumerate(document):
        springs, count_str = line.split(" ")
        counts = [int(value) for value in count_str.split(",")]

        total += count_arrangements(springs, tuple(counts))

    return total


def part_2(document: list[str]) -> int:
    total = 0

    for index, line in enumerate(document):
        springs, count_str = line.split(" ")
        counts = [int(value) for value in count_str.split(",")]

        unfolded_counts = counts * 5
        unfolded_springs = "?".join([springs] * 5)

        total += count_arrangements(unfolded_springs, tuple(unfolded_counts))

    return total


@pytest.mark.parametrize(
    "springs,counts,output",
    [
        ("#", [1], 1),
        ("#.", [1], 1),
        (".#", [1], 1),
        ("?#", [1], 1),
        ("#?", [1], 1),
        ("??", [1], 2),
        ("???", [1], 3),
        ("?.?", [1], 2),
        ("?.??", [1, 2], 1),
        ("??.??", [1, 2], 2),
        ("???.???", [1, 1], 11),
        ("???.###", [1, 3], 3),
        ("?.?.###", [1, 3], 2),
        ("???.#", [3, 1], 1),
        ("???.###", [1, 1, 3], 1),
        ("???.###", [2, 3], 2),
        (".??..??...?##.", [1, 1, 3], 4),
        ("?#?#?#?#?#?#?#?", [1, 3, 1, 6], 1),
        ("????.#...#...", [4, 1, 1], 1),
        ("????.######..#####.", [1, 6, 5], 4),
        ("?###????????", [3, 2, 1], 10),
        (".###...?????", [3, 2, 1], 3),
        (".??.?.????", [1, 1, 1], 17),
        ("???#???????##?", [1, 7, 3], 4),
        ("?#.???#???????##?.?", [2, 1, 7, 3, 1], 4),
    ],
)
def test_update_arrangements(springs: str, counts: list[int], output: int) -> None:
    assert count_arrangements(springs, tuple(counts)) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 21),
        ("input.txt", 7705),
    ],
)
def test_part_1(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 525152),
        ("input.txt", 50338344809230),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
