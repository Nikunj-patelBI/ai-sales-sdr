"""Initialize all Qdrant vector collections required by the pipeline."""
from __future__ import annotations

import os

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

COLLECTIONS = [
    "company_profiles",
    "prospect_contacts",
    "ag_content",
    "email_history",
    "industry_knowledge",
    "successful_patterns",
]

VECTOR_SIZE = 1024  # voyage-3


def main() -> None:
    client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
    existing = {c.name for c in client.get_collections().collections}

    for name in COLLECTIONS:
        if name in existing:
            print(f"[skip] {name} already exists")
            continue
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"[created] {name}")


if __name__ == "__main__":
    main()
