# Day 3: Gear Ratios

## Part 1

### Prompt

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

### Solution

1. Extract numbers and their positions (start through stop coordinates) from the input
2. Extract symbols (non-numeric and non-`.` characters) and their positions (single coordinate)
3. For each number, check to see if the coordinates 1 position away contain a symbol
    - If so, add the number to the total and mark that number as "already found"

```python
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 3: Gear Ratios"])


@router.post("/part-1")
async def year_2023_day_3_part_1(document: list[str] = Body(..., embed=True)) -> int:
    total = 0

    number_index: dict[int, int] = {}
    number_counter = 0

    number_map: dict[tuple[int, int], int] = {}

    symbol_coordinates: set[tuple[int, int]] = set()

    # Iterate over lines
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
```

## Part 2

### Prompt

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

### Solution

This builds off of Part 1, but checks for coordinates around each gear for two numbers instead of coordinates around each number for a symbol.

I misunderstood some of the requirements, so there's a few silly things in the presented solution that I didn't bother removing before I completed the problem.

```python
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 3: Gear Ratios"])


@router.post("/part-2")
async def year_2023_day_3_part_2(document: list[str] = Body(..., embed=True)) -> int:
    total = 0

    number_index: dict[int, int] = {}
    number_counter = 0

    number_map: dict[tuple[int, int], int] = {}

    symbol_coordinates: dict[tuple[int, int], bool] = {}

    # Iterate over lines
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
```

## Recap

| Day | Part 1 Time | Part 1 Rank | Part 2 Time | Part 2 Rank |
|-----|-------------|-------------|-------------|-------------|
| 3   | 00:25:44    | 2,399       | 00:36:21    | 2,067       |

This was actually a bit of a challenge!
I'm pretty happy that I got a working solution (relatively) quickly, but...
The code is pretty gross, it's pretty hard to understand without context, there's a handful of repeated sections, it's not particularly efficient.

The worst part was keeping track of whether or not I had added a number to the running total.
I did this with the `number_index`, which maps from "order of this number in the entire input" to "the actual number".

It's useful to think of the input string as a grid with coordinates.

|        | x0 | x1 | x2 | x3 | x4 | x5 | x6 | x7 | x8 | x9 |
|--------|----|----|----|----|----|----|----|----|----|----|
| **y0** | 4  | 6  | 7  | .  | .  | 1  | 1  | 4  | .  | .  |
| **y1** | .  | .  | .  | *  | .  | .  | .  | .  | .  | .  |
| **y2** | .  | .  | 3  | 5  | .  | .  | 6  | 3  | 3  | .  |
| **y3** | .  | .  | .  | .  | .  | .  | #  | .  | .  | .  |
| **y4** | 6  | 1  | 7  | *  | .  | .  | .  | .  | .  | .  |
| **y5** | .  | .  | .  | .  | .  | +  | .  | 5  | 8  | .  |
| **y6** | .  | .  | 5  | 9  | 2  | .  | .  | .  | .  | .  |
| **y7** | .  | .  | .  | .  | .  | .  | 7  | 5  | 5  | .  |
| **y8** | .  | .  | .  | $  | .  | *  | .  | .  | .  | .  |
| **y9** | .  | 6  | 6  | 4  | .  | 5  | 9  | 8  | .  | .  |

Let's say we want to check for numbers around `(x3, y1)` (a gear).
We need to check all coordinates adjacent and diagonal to `(x3, y1)`, which we can do with a nested for loop, adding offsets to each coordinate component (-1, 0, and 1 for both the `x` and `y` axes).
We'll find the `7` of `467` at `(x2, y0)` first, which gives us the number `467` (sorta).
We'll also find `3` of `35` at `(x2, y2)` and `5` of `35` at `(x3, y2)`, which gives us the number `35` (twice) (sorta).

Instead of referencing each number as-is, we instead reference it through an index.
This lets us differentiate between a gear next to two parts of a number (as in the example above) and a gear next to two separate but identical numbers.
We do get the number eventually, but we work with the de-duplicated indexes first.
