"""RAG retrieval from Qdrant."""
from __future__ import annotations

import os

from qdrant_client import QdrantClient

from .embedder import embed_text

_client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))


def retrieve(
    query: str,
    collection: str,
    top_k: int = 5,
    filters: dict | None = None,
) -> list[dict]:
    """Retrieve top-K similar items from a collection with optional metadata filtering."""
    query_vector = embed_text(query)
    hits = _client.search(
        collection_name=collection,
        query_vector=query_vector,
        limit=top_k,
        query_filter=filters,
    )
    return [{"score": h.score, "payload": h.payload} for h in hits]
