"""Load prospects from CSV with dedup against the database."""
from __future__ import annotations

import csv
from pathlib import Path

from .database import connect, log_activity, upsert_prospect

DEFAULT_CSV = Path("data/prospects.csv")
REQUIRED_FIELDS = {"name", "email", "company"}


def load_prospects_from_csv(csv_path: Path = DEFAULT_CSV) -> dict:
    """Read prospects from CSV and upsert into DB. Returns counts."""
    if not csv_path.exists():
        return {"total_in_csv": 0, "new_added": 0, "already_existed": 0}

    new_added = 0
    already_existed = 0
    errors = 0

    with csv_path.open(encoding="utf-8") as f, connect() as conn:
        reader = csv.DictReader(f)

        for row in reader:
            # Validate required fields
            if not REQUIRED_FIELDS.issubset({k for k, v in row.items() if v}):
                errors += 1
                continue

            existing = conn.execute(
                "SELECT id FROM prospects WHERE email = ?", (row["email"],)
            ).fetchone()
            if existing:
                already_existed += 1
                continue

            prospect_id = upsert_prospect(
                conn,
                {
                    "email": row["email"].strip().lower(),
                    "name": row["name"].strip(),
                    "title": row.get("title", "").strip(),
                    "company": row["company"].strip(),
                    "source": row.get("source", "csv").strip(),
                },
            )
            log_activity(conn, prospect_id, action="discovered", channel="csv",
                         details=f"Loaded from {csv_path.name}")
            new_added += 1

    return {
        "total_in_csv": new_added + already_existed,
        "new_added": new_added,
        "already_existed": already_existed,
        "errors": errors,
    }
