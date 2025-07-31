import pytest
from fastapi.testclient import TestClient
from pm_work.v1.main import app

client = TestClient(app)

def test_whisper_ping():
    response = client.get("/whisper/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "whisper ok"}
