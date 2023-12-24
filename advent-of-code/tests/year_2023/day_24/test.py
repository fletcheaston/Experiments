from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,lower,upper,output",
    [
        ("example-1.txt", 7, 27, 2),
        ("input.txt", 200000000000000, 400000000000000, 15558),
    ],
)
def test_part_1(
    filename: str,
    lower: int,
    upper: int,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-24/part-1",
            json={
                "document": file.read().splitlines(),
                "lower": lower,
                "upper": upper,
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 47),
        # ("input.txt", 765636044333842),
    ],
)
def test_part_2(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-24/part-2",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output
