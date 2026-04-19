"""MCP server: Google Sheets CRM."""
from __future__ import annotations

import asyncio
import os
from datetime import datetime

import gspread
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

server = Server("mcp-crm")

_gc = gspread.service_account(filename=os.getenv("GOOGLE_CREDS_PATH", "./credentials.json"))
_sheet = _gc.open_by_key(os.getenv("CRM_SHEET_ID"))


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="read_leads",
            description="Read leads from CRM filtered by status or tier.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "tier": {"type": "string", "enum": ["HOT", "WARM", "COLD"]},
                    "limit": {"type": "integer", "default": 50},
                },
            },
        ),
        Tool(
            name="write_lead",
            description="Add a new lead to the CRM.",
            inputSchema={
                "type": "object",
                "required": ["name", "email", "company"],
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "company": {"type": "string"},
                    "title": {"type": "string"},
                    "score": {"type": "integer"},
                    "tier": {"type": "string"},
                    "source": {"type": "string"},
                },
            },
        ),
        Tool(
            name="log_activity",
            description="Log a sales activity (email sent, call made, etc.).",
            inputSchema={
                "type": "object",
                "required": ["lead_id", "channel", "action"],
                "properties": {
                    "lead_id": {"type": "string"},
                    "channel": {"type": "string"},
                    "action": {"type": "string"},
                    "details": {"type": "string"},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "write_lead":
        ws = _sheet.worksheet("Master Leads")
        ws.append_row(
            [
                arguments["name"],
                arguments["email"],
                arguments.get("company", ""),
                arguments.get("title", ""),
                arguments.get("score", 0),
                arguments.get("tier", "COLD"),
                arguments.get("source", "unknown"),
                datetime.utcnow().isoformat(),
            ]
        )
        return [TextContent(type="text", text=f"Lead {arguments['name']} added")]

    if name == "log_activity":
        ws = _sheet.worksheet("Activity Log")
        ws.append_row(
            [
                datetime.utcnow().isoformat(),
                arguments["lead_id"],
                arguments["channel"],
                arguments["action"],
                arguments.get("details", ""),
            ]
        )
        return [TextContent(type="text", text="Activity logged")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
