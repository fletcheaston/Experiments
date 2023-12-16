from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 46),
        ("example-2.txt", 3),
        ("example-3.txt", 3),
        ("example-4.txt", 2),
        ("example-5.txt", 2),
        ("example-6.txt", 4),
        ("example-7.txt", 41),
        ("example-8.txt", 31),
        ("input.txt", 7543),
    ],
)
def test_part_1(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-16/part-1",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 51),
        ("input.txt", 8231),
    ],
)
def test_part_2(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-16/part-2",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output
