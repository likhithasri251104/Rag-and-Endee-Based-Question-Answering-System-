from pathlib import Path

from backend.embedder import embed_text
from backend.endee_client import search

INDEX_NAME = "docs"
SAMPLE_FILE = Path(__file__).resolve().parent.parent / "data" / "sample.txt"


def _fallback_retrieve(query: str) -> str:
    """Fallback when Endee is unreachable: load sample.txt and match by keywords."""
    if not SAMPLE_FILE.exists():
        return ""
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        chunks = [line.strip() for line in f if line.strip()]
    if not chunks:
        return ""
    query_lower = query.lower().split()
    matched = [c for c in chunks if any(word in c.lower() for word in query_lower)]
    return " ".join(matched) if matched else " ".join(chunks)


def retrieve_context(query: str) -> str:
    try:
        query_vec = embed_text(query)
        results = search(INDEX_NAME, query_vec)
    except (ConnectionError, RuntimeError):
        return _fallback_retrieve(query)

    if not results:
        return ""

    # Endee SDK returns 'meta' (not 'metadata'); defensive check for non-dict
    contexts = []
    for r in results:
        if not isinstance(r, dict):
            continue
        text = (r.get("meta") or {}).get("text", "")
        if text:
            contexts.append(text)
    return " ".join(contexts)
