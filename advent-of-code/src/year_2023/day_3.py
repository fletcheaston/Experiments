from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 3: Gear Ratios"])


DOCUMENT_EXAMPLE = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


@router.post("/part-1")
async def year_2023_day_3_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the **water source**, but this is as far as he can bring you.
    You go inside.

    It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

    "Aaah!"

    You turn around to see a slightly-greasy Elf with a wrench and a look of surprise.
    "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it."
    You offer to help.

    The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one.
    If you can **add up all the part numbers** in the engine schematic, it should be easy to work out which part is missing.

    The engine schematic (your puzzle input) consists of a visual representation of the engine.
    There are lots of numbers and symbols you don't really understand, but apparently **any number adjacent to a symbol**, even diagonally, is a "part number" and should be included in your sum.
    (Periods (.) do not count as a symbol.)

    Here is an example engine schematic:

    ```
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    ```

    In this schematic, two numbers are **not** part numbers because they are not adjacent to a symbol: `114` (top right) and `58` (middle right).
    Every other number is adjacent to a symbol and so is a part number; their sum is **`4361`**.

    Of course, the actual engine schematic is much larger.
    **What is the sum of all of the part numbers in the engine schematic?**
    """
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


@router.post("/part-2")
async def year_2023_day_3_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    The engineer finds the missing part and installs it in the engine!
    As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

    You don't seem to be going very fast, though.
    Maybe something is still wrong?
    Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

    Before you can explain the situation, she suggests that you look out the window.
    There stands the engineer, holding a phone in one hand and waving with the other.
    You're going so slowly that you haven't even left the station.
    You exit the gondola.

    The missing part wasn't the only issue - one of the gears in the engine is wrong.
    A **gear** is any `*` symbol that is adjacent to **exactly two part numbers**.
    Its **gear ratio** is the result of multiplying those two numbers together.

    This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

    Consider the same engine schematic again:

    ```
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    ```

    In this schematic, there are **two** gears.
    The first is in the top left; it has part numbers `467` and `35`, so its gear ratio is `16345`.
    The second gear is in the lower right; its gear ratio is `451490`.
    (The `*` adjacent to `617` is **not** a gear because it is only adjacent to one part number.)
    Adding up all of the gear ratios produces **`467835`**.

    **What is the sum of all of the gear ratios in your engine schematic?**
    """
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
