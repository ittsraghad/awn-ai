import pytest

from fastapi.testclient import TestClient
from src import api


client = TestClient(api.app)


def test_api_handles_out_of_scope(monkeypatch):

    monkeypatch.setattr(
        api,
        "analyze_message",
        lambda message: {
            "message": message,
            "scope": "OUT_OF_SCOPE",
            "category": None,
            "intent": None
        }
    )

    def unexpected_retrieval(*args, **kwargs):
        raise AssertionError(
            "Retrieval should not be called."
        )

    monkeypatch.setattr(
        api,
        "retrieve_documents",
        unexpected_retrieval
    )

    response = client.post(
        "/api/chat",
        json={"message": "Tell me a joke."}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["scope"] == "OUT_OF_SCOPE"
    assert data["category"] is None
    assert data["intent"] is None
    assert data["sources"] == []
    assert isinstance(data["response"], str)


def test_api_handles_unclear_scope(monkeypatch):

    monkeypatch.setattr(
        api,
        "analyze_message",
        lambda message: {
            "message": message,
            "scope": "UNCLEAR_SCOPE",
            "category": None,
            "intent": None
        }
    )

    def unexpected_retrieval(*args, **kwargs):
        raise AssertionError(
            "Retrieval should not be called."
        )

    monkeypatch.setattr(
        api,
        "retrieve_documents",
        unexpected_retrieval
    )

    response = client.post(
        "/api/chat",
        json={"message": "I need some help."}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["scope"] == "UNCLEAR_SCOPE"
    assert data["category"] is None
    assert data["intent"] is None
    assert data["sources"] == []
    assert isinstance(data["response"], str)


def test_api_handles_in_scope(monkeypatch):

    monkeypatch.setattr(
        api,
        "analyze_message",
        lambda message: {
            "message": message,
            "scope": "IN_SCOPE",
            "category": "ORDER",
            "intent": "track_order"
        }
    )

    expected_documents = [
        {
            "title": "Order Tracking",
            "content": "You can track your order online.",
            "score": 0.95
        }
    ]

    monkeypatch.setattr(
        api,
        "retrieve_documents",
        lambda **kwargs: expected_documents
    )

    response = client.post(
        "/api/chat",
        json={"message": "Where is my order?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["scope"] == "IN_SCOPE"
    assert data["category"] == "ORDER"
    assert data["intent"] == "track_order"
    assert data["sources"] == expected_documents
    assert "track your order online" in data["response"]


def test_api_rejects_empty_message():

    response = client.post(
        "/api/chat",
        json={"message": "   "}
    )

    assert response.status_code == 422


def test_api_health_check():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
