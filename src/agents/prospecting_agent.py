"""Prospecting Agent — finds and qualifies new leads matching ICP."""
from pathlib import Path

from .base_agent import BaseAgent

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "prospecting.txt").read_text(
    encoding="utf-8"
) if (Path(__file__).parent.parent / "prompts" / "prospecting.txt").exists() else ""


class ProspectingAgent(BaseAgent):
    """Autonomous agent that finds 25 qualified leads per day."""

    def __init__(self) -> None:
        super().__init__(name="ProspectingAgent", system_prompt=SYSTEM_PROMPT)
