"""Outreach Agent — crafts and sends personalized outreach using RAG."""
from pathlib import Path

from .base_agent import BaseAgent

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "outreach.txt").read_text(
    encoding="utf-8"
) if (Path(__file__).parent.parent / "prompts" / "outreach.txt").exists() else ""


class OutreachAgent(BaseAgent):
    """Generates personalized emails and LinkedIn messages using retrieved context."""

    def __init__(self) -> None:
        super().__init__(name="OutreachAgent", system_prompt=SYSTEM_PROMPT)
