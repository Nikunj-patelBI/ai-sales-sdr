# Project Status

> Living document — update at end of each working day. Source of truth for sprint progress.

**Last updated:** 2026-04-19
**Current sprint:** Sprint 1 (Apr 20 – Apr 26)
**Current day:** Day 1 — *partially complete, paused*
**Overall progress:** 3 / 92 tasks complete (3%)

---

## Where We Are

Sprint 1 started one day early (prep work on 2026-04-19). Environment is set up and the repo is live on GitHub. Waiting on API keys and Docker Desktop to finish Day 1 and move to Day 2.

## Sprint 1 (Apr 20 – Apr 26) — Foundation + RAG + First MCP Server

### Day 1 — Environment Setup

| Task | Status | Notes |
|------|--------|-------|
| AG-001 Initialize git repo & project structure | ✅ Done | Pushed to `Nikunj-patelBI/sales_pipeline` |
| AG-002 Set up Python 3.12+ venv | ✅ Done | Python 3.13.5 at `.venv/` |
| AG-003 Install core dependencies | ✅ Done | 50+ packages including anthropic, qdrant-client, voyageai, mcp, gspread, sendgrid, langfuse, pytest, ruff, mypy |
| AG-004 Configure `.env` with API keys | 🟡 In progress | Template copied; **needs real `ANTHROPIC_API_KEY`** |
| AG-005 Start Qdrant via Docker Compose | ⏸️ Blocked | **Docker Desktop not running** |
| AG-006 Validate Claude API access | ⏸️ Blocked | Blocked on AG-004 |

### Day 2-7 — Not started
- Day 2: Vector DB collections + embedder + chunker
- Day 3: Ingest 50 companies + AG blog content + industry knowledge
- Day 4: RAG retrieval + context builder + quality evaluation
- Day 5: Claude client + first RAG-augmented email generation
- Day 6: First MCP server (`mcp-crm`) + Claude Desktop integration
- Day 7: Sprint 1 retro + **start email warmup** (critical — 3-week lead time)

---

## Blockers

1. **Anthropic API key** — needed to validate Claude access (AG-006). Get at https://console.anthropic.com/settings/keys
2. **Docker Desktop not running** — needed to start Qdrant (AG-005)

---

## How to Pick Up From Here

```bash
# 1. Start Docker Desktop (wait ~1 min for it to initialize)

# 2. Activate venv
cd c:/analyticsgear/sales_pipeline
.venv/Scripts/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1

# 3. Add your Anthropic key to .env
#    Edit .env and set: ANTHROPIC_API_KEY=sk-ant-...

# 4. Run smoke tests to confirm env still healthy
python -m pytest tests/ -v

# 5. Start Qdrant
docker compose up -d qdrant

# 6. Finish Day 1 — validate Claude API works (AG-006)
python -c "from anthropic import Anthropic; print(Anthropic().messages.create(model='claude-sonnet-4-6', max_tokens=50, messages=[{'role':'user','content':'ping'}]))"
```

---

## Upcoming Sprints

| Sprint | Dates | Goal |
|--------|-------|------|
| Sprint 1 | Apr 20 – Apr 26 | ✅ Foundation + RAG + first MCP server (mcp-crm) |
| Sprint 2 | Apr 27 – May 3 | All 6 MCP servers + Prospecting Agent live |
| Sprint 3 | May 4 – May 10 | Outreach + Follow-up agents + Memory system |
| Sprint 4 | May 11 – May 17 | Analytics + Orchestration + **GO LIVE** |

Full 92-task breakdown: [project_management/AnalyticsGear_AI_Pipeline_Project_Plan.xlsx](./project_management/AnalyticsGear_AI_Pipeline_Project_Plan.xlsx)

---

## Decisions Log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-04-19 | Python 3.13 instead of 3.12 | 3.13 already installed, `>=3.12` in pyproject covers it |
| 2026-04-19 | Qdrant over Pinecone | Free self-host, better filtering, Python-native |
| 2026-04-19 | Voyage AI over OpenAI for embeddings | Better price-performance at voyage-3 quality |
| 2026-04-19 | Google Sheets CRM to start, HubSpot later | Zero friction to start, easy migration path |
| 2026-04-19 | Private GitHub repo | docs/ contains pricing, ICP, and sales strategy |

---

## Risks Currently Active

See [project_management/AnalyticsGear_AI_Pipeline_Project_Plan.xlsx](./project_management/AnalyticsGear_AI_Pipeline_Project_Plan.xlsx) → *Risk Register* sheet for the full list.

Top-of-mind right now:
- **R-01** Email domain warmup must start by Day 7 (Apr 26) or we miss the 3-week window before go-live
- **R-05** RAG retrieval quality — will be evaluated on Day 4 (AG-016)
