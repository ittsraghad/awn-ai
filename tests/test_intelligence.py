import pytest

from src.intelligence import analyze_message, load_intent_model


def test_intent_model_loads_successfully():
    artifact = load_intent_model()

    assert artifact is not None
    assert "vectorizer" in artifact
    assert "classifier" in artifact
    assert "intents" in artifact
    assert len(artifact["intents"]) == 27


def test_analyze_message_returns_expected_structure():
    result = analyze_message("I want to track my order")

    assert result["message"] == "I want to track my order"
    assert result["category"] == "ORDER"
    assert result["intent"] == "track_order"


def test_analyze_message_predicts_refund():
    result = analyze_message("I want to request a refund")

    assert result["scope"] == "IN_SCOPE"
    assert result["category"] == "REFUND"
    assert result["intent"] == "get_refund"


def test_analyze_message_handles_unclear_scope():
    result = analyze_message("I need help getting a refund")

    assert result["scope"] == "UNCLEAR_SCOPE"
    assert result["category"] is None
    assert result["intent"] is None


def test_analyze_message_predicts_payment():
    result = analyze_message("What payment methods do you accept?")

    assert result["category"] == "PAYMENT"
    assert result["intent"] == "check_payment_methods"


def test_empty_message_raises_value_error():
    with pytest.raises(ValueError, match="Message cannot be empty."):
        analyze_message("   ")


def test_non_string_message_raises_type_error():
    with pytest.raises(TypeError, match="Message must be a string."):
        analyze_message(12345)
