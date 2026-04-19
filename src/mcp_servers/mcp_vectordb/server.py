"""MCP server: Qdrant vector DB operations."""
from __future__ import annotations

import asyncio
import os

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from src.rag.embedder import embed_text

server = Server("mcp-vectordb")
_client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_similar",
            description="Semantic search in a vector collection.",
            inputSchema={
                "type": "object",
                "required": ["collection", "query"],
                "properties": {
                    "collection": {"type": "string"},
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 5},
                },
            },
        ),
        Tool(
            name="store_embedding",
            description="Store a new item with its embedding in a collection.",
            inputSchema={
                "type": "object",
                "required": ["collection", "id", "text", "payload"],
                "properties": {
                    "collection": {"type": "string"},
                    "id": {"type": "string"},
                    "text": {"type": "string"},
                    "payload": {"type": "object"},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_similar":
        vector = embed_text(arguments["query"])
        hits = _client.search(
            collection_name=arguments["collection"],
            query_vector=vector,
            limit=arguments.get("top_k", 5),
        )
        results = [{"score": h.score, "payload": h.payload} for h in hits]
        return [TextContent(type="text", text=str(results))]

    if name == "store_embedding":
        vector = embed_text(arguments["text"])
        _client.upsert(
            collection_name=arguments["collection"],
            points=[
                PointStruct(id=arguments["id"], vector=vector, payload=arguments["payload"])
            ],
        )
        return [TextContent(type="text", text=f"Stored {arguments['id']}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
