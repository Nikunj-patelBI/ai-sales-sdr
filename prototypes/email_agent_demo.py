"""
Prototype: AI Outreach Agent (Day 1 working demo)

Demonstrates the SAME architecture pattern we'll use in production:
  - Claude as the reasoning engine
  - Tool use: agent autonomously decides what context to fetch
  - "RAG" simulated with dict lookups (becomes Qdrant queries later)

In production, the three tools below get swapped for real MCP servers:
  - get_company_context  ->  mcp-vectordb (search company_profiles collection)
  - get_relevant_ag_content -> mcp-vectordb (search ag_content collection)
  - score_lead           ->  Claude Haiku scoring call

Agent code stays IDENTICAL. That's the power of the architecture.

Run:
  .venv/Scripts/python prototypes/email_agent_demo.py

Cost: ~$0.01-0.02 per run with claude-sonnet-4-6.
"""
from __future__ import annotations

import json
import os
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax

load_dotenv()
console = Console()


# ════════════════════════════════════════════════════════════════════
#  FAKE "KNOWLEDGE BASE" — will become Qdrant vector collections
# ════════════════════════════════════════════════════════════════════

COMPANY_PROFILES: dict[str, dict] = {
    "DataFlow Inc": {
        "industry": "B2B SaaS — Analytics platform",
        "size": 350,
        "hq": "Austin, TX",
        "tech_stack": ["Snowflake", "Airflow", "dbt", "Looker", "AWS"],
        "recent_news": "Raised $18M Series B on March 1, 2026. Plans to double engineering headcount.",
        "pain_signals": [
            "Hiring 3 data engineers (LinkedIn, posted 8 days ago)",
            "CTO Sarah Chen posted about Airflow scheduling pain on LinkedIn",
            "Recent dbt migration noted in engineering blog",
        ],
        "description": (
            "DataFlow Inc helps mid-market SaaS companies turn product usage data into "
            "revenue insights. Customers include 200+ companies."
        ),
    },
    "MedSync Health": {
        "industry": "Healthcare IT",
        "size": 1200,
        "hq": "Boston, MA",
        "tech_stack": ["Databricks", "Azure", "Kafka", "Power BI"],
        "recent_news": "Just announced HIPAA-compliant patient data platform initiative for Q3.",
        "pain_signals": [
            "Hiring Director of Data Governance",
            "Pre-IPO — compliance pressure on data lineage and quality frameworks",
        ],
        "description": (
            "MedSync Health builds patient data interoperability platforms for hospital networks. "
            "Serving 80+ hospitals across the Northeast."
        ),
    },
    "ShopWave Retail": {
        "industry": "Retail / E-commerce",
        "size": 600,
        "hq": "London, UK",
        "tech_stack": ["BigQuery", "GCP", "Looker", "dbt"],
        "recent_news": "Launched personalization feature using ML for product recommendations.",
        "pain_signals": [
            "Hiring 2 ML Engineers and 1 Analytics Engineer",
            "Head of Data presented at conference about real-time analytics challenges",
        ],
        "description": "Mid-market e-commerce platform for fashion and lifestyle brands across EMEA.",
    },
}

AG_CONTENT: list[dict] = [
    {
        "title": "RAG vs Fine-Tuning: When Each Wins",
        "topic": "genai",
        "summary": "Decision framework for choosing between RAG and fine-tuning approaches for production LLM applications.",
        "url": "https://analyticsgear.com/insights/rag-vs-fine-tuning",
    },
    {
        "title": "Lakehouse Migration Playbook",
        "topic": "data-engineering",
        "summary": "Step-by-step playbook for migrating from legacy data warehouses to modern lakehouse architectures (Snowflake, Databricks).",
        "url": "https://analyticsgear.com/insights/lakehouse-migration",
    },
    {
        "title": "Semantic Layer Strategy for Self-Service Analytics",
        "topic": "analytics",
        "summary": "How to build a semantic layer that makes data self-service-ready without sacrificing governance.",
        "url": "https://analyticsgear.com/insights/semantic-layer",
    },
    {
        "title": "MLOps Without Ceremony",
        "topic": "mlops",
        "summary": "Pragmatic MLOps for teams that need to ship ML models without 18-month platform builds.",
        "url": "https://analyticsgear.com/insights/mlops-pragmatic",
    },
    {
        "title": "FinOps for Data Teams",
        "topic": "data-platform",
        "summary": "Reducing Snowflake/Databricks/BigQuery costs without sacrificing performance. Real case studies.",
        "url": "https://analyticsgear.com/insights/finops-data",
    },
    {
        "title": "Data Contracts in Practice",
        "topic": "data-governance",
        "summary": "Implementing data contracts to prevent breaking changes between data producers and consumers.",
        "url": "https://analyticsgear.com/insights/data-contracts",
    },
]


# ════════════════════════════════════════════════════════════════════
#  TOOLS — the agent will call these autonomously
# ════════════════════════════════════════════════════════════════════

def tool_get_company_context(company_name: str) -> dict:
    """Production: queries mcp-vectordb on collection=company_profiles."""
    return COMPANY_PROFILES.get(company_name, {"error": f"No profile found for {company_name}"})


def tool_get_relevant_ag_content(topics: list[str]) -> list[dict]:
    """Production: semantic search on collection=ag_content."""
    topics_lower = [t.lower() for t in topics]
    results = []
    for c in AG_CONTENT:
        if any(t in c["topic"].lower() or t in c["title"].lower() or t in c["summary"].lower() for t in topics_lower):
            results.append(c)
    return results[:3]  # Top 3


def tool_score_lead(prospect: dict, company: dict) -> dict:
    """Score lead 1-100 based on ICP fit. Production: dedicated Claude Haiku call."""
    title = prospect.get("title", "").lower()
    size = company.get("size", 0)
    tech = [t.lower() for t in company.get("tech_stack", [])]
    pain = company.get("pain_signals", [])

    # Decision authority (0-25)
    senior_titles = ["cto", "vp", "head", "director", "cdo", "chief"]
    authority = 25 if any(t in title for t in senior_titles) else 10

    # Industry fit (0-20) — assume in-target for demo
    industry_fit = 18

    # Tech stack alignment (0-20)
    target_tech = ["snowflake", "databricks", "bigquery", "dbt", "airflow", "kafka"]
    tech_score = min(20, len([t for t in tech if t in target_tech]) * 5)

    # Intent signals (0-20)
    intent_score = min(20, len(pain) * 7)

    # Company size fit (0-15)
    size_score = 15 if 100 <= size <= 5000 else 5

    total = authority + industry_fit + tech_score + intent_score + size_score
    tier = "HOT" if total >= 75 else "WARM" if total >= 50 else "COLD" if total >= 25 else "DISCARD"

    return {
        "score": total,
        "tier": tier,
        "breakdown": {
            "authority": authority,
            "industry_fit": industry_fit,
            "tech_alignment": tech_score,
            "intent_signals": intent_score,
            "size_fit": size_score,
        },
    }


# Tool schemas — what Claude sees
TOOL_SCHEMAS = [
    {
        "name": "get_company_context",
        "description": (
            "Retrieve detailed company profile: industry, size, tech stack, recent news, and pain signals. "
            "Always call this first when writing outreach to a new prospect."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "company_name": {"type": "string", "description": "Exact company name to look up"}
            },
            "required": ["company_name"],
        },
    },
    {
        "name": "get_relevant_ag_content",
        "description": (
            "Find AnalyticsGear blog posts/case studies relevant to the prospect's challenges. "
            "Pass topic keywords like 'data-engineering', 'mlops', 'genai', 'data-governance', "
            "'analytics', 'data-platform'. Use this to find content worth sharing in the email."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of topic keywords to search for",
                }
            },
            "required": ["topics"],
        },
    },
    {
        "name": "score_lead",
        "description": (
            "Score the lead 1-100 based on ICP fit (authority, industry, tech, intent, size). "
            "Returns score, tier (HOT/WARM/COLD/DISCARD), and breakdown. Call after gathering context."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "prospect": {
                    "type": "object",
                    "description": "Prospect dict with name, title, email, company",
                },
                "company": {
                    "type": "object",
                    "description": "Company dict from get_company_context",
                },
            },
            "required": ["prospect", "company"],
        },
    },
]


TOOL_DISPATCH = {
    "get_company_context": lambda args: tool_get_company_context(args["company_name"]),
    "get_relevant_ag_content": lambda args: tool_get_relevant_ag_content(args["topics"]),
    "score_lead": lambda args: tool_score_lead(args["prospect"], args["company"]),
}


# ════════════════════════════════════════════════════════════════════
#  AGENT — Claude with tool use in a ReAct loop
# ════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are AnalyticsGear's Outreach Agent. You craft personalized cold emails to qualified leads.

About AnalyticsGear:
- Data Engineering, Analytics, AI & Cloud consultancy
- Services: Data pipelines, Snowflake/Databricks/BigQuery, GenAI/LLM engineering, MLOps, Cloud Migration, BI
- Engagement models: Discovery Sprint (2-4 weeks), Delivery Program, Embedded Retainer, Platform Rescue
- Based in India, serving global clients

Your workflow for each prospect:
1. Call get_company_context to retrieve their company profile
2. Identify their key pain points and technology
3. Call get_relevant_ag_content with topic keywords matching their pain (e.g., if they use Airflow with issues, search 'data-engineering')
4. Call score_lead to assess ICP fit
5. Compose the final email following these rules:
   - Under 120 words
   - Reference something specific about their company (tech stack, recent news, or pain signal)
   - Mention one piece of relevant AnalyticsGear content if it fits naturally
   - No salesy buzzwords
   - Soft CTA — not "book a call". Try "worth a quick chat?" or "happy to share what worked"
   - Peer-to-peer consultative tone
   - Lowercase, short subject line

Output your final email in this exact format:

SCORE: <number>/100  TIER: <HOT|WARM|COLD>
REASONING: <one-line reason for the score>

SUBJECT: <subject line>

<email body>

---
"""


def run_agent(prospect: dict[str, Any], model: str = "claude-sonnet-4-6") -> str:
    """Run the agent loop until it produces a final email."""
    client = Anthropic()

    messages = [
        {
            "role": "user",
            "content": (
                f"Write a personalized cold email to:\n"
                f"  Name: {prospect['name']}\n"
                f"  Title: {prospect['title']}\n"
                f"  Company: {prospect['company']}\n"
                f"  Email: {prospect.get('email', 'n/a')}\n\n"
                "Use your tools to gather context, score the lead, then write the email."
            ),
        }
    ]

    for iteration in range(10):
        response = client.messages.create(
            model=model,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=TOOL_SCHEMAS,
            max_tokens=2048,
        )

        # Show what the agent did this turn
        for block in response.content:
            if getattr(block, "type", None) == "tool_use":
                console.print(
                    f"  [cyan]-> tool[/cyan] [bold]{block.name}[/bold]([dim]{json.dumps(block.input)[:100]}...[/dim])"
                )

        if response.stop_reason == "end_turn":
            final_text = next(
                (b.text for b in response.content if getattr(b, "type", None) == "text"), ""
            )
            return final_text

        # Execute tool calls
        tool_results = []
        for block in response.content:
            if getattr(block, "type", None) == "tool_use":
                try:
                    result = TOOL_DISPATCH[block.name](block.input)
                except Exception as exc:
                    result = {"error": str(exc)}
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    return "[agent hit max iterations without finishing]"


# ════════════════════════════════════════════════════════════════════
#  MAIN — runs the demo end-to-end
# ════════════════════════════════════════════════════════════════════

PROSPECTS = [
    {
        "name": "Sarah Chen",
        "title": "CTO",
        "company": "DataFlow Inc",
        "email": "sarah@dataflow.example",
    },
    {
        "name": "James Patel",
        "title": "VP Data Engineering",
        "company": "MedSync Health",
        "email": "jpatel@medsync.example",
    },
    {
        "name": "Olivia Hart",
        "title": "Head of Analytics",
        "company": "ShopWave Retail",
        "email": "olivia@shopwave.example",
    },
]


def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY") or "your-key" in os.getenv("ANTHROPIC_API_KEY", ""):
        console.print(
            "[bold red]ANTHROPIC_API_KEY is missing or still set to placeholder.[/bold red]\n"
            "Add a real key to .env and re-run."
        )
        return

    console.print(Rule("[bold magenta]AnalyticsGear AI Outreach Agent — Demo[/bold magenta]"))
    console.print(
        "[dim]This is a working prototype. Tools currently use in-memory data; "
        "they'll be swapped for MCP servers + Qdrant later. Agent code is unchanged.[/dim]\n"
    )

    for i, prospect in enumerate(PROSPECTS, 1):
        console.print(
            Rule(f"[bold cyan]Prospect {i}/{len(PROSPECTS)}: {prospect['name']} @ {prospect['company']}[/bold cyan]")
        )
        console.print(f"  Title: {prospect['title']}")
        console.print(f"  Email: {prospect['email']}\n")

        console.print("[bold]Agent steps:[/bold]")
        result = run_agent(prospect)

        console.print()
        console.print(Panel(result, title="[bold green]Final Output[/bold green]", border_style="green"))
        console.print()


if __name__ == "__main__":
    main()
