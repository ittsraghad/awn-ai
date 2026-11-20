import pytest

from src.retriever import retrieve_documents, load_retriever


def test_retriever_loads_successfully():
    retriever = load_retriever()

    assert "documents" in retriever
    assert "vectorizer" in retriever
    assert "document_matrix" in retriever
    assert len(retriever["documents"]) > 0


def test_retrieve_documents_returns_results():
    results = retrieve_documents("How long does a refund take?")

    assert len(results) > 0
    assert len(results) <= 3


def test_retrieved_documents_have_expected_fields():
    results = retrieve_documents("How long does a refund take?")

    expected_fields = {
        "chunk_id",
        "title",
        "section",
        "subsection",
        "content",
        "score"
    }

    assert results

    for document in results:
        assert expected_fields.issubset(document.keys())


def test_refund_query_retrieves_refund_information():
    results = retrieve_documents("How long does a refund take?")

    assert results
    assert "refund" in results[0]["content"].lower()


def test_shipping_query_retrieves_shipping_information():
    results = retrieve_documents("Can I change my shipping address?")

    assert results
    assert (
        "shipping" in results[0]["content"].lower()
        or "address" in results[0]["content"].lower()
    )


def test_empty_query_raises_value_error():
    with pytest.raises(ValueError):
        retrieve_documents("")


def test_non_string_query_raises_type_error():
    with pytest.raises(TypeError):
        retrieve_documents(123)


def test_invalid_top_k_raises_value_error():
    with pytest.raises(ValueError):
        retrieve_documents("refund", top_k=0)