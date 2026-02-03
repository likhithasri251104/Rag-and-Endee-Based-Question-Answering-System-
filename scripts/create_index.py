"""Create the docs index using Endee SDK. Use ingest.py instead for full setup."""
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.endee_client import create_index

INDEX_NAME = "docs"
DIMENSION = 384

if __name__ == "__main__":
    try:
        create_index(INDEX_NAME, DIMENSION)
        print("Index created successfully.")
    except ConnectionError as e:
        print(f"Error: {e}")
        sys.exit(1)
