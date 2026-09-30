from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "ComicCraft" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_api():
    response = client.post(
        "/api/generate",
        json={
            "title": "Test Comic",
            "idea": "A tiny robot finds a flower.",
            "genre": "Sci-Fi",
            "tone": "Hopeful",
            "panel_count": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Comic"
    assert len(data["panels"]) == 2
    assert data["pdf_url"].endswith(".pdf")
