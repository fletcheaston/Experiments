from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.year_2023.day_14 import tilt_left, transpose_90


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
def test_tilt_left(line: str, output: str) -> None:
    assert tilt_left(line) == output


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
    "lines,output",
    [
        (["ABC", "DEF", "GHI"], ["CFI", "BEH", "ADG"]),
        (["CFI", "BEH", "ADG"], ["IHG", "FED", "CBA"]),
        (["IHG", "FED", "CBA"], ["GDA", "HEB", "IFC"]),
        (["GDA", "HEB", "IFC"], ["ABC", "DEF", "GHI"]),
    ],
)
def test_transpose(lines: list[str], output: list[str]) -> None:
    assert transpose_90(lines) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 64),
        ("input.txt", 90551),
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
