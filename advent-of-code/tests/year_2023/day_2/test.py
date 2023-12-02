from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,total",
    [
        ("part-1.txt", 8),
        ("input.txt", 2505),
    ],
)
def test_part_1(filename: str, total: int, test_client: TestClient) -> None:
    with open(Path(__file__).with_name(filename), "rb") as file:
        response = test_client.post(
            "2023/day-2/part-1",
            params={
                "red": 12,
                "green": 13,
                "blue": 14,
            },
            files={"document": file},
        )

        assert response.status_code == 200
        assert response.json() == total


@pytest.mark.parametrize(
    "filename,total",
    [
        ("part-2.txt", 2286),
        ("input.txt", 70265),
    ],
)
def test_part_2(filename: str, total: int, test_client: TestClient) -> None:
    with open(Path(__file__).with_name(filename), "rb") as file:
        response = test_client.post(
            "2023/day-2/part-2",
            files={"document": file},
        )

        assert response.status_code == 200
        assert response.json() == total
