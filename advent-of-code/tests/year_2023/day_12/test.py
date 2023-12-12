from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.year_2023.day_12 import count_arrangements


@pytest.mark.parametrize(
    "springs,counts,output",
    [
        ("#", [1], 1),
        ("#.", [1], 1),
        (".#", [1], 1),
        ("?#", [1], 1),
        ("#?", [1], 1),
        ("??", [1], 2),
        ("???", [1], 3),
        ("?.?", [1], 2),
        ("?.??", [1, 2], 1),
        ("??.??", [1, 2], 2),
        ("???.???", [1, 1], 11),
        ("???.###", [1, 3], 3),
        ("?.?.###", [1, 3], 2),
        ("???.#", [3, 1], 1),
        ("???.###", [1, 1, 3], 1),
        ("???.###", [2, 3], 2),
        (".??..??...?##.", [1, 1, 3], 4),
        ("?#?#?#?#?#?#?#?", [1, 3, 1, 6], 1),
        ("????.#...#...", [4, 1, 1], 1),
        ("????.######..#####.", [1, 6, 5], 4),
        ("?###????????", [3, 2, 1], 10),
        (".###...?????", [3, 2, 1], 3),
        (".??.?.????", [1, 1, 1], 17),
        ("???#???????##?", [1, 7, 3], 4),
        ("?#.???#???????##?.?", [2, 1, 7, 3, 1], 4),
    ],
)
def test_update_arrangements(springs: str, counts: list[int], output: int) -> None:
    assert count_arrangements(springs, tuple(counts)) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 21),
        ("input.txt", 7705),
    ],
)
def test_part_1(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-12/part-1",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 525152),
        ("input.txt", 50338344809230),
    ],
)
def test_part_2(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-12/part-2",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output
