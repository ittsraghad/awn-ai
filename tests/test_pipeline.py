import pytest

from src.pipeline import process_customer_message


def fake_llm(messages):
    return "You can track your order using the tracking link."


def test_pipeline_returns_complete_result():
    result = process_customer_message(
        message="Where is my order?",
        llm_callable=fake_llm
    )

    assert result["message"] == "Where is my order?"
    assert result["scope"] == "IN_SCOPE"
    assert isinstance(result["category"], str)
    assert isinstance(result["intent"], str)
    assert isinstance(result["retrieved_documents"], list)
    assert isinstance(result["response"], str)


def test_pipeline_predicts_order_tracking_intent():
    result = process_customer_message(
        message="Where is my order?",
        llm_callable=fake_llm
    )

    assert result["intent"] == "track_order"


def test_pipeline_returns_retrieved_documents():
    result = process_customer_message(
        message="How can I track my shipment?",
        llm_callable=fake_llm
    )

    assert len(result["retrieved_documents"]) > 0

    document = result["retrieved_documents"][0]

    assert "title" in document
    assert "content" in document
    assert "score" in document


def test_pipeline_uses_llm_response():
    expected_response = "Your order can be tracked online."

    def custom_llm(messages):
        return expected_response

    result = process_customer_message(
        message="Where is my order?",
        llm_callable=custom_llm
    )

    assert result["response"] == expected_response


def test_pipeline_handles_out_of_scope(monkeypatch):
    from src import pipeline

    monkeypatch.setattr(
        pipeline,
        "analyze_message",
        lambda message: {
            "message": message,
            "scope": "OUT_OF_SCOPE",
            "category": None,
            "intent": None
        }
    )

    def unexpected_call(*args, **kwargs):
        raise AssertionError(
            "Retrieval or LLM should not be called."
        )

    monkeypatch.setattr(
        pipeline,
        "retrieve_documents",
        unexpected_call
    )

    monkeypatch.setattr(
        pipeline,
        "generate_response",
        unexpected_call
    )

    result = process_customer_message(
        message="Tell me a joke.",
        llm_callable=fake_llm
    )

    assert result["scope"] == "OUT_OF_SCOPE"
    assert result["category"] is None
    assert result["intent"] is None
    assert result["retrieved_documents"] == []
    assert isinstance(result["response"], str)


def test_pipeline_handles_unclear_scope(monkeypatch):
    from src import pipeline

    monkeypatch.setattr(
        pipeline,
        "analyze_message",
        lambda message: {
            "message": message,
            "scope": "UNCLEAR_SCOPE",
            "category": None,
            "intent": None
        }
    )

    def unexpected_call(*args, **kwargs):
        raise AssertionError(
            "Retrieval or LLM should not be called."
        )

    monkeypatch.setattr(
        pipeline,
        "retrieve_documents",
        unexpected_call
    )

    monkeypatch.setattr(
        pipeline,
        "generate_response",
        unexpected_call
    )

    result = process_customer_message(
        message="I need some help.",
        llm_callable=fake_llm
    )

    assert result["scope"] == "UNCLEAR_SCOPE"
    assert result["category"] is None
    assert result["intent"] is None
    assert result["retrieved_documents"] == []
    assert isinstance(result["response"], str)


def test_pipeline_rejects_empty_message():
    with pytest.raises(ValueError):
        process_customer_message(
            message="   ",
            llm_callable=fake_llm
        )


def test_pipeline_rejects_non_string_message():
    with pytest.raises(TypeError):
        process_customer_message(
            message=123,
            llm_callable=fake_llm
        )


def test_pipeline_rejects_invalid_llm():
    with pytest.raises(TypeError):
        process_customer_message(
            message="Where is my order?",
            llm_callable="invalid"
        )


def test_pipeline_rejects_invalid_top_k():
    with pytest.raises(ValueError):
        process_customer_message(
            message="Where is my order?",
            llm_callable=fake_llm,
            top_k=0
        )