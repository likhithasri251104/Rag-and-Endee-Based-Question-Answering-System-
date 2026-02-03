import sys
from pathlib import Path

# Ensure project root is on path when run as script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.embedder import embed_text
from backend.endee_client import create_index, insert_vector

INDEX_NAME = "docs"
DIMENSION = 384
DATA_FILE = PROJECT_ROOT / "data" / "sample.txt"


def main():
    if not DATA_FILE.exists():
        print(f"Error: Data file not found: {DATA_FILE}")
        sys.exit(1)

    try:
        create_index(INDEX_NAME, DIMENSION)
    except ConnectionError as e:
        print(f"Error: {e}")
        sys.exit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = text.split("\n")

    try:
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                embedding = embed_text(chunk)
                insert_vector(
                    INDEX_NAME,
                    embedding,
                    {"text": chunk, "chunk_id": i},
                    vector_id=f"docs_chunk_{i}"
                )
    except ConnectionError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("Documents ingested successfully.")


if __name__ == "__main__":
    main()
