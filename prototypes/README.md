# Prototypes

Working demos that prove the architecture before we build the full thing.

## `email_agent_demo.py` — AI Outreach Agent (Day 1)

**What it does:** An AI agent autonomously researches a prospect, scores them against ICP, and writes a personalized cold email — using the same Claude tool-use pattern we'll use in production.

**What it demonstrates:**
- Agent loop with tool use (Reason → Act → Observe → Repeat)
- Multi-step reasoning: the agent decides which tools to call and in what order
- "RAG-style" retrieval (currently dict lookups — will become real vector DB queries later)
- ICP-based lead scoring with breakdown
- Personalized email generation referencing real prospect details

**Architecture note:** The three tools (`get_company_context`, `get_relevant_ag_content`, `score_lead`) are local Python functions today. In production, they get swapped for:

| Tool today | Tool in production |
|------------|--------------------|
| `get_company_context` (dict lookup) | `mcp-vectordb` querying the `company_profiles` collection |
| `get_relevant_ag_content` (keyword match) | `mcp-vectordb` semantic search on `ag_content` collection |
| `score_lead` (Python heuristic) | Dedicated Claude Haiku call for AI scoring |

**The agent code stays identical.** That's the power of MCP + tool use.

## How to Run

```bash
# 1. Make sure ANTHROPIC_API_KEY is in .env (real key, not placeholder)
#    Get one at https://console.anthropic.com/settings/keys

# 2. Activate venv
cd c:/analyticsgear/sales_pipeline
.venv/Scripts/activate

# 3. Run the demo
python prototypes/email_agent_demo.py
```

**Expected runtime:** ~30 seconds for 3 prospects
**Expected cost:** ~$0.03 total (one tool-using session per prospect)

## What You'll See

For each of 3 prospects, the script prints:
1. The agent's tool calls in real time (`→ tool get_company_context(...)`)
2. The final output — score, tier, reasoning, subject, and full email

Sample output:

```
─── Prospect 1/3: Sarah Chen @ DataFlow Inc ───
  Title: CTO
  Email: sarah@dataflow.example

Agent steps:
  → tool get_company_context({"company_name": "DataFlow Inc"...})
  → tool get_relevant_ag_content({"topics": ["data-engineering", "data-platform"]...})
  → tool score_lead({"prospect": {...}, "company": {...}...})

┌─ Final Output ────────────────────────────────────────────────────┐
│ SCORE: 88/100  TIER: HOT                                          │
│ REASONING: Senior decision-maker at right-sized SaaS company...   │
│                                                                   │
│ SUBJECT: airflow at dataflow                                      │
│                                                                   │
│ Hi Sarah,                                                         │
│                                                                   │
│ Saw your team is hiring data engineers and you've been posting    │
│ about Airflow scheduling pain. We hit the same wall with a SaaS   │
│ client last quarter — moved critical DAGs to Dagster, kept        │
│ Airflow for batch. Cut incident rate by 70%.                      │
│                                                                   │
│ Happy to share the migration pattern if useful.                   │
│                                                                   │
│ Best,                                                             │
│ AnalyticsGear                                                     │
└───────────────────────────────────────────────────────────────────┘
```

## Why This Matters

This 350-line prototype proves the **entire core architecture** of the production system. When we replace the dict-lookup tools with real MCP servers next sprint, the agent code doesn't change. We're just upgrading the plumbing.
