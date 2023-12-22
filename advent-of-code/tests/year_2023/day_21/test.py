from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,steps,output",
    [
        ("example.txt", 6, 16),
        ("example.txt", 7, 21),
        ("example.txt", 64, 42),
        ("input.txt", 64, 3758),
        ("input-p2-l.txt", 65, 3848),
        ("input-p2-l.txt", 64, 3758),
        ("input-p2-r.txt", 65, 3848),
        ("input-p2-r.txt", 64, 3758),
        ("input-p2-t.txt", 65, 3848),
        ("input-p2-t.txt", 64, 3758),
        ("input-p2-b.txt", 65, 3848),
        ("input-p2-b.txt", 64, 3758),
        ("input-p2-tl.txt", 65, 3848),
        ("input-p2-tl.txt", 64, 3758),
        ("input-p2-tr.txt", 65, 3848),
        ("input-p2-tr.txt", 64, 3758),
        ("input-p2-bl.txt", 65, 3848),
        ("input-p2-bl.txt", 64, 3758),
        ("input-p2-br.txt", 65, 3848),
        ("input-p2-br.txt", 64, 3758),
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
        # assert response.json() == output
        print(
            filename.replace("input-p2-", "").replace(".txt", ""),
            steps % 2,
            response.json(),
        )
