"""Analytics Agent — analyzes weekly performance and recommends improvements."""
from pathlib import Path

from .base_agent import BaseAgent

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "analytics.txt").read_text(
    encoding="utf-8"
) if (Path(__file__).parent.parent / "prompts" / "analytics.txt").exists() else ""


class AnalyticsAgent(BaseAgent):
    """Reviews pipeline metrics and generates weekly report with recommendations."""

    def __init__(self) -> None:
        super().__init__(name="AnalyticsAgent", system_prompt=SYSTEM_PROMPT)
