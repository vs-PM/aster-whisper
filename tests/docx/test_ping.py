import pytest
from fastapi.testclient import TestClient

from v1.main import app

client = TestClient(app)

def test_docx_ping():
    response = client.get("/docx/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "docx ok"}
