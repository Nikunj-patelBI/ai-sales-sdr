# AnalyticsGear AI Sales Pipeline

A **simple** AI sales pipeline: it reads your leads, scores each one against your ideal customer profile, and writes a personalized cold email — automatically, every day.

Built for a solo founder. No servers, no vector DB, no complex infrastructure. One Python script + one Claude call per lead.

---

## What It Does

Every run:
1. **Loads** new leads from `data/prospects.csv` (skips ones it's seen before)
2. **Scores** each lead 0-100 against your ICP (one Claude call)
3. **Drafts** a personalized email referencing their company, role, and tech
4. **Saves** everything to a local SQLite database (your CRM)
5. **Writes** a daily markdown report with the drafts + pipeline status

You review the report, send the good emails, and record outcomes. The system never forgets a lead and always shows you what's next.

## Architecture (deliberately simple)

```
  data/prospects.csv  ──►  csv_loader  ──►  scorer (1 Claude call)  ──►  SQLite
                                                                            │
                              data/reports/today.md  ◄──  reporter  ◄───────┘
```

Six files, ~700 lines:

```
src/pipeline/
├── database.py       SQLite CRM (prospects, drafts, activity, runs)
├── csv_loader.py     Load + dedupe leads
├── scorer.py         ★ One Claude call: score + draft email
├── daily_runner.py   Runs the daily cycle
├── reporter.py       Daily markdown report
└── update_status.py  Record outcomes (sent / replied / meeting / won / lost)
```

## Tech Stack

| Layer | Tech | Cost |
|-------|------|------|
| Language | Python 3.12+ | Free |
| AI | Anthropic Claude API | ~$5-10/mo |
| CRM | SQLite (local file) | Free |
| Scheduling | Windows Task Scheduler | Free |
| Lead source | Apollo.io free tier (CSV export) | Free |

Three Python deps: `anthropic`, `python-dotenv`, `pyyaml`.

## Quick Start

```bash
# 1. Install
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"

# 2. Configure
copy .env.example .env
# Edit .env -> add your ANTHROPIC_API_KEY

# 3. Add leads to data/prospects.csv (or convert an Apollo export):
python scripts/apollo_to_prospects.py data/apollo_export.csv

# 4. Run the pipeline
python -m src.pipeline.daily_runner

# 5. Read the report
#    data/reports/<today>.md  -> review drafts, send the good ones

# 6. Record outcomes as they happen
python -m src.pipeline.update_status sarah@acme.com replied --note "asked about pricing"
```

## Automate It (daily, hands-off)

```powershell
# Registers a Windows scheduled task to run every morning at 8 AM
powershell -ExecutionPolicy Bypass -File scripts\schedule_daily.ps1
```

## The Workflow Today

| Step | Who |
|------|-----|
| Find leads → CSV | You (Apollo export) |
| Score + draft emails | The pipeline |
| Review + send | You (from Gmail/Outlook) |
| Track replies/meetings | You (`update_status`) |
| Remember everything + report | The pipeline |

Later phases automate sending (SendGrid) and reply tracking. See [ROADMAP.md](ROADMAP.md).

## Roadmap

- **Phase 1-2 (now):** This — load leads, draft emails, manual send, daily report
- **Phase 3:** Automated sending (SendGrid + email warmup)
- **Phase 4:** Auto lead sourcing (Apollo API)
- **Phase 5:** Deploy to run unattended
- **Later:** Evaluate n8n or OpenClaw for automation/chat updates

Full detail in [ROADMAP.md](ROADMAP.md). Current progress in [STATUS.md](STATUS.md).

## License

Proprietary. Internal AnalyticsGear project.
