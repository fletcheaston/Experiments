from enum import StrEnum
from pathlib import Path

import pytest


class Hand(StrEnum):
    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"


CHARACTER_TO_HAND: dict[str, Hand] = {
    "A": Hand.ROCK,
    "B": Hand.PAPER,
    "C": Hand.SCISSORS,
    "X": Hand.ROCK,
    "Y": Hand.PAPER,
    "Z": Hand.SCISSORS,
}


HAND_TO_SCORE: dict[Hand, int] = {
    Hand.ROCK: 1,
    Hand.PAPER: 2,
    Hand.SCISSORS: 3,
}


class Outcome(StrEnum):
    WIN = "Win"
    DRAW = "Draw"
    LOSS = "Loss"


OUTCOME_TO_SCORE: dict[Outcome, int] = {
    Outcome.WIN: 6,
    Outcome.DRAW: 3,
    Outcome.LOSS: 0,
}

# Hand #1 is opponents, hand #2 is ours. Outcome is our outcome
HANDS_TO_OUTCOME: dict[tuple[Hand, Hand], Outcome] = {
    (Hand.ROCK, Hand.ROCK): Outcome.DRAW,
    (Hand.ROCK, Hand.PAPER): Outcome.WIN,
    (Hand.ROCK, Hand.SCISSORS): Outcome.LOSS,
    (Hand.PAPER, Hand.ROCK): Outcome.LOSS,
    (Hand.PAPER, Hand.PAPER): Outcome.DRAW,
    (Hand.PAPER, Hand.SCISSORS): Outcome.WIN,
    (Hand.SCISSORS, Hand.ROCK): Outcome.WIN,
    (Hand.SCISSORS, Hand.PAPER): Outcome.LOSS,
    (Hand.SCISSORS, Hand.SCISSORS): Outcome.DRAW,
}

CHARACTER_TO_OUTCOME: dict[str, Outcome] = {
    "X": Outcome.LOSS,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}

HAND_OUTCOME_TO_HAND: dict[tuple[Hand, Outcome], Hand] = {
    (Hand.ROCK, Outcome.WIN): Hand.PAPER,
    (Hand.ROCK, Outcome.DRAW): Hand.ROCK,
    (Hand.ROCK, Outcome.LOSS): Hand.SCISSORS,
    (Hand.PAPER, Outcome.WIN): Hand.SCISSORS,
    (Hand.PAPER, Outcome.DRAW): Hand.PAPER,
    (Hand.PAPER, Outcome.LOSS): Hand.ROCK,
    (Hand.SCISSORS, Outcome.WIN): Hand.ROCK,
    (Hand.SCISSORS, Outcome.DRAW): Hand.SCISSORS,
    (Hand.SCISSORS, Outcome.LOSS): Hand.PAPER,
}


def part_1(document: list[str]) -> int:
    total = 0

    for line in document:
        other_character, my_character = line.split(" ")

        other_hand = CHARACTER_TO_HAND[other_character]
        my_hand = CHARACTER_TO_HAND[my_character]

        outcome = HANDS_TO_OUTCOME[(other_hand, my_hand)]
        outcome_score = OUTCOME_TO_SCORE[outcome]

        hand_score = HAND_TO_SCORE[my_hand]

        total += outcome_score
        total += hand_score

    return total


def part_2(document: list[str]) -> int:
    total = 0

    for line in document:
        other_character, outcome_character = line.split(" ")

        other_hand = CHARACTER_TO_HAND[other_character]
        outcome = CHARACTER_TO_OUTCOME[outcome_character]

        outcome_score = OUTCOME_TO_SCORE[outcome]

        my_hand = HAND_OUTCOME_TO_HAND[(other_hand, outcome)]
        hand_score = HAND_TO_SCORE[my_hand]

        total += outcome_score
        total += hand_score

    return total


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 15),
        ("input.txt", 10816),
    ],
)
def test_part_1(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 12),
        ("input.txt", 11657),
    ],
)
def test_part_2(filename: str, output: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
