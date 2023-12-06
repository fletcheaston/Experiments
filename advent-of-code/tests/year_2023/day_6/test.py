import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "times,distances,output",
    [
        ([7, 15, 30], [9, 40, 200], 288),
        ([47, 98, 66, 98], [400, 1213, 1011, 1540], 1660968),
    ],
)
def test_part_1(
    times: list[int], distances: list[int], output: int, test_client: TestClient
) -> None:
    response = test_client.post(
        "2023/day-6/part-1",
        json={
            "times": times,
            "distances": distances,
        },
    )

    assert response.status_code == 200
    assert response.json() == output


@pytest.mark.parametrize(
    "time,distance,output",
    [
        (71530, 940200, 71503),
        (47986698, 400121310111540, 26499773),
    ],
)
def test_part_2(time: int, distance: int, output: int, test_client: TestClient) -> None:
    response = test_client.post(
        "2023/day-6/part-2",
        json={
            "time": time,
            "distance": distance,
        },
    )

    assert response.status_code == 200
    assert response.json() == output
