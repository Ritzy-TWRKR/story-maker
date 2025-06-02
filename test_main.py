from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_create_story():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": True,
        "genre": "Adventure"
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 200
    assert response.json() == payload

def test_create_story_missing_field():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": True
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 422

def test_create_story_invalid_type():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": "yes",
        "genre": "Adventure"
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 422


def test_create_story_with_temperature():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": False,
        "genre": "Adventure",
        "experimentBoundary": 0.8
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert data["story"]
    assert "modelStatistics" in data
    assert data["modelStatistics"] is not None
    assert "tokensUsedCount" in data["modelStatistics"]
    assert "timeTakenToProcessPrompt" in data["modelStatistics"]

def test_create_story_with_default_temperature():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": False,
        "genre": "Adventure"
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert data["story"]
    assert "modelStatistics" in data
    assert data["modelStatistics"] is not None
    assert "tokensUsedCount" in data["modelStatistics"]
    assert "timeTakenToProcessPrompt" in data["modelStatistics"]

def test_create_story_with_all_fields():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": True,
        "genre": "Adventure",
        "experimentBoundary": 0.7,
        "totalStoryCharacters": 3,
        "totalParagraphs": 2,
        "totalWords": 200
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert data["story"]
    assert "modelStatistics" in data
    assert data["modelStatistics"] is not None
    assert "tokensUsedCount" in data["modelStatistics"]
    assert "timeTakenToProcessPrompt" in data["modelStatistics"]
    if payload["imageNeeded"]:
        assert "image" in data

def test_create_story_invalid_totalStoryCharacters():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": True,
        "genre": "Adventure",
        "totalStoryCharacters": 20  # Invalid, should be between 1 and 10
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 422

def test_create_story_invalid_totalParagraphs():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": True,
        "genre": "Adventure",
        "totalParagraphs": 10  # Invalid, should be between 1 and 5
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 422

def test_create_story_invalid_totalWords():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": True,
        "genre": "Adventure",
        "totalWords": 50  # Invalid, should be between 100 and 400
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 422

def test_develop_story():
    payload = {
        "plot": "A hero faces a new challenge.",
        "imageNeeded": True,
        "genre": "Drama",
        "experimentBoundary": 0.5,
        "summary": "A hero saved the world but now must find peace."
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert data["story"]
    assert "storySummary" in data
    assert data["storySummary"]
    assert "modelStatistics" in data
    assert data["modelStatistics"] is not None
    assert "tokensUsedCount" in data["modelStatistics"]
    assert "timeTakenToProcessPrompt" in data["modelStatistics"]

def test_develop_story_success():
    payload = {
        "plot": "A hero faces a new challenge.",
        "imageNeeded": True,
        "genre": "Drama",
        "experimentBoundary": 0.5,
        "summary": "A hero saved the world but now must find peace."
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert data["story"]
    assert "storySummary" in data
    assert data["storySummary"]
    assert "modelStatistics" in data
    assert data["modelStatistics"] is not None
    assert "tokensUsedCount" in data["modelStatistics"]
    assert "timeTakenToProcessPrompt" in data["modelStatistics"]
    if payload["imageNeeded"]:
        assert "image" in data

def test_develop_story_missing_summary():
    payload = {
        "plot": "A hero faces a new challenge.",
        "imageNeeded": True,
        "genre": "Drama",
        "experimentBoundary": 0.5
        # summary is missing
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 422  # Unprocessable Entity due to missing required field

# Integration test: test with different temperature

def test_develop_story_with_temperature_variation():
    payload = {
        "plot": "A hero faces a new challenge.",
        "imageNeeded": False,
        "genre": "Drama",
        "experimentBoundary": 1.2,
        "summary": "A hero saved the world but now must find peace."
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert data["story"]
    assert "modelStatistics" in data
    assert data["modelStatistics"] is not None
    assert "tokensUsedCount" in data["modelStatistics"]
    assert "timeTakenToProcessPrompt" in data["modelStatistics"]

def test_develop_story_with_all_fields():
    payload = {
        "plot": "A hero faces a new challenge.",
        "imageNeeded": True,
        "genre": "Drama",
        "experimentBoundary": 1.0,
        "summary": "A hero saved the world but now must find peace.",
        "totalStoryCharacters": 2,
        "totalParagraphs": 3,
        "totalWords": 250
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert data["story"]
    assert "storySummary" in data
    assert data["storySummary"]
    assert "modelStatistics" in data
    assert data["modelStatistics"] is not None
    assert "tokensUsedCount" in data["modelStatistics"]
    assert "timeTakenToProcessPrompt" in data["modelStatistics"]
    if payload["imageNeeded"]:
        assert "image" in data

def test_develop_story_invalid_totalStoryCharacters():
    payload = {
        "plot": "A hero faces a new challenge.",
        "imageNeeded": True,
        "genre": "Drama",
        "summary": "A hero saved the world but now must find peace.",
        "totalStoryCharacters": 0  # Invalid, should be between 1 and 10
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 422

def test_develop_story_invalid_totalParagraphs():
    payload = {
        "plot": "A hero faces a new challenge.",
        "imageNeeded": True,
        "genre": "Drama",
        "summary": "A hero saved the world but now must find peace.",
        "totalParagraphs": 0  # Invalid, should be between 1 and 5
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 422

def test_develop_story_invalid_totalWords():
    payload = {
        "plot": "A hero faces a new challenge.",
        "imageNeeded": True,
        "genre": "Drama",
        "summary": "A hero saved the world but now must find peace.",
        "totalWords": 500  # Invalid, should be between 100 and 400
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 422
