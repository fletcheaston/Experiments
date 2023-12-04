from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,output",
    [
        (
            "part-1.txt",
            7,
        ),
        (
            "input.txt",
            1134,
        ),
    ],
)
def test_part_1(
    filename: str,
    output: str,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2022/day-6/part-1",
            json={
                "document": file.read().splitlines()[0],
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "filename,output",
    [
        (
            "part-2.txt",
            19,
        ),
        (
            "input.txt",
            2263,
        ),
    ],
)
def test_part_2(
    filename: str,
    output: str,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2022/day-6/part-2",
            json={
                "document": file.read().splitlines()[0],
            },
        )

        assert response.status_code == 200
        assert response.json() == output
