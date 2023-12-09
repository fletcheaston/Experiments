from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,output",
    [
        ("part-1.txt", 114),
        ("input.txt", 1647269739),
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
            "2023/day-9/part-1",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("part-2.txt", 2),
        ("input.txt", 864),
    ],
)
def test_part_2(
    filename: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-9/part-2",
            json={
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output
