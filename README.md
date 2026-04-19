# AnalyticsGear AI Sales Pipeline

An AI-native sales pipeline built with **MCP**, **AI Agents**, **RAG**, and **Vector Databases**.

Dual-purpose project: (1) automates AnalyticsGear's sales outreach without a human SDR, (2) serves as a production reference implementation for AI consulting services we sell.

---

## What This Is

A multi-agent AI system that runs daily and handles the full sales cycle:

- **Discovers** 25+ qualified leads per day from Apollo, LinkedIn, job boards, and intent signals
- **Enriches & scores** each lead 1-100 against ICP criteria
- **Generates** personalized outreach using RAG over company data + AnalyticsGear content
- **Sends** across email + LinkedIn with multi-step sequences
- **Monitors** engagement and classifies replies with AI
- **Learns** from outcomes — successful patterns get stored and reused
- **Reports** weekly performance with AI-generated insights

Runs 2-4 hours/day on a schedule. Costs ~$350/month to operate vs. $3-5K/month for a junior SDR.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT LAYER                           │
│   Prospecting · Outreach · Follow-Up · Analytics        │
├─────────────────────────────────────────────────────────┤
│                  MCP PROTOCOL LAYER                      │
│  mcp-apollo · mcp-linkedin · mcp-email · mcp-crm ·       │
│  mcp-vectordb · mcp-scraper                              │
├─────────────────────────────────────────────────────────┤
│                 KNOWLEDGE LAYER                          │
│   Qdrant Vector DB · RAG Engine · Memory Store           │
└─────────────────────────────────────────────────────────┘
```

See [docs/](./docs/) for full architecture and build plans.

## Repository Structure

```
sales-pipeline/
├── docs/                   # Strategy, architecture, and technical blueprints
├── project_management/     # Sprint plan, Jira-style tracker (Excel)
├── scripts/                # Document generation scripts
├── src/
│   ├── agents/             # Prospecting, Outreach, Follow-Up, Analytics agents
│   ├── mcp_servers/        # 6 MCP servers (CRM, VectorDB, Email, Apollo, LinkedIn, Scraper)
│   ├── rag/                # Embedding, chunking, retrieval modules
│   ├── memory/             # Lead memory, pattern memory
│   ├── feedback/           # Engagement tracking, pattern analysis, self-improvement
│   ├── config/             # ICP, sequences, scoring configs
│   ├── prompts/            # Agent system prompts
│   └── data/               # Target company lists, exclusions
├── tests/
├── pyproject.toml
├── docker-compose.yml
└── .env.example
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ |
| LLM | Anthropic Claude (Sonnet for agents, Haiku for scoring) |
| Vector DB | Qdrant |
| Embeddings | Voyage AI (voyage-3) |
| Agent Framework | Custom ReAct loop + Claude Agent SDK |
| MCP | `@modelcontextprotocol/sdk` |
| Orchestration | APScheduler / Prefect |
| Email | SendGrid + Instantly.ai (warmup) |
| CRM | Google Sheets (migrating to HubSpot) |
| Monitoring | Langfuse |

## Build Plan

4-week sprint plan with 92 tasks — see [project_management/AnalyticsGear_AI_Pipeline_Project_Plan.xlsx](./project_management/AnalyticsGear_AI_Pipeline_Project_Plan.xlsx).

| Sprint | Dates | Goal |
|--------|-------|------|
| Sprint 1 | Apr 20-26 | Foundation, RAG pipeline, first MCP server |
| Sprint 2 | Apr 27-May 3 | All 6 MCP servers, Prospecting Agent |
| Sprint 3 | May 4-10 | Outreach + Follow-Up agents, memory system |
| Sprint 4 | May 11-17 | Analytics, orchestration, production, **GO LIVE** |

## Getting Started (Local Dev)

```bash
# 1. Clone and set up environment
git clone <repo-url>
cd sales-pipeline
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .

# 2. Configure secrets
cp .env.example .env
# Fill in: ANTHROPIC_API_KEY, VOYAGE_API_KEY, APOLLO_API_KEY, SENDGRID_API_KEY

# 3. Start Qdrant
docker compose up -d qdrant

# 4. Initialize vector collections
python -m src.rag.init_collections

# 5. Run first agent (dry run)
python -m src.agents.orchestrator --dry-run
```

## Status

🚧 **Sprint 1 in progress** (Apr 20 – Apr 26). Day 1 partially complete: env + deps installed, tests passing, blocked on API keys + Docker Desktop.

See [STATUS.md](./STATUS.md) for detailed progress, blockers, and how to pick up where we left off.

## License

Proprietary. Internal AnalyticsGear project.
