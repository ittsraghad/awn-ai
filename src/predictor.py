from pathlib import Path
from functools import lru_cache

import joblib


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "lumora_model_v2.joblib"
)


@lru_cache(maxsize=1)
def load_model():
    """
    Load and cache the trained Lumora model artifact.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    artifact = joblib.load(MODEL_PATH)

    return artifact


def predict_category(text):
    """
    Predict the category of a customer support ticket.
    """

    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text = text.strip()

    if not text:
        raise ValueError("Input text cannot be empty.")

    artifact = load_model()

    vectorizer = artifact["vectorizer"]
    classifier = artifact["classifier"]

    text_vector = vectorizer.transform([text])

    prediction = classifier.predict(text_vector)[0]

    return prediction