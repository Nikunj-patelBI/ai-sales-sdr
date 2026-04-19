"""Follow-Up Agent — monitors engagement signals and manages responses."""
from pathlib import Path

from .base_agent import BaseAgent

SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "followup.txt").read_text(
    encoding="utf-8"
) if (Path(__file__).parent.parent / "prompts" / "followup.txt").exists() else ""


class FollowUpAgent(BaseAgent):
    """Classifies replies, drafts responses, and updates sequences."""

    def __init__(self) -> None:
        super().__init__(name="FollowUpAgent", system_prompt=SYSTEM_PROMPT)
