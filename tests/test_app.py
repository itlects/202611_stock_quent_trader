from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["orders_enabled"] is False

def test_candidates_sorted():
    response = client.get("/api/candidates")
    assert response.status_code == 200
    scores = [x["score"] for x in response.json()]
    assert scores == sorted(scores, reverse=True)

def test_manual_selection():
    response = client.post("/api/selection", json={"mode": "approval", "codes": ["DEMO001"]})
    assert response.status_code == 200
    assert response.json()["selected_codes"] == ["DEMO001"]
    assert response.json()["orders_enabled"] is False
