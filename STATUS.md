# Project Status

> Living document. Source of truth for where the project is.

**Last updated:** 2026-04-19
**Branch:** `simplify-architecture`
**Architecture:** Simple — single daily script, one Claude call per lead, SQLite CRM. No MCP/RAG/agents.

---

## Where We Are

Pivoted from the complex multi-agent/MCP/RAG design to a **simple, shippable pipeline**.
Removed all the over-engineered scaffolding. Building Phase 1-2 now.

## The System (6 files in `src/pipeline/`)

| File | Status |
|------|--------|
| `database.py` — SQLite CRM | ✅ Built |
| `csv_loader.py` — load + dedupe leads | ✅ Built |
| `scorer.py` — one Claude call: score + draft | ✅ Built |
| `daily_runner.py` — daily cycle | ✅ Built |
| `reporter.py` — daily markdown report | ✅ Built |
| `update_status.py` — record outcomes | ✅ Built |

Plus: `scripts/schedule_daily.ps1` (Task Scheduler), `scripts/apollo_to_prospects.py` (CSV adapter).

## What Works Now

- Load leads from `data/prospects.csv`, dedupe against DB
- Score + draft personalized email per lead (one Claude call)
- Save to SQLite, generate daily markdown report
- Update prospect status as outcomes happen
- Schedule daily via Windows Task Scheduler

## Next Steps (Phase 1 — get real value)

1. Sign up Apollo free tier → export 5-10 real prospects
2. `python scripts/apollo_to_prospects.py data/apollo_export.csv`
3. `python -m src.pipeline.daily_runner`
4. Review `data/reports/<today>.md`, send the best drafts manually
5. `update_status` as replies come in

## Later (Phase 3+)

- Automated sending (SendGrid + 3-week email warmup)
- Auto lead sourcing (Apollo API)
- Evaluate n8n / OpenClaw for automation + chat updates

## Decisions Locked

| Decision | Choice |
|----------|--------|
| Architecture | Simple single-script, no MCP/RAG/agents |
| CRM | SQLite (local) |
| Deployment | Laptop + Windows Task Scheduler |
| Email send | Manual now → SendGrid (Phase 3) |
| Automation tool (later) | n8n vs OpenClaw — decide at Phase 3 |

## Note

The complex version (multi-agent, MCP servers, RAG, vector DB, 92-task plan, Word
blueprints) lives on the `main` branch and in git history if ever needed.
