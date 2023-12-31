from pathlib import Path

import pytest


def is_possible(score: str, red: int, green: int, blue: int) -> bool:
    if "red" in score:
        if int(score.replace(" red", "")) > red:
            return False

    if "green" in score:
        if int(score.replace(" green", "")) > green:
            return False

    if "blue" in score:
        if int(score.replace(" blue", "")) > blue:
            return False

    return True


def part_1(document: list[str]) -> int:
    total = 0

    for line in document:
        possible = True

        game_text, ball_text = line.split(": ")

        # Extract game number
        game_number = int(str(game_text).replace("Game ", ""))

        # Check if scores are possible
        for scores in ball_text.split(";"):
            for score in scores.split(", "):
                if not is_possible(score, 12, 13, 14):
                    possible = False

        if possible:
            total += game_number

    return total


def part_2(document: list[str]) -> int:
    total = 0

    for line in document:
        red = 0
        green = 0
        blue = 0

        _, ball_text = line.split(": ")

        for scores in ball_text.split(";"):
            for score in scores.split(", "):
                if "red" in score:
                    red = max(red, int(score.replace(" red", "")))

                if "green" in score:
                    green = max(green, int(score.replace(" green", "")))

                if "blue" in score:
                    blue = max(blue, int(score.replace(" blue", "")))

        total += red * green * blue

    return total


@pytest.mark.parametrize(
    "filename,total",
    [
        ("example.txt", 8),
        ("input.txt", 2505),
    ],
)
def test_part_1(filename: str, total: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == total


@pytest.mark.parametrize(
    "filename,total",
    [
        ("example.txt", 2286),
        ("input.txt", 70265),
    ],
)
def test_part_2(filename: str, total: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == total
