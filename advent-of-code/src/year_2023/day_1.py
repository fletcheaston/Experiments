import functools

from fastapi import APIRouter, Body

from src.utils import reduce_lfind, reduce_rfind

router = APIRouter(tags=["2023 - Day 1: Trebuchet?!"])


DOCUMENT_EXAMPLE = [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
]


@router.post("/part-1")
async def year_2023_day_1_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    Something is wrong with global snow production, and you've been selected to take a look.
    The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

    You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

    Collect stars by solving puzzles.
    Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first.
    Each puzzle grants one star.
    Good luck!

    You try to ask why they can't just use a weather machine ("not powerful enough")
    and where they're even sending you ("the sky")
    and why your map looks mostly blank ("you sure ask a lot of questions")
    and hang on did you just say the sky ("of course, where do you think snow comes from")
    when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

    As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf
    who was apparently just excited to show off her art skills.
    Consequently, the Elves are having trouble reading the values on the document.

    The newly-improved calibration document consists of lines of text; each line originally contained a specific **calibration value** that the Elves now need to recover.
    On each line, the calibration value can be found by combining the **first digit** and the **last digit** (in that order) to form a single **two-digit number**.

    For example:

    ```
    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet
    ```

    In this example, the calibration values of these four lines are `12`, `38`, `15`, and `77`.
    Adding these together produces **`142`**.

    Consider your entire calibration document.
    **What is the sum of all of the calibration values?**
    """
    total = 0

    # Iterate over lines
    for line in document:
        # Remove all non-numeric characters from the string
        numerics = [character for character in line if character.isnumeric()]

        # Combine first and last digits, add to total
        total += int(f"{numerics[0]}{numerics[-1]}")

    return total


VALID_DIGIT_TO_NUM: dict[str, int] = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

VALID_DIGITS = VALID_DIGIT_TO_NUM.keys()


@router.post("/part-2")
async def year_2023_day_1_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    """
    Your calculation isn't quite right.
    It looks like some of the digits are actually **spelled out with letters**:
    `one`, `two`, `three`, `four`, `five`, `six`, `seven`, `eight`, and `nine` **also** count as valid "digits".

    Equipped with this new information, you now need to find the real first and last digit on each line.
    For example:

    ```
    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    ```

    In this example, the calibration values are `29`, `83`, `13`, `24`, `42`, `14`, and `76`.
    Adding these together produces **`281`**.

    **What is the sum of all of the calibration values?**
    """
    total = 0

    # Iterate over lines
    for line in document:
        # Find the earliest "digit"
        first_digit = functools.reduce(
            lambda a, b: reduce_lfind(a, b, line), VALID_DIGITS
        )
        last_digit = functools.reduce(
            lambda a, b: reduce_rfind(a, b, line), VALID_DIGITS
        )

        first = VALID_DIGIT_TO_NUM[first_digit]
        last = VALID_DIGIT_TO_NUM[last_digit]

        # Combine first and last digits, add to total
        total += int(f"{first}{last}")

    return total
