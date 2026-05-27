"""Generate daily markdown reports — your one-stop dashboard.

Reports are saved to data/reports/YYYY-MM-DD.md. Open the latest one each morning
to see what the pipeline did overnight.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .database import connect, pipeline_stats, todays_new_prospects

REPORTS_DIR = Path("data/reports")


def generate_daily_report() -> Path:
    """Build a markdown report for today's pipeline run."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    path = REPORTS_DIR / f"{date}.md"

    with connect() as conn:
        stats = pipeline_stats(conn)
        new_today = todays_new_prospects(conn)
        latest_run = conn.execute(
            "SELECT * FROM runs ORDER BY run_at DESC LIMIT 1"
        ).fetchone()

    lines: list[str] = []
    lines.append(f"# Daily Pipeline Report — {date}")
    lines.append("")
    lines.append(f"*Generated at {datetime.now().strftime('%H:%M %Z')}*")
    lines.append("")

    # ─── Run summary ───
    if latest_run:
        lines.append("## Today's Run")
        lines.append("")
        lines.append(f"- **Started:** {latest_run['run_at']}")
        lines.append(f"- **Duration:** {latest_run['duration_sec'] or 0:.1f}s")
        lines.append(f"- **New prospects added:** {latest_run['new_prospects'] or 0}")
        lines.append(f"- **Email drafts created:** {latest_run['drafted'] or 0}")
        lines.append(f"- **By tier:** "
                     f"HOT={latest_run['hot_count'] or 0} · "
                     f"WARM={latest_run['warm_count'] or 0} · "
                     f"COLD={latest_run['cold_count'] or 0} · "
                     f"DISCARD={latest_run['discard_count'] or 0}")
        if latest_run["errors"]:
            lines.append(f"- **Errors:** ⚠ {latest_run['errors']}")
        lines.append("")

    # ─── Pipeline state ───
    lines.append("## Pipeline State")
    lines.append("")
    lines.append(f"**Total prospects in system:** {stats['total']}")
    lines.append("")
    lines.append("### By Status")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|--------|-------|")
    for status, count in sorted(stats["by_status"].items()):
        lines.append(f"| {status} | {count} |")
    lines.append("")

    lines.append("### By Tier")
    lines.append("")
    lines.append("| Tier | Count |")
    lines.append("|------|-------|")
    for tier, count in sorted(stats["by_tier"].items()):
        lines.append(f"| {tier} | {count} |")
    lines.append("")

    # ─── New leads today (with draft emails) ───
    if new_today:
        lines.append(f"## New Leads Today ({len(new_today)})")
        lines.append("")
        lines.append("Sorted by score (highest first).")
        lines.append("")

        for row in new_today:
            lines.append(f"### {row['name']} @ {row['company']}")
            lines.append("")
            lines.append(f"- **Title:** {row['title'] or '—'}")
            lines.append(f"- **Email:** {row['email']}")
            lines.append(f"- **Source:** {row['source'] or '—'}")
            if row['score'] is not None:
                lines.append(f"- **Score:** {row['score']}/100 — **{row['tier']}**")
            lines.append(f"- **Status:** {row['status']}")
            lines.append("")

            if row['draft_subject']:
                lines.append("**Draft email:**")
                lines.append("")
                lines.append(f"> **Subject:** {row['draft_subject']}")
                lines.append(">")
                for body_line in (row['draft_body'] or "").split("\n"):
                    lines.append(f"> {body_line}")
                lines.append("")
            lines.append("---")
            lines.append("")
    else:
        lines.append("## New Leads Today")
        lines.append("")
        lines.append("*No new prospects added today. Add some to `data/prospects.csv` and re-run.*")
        lines.append("")

    # ─── Next actions ───
    lines.append("## Next Actions")
    lines.append("")
    hot_warm = stats["by_tier"].get("HOT", 0) + stats["by_tier"].get("WARM", 0)
    if hot_warm > 0:
        lines.append(f"1. **Review the {hot_warm} HOT/WARM drafts above** — approve or edit, then send manually for now.")
    lines.append("2. **Add more prospects** to `data/prospects.csv` for tomorrow's run.")
    lines.append("3. **Track replies** — once outreach is sent, log them so the system knows status.")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
