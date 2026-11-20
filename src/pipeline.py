from src.intelligence import analyze_message
from src.retriever import retrieve_documents
from src.response_generator import (
    generate_response,
    FALLBACK_RESPONSE,
    OUT_OF_SCOPE_RESPONSE,
    UNCLEAR_SCOPE_RESPONSE,
)


def process_customer_message(
    message: str,
    llm_callable,
    top_k: int = 3
) -> dict:
    """
    Process a customer message through the complete
    AWN AI intelligence, retrieval, and response pipeline.
    """

    if not isinstance(message, str):
        raise TypeError("Message must be a string.")

    message = message.strip()

    if not message:
        raise ValueError("Message cannot be empty.")

    if not callable(llm_callable):
        raise TypeError("llm_callable must be callable.")

    # Step 1: Analyze the customer message
    analysis = analyze_message(message)

    scope = analysis["scope"]

    # Step 2: Handle messages outside the service scope
    if scope == "OUT_OF_SCOPE":
        return {
            "message": message,
            "scope": scope,
            "category": None,
            "intent": None,
            "retrieved_documents": [],
            "response": OUT_OF_SCOPE_RESPONSE
        }

    # Step 3: Ask for clarification when scope is unclear
    if scope == "UNCLEAR_SCOPE":
        return {
            "message": message,
            "scope": scope,
            "category": None,
            "intent": None,
            "retrieved_documents": [],
            "response": UNCLEAR_SCOPE_RESPONSE
        }

    # Step 4: Retrieve relevant knowledge
    documents = retrieve_documents(
        query=message,
        top_k=top_k,
        intent=analysis["intent"]
    )

    # Step 5: Generate a grounded response
    if documents:
        response = generate_response(
            message=message,
            documents=documents,
            llm_callable=llm_callable
        )
    else:
        response = FALLBACK_RESPONSE

    return {
        "message": message,
        "scope": scope,
        "category": analysis["category"],
        "intent": analysis["intent"],
        "retrieved_documents": documents,
        "response": response
    }