# Day 1: Trebuchet?!

## Part 1

### Prompt

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

### Solution

Remove all non-numeric characters from a calibration line,
combine the first and last numeric characters into the sum for that calibration line,
and keep a running total.

```python
import io

from fastapi import APIRouter, UploadFile

router = APIRouter()


@router.post("/part-1")
async def day_1_part_1(calibration_document: UploadFile) -> int:
    total = 0

    # Iterate over lines
    with calibration_document.file as file:
        for calibration_line in io.TextIOWrapper(file, encoding="utf-8"):
            # Remove all non-numeric characters from the string
            numerics = [
                character for character in calibration_line if character.isnumeric()
            ]

            # Combine first and last digits, add to total
            total += int(f"{numerics[0]}{numerics[-1]}")

    return total
```

## Part 2

### Prompt

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

### Solution

The solution for Part 2 builds off of Part 1, but breaks a few assumptions.

1. A "valid digit" can correspond to any number
2. The set of "valid digits" isn't limited to characters of numbers 1-9
3. A "valid digit" isn't limited to one character long

That's pretty much it.
For an example of breaking these assumptions, let's look at the "valid digit" of `three`.

1. `three` corresponds to a calibration score of 3
2. `three` isn't in this set of characters: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`
3. `three` is 5 characters long

With that in mind, we need to...

1. Enable a mapping from "valid digits" to their calibration score
2. Enable substring index searching/comparisons, starting from both the left and right sides of the string

```python
import functools
import io

from fastapi import APIRouter, UploadFile

router = APIRouter()

...

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


def reduce_lfind(a: str, b: str, line: str) -> str:
    position_a = line.find(a)
    position_b = line.find(b)

    if position_a == -1:
        return b

    if position_b == -1:
        return a

    if position_a < position_b:
        return a

    return b


def reduce_rfind(a: str, b: str, line: str) -> str:
    position_a = line.rfind(a)
    position_b = line.rfind(b)

    if position_a == -1:
        return b

    if position_b == -1:
        return a

    if position_a > position_b:
        return a

    return b


@router.post("/part-2")
async def day_1_part_2(calibration_document: UploadFile) -> int:
    total = 0

    # Iterate over lines
    with calibration_document.file as file:
        for calibration_line in io.TextIOWrapper(file, encoding="utf-8"):
            # Find the earliest "digit"
            first_digit = functools.reduce(lambda a, b: reduce_lfind(a, b, calibration_line), VALID_DIGITS)
            last_digit = functools.reduce(lambda a, b: reduce_rfind(a, b, calibration_line), VALID_DIGITS)

            first = VALID_DIGIT_TO_NUM[first_digit]
            last = VALID_DIGIT_TO_NUM[last_digit]

            # Combine first and last digits, add to total
            total += int(f"{first}{last}")

    return total
```

## Recap

| Day | Part 1 Time | Part 1 Rank | Part 2 Time | Part 2 Rank |
|-----|-------------|-------------|-------------|-------------|
| 1   | 02:00:23    | 19,252      | 02:49:23    | 14,553      |

This took a **LOT** longer than expected, mostly because I was setting up the project and playing around with various config tools while doing so 😅.

I also spent way too much time on a silly mistake.
I made the `reduce_rfind` function first, copied that for the `reduce_lfind` function, and forgot to change the `line.rfind` calls to `line.find`.
So I spent a bunch of time troubleshooting that 🙃.

But overall, super fun! I'm sure tomorrow will go much smoother 😁.
