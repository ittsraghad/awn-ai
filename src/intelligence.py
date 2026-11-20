from pathlib import Path
from functools import lru_cache

import joblib

from src.predictor import predict_category


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SCOPE_MODEL_PATH = (
    PROJECT_ROOT / "models" / "scope_detection_v3.joblib"
)

INTENT_MODEL_PATH = (
    PROJECT_ROOT / "models" / "lumora_intent_model_v2.joblib"
)


@lru_cache(maxsize=1)
def load_scope_model():
    if not SCOPE_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Scope detection model not found: {SCOPE_MODEL_PATH}"
        )

    return joblib.load(SCOPE_MODEL_PATH)


@lru_cache(maxsize=1)
def load_intent_model():
    if not INTENT_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Intent model not found: {INTENT_MODEL_PATH}"
        )

    return joblib.load(INTENT_MODEL_PATH)


def analyze_message(message: str) -> dict:
    """
    Analyze a message using Scope Detection V3.

    Only messages classified as IN_SCOPE proceed to
    category and intent prediction.
    """

    if not isinstance(message, str):
        raise TypeError("Message must be a string.")

    message = message.strip()

    if not message:
        raise ValueError("Message cannot be empty.")

    # Step 1: Detect message scope
    scope_model = load_scope_model()
    scope = scope_model.predict([message])[0]

    # Step 2: Stop processing messages outside the service scope
    if scope != "IN_SCOPE":
        return {
            "message": message,
            "scope": scope,
            "category": None,
            "intent": None
        }

    # Step 3: Predict category
    category = predict_category(message)

    # Step 4: Predict intent using V2
    intent_artifact = load_intent_model()

    vectorizer = intent_artifact["vectorizer"]
    classifier = intent_artifact["classifier"]

    message_vector = vectorizer.transform([message])
    intent = classifier.predict(message_vector)[0]

    return {
        "message": message,
        "scope": scope,
        "category": category,
        "intent": intent
    }