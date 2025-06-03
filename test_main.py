from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_create_story():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": False,
        "genre": "Adventure",
        "experimentBoundary": 3.0,
        "totalStoryCharacters": 2,
        "totalParagraphs": 2,
        "totalWords": 150
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert isinstance(data["story"], str)
    assert len(data["story"]) > 0
    assert "storySummary" in data
    assert isinstance(data["storySummary"], str)
    assert "modelStatistics" in data
    assert data["modelStatistics"] is not None
    assert "tokensUsedCount" in data["modelStatistics"]
    assert "timeTakenToProcessPrompt" in data["modelStatistics"]
    assert data["error"] is None

def test_create_story_missing_field():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": False
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 422

def test_create_story_invalid_type():
    payload = {
        "plot": "A hero saves the world.",
        "imageNeeded": "hello",
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
    
@pytest.mark.skipif(True, reason="Skip this test for now")
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
        "imageNeeded": False,
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
        "imageNeeded": False,
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


@pytest.mark.skipif(True, reason="Skip this test for now")
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

def test_create_story_success():
    payload = {
        "plot": "A young wizard discovers her powers.",
        "imageNeeded": False,
        "genre": "Fantasy",
        "experimentBoundary": 0.3,
        "totalStoryCharacters": 3,
        "totalParagraphs": 2,
        "totalWords": 200
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert "storySummary" in data
    assert "modelStatistics" in data
    assert data["error"] is None

def test_create_story_validation_error():
    payload = {
        "plot": "",
        "imageNeeded": False,
        "genre": "Fantasy",
        "experimentBoundary": 0.3,
        "totalStoryCharacters": 0,  # Invalid: less than min
        "totalParagraphs": 6,       # Invalid: more than max
        "totalWords": 50            # Invalid: less than min
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 422

def test_develop_story_success():
    payload = {
        "plot": "The hero faces a new rival.",
        "imageNeeded": False,
        "genre": "Fantasy",
        "experimentBoundary": 0.4,
        "totalStoryCharacters": 2,
        "totalParagraphs": 3,
        "totalWords": 150,
        "summary": "A young wizard discovers her powers and saves her village."
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert "storySummary" in data
    assert "modelStatistics" in data
    assert data["error"] is None

def test_develop_story_missing_summary():
    payload = {
        "plot": "The hero faces a new rival.",
        "imageNeeded": False,
        "genre": "Fantasy",
        "experimentBoundary": 0.4,
        "totalStoryCharacters": 2,
        "totalParagraphs": 3,
        "totalWords": 150
        # Missing 'summary'
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 422

def test_develop_story_invalid_characters():
    payload = {
        "plot": "The hero faces a new rival.",
        "imageNeeded": False,
        "genre": "Fantasy",
        "experimentBoundary": 0.4,
        "totalStoryCharacters": 11,  # Invalid: more than max
        "totalParagraphs": 3,
        "totalWords": 150,
        "summary": "A young wizard discovers her powers and saves her village."
    }
    response = client.post("/develop-story", json=payload)
    assert response.status_code == 422

def test_create_story_min_max_values():
    payload = {
        "plot": "A test plot.",
        "imageNeeded": False,
        "genre": "Adventure",
        "experimentBoundary": 0.0,
        "totalStoryCharacters": 1,
        "totalParagraphs": 5,
        "totalWords": 400
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "story" in data
    assert "storySummary" in data
    assert "modelStatistics" in data
    assert data["error"] is None
