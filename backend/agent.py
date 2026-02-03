from backend.rag import retrieve_context

def agent_answer(question: str):
    context = retrieve_context(question)

    if not context:
        return (
            "I could not find relevant information in the documents. "
            "Please ask a question related to the uploaded documents."
        )

    return f"Answer based on retrieved documents:\n{context}"
