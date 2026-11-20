
from functools import lru_cache

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.knowledge_base import get_knowledge_documents
from src.intelligence import analyze_message


INTENT_SEARCH_TERMS = {
    "track_order": "order tracking shipment delivery status package location",
    "cancel_order": "cancel order cancellation stop purchase",
    "get_refund": "refund reimbursement money returned",
    "check_refund_policy": "refund policy return eligibility conditions",
    "check_invoice": "invoice bill payment document",
    "get_invoice": "download invoice obtain bill",
    "change_shipping_address": "change update shipping delivery address",
    "set_up_shipping_address": "add create set up shipping address",
    "reset_password": "reset recover forgotten password account access",
    "contact_human_agent": "contact human customer support representative",
}


# Hybrid retrieval weights
ORIGINAL_WEIGHT = 0.75
INTENT_WEIGHT = 0.25


def prepare_document_text(document: dict) -> str:
    title = document.get("title") or ""
    section = document.get("section") or ""
    subsection = document.get("subsection") or ""
    content = document.get("content") or ""

    return " ".join([
        title,
        section,
        subsection,
        content
    ])


@lru_cache(maxsize=1)
def load_retriever() -> dict:
    documents = get_knowledge_documents()

    if not documents:
        raise ValueError("No knowledge documents available.")

    document_texts = [
        prepare_document_text(document)
        for document in documents
    ]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        sublinear_tf=True,
        strip_accents="unicode"
    )

    document_matrix = vectorizer.fit_transform(document_texts)

    return {
        "documents": documents,
        "vectorizer": vectorizer,
        "document_matrix": document_matrix
    }


def retrieve_documents(
    query: str,
    top_k: int = 3,
    intent: str | None = None
) -> list[dict]:

    if not isinstance(query, str):
        raise TypeError("Query must be a string.")

    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    if (
        not isinstance(top_k, int)
        or isinstance(top_k, bool)
        or top_k < 1
    ):
        raise ValueError("top_k must be a positive integer.")

    if intent is not None and not isinstance(intent, str):
        raise TypeError("Intent must be a string or None.")

    retriever = load_retriever()

    vectorizer = retriever["vectorizer"]
    document_matrix = retriever["document_matrix"]
    documents = retriever["documents"]

    # Original query similarity
    original_vector = vectorizer.transform([query])

    original_scores = cosine_similarity(
        original_vector,
        document_matrix
    ).flatten()

    # Intent-enriched query similarity
    intent_terms = INTENT_SEARCH_TERMS.get(intent, "")

    if intent_terms:
        enriched_query = f"{query} {intent_terms}"
    else:
        enriched_query = query

    enriched_vector = vectorizer.transform([enriched_query])

    intent_scores = cosine_similarity(
        enriched_vector,
        document_matrix
    ).flatten()

    # Hybrid scoring
    final_scores = (
        ORIGINAL_WEIGHT * original_scores
        + INTENT_WEIGHT * intent_scores
    )

    ranked_indices = final_scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        final_score = float(final_scores[index])

        if final_score <= 0:
            continue

        document = documents[index]

        results.append({
            "chunk_id": document["chunk_id"],
            "title": document["title"],
            "section": document["section"],
            "subsection": document["subsection"],
            "content": document["content"],
            "score": round(final_score, 4),
            "original_score": round(
                float(original_scores[index]), 4
            ),
            "intent_score": round(
                float(intent_scores[index]), 4
            )
        })

    return results


def retrieve_for_customer(
    query: str,
    top_k: int = 3
) -> dict:

    analysis = analyze_message(query)

    documents = retrieve_documents(
        query=query,
        top_k=top_k,
        intent=analysis["intent"]
    )

    return {
        "message": query,
        "category": analysis["category"],
        "intent": analysis["intent"],
        "documents": documents
    }
