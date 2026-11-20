import pytest

from src.response_generator import (
    FALLBACK_RESPONSE,
    build_generation_messages,
    generate_response,
)


SAMPLE_MESSAGE = "Where is my order?"

SAMPLE_DOCUMENTS = [
    {
        "chunk_id": "KB001",
        "title": "Order Tracking",
        "section": "Orders",
        "subsection": "Tracking",
        "content": "Customers can track their orders using the tracking link.",
    }
]


def test_build_generation_messages():
    messages = build_generation_messages(
        SAMPLE_MESSAGE,
        SAMPLE_DOCUMENTS
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert SAMPLE_MESSAGE in messages[1]["content"]


def test_prompt_contains_knowledge_context():
    messages = build_generation_messages(
        SAMPLE_MESSAGE,
        SAMPLE_DOCUMENTS
    )

    user_prompt = messages[1]["content"]

    assert "Order Tracking" in user_prompt
    assert "Customers can track their orders" in user_prompt


def test_message_whitespace_is_stripped():
    messages = build_generation_messages(
        "  Where is my order?  ",
        SAMPLE_DOCUMENTS
    )

    assert "Where is my order?" in messages[1]["content"]


def test_empty_message_raises_error():
    with pytest.raises(ValueError):
        build_generation_messages(
            "   ",
            SAMPLE_DOCUMENTS
        )


def test_non_string_message_raises_error():
    with pytest.raises(TypeError):
        build_generation_messages(
            123,
            SAMPLE_DOCUMENTS
        )


def test_empty_documents_raise_error():
    with pytest.raises(ValueError):
        build_generation_messages(
            SAMPLE_MESSAGE,
            []
        )


def test_invalid_document_content_raises_error():
    documents = [
        {
            "title": "Empty Document",
            "section": "Test",
            "content": "   ",
        }
    ]

    with pytest.raises(ValueError):
        build_generation_messages(
            SAMPLE_MESSAGE,
            documents
        )


def test_generate_response_with_mock_llm():
    def fake_llm(messages):
        return "You can track your order using the tracking link."

    response = generate_response(
        SAMPLE_MESSAGE,
        SAMPLE_DOCUMENTS,
        fake_llm
    )

    assert isinstance(response, str)
    assert "tracking link" in response


def test_generate_response_passes_messages_to_llm():
    received_messages = []

    def fake_llm(messages):
        received_messages.extend(messages)
        return "Your order can be tracked online."

    generate_response(
        SAMPLE_MESSAGE,
        SAMPLE_DOCUMENTS,
        fake_llm
    )

    assert len(received_messages) == 2
    assert received_messages[0]["role"] == "system"


def test_empty_documents_return_fallback():
    def fake_llm(messages):
        raise AssertionError("LLM should not be called.")

    response = generate_response(
        SAMPLE_MESSAGE,
        [],
        fake_llm
    )

    assert response == FALLBACK_RESPONSE


def test_non_callable_llm_raises_error():
    with pytest.raises(TypeError):
        generate_response(
            SAMPLE_MESSAGE,
            SAMPLE_DOCUMENTS,
            "not a function"
        )


def test_non_string_llm_response_raises_error():
    def fake_llm(messages):
        return 123

    with pytest.raises(TypeError):
        generate_response(
            SAMPLE_MESSAGE,
            SAMPLE_DOCUMENTS,
            fake_llm
        )


def test_empty_llm_response_raises_error():
    def fake_llm(messages):
        return "   "

    with pytest.raises(ValueError):
        generate_response(
            SAMPLE_MESSAGE,
            SAMPLE_DOCUMENTS,
            fake_llm
        )