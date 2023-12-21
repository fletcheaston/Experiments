from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,steps,output",
    [
        # ("example.txt", 6, 16),
        # ("example.txt", 7, 21),
        # ("example.txt", 64, 42),
        # ("input.txt", 64, 3758),
    ],
)
def test_part_1(
    filename: str,
    steps: int,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-21/part-1",
            json={
                "document": file.read().splitlines(),
                "steps": steps,
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "filename,steps,output",
    [
        ("example.txt", 6, 16),
        # ("example.txt", 10, 50),
        # ("example.txt", 50, 1594),
        # ("example.txt", 100, 6536),
        # ("example.txt", 500, 167004),
        # ("example.txt", 1000, 668697),
        # ("example.txt", 5000, 16733044),
        # ("input.txt", 26501365, 0),
    ],
)
def test_part_2(
    filename: str,
    steps: int,
    output: int,
    test_client: TestClient,
) -> None:
    print()
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-21/part-2",
            json={
                "document": file.read().splitlines(),
                "steps": steps,
            },
        )

        assert response.status_code == 200
        # assert response.json() == output
        print(response.json())
