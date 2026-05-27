"""Convert an Apollo.io CSV export into our prospects.csv format.

Apollo exports columns like: First Name, Last Name, Title, Company, Email, ...
We need: name, title, company, email, source

Usage:
    python scripts/apollo_to_prospects.py data/apollo_export.csv
    # writes/append to data/prospects.csv
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

OUT_PATH = Path("data/prospects.csv")
OUT_FIELDS = ["name", "title", "company", "email", "source"]


def _get(row: dict, *candidates: str) -> str:
    """Return the first non-empty value among candidate column names (case-insensitive)."""
    lower = {k.lower().strip(): v for k, v in row.items()}
    for c in candidates:
        v = lower.get(c.lower())
        if v and v.strip():
            return v.strip()
    return ""


def convert(apollo_csv: Path) -> int:
    rows_out = []
    with apollo_csv.open(encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            first = _get(row, "first name", "first_name")
            last = _get(row, "last name", "last_name")
            name = (first + " " + last).strip() or _get(row, "name", "full name")
            email = _get(row, "email", "email address", "work email")
            company = _get(row, "company", "company name", "organization", "account name")
            title = _get(row, "title", "job title")
            if not (name and email and company):
                continue
            rows_out.append({
                "name": name, "title": title, "company": company,
                "email": email.lower(), "source": "apollo",
            })

    # Append to existing prospects.csv (the loader dedupes by email anyway)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not OUT_PATH.exists()
    with OUT_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerows(rows_out)

    return len(rows_out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Apollo export to prospects.csv")
    parser.add_argument("apollo_csv", type=Path, help="Path to Apollo CSV export")
    args = parser.parse_args()

    if not args.apollo_csv.exists():
        raise SystemExit(f"File not found: {args.apollo_csv}")

    n = convert(args.apollo_csv)
    print(f"Added {n} prospects to {OUT_PATH} (duplicates skipped on next pipeline run).")


if __name__ == "__main__":
    main()
