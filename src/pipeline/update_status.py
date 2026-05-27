"""Update a prospect's status — your tool for tracking progress.

When you send an email, get a reply, or book a meeting, record it here so the
pipeline's memory stays accurate and the daily report reflects reality.

Usage:
    python -m src.pipeline.update_status <email> <status> [--note "..."]

Valid statuses:
    sent      - you sent the outreach
    replied   - they replied
    meeting   - meeting booked
    won       - became a client
    lost      - not interested / dead
    dropped   - you decided not to pursue

Examples:
    python -m src.pipeline.update_status sarah@acme.com sent
    python -m src.pipeline.update_status sarah@acme.com replied --note "asked about pricing"
    python -m src.pipeline.update_status sarah@acme.com meeting --note "Tuesday 3pm"
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone

from .database import connect, init_db, log_activity

VALID_STATUSES = {"sent", "replied", "meeting", "won", "lost", "dropped"}


def update_status(email: str, status: str, note: str = "") -> bool:
    """Update a prospect's status by email. Returns True if found."""
    status = status.lower()
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Use one of: {', '.join(sorted(VALID_STATUSES))}")

    init_db()
    now = datetime.now(timezone.utc).isoformat()

    with connect() as conn:
        row = conn.execute(
            "SELECT id, name, company FROM prospects WHERE email = ?", (email.lower(),)
        ).fetchone()
        if not row:
            return False

        set_contacted = status in ("sent",)
        conn.execute(
            """
            UPDATE prospects
            SET status = ?,
                last_contacted = CASE WHEN ? THEN ? ELSE last_contacted END,
                notes = COALESCE(notes,'') || ?
            WHERE id = ?
            """,
            (status, set_contacted, now, f"\n[{status} {now}] {note}".rstrip(), row["id"]),
        )
        log_activity(conn, prospect_id=row["id"], action=status, details=note)

    print(f"Updated {row['name']} @ {row['company']} -> {status.upper()}"
          + (f" ({note})" if note else ""))
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Update a prospect's status.")
    parser.add_argument("email", help="Prospect email (their unique key)")
    parser.add_argument("status", help=f"New status: {', '.join(sorted(VALID_STATUSES))}")
    parser.add_argument("--note", default="", help="Optional note (e.g., 'asked about pricing')")
    args = parser.parse_args()

    found = update_status(args.email, args.status, args.note)
    if not found:
        print(f"No prospect found with email: {args.email}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
