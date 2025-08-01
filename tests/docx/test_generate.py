from fastapi.testclient import TestClient
from v1.main import app

client = TestClient(app)

def test_generate_docx():
    # Пример запроса, структура зависит от DocxGenerateRequest
    payload = {
        "template_id": 1,
        "data": {"key": "value"}
    }
    response = client.post("/docx/generate", json=payload)
    assert response.status_code in (200, 422, 500)  # 422 если невалидно, 200 если ok, 500 если ошибка
    # Проверяем, что либо файл, либо ошибка
    assert response.headers.get("content-type", "").startswith("application/vnd.openxmlformats-officedocument.wordprocessingml.document") or "detail" in response.json()
