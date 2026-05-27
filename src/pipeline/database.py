"""SQLite database — the local CRM for tracking prospects, activities, and runs.

In production we'll migrate to Google Sheets or HubSpot, but SQLite is perfect
for solo dev: zero setup, full SQL, durable on disk.
"""
from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

DB_PATH = Path(os.getenv("PIPELINE_DB_PATH", "data/pipeline.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS prospects (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email           TEXT UNIQUE NOT NULL,
    name            TEXT NOT NULL,
    title           TEXT,
    company         TEXT NOT NULL,
    source          TEXT,             -- csv | apollo | linkedin | manual | inbound
    score           INTEGER,          -- 0-100 from AI scoring
    tier            TEXT,             -- HOT | WARM | COLD | DISCARD
    status          TEXT NOT NULL DEFAULT 'new',  -- new | drafted | sent | replied | won | lost | dropped
    notes           TEXT,
    added_at        TEXT NOT NULL,
    last_processed  TEXT,
    last_contacted  TEXT
);

CREATE INDEX IF NOT EXISTS idx_prospects_status ON prospects(status);
CREATE INDEX IF NOT EXISTS idx_prospects_tier ON prospects(tier);

CREATE TABLE IF NOT EXISTS outreach (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id     INTEGER NOT NULL,
    channel         TEXT NOT NULL,    -- email | linkedin | phone
    subject         TEXT,
    body            TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'draft',  -- draft | approved | sent | bounced
    sequence_step   INTEGER DEFAULT 1,
    created_at      TEXT NOT NULL,
    sent_at         TEXT,
    FOREIGN KEY(prospect_id) REFERENCES prospects(id)
);

CREATE INDEX IF NOT EXISTS idx_outreach_prospect ON outreach(prospect_id);
CREATE INDEX IF NOT EXISTS idx_outreach_status ON outreach(status);

CREATE TABLE IF NOT EXISTS activities (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id     INTEGER,
    timestamp       TEXT NOT NULL,
    channel         TEXT,
    action          TEXT NOT NULL,    -- discovered | scored | drafted | sent | opened | clicked | replied | called
    details         TEXT,
    FOREIGN KEY(prospect_id) REFERENCES prospects(id)
);

CREATE INDEX IF NOT EXISTS idx_activities_prospect ON activities(prospect_id);
CREATE INDEX IF NOT EXISTS idx_activities_timestamp ON activities(timestamp);

CREATE TABLE IF NOT EXISTS runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_at          TEXT NOT NULL,
    duration_sec    REAL,
    prospects_seen  INTEGER DEFAULT 0,
    new_prospects   INTEGER DEFAULT 0,
    drafted         INTEGER DEFAULT 0,
    hot_count       INTEGER DEFAULT 0,
    warm_count      INTEGER DEFAULT 0,
    cold_count      INTEGER DEFAULT 0,
    discard_count   INTEGER DEFAULT 0,
    errors          INTEGER DEFAULT 0,
    cost_usd        REAL DEFAULT 0,
    summary         TEXT
);
"""


def init_db(db_path: Path = DB_PATH) -> None:
    """Create the database and schema if they don't exist."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)


@contextmanager
def connect(db_path: Path = DB_PATH) -> Iterator[sqlite3.Connection]:
    """Context manager for a SQLite connection with sensible defaults."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# ─── Prospect helpers ──────────────────────────────────────────────

def upsert_prospect(conn: sqlite3.Connection, prospect: dict) -> int:
    """Insert a prospect if email is new, else return existing id."""
    now = datetime.now(timezone.utc).isoformat()
    existing = conn.execute(
        "SELECT id FROM prospects WHERE email = ?", (prospect["email"],)
    ).fetchone()
    if existing:
        return existing["id"]

    cur = conn.execute(
        """
        INSERT INTO prospects (email, name, title, company, source, added_at)
        VALUES (:email, :name, :title, :company, :source, :added_at)
        """,
        {**prospect, "added_at": now},
    )
    return cur.lastrowid


def get_new_prospects(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Prospects that haven't been scored / drafted yet."""
    return conn.execute(
        "SELECT * FROM prospects WHERE status = 'new' ORDER BY added_at ASC"
    ).fetchall()


def mark_prospect_scored(
    conn: sqlite3.Connection,
    prospect_id: int,
    score: int,
    tier: str,
    reasoning: str = "",
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        UPDATE prospects
        SET score = ?, tier = ?, status = 'drafted', last_processed = ?, notes = COALESCE(notes,'') || ?
        WHERE id = ?
        """,
        (score, tier, now, f"\n[scored {now}] {reasoning}", prospect_id),
    )


def save_outreach_draft(
    conn: sqlite3.Connection,
    prospect_id: int,
    channel: str,
    subject: str,
    body: str,
) -> int:
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """
        INSERT INTO outreach (prospect_id, channel, subject, body, status, created_at)
        VALUES (?, ?, ?, ?, 'draft', ?)
        """,
        (prospect_id, channel, subject, body, now),
    )
    return cur.lastrowid


def log_activity(
    conn: sqlite3.Connection,
    prospect_id: int | None,
    action: str,
    channel: str = "",
    details: str = "",
) -> None:
    conn.execute(
        """
        INSERT INTO activities (prospect_id, timestamp, channel, action, details)
        VALUES (?, ?, ?, ?, ?)
        """,
        (prospect_id, datetime.now(timezone.utc).isoformat(), channel, action, details),
    )


# ─── Run helpers ──────────────────────────────────────────────

def start_run(conn: sqlite3.Connection) -> int:
    cur = conn.execute(
        "INSERT INTO runs (run_at) VALUES (?)",
        (datetime.now(timezone.utc).isoformat(),),
    )
    return cur.lastrowid


def finish_run(conn: sqlite3.Connection, run_id: int, stats: dict) -> None:
    cols = ", ".join(f"{k} = :{k}" for k in stats)
    conn.execute(f"UPDATE runs SET {cols} WHERE id = :id", {**stats, "id": run_id})


# ─── Reporting queries ──────────────────────────────────────────

def pipeline_stats(conn: sqlite3.Connection) -> dict:
    """Snapshot of pipeline state by tier and status."""
    by_status = {
        row["status"]: row["n"]
        for row in conn.execute(
            "SELECT status, COUNT(*) AS n FROM prospects GROUP BY status"
        )
    }
    by_tier = {
        row["tier"] or "UNSCORED": row["n"]
        for row in conn.execute(
            "SELECT tier, COUNT(*) AS n FROM prospects GROUP BY tier"
        )
    }
    total = sum(by_status.values())
    return {"total": total, "by_status": by_status, "by_tier": by_tier}


def todays_new_prospects(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Prospects added in the last 24 hours."""
    return conn.execute(
        """
        SELECT p.*, o.subject AS draft_subject, o.body AS draft_body
        FROM prospects p
        LEFT JOIN outreach o ON o.prospect_id = p.id AND o.channel = 'email'
        WHERE p.added_at >= datetime('now', '-1 day')
        ORDER BY p.score DESC NULLS LAST, p.added_at DESC
        """
    ).fetchall()
