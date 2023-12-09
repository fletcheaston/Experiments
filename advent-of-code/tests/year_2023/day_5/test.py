from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,seeds,total",
    [
        ("example.txt", [79, 14, 55, 13], 35),
        (
            "input.txt",
            [
                1972667147,
                405592018,
                1450194064,
                27782252,
                348350443,
                61862174,
                3911195009,
                181169206,
                626861593,
                138786487,
                2886966111,
                275299008,
                825403564,
                478003391,
                514585599,
                6102091,
                2526020300,
                15491453,
                3211013652,
                546191739,
            ],
            662197086,
        ),
    ],
)
def test_part_1(
    filename: str, seeds: list[int], total: int, test_client: TestClient
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-5/part-1",
            json={
                "document": file.read().splitlines(),
                "seeds": seeds,
            },
        )

        assert response.status_code == 200
        assert response.json() == total


@pytest.mark.parametrize(
    "filename,seeds,total",
    [
        ("example.txt", [79, 14, 55, 13], 46),
        (
            "input.txt",
            [
                1972667147,
                405592018,
                1450194064,
                27782252,
                348350443,
                61862174,
                3911195009,
                181169206,
                626861593,
                138786487,
                2886966111,
                275299008,
                825403564,
                478003391,
                514585599,
                6102091,
                2526020300,
                15491453,
                3211013652,
                546191739,
            ],
            52510809,
        ),
    ],
)
def test_part_2(
    filename: str, seeds: list[int], total: int, test_client: TestClient
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-5/part-2",
            json={
                "document": file.read().splitlines(),
                "seeds": seeds,
            },
        )

        assert response.status_code == 200
        assert response.json() == total
