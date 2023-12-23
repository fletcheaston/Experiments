from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,output",
    [
        # ("example-1.txt", 0),
        ("example-2.txt", 0),
        # ("input.txt", 0),
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
            "2023/day-23/part-1",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        # assert response.json() == output
        print(response.json())


@pytest.mark.parametrize(
    "filename,output",
    [
        # ("example-1.txt", 0),
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
            "2023/day-23/part-2",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output
