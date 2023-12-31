from pathlib import Path

import pytest


def part_1(document: list[str]) -> int:
    total = 0

    number_index: dict[int, int] = {}
    number_counter = 0

    number_map: dict[tuple[int, int], int] = {}

    symbol_coordinates: set[tuple[int, int]] = set()

    for line_index, line in enumerate(document):
        character_indexes: list[int] = []
        running_number = ""

        for character_index, character in enumerate(line.strip()):
            if character.isnumeric():
                character_indexes.append(character_index)
                running_number += character

            elif character == ".":
                if running_number:
                    for inner_character_index in character_indexes:
                        number_map[(line_index, inner_character_index)] = number_counter

                    number_index[number_counter] = int(running_number)
                    number_counter += 1

                running_number = ""
                character_indexes = []

            else:
                symbol_coordinates.add((line_index, character_index))

                if running_number:
                    for inner_character_index in character_indexes:
                        number_map[(line_index, inner_character_index)] = number_counter

                    number_index[number_counter] = int(running_number)
                    number_counter += 1

                running_number = ""
                character_indexes = []

        if running_number:
            for inner_character_index in character_indexes:
                number_map[(line_index, inner_character_index)] = number_counter

            number_index[number_counter] = int(running_number)
            number_counter += 1

    # Iterate over the number map
    # Check for any coordinates next to/diagnol from the the coordinate
    found_indexes: set[int] = set()

    for coordinate, index in number_map.items():
        number = number_index[index]

        for x in [-1, 0, 1]:
            if index in found_indexes:
                continue

            for y in [-1, 0, 1]:
                if index in found_indexes:
                    continue

                new_coordinate = (coordinate[0] + y, coordinate[1] + x)

                # Next to symbol
                if new_coordinate in symbol_coordinates:
                    found_indexes.add(index)
                    total += number

    return total


def part_2(document: list[str]) -> int:
    total = 0

    number_index: dict[int, int] = {}
    number_counter = 0

    number_map: dict[tuple[int, int], int] = {}

    symbol_coordinates: dict[tuple[int, int], bool] = {}

    for line_index, line in enumerate(document):
        character_indexes: list[int] = []
        running_number = ""

        for character_index, character in enumerate(line.strip()):
            if character.isnumeric():
                character_indexes.append(character_index)
                running_number += character

            elif character == ".":
                if running_number:
                    for inner_character_index in character_indexes:
                        number_map[(line_index, inner_character_index)] = number_counter

                    number_index[number_counter] = int(running_number)
                    number_counter += 1

                running_number = ""
                character_indexes = []

            else:
                if character == "*":
                    symbol_coordinates[(line_index, character_index)] = True
                else:
                    symbol_coordinates[(line_index, character_index)] = False

                if running_number:
                    for inner_character_index in character_indexes:
                        number_map[(line_index, inner_character_index)] = number_counter

                    number_index[number_counter] = int(running_number)
                    number_counter += 1

                running_number = ""
                character_indexes = []

        if running_number:
            for inner_character_index in character_indexes:
                number_map[(line_index, inner_character_index)] = number_counter

            number_index[number_counter] = int(running_number)
            number_counter += 1

    # Check for gears
    found_indexes: set[int] = set()

    for coordinate, is_gear in symbol_coordinates.items():
        if not is_gear:
            continue

        gear_indexes: set[int] = set()

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                new_coordinate = (coordinate[0] + y, coordinate[1] + x)

                if new_coordinate in number_map:
                    gear_indexes.add(number_map[new_coordinate])

        if len(gear_indexes) == 2:
            first = gear_indexes.pop()
            second = gear_indexes.pop()

            # Add to total
            total += number_index[first] * number_index[second]

            # Mark these as found
            found_indexes.add(first)
            found_indexes.add(second)

    return total


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 4361),
        ("input.txt", 512794),
    ],
)
def test_part_1(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 467835),
        ("input.txt", 67779080),
    ],
)
def test_part_2(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
