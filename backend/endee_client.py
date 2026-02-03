"""
Endee vector database client using the official Python SDK.
Configured for local Docker (endee-server on localhost:8080).
"""

from endee import Endee
from endee.exceptions import APIException

# Base URL for Endee Docker - use localhost for local development
BASE_URL = "http://localhost:8080"

# Initialize client - empty token for local Docker (NDD_AUTH_TOKEN="")
_client = Endee(token="")
_client.set_base_url(BASE_URL)


def create_index(index_name: str, dim: int):
    """Create a vector index if it doesn't exist."""
    try:
        _client.create_index(
            name=index_name,
            dimension=dim,
            space_type="cosine"
        )
    except (ConnectionError, OSError) as e:
        raise ConnectionError(
            "Cannot connect to Endee database. Run: docker-compose up -d"
        ) from e
    except APIException as e:
        err = str(e).lower()
        if "unknown error" in err or "connection" in err or "refused" in err or "timeout" in err:
            raise ConnectionError(
                "Cannot connect to Endee database. Run: docker-compose up -d"
            ) from e
        if "already exists" in err or "duplicate" in err:
            pass  # Index already exists, continue
        else:
            raise
    except Exception as e:
        err = str(e).lower()
        if "connection" in err or "refused" in err or "timeout" in err:
            raise ConnectionError(
                "Cannot connect to Endee database. Run: docker-compose up -d"
            ) from e
        if "already exists" in err or "duplicate" in err:
            pass  # Index already exists, continue
        else:
            raise


def insert_vector(index_name: str, vector: list, metadata: dict, vector_id: str = None):
    """Insert a vector with metadata into the index."""
    try:
        index = _client.get_index(name=index_name)
        vid = vector_id if vector_id else metadata.get("id") or str(metadata.get("chunk_id", abs(hash(str(metadata))) % (10**9)))
        index.upsert([{
            "id": str(vid),
            "vector": vector,
            "meta": metadata
        }])
    except (ConnectionError, OSError) as e:
        raise ConnectionError(
            "Cannot connect to Endee database. Run: docker-compose up -d"
        ) from e
    except APIException as e:
        err = str(e).lower()
        if "unknown error" in err or "connection" in err or "refused" in err or "timeout" in err:
            raise ConnectionError(
                "Cannot connect to Endee database. Run: docker-compose up -d"
            ) from e
        raise
    except Exception as e:
        err = str(e).lower()
        if "connection" in err or "refused" in err or "timeout" in err:
            raise ConnectionError(
                "Cannot connect to Endee database. Run: docker-compose up -d"
            ) from e
        raise


def search(index_name: str, vector: list, top_k: int = 3):
    """Search for similar vectors. Returns list with 'meta' (SDK uses meta not metadata)."""
    try:
        index = _client.get_index(name=index_name)
        results = index.query(vector=vector, top_k=top_k)
        return results or []
    except (ConnectionError, OSError) as e:
        raise ConnectionError(
            "Cannot connect to Endee database. Is it running? Run: docker-compose up -d"
        ) from e
    except APIException as e:
        err_msg = str(e).lower()
        if "unknown error" in err_msg or "connection" in err_msg or "refused" in err_msg or "timeout" in err_msg:
            raise ConnectionError(
                "Cannot connect to Endee database. Run: docker-compose up -d"
            ) from e
        raise RuntimeError(f"Endee search failed: {e}") from e
    except Exception as e:
        err_msg = str(e).lower()
        if "connection" in err_msg or "refused" in err_msg or "timeout" in err_msg:
            raise ConnectionError(
                "Cannot connect to Endee database. Run: docker-compose up -d"
            ) from e
        raise RuntimeError(f"Endee search failed: {e}") from e
