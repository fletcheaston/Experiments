import pytest
from fastapi.testclient import TestClient

from app import PREFIX, app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(
        app=app,
        base_url=f"http://testserver/{PREFIX}",
    )
