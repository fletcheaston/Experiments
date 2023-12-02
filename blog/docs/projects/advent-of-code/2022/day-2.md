# Day 2: Rock Paper Scissors

## Part 1

### Prompt

The Elves begin to set up camp on the beach.
To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players.
Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape.
Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock.
If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win.
"The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors.
Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score.
Your **total score** is the sum of your scores for each round.
The score for a single round is the score for the **shape you selected** (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the **outcome of the round** (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

```
A Y
B X
C Z
```

This strategy guide predicts and recommends the following:

- In the first round, your opponent will choose Rock (a), and you should choose Paper (a). This ends in a win for you with a score of **`8`** (2 because you chose Paper + 6 because you won).
- In the second round, your opponent will choose Paper (`B`), and you should choose Rock (`X`). This ends in a loss for you with a score of **`1`** (1 + 0).
- The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = **`6`**.

In this example, if you were to follow the strategy guide, you would get a total score of **`15`** (8 + 1 + 6).

**What would your total score be if everything goes exactly according to your strategy guide?**

### Solution

Extract characters from the string and run through the pre-configured dictionaries to eventually arrive at the final scores.

```python
from enum import StrEnum

from fastapi import APIRouter

from src.types import Lines

router = APIRouter(tags=["2022 - Day 2: Rock Paper Scissors"])


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


@router.post("/part-1")
async def year_2022_day_2_part_1(lines: Lines) -> int:
    """ """
    total = 0

    # Iterate over lines
    for line in lines:
        other_character, my_character = line.split(" ")

        other_hand = CHARACTER_TO_HAND[other_character]
        my_hand = CHARACTER_TO_HAND[my_character]

        outcome = HANDS_TO_OUTCOME[(other_hand, my_hand)]
        outcome_score = OUTCOME_TO_SCORE[outcome]

        hand_score = HAND_TO_SCORE[my_hand]

        total += outcome_score
        total += hand_score

    return total
```

## Part 2

### Prompt

The Elf finishes helping with the tent and sneaks back over to you.
"Anyway, the second column says how the round needs to end: `X` means you need to lose, `Y` means you need to end the round in a draw, and `Z` means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated.
The example above now goes like this:

- In the first round, your opponent will choose Rock (`A`), and you need the round to end in a draw (`Y`), so you also choose Rock. This gives you a score of 1 + 3 = **`4`**.
- In the second round, your opponent will choose Paper (`B`), and you choose Rock so you lose (`X`) with a score of 1 + 0 = **`1`**.
- In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = **`7`**.

Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of **`12`**.

Following the Elf's instructions for the second column, **what would your total score be if everything goes exactly according to your strategy guide?**

### Solution

Extract characters from the string and run through the pre-configured dictionaries to eventually arrive at the final scores.

```python
from enum import StrEnum

from fastapi import APIRouter

from src.types import Lines

router = APIRouter(tags=["2022 - Day 2: Rock Paper Scissors"])


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


@router.post("/part-2")
async def year_2022_day_2_part_2(lines: Lines) -> int:
    total = 0

    # Iterate over lines
    for line in lines:
        other_character, outcome_character = line.split(" ")

        other_hand = CHARACTER_TO_HAND[other_character]
        outcome = CHARACTER_TO_OUTCOME[outcome_character]

        outcome_score = OUTCOME_TO_SCORE[outcome]

        my_hand = HAND_OUTCOME_TO_HAND[(other_hand, outcome)]
        hand_score = HAND_TO_SCORE[my_hand]

        total += outcome_score
        total += hand_score

    return total
```

## Recap

Ez pz 😎.
I'm really happy about how elegant this solution was.

I also did some refactoring so the upload file is abstracted away through a dependency.
Now I can just iterate over the lines in the file.
I could use this for testing, but I like testing the endpoints directly.
