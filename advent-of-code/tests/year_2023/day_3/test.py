from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,total",
    [
        (
            "part-1.txt",
            4361,
        ),
        (
            "input.txt",
            512794,
        ),
    ],
)
def test_part_1(
    filename: str,
    total: str,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-3/part-1",
            json={
                "document": file.readlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == total


@pytest.mark.parametrize(
    "filename,total",
    [
        (
            "part-2.txt",
            467835,
        ),
        (
            "input.txt",
            67779080,
        ),
    ],
)
def test_part_2(
    filename: str,
    total: str,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-3/part-2",
            json={
                "document": file.readlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == total
