"""Pipeline Orchestrator — coordinates daily execution of all agents."""
from __future__ import annotations

import argparse
import asyncio

import structlog

from .analytics_agent import AnalyticsAgent
from .followup_agent import FollowUpAgent
from .outreach_agent import OutreachAgent
from .prospecting_agent import ProspectingAgent

log = structlog.get_logger(__name__)


class PipelineOrchestrator:
    """Coordinates the daily pipeline across all agents."""

    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.prospecting = ProspectingAgent()
        self.outreach = OutreachAgent()
        self.followup = FollowUpAgent()
        self.analytics = AnalyticsAgent()

    async def run_daily(self) -> None:
        log.info("pipeline_start", dry_run=self.dry_run)

        prospect_result = await self.prospecting.run(
            "Find 25 new qualified leads matching our ICP. Score and store them."
        )
        log.info("prospecting_done", result=prospect_result.get("status"))

        outreach_result = await self.outreach.run(
            "Send personalized outreach to new qualified leads. "
            "Continue sequences for existing leads in pipeline."
        )
        log.info("outreach_done", result=outreach_result.get("status"))

        followup_result = await self.followup.run(
            "Check for new replies, engagement signals, and LinkedIn acceptances. "
            "Draft responses and update lead statuses."
        )
        log.info("followup_done", result=followup_result.get("status"))

    async def run_weekly(self) -> None:
        await self.analytics.run(
            "Analyze this week's pipeline performance. "
            "Identify what worked, what didn't, and recommend next steps."
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Do not send real outreach")
    parser.add_argument("--weekly", action="store_true", help="Run weekly analytics instead")
    args = parser.parse_args()

    orch = PipelineOrchestrator(dry_run=args.dry_run)
    if args.weekly:
        asyncio.run(orch.run_weekly())
    else:
        asyncio.run(orch.run_daily())


if __name__ == "__main__":
    main()
