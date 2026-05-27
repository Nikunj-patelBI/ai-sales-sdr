"""Score a prospect and draft an email — in a SINGLE Claude call.

This replaces the multi-tool agent from the prototype. For our scale,
one well-crafted LLM call does everything we need: read the prospect's
data, score the ICP fit, and write a personalized email.

No vector DB, no MCP, no agent loop. Just one call. Cheaper, faster, simpler.
When we genuinely need RAG (thousands of docs) we can add it later.
"""
from __future__ import annotations

import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

_client = Anthropic()
MODEL = os.getenv("ANTHROPIC_MODEL_AGENT", "claude-sonnet-4-6")

# AnalyticsGear context — small enough to live in the prompt, no RAG needed.
AG_CONTEXT = """
About AnalyticsGear (the company sending this email):
- Data Engineering, Analytics, AI & Cloud consultancy. Based in India, serving global clients.
- Services: data pipelines, Snowflake/Databricks/BigQuery platforms, GenAI/LLM engineering,
  MLOps, cloud migration, BI dashboards.
- Engagement models: Discovery Sprint (2-4 weeks), Delivery Program, Embedded Retainer, Platform Rescue.
- Relevant published content (link only if it genuinely fits the prospect):
  - "Lakehouse Migration Playbook" - https://analyticsgear.com/insights/lakehouse-migration
  - "FinOps for Data Teams" (cutting Snowflake/Databricks cost) - https://analyticsgear.com/insights/finops-data
  - "Semantic Layer Strategy" - https://analyticsgear.com/insights/semantic-layer
  - "MLOps Without Ceremony" - https://analyticsgear.com/insights/mlops-pragmatic
  - "Data Contracts in Practice" - https://analyticsgear.com/insights/data-contracts
  - "RAG vs Fine-Tuning" - https://analyticsgear.com/insights/rag-vs-fine-tuning
"""

SYSTEM_PROMPT = f"""You are AnalyticsGear's sales assistant. Given a prospect, you do two things in one shot:
1. Score them 0-100 for ICP fit.
2. Write a personalized cold email.

{AG_CONTEXT}

SCORING (0-100):
- Decision authority (title seniority): 0-25
- Industry fit (Banking, Retail, Healthcare, SaaS, Manufacturing, Logistics): 0-20
- Tech stack alignment (Snowflake, Databricks, BigQuery, dbt, Airflow, cloud): 0-20
- Intent signals (hiring data roles, recent funding, growth, stated pain): 0-20
- Company size fit (50-5000 employees is ideal): 0-15
Tier: HOT (75-100), WARM (50-74), COLD (25-49), DISCARD (0-24).

EMAIL RULES:
- Under 120 words.
- Reference something SPECIFIC and TRUE from the prospect data provided (their tech, industry, role).
- NEVER invent facts. If you don't have a specific detail, stay general but relevant.
- No buzzwords. Peer-to-peer, consultative tone.
- Lowercase, short subject line.
- Soft CTA: "worth a quick chat?" not "book a demo".
- Only link AnalyticsGear content if it genuinely fits.

Respond with ONLY a JSON object, no other text:
{{
  "score": <int 0-100>,
  "tier": "<HOT|WARM|COLD|DISCARD>",
  "reasoning": "<one sentence why this score>",
  "subject": "<email subject line>",
  "body": "<full email body, plain text with line breaks>"
}}"""


def score_and_draft(prospect: dict) -> dict:
    """One Claude call: score the prospect and draft an email.

    `prospect` can include any fields you have: name, title, company, email,
    industry, employee_count, technologies, keywords, linkedin, etc.
    Whatever you pass, the model uses for personalization.
    """
    # Build a clean description of everything we know about the prospect.
    known = {k: v for k, v in prospect.items() if v and k != "email"}
    prospect_block = "\n".join(f"- {k}: {v}" for k, v in known.items())

    message = (
        f"Prospect data:\n{prospect_block}\n\n"
        "Score this prospect and write the email. Return only the JSON."
    )

    response = _client.messages.create(
        model=MODEL,
        system=SYSTEM_PROMPT,
        max_tokens=1024,
        messages=[{"role": "user", "content": message}],
    )

    text = response.content[0].text.strip()
    result = _parse_json(text)

    # Attach token usage for cost tracking
    result["_usage"] = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
    return result


def _parse_json(text: str) -> dict:
    """Robustly extract the JSON object from the model response."""
    # Handle accidental markdown fences
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    # Find the outermost { }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start : end + 1]
    return json.loads(text)


def estimate_cost(usage: dict) -> float:
    """Rough USD cost for a Sonnet call."""
    return usage["input_tokens"] * 3 / 1_000_000 + usage["output_tokens"] * 15 / 1_000_000
