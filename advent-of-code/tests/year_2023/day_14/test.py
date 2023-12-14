from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.year_2023.day_14 import tilt


@pytest.mark.parametrize(
    "line,output",
    [
        ("OOO", "OOO"),
        ("O.O", "OO."),
        ("O..O", "OO.."),
        ("O#.O", "O#O."),
        ("O.#.O", "O.#O."),
        ("O.O#..OO.#.O", "OO.#OO...#O."),
    ],
)
def test_tilt(line: str, output: str) -> None:
    assert tilt(line) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 136),
        ("input.txt", 110677),
    ],
)
def test_part_1(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    print()
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-14/part-1",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 0),
        # ("input.txt", 0),
    ],
)
def test_part_2(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-14/part-2",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output
