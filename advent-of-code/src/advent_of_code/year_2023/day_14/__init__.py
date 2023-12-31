from collections import Counter
from pathlib import Path

import pytest


def tilt_left(line: str) -> str:
    rock_map: Counter[int, int] = Counter({0: 0})
    square_rock_map: list[int] = [-1]
    current_index = 0

    rock_line: list[str] = []

    for index, character in enumerate(line):
        if character == "#":
            current_index += 1
            rock_line.append("#")
            square_rock_map.append(index)

        elif character == ".":
            rock_line.append(".")

        elif character == "O":
            rock_map[current_index] += 1
            rock_line.append(".")

    for index, square_rock_index in enumerate(square_rock_map):
        round_rocks = rock_map[index]

        for offset in range(round_rocks):
            rock_line[square_rock_index + offset + 1] = "O"

    return "".join(rock_line)


def part_1(document: list[str]) -> int:
    total = 0

    line_size = len(document[0])
    lines: list[str] = ["" for _ in range(line_size)]

    for line in document:
        for index, character in enumerate(line):
            lines[index] += character

    for index, line in enumerate(lines):
        lines[index] = tilt_left(line)

    for row_index in range(line_size):
        line_total = 0

        for line in lines:
            if line[row_index] == "O":
                line_total += 1

        line_total *= line_size - row_index
        total += line_total

    return total


def rotate_90(raw_lines: list[str]) -> list[str]:
    # Rotates 90 degrees clockwise
    line_size = len(raw_lines[0])
    lines: list[str] = ["" for _ in range(line_size)]

    for line in raw_lines:
        for index, character in enumerate(reversed(line)):
            lines[index] += character

    return lines


def rotate_180(raw_lines: list[str]) -> list[str]:
    new_lines = raw_lines.copy()

    for _ in range(2):
        new_lines = rotate_90(new_lines)

    return new_lines


def rotate_270(raw_lines: list[str]) -> list[str]:
    new_lines = raw_lines.copy()

    for _ in range(3):
        new_lines = rotate_90(new_lines)

    return new_lines


def part_2(document: list[str]) -> int:
    size = 1_000_000_000

    counter = 0
    cycle_repeats: int | None = None
    cycle_counter: dict[str, int] = {}
    cycles: dict[int, list[str]] = {}

    while counter < size:
        north = [tilt_left(line) for line in rotate_90(document)]
        west = [tilt_left(line) for line in rotate_270(north)]
        south = [tilt_left(line) for line in rotate_270(west)]
        east = [tilt_left(line) for line in rotate_270(south)]

        cycled = rotate_180(east)

        cycles[counter] = cycled

        cycle_key = "".join(cycled)

        if cycle_key in cycle_counter:
            cycle_repeats = cycle_counter[cycle_key]
            break

        else:
            cycle_counter[cycle_key] = counter

        counter += 1
        document = cycled

    if cycle_repeats is None:
        last_cycle = cycles[counter - 1]
    else:
        final_cycle = (
            cycle_repeats + (size - cycle_repeats) % (counter - cycle_repeats) - 1
        )
        last_cycle = cycles[final_cycle]

    total = 0

    for index, line in enumerate(last_cycle):
        total += line.count("O") * (len(last_cycle) - index)

    return total


@pytest.mark.parametrize(
    "line,output",
    [
        ("OOO", "OOO"),
        ("O.O", "OO."),
        ("O..O", "OO.."),
        ("O#.O", "O#O."),
        ("O.#.O", "O.#O."),
        ("O.O#..OO.#.O", "OO.#OO...#O."),
    ],
)
def test_tilt_left(line: str, output: str) -> None:
    assert tilt_left(line) == output


@pytest.mark.parametrize(
    "lines,output",
    [
        (["ABC", "DEF", "GHI"], ["CFI", "BEH", "ADG"]),
        (["CFI", "BEH", "ADG"], ["IHG", "FED", "CBA"]),
        (["IHG", "FED", "CBA"], ["GDA", "HEB", "IFC"]),
        (["GDA", "HEB", "IFC"], ["ABC", "DEF", "GHI"]),
    ],
)
def test_rotate(lines: list[str], output: list[str]) -> None:
    assert rotate_90(lines) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 136),
        ("input.txt", 110677),
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
        ("example.txt", 64),
        ("input.txt", 90551),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
