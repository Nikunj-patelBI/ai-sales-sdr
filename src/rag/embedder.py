"""Embedding pipeline using Voyage AI."""
from __future__ import annotations

import os

import voyageai

_client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
MODEL = os.getenv("EMBEDDING_MODEL", "voyage-3")


def embed_text(text: str) -> list[float]:
    """Embed a single piece of text."""
    return _client.embed([text], model=MODEL).embeddings[0]


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts (up to 128 per call for voyage-3)."""
    return _client.embed(texts, model=MODEL).embeddings
