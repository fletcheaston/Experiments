# Day 4: Scratchcards

## Part 1

### Prompt

The gondola takes you up.
Strangely, though, the ground doesn't seem to be coming with you; you're not climbing a mountain.
As the circle of Snow Island recedes below you, an entire new landmass suddenly appears above you!
The gondola carries you to the surface of the new island and lurches into the station.

As you exit the gondola, the first thing you notice is that the air here is much **warmer** than it was on Snow Island.
It's also quite **humid**.
Is this where the water source is?

The next thing you notice is an Elf sitting on the floor across the station in what seems to be a pile of colorful square cards.

"Oh! Hello!" The Elf excitedly runs over to you.
"How may I be of service?"
You ask about water sources.

"I'm not sure; I just operate the gondola lift.
That does sound like something we'd have, though - this is **Island Island**, after all! I bet the **gardener** would know.
He's on a different island, though - er, the small kind surrounded by water, not the floating kind.
We really need to come up with a better naming scheme.
Tell you what: if you can help me with something quick, I'll let you **borrow my boat** and you can go visit the gardener.
I got all these scratchcards as a gift, but I can't figure out what I've won."

The Elf leads you over to the pile of colorful cards.
There, you discover dozens of scratchcards, all with their opaque covering already scratched off.
Picking one up, it looks like each card has two lists of numbers separated by a vertical bar (|): a list of **winning numbers** and then a list of **numbers you have**.
You organize the information into a table (your puzzle input).

As far as the Elf has been able to figure out, you have to figure out which of the **numbers you have** appear in the list of **winning numbers**.
The first match makes the card worth one point and each match after the first **doubles** the point value of that card.

For example:

```
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
```

In the above example, card 1 has five winning numbers (`41`, `48`, `83`, `86`, and `17`) and eight numbers you have (`83`, `86`, `6`, `31`, `17`, `9`, `48`, and `53`).
Of the numbers you have, four of them (`48`, `83`, `17`, and `86`) are winning numbers!
That means card 1 is worth **`8`** points (1 for the first match, then doubled three times for each of the three matches after the first).

- Card 2 has two winning numbers (`32` and `61`), so it is worth **`2`** points.
- Card 3 has two winning numbers (`1` and `21`), so it is worth **`2`** points.
- Card 4 has one winning number (`84`), so it is worth **`1`** point.
- Card 5 has no winning numbers, so it is worth no points.
- Card 6 has no winning numbers, so it is worth no points.

So, in this example, the Elf's pile of scratchcards is worth **`13`** points.

Take a seat in the large pile of colorful cards.
**How many points are they worth in total?**

### Solution

For each line:

1. Extract the winning numbers and my numbers
2. Check for which of my numbers are in the winning numbers
3. Keep a running score for each card of matches numbers
    - 1 match = 1 score
    - N matches = 2**(N - 1) score (for N > 1)
4. Keep a running total of score for all cards

```python
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 4: Scratchcards"])


DOCUMENT_EXAMPLE = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


@router.post("/part-1")
async def year_2023_day_4_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for line in document:
        rest = line.split(": ")[1]
        winning_str, my_str = rest.split(" | ")

        winning_numbers: list[int] = [int(num) for num in winning_str.strip().split(" ") if num]
        my_numbers: list[int] = [int(num) for num in my_str.strip().split(" ") if num]

        score = 0

        for num in my_numbers:
            if num in winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score *= 2

        total += score

    return total
```

## Part 2

### Prompt

Just as you're about to report your findings to the Elf, one of you realizes that the rules have actually been printed on the back of every card this whole time.

There's no such thing as "points".
Instead, scratchcards only cause you to **win more scratchcards** equal to the number of winning numbers you have.

Specifically, you win **copies** of the scratchcards below the winning card equal to the number of matches.
So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the **same card number** as the card they copied.
So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15.
This process repeats until none of the copies cause you to win any more cards.
(Cards will never make you copy a card past the end of the table.)

This time, the above example goes differently:

```
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
```

- Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
- Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
- Your copy of card 2 also wins one copy each of cards 3 and 4.
- Your four instances of card 3 (one original and three copies) have two matching numbers, so you win **four** copies each of cards 4 and 5.
- Your eight instances of card 4 (one original and seven copies) have one matching number, so you win **eight** copies of card 5.
- Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
- Your one instance of card 6 (one original) has no matching numbers and wins no more cards.

Once all of the originals and copies have been processed, you end up with **`1`** instance of card 1, **`2`** instances of card 2, **`4`** instances of card 3, **`8`** instances of card 4, **`14`** instances of card 5, and **`1`** instance of card 6.
In total, this example pile of scratchcards causes you to ultimately have **`30`** scratchcards!

Process all of the original and copied scratchcards until no more scratchcards are won.
Including the original set of scratchcards, **how many total scratchcards do you end up with?**

### Solution

- Set up a pre-filled map (`copies`) from card index (0 based) to number of copies

For each line:

1. Extract the winning numbers and my numbers
2. Check for which of my numbers are in the winning numbers

For each matching number:

1. Increment the number of matches we've made for the current card
2. Increase the number of copies for the next card by the number of copies we have for the current card
    - The next card (index) is the current card index + running number of matches for this card

Then add the number of copies for the current card to the running total.

```python
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 4: Scratchcards"])


DOCUMENT_EXAMPLE = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


@router.post("/part-2")
async def year_2023_day_4_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Map from index to count
    copies: dict[int, int] = {
        index: 1 for index in range(len(document))
    }

    # Iterate over lines
    for index, line in enumerate(document):
        rest = line.split(": ")[1]
        winning_str, my_str = rest.split(" | ")

        winning_numbers: list[int] = [int(num) for num in winning_str.strip().split(" ") if num]
        my_numbers: list[int] = [int(num) for num in my_str.strip().split(" ") if num]

        matches = 0

        for num in my_numbers:
            if num in winning_numbers:
                matches += 1
                copies[index + matches] += copies[index]

        total += copies[index]

    return total
```

This is the most important line:

```python
copies[index + matches] += copies[index]
```

I increase the number of copies for the **next card** by the **number of copies we have of the existing card**.

My initial solution was something like this:

```python
for _ in range(copies[index]):
    ...
    
    copies[index + matches] += 1
```

This closely matches what I did in Part 1, and this worked for the example input.
However, when I ran this on the real input, my solution didn't complete (at least not within 10 seconds).

## Recap

| Day | Part 1 Time | Part 1 Rank | Part 2 Time | Part 2 Rank |
|-----|-------------|-------------|-------------|-------------|
| 4   | 00:04:14    | 426         | 00:19:36    | 2,104       |

Hot out the gate in T500 for Part 1, I'm really happy about that 😁.
I made some major mistakes on Part 2:

- **COMPLETELY** misread the prompt (~5 minutes wasted)
- Came up with a solution that worked for the example input but didn't complete for the real input (~5 minutes wasted)
    - Nested loops are bad 😅

... So my rank was pretty bad compared to Part 1.

But overall, I'm really happy!
I'm figuring out some of the obvious time-saving strategies, such as:

- Scaffolded project, designed for quick feedback cycles
    - `pytest {path to test file} -s` is *extremely* helpful
    - Script file with scaffolded functions for Part 1 and Part 2
- Skipping the "story time" part of the prompts
    - This part caused me to misread the prompt on Part 2 so ¯\\\_(ツ)_/¯ don't skip everything 🙃
- Pulling test inputs ASAP
- Pulling your real input ASAP (loading this webpage in a separate window, refreshing when the puzzle is released)

I'm really excited for tomorrow, hoping I can remedy the mistakes I made on Part 2 and further the excellent performance on Part 1.
