"""Smoke tests for the simple pipeline — no API calls, all free/offline."""
import tempfile
from pathlib import Path

from src.pipeline import database


def test_package_imports():
    import src
    assert src.__version__ == "0.1.0"


def test_db_init_and_schema(tmp_path):
    db = tmp_path / "test.db"
    database.init_db(db)
    with database.connect(db) as conn:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
    assert {"prospects", "outreach", "activities", "runs"}.issubset(tables)


def test_upsert_and_dedup(tmp_path):
    db = tmp_path / "test.db"
    database.init_db(db)
    lead = {"email": "a@b.com", "name": "A B", "title": "CTO",
            "company": "Acme", "source": "test"}
    with database.connect(db) as conn:
        id1 = database.upsert_prospect(conn, lead)
        id2 = database.upsert_prospect(conn, lead)  # same email -> no dup
    assert id1 == id2


def test_pipeline_stats_empty(tmp_path):
    db = tmp_path / "test.db"
    database.init_db(db)
    with database.connect(db) as conn:
        stats = database.pipeline_stats(conn)
    assert stats["total"] == 0
