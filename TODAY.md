# Today's Plan — Phase 1: First Real Drafts

**Date:** 2026-04-19
**Goal:** Go from fake demo → real, personalized email drafts you can actually send.
**Total time:** ~1 hour

---

## The 5 Steps

| # | Task | Who | Time | Status |
|---|------|-----|------|--------|
| 1 | Sign up for Apollo.io free tier | **You** | 5 min | ⬜ |
| 2 | Search ICP + export 5-10 real prospects to CSV | **You** | 15 min | ⬜ |
| 3 | Convert Apollo CSV to our pipeline format | Me | 5 min | ⬜ |
| 4 | Run pipeline → generate real drafts | Me | 5 min | ⬜ |
| 5 | Review drafts + send the good ones manually | **You** | 20 min | ⬜ |

**End state tonight:** Real AI-written personalized emails in front of you. Send a few by hand, watch for replies.

---

## Step 1 — Apollo Signup (You)

- Go to https://app.apollo.io
- Sign up (no credit card needed)
- Free tier = 50 verified emails/month

## Step 2 — Search + Export (You)

In Apollo: **Search → People**, apply filters:

| Filter | Value |
|--------|-------|
| Job Title | CTO, Head of Data, VP Engineering |
| Headcount | 50 – 1000 |
| Technology | Snowflake OR Databricks OR dbt |
| Country | Pick 1-2 (US / UK / India) |

Then:
- Check 5-10 boxes next to prospects with verified emails (green check)
- Click **Save Selected → Export CSV**
- Save to: `c:\analyticsgear\sales_pipeline\data\apollo_export.csv`

## Step 3-4 — I Handle (Me)

Once you say "done":
- I build `scripts/apollo_to_prospects.py` to convert the format
- I run `python -m src.pipeline.daily_runner`
- Cost: ~$0.05-0.10 in Claude API

## Step 5 — Review + Send (You)

- Open the report: `data/reports/2026-04-19.md`
- Each prospect has a score, tier, and a draft email
- Copy the good ones into Gmail/Outlook, edit if needed, send

---

## Optional (If You Have 15 Spare Minutes)

Start the **email warmup** — it's the only 3-week-wait item, so starting early helps:
- Buy a cold-outreach domain (~$12) e.g. `getanalyticsgear.com`
- We'll set up DNS + warmup later

**Not required for today.** Do Apollo first.

---

## What's NOT in Scope Today

- ❌ Automated email sending (Phase 3 — needs 3-week warmup)
- ❌ Auto lead sourcing via API (Phase 4)
- ❌ Server deployment (Phase 5)
- ❌ Real vector DB / RAG (Phase 6)

Today is just: **real prospects in → real drafts out → you send manually.**

---

## Next Action

👉 **Go sign up for Apollo (Step 1), then come back and say "done".**
