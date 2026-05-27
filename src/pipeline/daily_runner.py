"""Daily sales pipeline run — the SIMPLE version.

What it does:
  1. Loads new prospects from data/prospects.csv (dedup'd against DB)
  2. For each new prospect: ONE Claude call scores + drafts an email
  3. Saves results to SQLite
  4. Generates a daily markdown report in data/reports/
  5. Logs every step for audit

No MCP servers, no vector DB, no multi-agent orchestration. Just a clean
read -> score+draft -> save -> report loop. Add sophistication later only
if the business genuinely needs it.

Run manually:
    python -m src.pipeline.daily_runner [--max-new N]

Schedule daily: see scripts/schedule_daily.ps1
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime

from .csv_loader import load_prospects_from_csv
from .database import (
    connect,
    finish_run,
    get_new_prospects,
    init_db,
    log_activity,
    mark_prospect_scored,
    save_outreach_draft,
    start_run,
)
from .reporter import generate_daily_report
from .scorer import estimate_cost, score_and_draft


def run_pipeline(max_new: int | None = None) -> dict:
    """Execute one full pipeline run. Returns stats dict."""
    init_db()
    start = time.time()

    print(f"[{datetime.now().isoformat(timespec='seconds')}] Pipeline run started")

    # ─── Step 1: Load CSV ───
    csv_stats = load_prospects_from_csv()
    print(
        f"  CSV: {csv_stats['new_added']} new, "
        f"{csv_stats['already_existed']} already known, "
        f"{csv_stats.get('errors', 0)} errors"
    )

    # ─── Step 2: Process new prospects ───
    with connect() as conn:
        run_id = start_run(conn)
        new_prospects = [dict(r) for r in get_new_prospects(conn)]

    if max_new:
        new_prospects = new_prospects[:max_new]

    print(f"  Processing {len(new_prospects)} new prospect(s)...")

    counts = {"HOT": 0, "WARM": 0, "COLD": 0, "DISCARD": 0}
    drafted = 0
    errors = 0
    total_cost = 0.0

    for row in new_prospects:
        prospect = {
            "name": row["name"],
            "title": row["title"] or "",
            "company": row["company"],
            "email": row["email"],
        }
        # Pull any extra enrichment columns stored in notes (industry/tech/etc.)
        print(f"    -> {prospect['name']} @ {prospect['company']}")

        try:
            result = score_and_draft(prospect)
            score = int(result["score"])
            tier = result["tier"].upper()
            total_cost += estimate_cost(result["_usage"])

            with connect() as conn:
                mark_prospect_scored(
                    conn, row["id"], score=score, tier=tier,
                    reasoning=result.get("reasoning", ""),
                )
                if result.get("subject") and result.get("body"):
                    save_outreach_draft(
                        conn, prospect_id=row["id"], channel="email",
                        subject=result["subject"], body=result["body"],
                    )
                    drafted += 1
                log_activity(
                    conn, prospect_id=row["id"], action="drafted", channel="email",
                    details=f"{tier} ({score}): {result.get('subject', '')}",
                )

            counts[tier] = counts.get(tier, 0) + 1
            print(f"       score={score} tier={tier}")

        except Exception as exc:
            errors += 1
            print(f"       [error] {exc}")
            with connect() as conn:
                log_activity(conn, prospect_id=row["id"], action="error", details=str(exc)[:200])

    # ─── Step 3: Finalize run ───
    duration = time.time() - start
    summary = (
        f"{drafted} drafts. HOT={counts['HOT']} WARM={counts['WARM']} "
        f"COLD={counts['COLD']} DISCARD={counts['DISCARD']} | ${total_cost:.4f}"
    )
    with connect() as conn:
        finish_run(conn, run_id, {
            "duration_sec": round(duration, 2),
            "prospects_seen": len(new_prospects) + csv_stats["already_existed"],
            "new_prospects": csv_stats["new_added"],
            "drafted": drafted,
            "hot_count": counts["HOT"],
            "warm_count": counts["WARM"],
            "cold_count": counts["COLD"],
            "discard_count": counts["DISCARD"],
            "errors": errors,
            "cost_usd": round(total_cost, 4),
            "summary": summary,
        })

    # ─── Step 4: Generate daily report ───
    report_path = generate_daily_report()
    print(f"  Report: {report_path}")
    print(f"  Done in {duration:.1f}s — {summary}")

    return {
        "run_id": run_id,
        "duration": round(duration, 1),
        "drafted": drafted,
        "counts": counts,
        "errors": errors,
        "cost_usd": round(total_cost, 4),
        "report_path": str(report_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the daily sales pipeline (simple version).")
    parser.add_argument("--max-new", type=int, default=None,
                        help="Cap number of new prospects to process this run")
    args = parser.parse_args()

    result = run_pipeline(max_new=args.max_new)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
