from dataclasses import dataclass
from functools import cached_property

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 7: Title"])

DOCUMENT_EXAMPLE = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]

CARD_ORDER_PART_ONE = [
    "A",
    "K",
    "Q",
    "J",
    "T",
    "9",
    "8",
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
]


def card_position_part_one(card: str) -> int:
    return CARD_ORDER_PART_ONE.index(card)


@dataclass
class HandPartOne:
    cards: list[str]
    card_count: dict[str, int]

    bid: int

    @property
    def is_five_of_kind(self) -> bool:
        return len(set(self.cards)) == 1

    @property
    def is_four_of_kind(self) -> bool:
        for count in self.card_count.values():
            if count == 4:
                return True

        return False

    @property
    def is_full_house(self) -> bool:
        found_three = False
        found_two = False

        for count in self.card_count.values():
            if count == 3:
                found_three = True

            if count == 2:
                found_two = True

        return found_three and found_two

    @property
    def is_three_of_kind(self) -> bool:
        found_three = False
        found_two = False

        for count in self.card_count.values():
            if count == 3:
                found_three = True

            if count == 2:
                found_two = True

        return found_three and not found_two

    @property
    def is_two_pair(self) -> bool:
        found_pair = 0

        for count in self.card_count.values():
            if count == 2:
                found_pair += 1

        return found_pair == 2

    @property
    def is_one_pair(self) -> bool:
        found_pair = 0

        for count in self.card_count.values():
            if count == 2:
                found_pair += 1

        return found_pair == 1

    @property
    def is_high_card(self) -> bool:
        return len(set(self.cards)) == 5

    @property
    def points(self) -> int:
        if self.is_five_of_kind:
            return 1

        if self.is_four_of_kind:
            return 2

        if self.is_full_house:
            return 3

        if self.is_three_of_kind:
            return 4

        if self.is_two_pair:
            return 5

        if self.is_one_pair:
            return 6

        if self.is_high_card:
            return 7

        return 8

    def __gt__(self, other: "HandPartOne"):
        if self.points == other.points:
            for self_card, other_card in zip(self.cards, other.cards):
                if self_card != other_card:
                    return card_position_part_one(self_card) > card_position_part_one(
                        other_card
                    )

        return self.points > other.points


@router.post("/part-1")
async def year_2023_day_7_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    hands: list[HandPartOne] = []

    # Iterate over lines
    for line in document:
        hand_str, bid_str = line.split(" ")

        hands.append(
            HandPartOne(
                cards=list(hand_str),
                card_count={
                    card: list(hand_str).count(card) for card in list(hand_str)
                },
                bid=int(bid_str),
            ),
        )

    hands.sort(reverse=True)
    return sum([hand.bid * (index + 1) for index, hand in enumerate(hands)])


CARD_ORDER_PART_TWO = [
    "A",
    "K",
    "Q",
    "T",
    "9",
    "8",
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
    "J",
]


def card_position_part_two(card: str) -> int:
    return CARD_ORDER_PART_TWO.index(card)


@dataclass
class HandPartTwo:
    cards: list[str]
    card_count: dict[str, int]

    bid: int

    @property
    def is_five_of_kind(self) -> bool:
        if "J" in self.card_count and len(set(self.cards)) == 2:
            return True

        return len(set(self.cards)) == 1

    @property
    def is_four_of_kind(self) -> bool:
        j_count = self.card_count.get("J", 0)

        temp_cards = {
            card: count for card, count in self.card_count.items() if card != "J"
        }

        card_counts = [(card, count) for card, count in temp_cards.items()]
        card_counts.sort(key=lambda x: x[1], reverse=True)

        for card, count in card_counts:
            if count == 4:
                return True

            if count + j_count == 4:
                return True

        return False

    @property
    def is_full_house(self) -> bool:
        j_count = self.card_count.get("J", 0)

        temp_cards = {
            card: count for card, count in self.card_count.items() if card != "J"
        }

        card_counts = [(card, count) for card, count in temp_cards.items()]
        card_counts.sort(key=lambda x: x[1], reverse=True)

        found_three = False
        found_two = False

        for card, count in card_counts:
            if count == 3:
                found_three = True

            elif count + j_count == 3:
                j_count = 0
                found_three = True

            elif count == 2:
                found_two = True

            elif count + j_count == 2:
                j_count = 0
                found_two = True

        return found_three and found_two

    @property
    def is_three_of_kind(self) -> bool:
        j_count = self.card_count.get("J", 0)

        temp_cards = {
            card: count for card, count in self.card_count.items() if card != "J"
        }

        card_counts = [(card, count) for card, count in temp_cards.items()]
        card_counts.sort(key=lambda x: x[1], reverse=True)

        found_three = False
        found_two = False

        for card, count in card_counts:
            if count == 3:
                found_three = True

            elif count + j_count == 3:
                j_count = 0
                found_three = True

            elif count == 2:
                found_two = True

            elif count + j_count == 2:
                j_count = 0
                found_two = True

        return found_three and not found_two

    @property
    def is_two_pair(self) -> bool:
        found_pair = 0

        card_counts = [(card, count) for card, count in self.card_count.items()]
        card_counts.sort(key=lambda x: x[1], reverse=True)

        for card, count in card_counts:
            if count == 2:
                found_pair += 1

        return found_pair == 2

    @property
    def is_one_pair(self) -> bool:
        j_count = self.card_count.get("J", 0)

        temp_cards = {
            card: count for card, count in self.card_count.items() if card != "J"
        }

        card_counts = [(card, count) for card, count in temp_cards.items()]
        card_counts.sort(key=lambda x: x[1], reverse=True)

        found_pair = 0

        for card, count in card_counts:
            if count == 2:
                found_pair += 1

            elif count + j_count == 2:
                j_count = 0
                found_pair += 1

        return found_pair == 1

    @property
    def is_high_card(self) -> bool:
        return "J" not in self.card_count and len(set(self.cards)) == 5

    @cached_property
    def points(self) -> int:
        if self.is_five_of_kind:
            return 1

        if self.is_four_of_kind:
            return 2

        if self.is_full_house:
            return 3

        if self.is_three_of_kind:
            return 4

        if self.is_two_pair:
            return 5

        if self.is_one_pair:
            return 6

        if self.is_high_card:
            return 7

        raise AssertionError

    def __gt__(self, other: "HandPartTwo") -> bool:
        if self.points == other.points:
            for self_card, other_card in zip(self.cards, other.cards):
                if self_card != other_card:
                    return card_position_part_two(self_card) > card_position_part_two(
                        other_card
                    )

        return self.points > other.points


@router.post("/part-2")
async def year_2023_day_7_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    hands: list[HandPartTwo] = []

    # Iterate over lines
    for line in document:
        hand_str, bid_str = line.split(" ")

        hand = HandPartTwo(
            cards=list(hand_str),
            card_count={card: list(hand_str).count(card) for card in list(hand_str)},
            bid=int(bid_str),
        )

        hands.append(hand)

    hands.sort(reverse=True)

    return sum([hand.bid * (index + 1) for index, hand in enumerate(hands)])
