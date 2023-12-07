from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.year_2023.day_7 import HandPartTwo


@pytest.mark.parametrize(
    "filename,output",
    [
        ("part-1.txt", 6440),
        ("input.txt", 251545216),
    ],
)
def test_part_1(filename: str, output: int, test_client: TestClient) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-7/part-1",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "cards,points",
    [
        ("JJJJJ", 1),
        ("JJJJK", 1),
        ("JJJKK", 1),
        ("JJKKK", 1),
        ("JKKKK", 1),
        ("A2KJJ", 4),
        ("ATJKT", 4),
    ],
)
def test_hand_part_two(
    cards: str,
    points: int,
) -> None:
    hand = HandPartTwo(
        cards=list(cards),
        card_count={card: list(cards).count(card) for card in list(cards)},
        bid=0,
    )

    assert hand.points == points


@pytest.mark.parametrize(
    "filename,output",
    [
        ("part-2.txt", 5905),
        ("input.txt", 250384185),
    ],
)
def test_part_2(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-7/part-2",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output
