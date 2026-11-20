
import pytest

from src.predictor import load_model, predict_category


def test_model_loads_successfully():
    """
    Verify that the V2 model artifact loads correctly.
    """
    artifact = load_model()

    assert artifact is not None
    assert "vectorizer" in artifact
    assert "classifier" in artifact
    assert "categories" in artifact
    assert artifact["model_name"] == "Character TF-IDF + Linear SVM"
    assert artifact["version"] == "2.0"


def test_model_has_eleven_categories():
    """
    Verify that the model contains all expected categories.
    """
    artifact = load_model()

    assert len(artifact["categories"]) == 11


def test_prediction_returns_valid_category():
    """
    Verify that prediction returns a valid category.
    """
    result = predict_category("I need help with my refund")

    artifact = load_model()

    assert result in artifact["categories"]
    assert result == "REFUND"


def test_empty_input_raises_value_error():
    """
    Verify that empty input is rejected.
    """
    with pytest.raises(
        ValueError,
        match="Input text cannot be empty."
    ):
        predict_category("   ")


def test_non_string_input_raises_type_error():
    """
    Verify that non-string input is rejected.
    """
    with pytest.raises(
        TypeError,
        match="Input must be a string."
    ):
        predict_category(12345)


def test_model_is_cached():
    """
    Verify that the model is loaded only once.
    """
    load_model.cache_clear()

    first_load = load_model()
    second_load = load_model()

    assert first_load is second_load

    cache_info = load_model.cache_info()

    assert cache_info.misses == 1
    assert cache_info.hits == 1
