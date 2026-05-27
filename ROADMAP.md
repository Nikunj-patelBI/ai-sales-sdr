# AI Sales Pipeline — Roadmap

> **Philosophy:** Manual-first, then automate. Get real value early, add sophistication only when needed.
> Each phase ends in a milestone you can see and feel.

**Last updated:** 2026-05-27
**Architecture:** Simple single-script pipeline — one Claude call per lead, SQLite CRM. No MCP/RAG/agents.

---

## The Big Picture

```
PHASE 0          PHASE 1          PHASE 2          PHASE 3          PHASE 4          PHASE 5
Foundation  -->  First Real  -->  Autonomous  -->  Automated   -->  Auto Lead   -->  Smarter
(DONE)           Drafts           Daily Runs       Sending          Sourcing        (optional)
```

| Phase | Goal | Milestone | Status |
|-------|------|-----------|--------|
| **0** | Build the simple pipeline | Scores leads + drafts emails, tested end-to-end | ✅ DONE |
| **1** | Real prospects → real drafts | First real personalized draft you send | 🟡 Ready — needs your Apollo leads |
| **2** | Autonomous local runs | Runs daily on your laptop, you get a report | 🟢 Tooling built — needs turning on |
| **3** | Automated email sending | Pipeline sends emails itself | ⬜ (3-week warmup lead time) |
| **4** | Automated lead sourcing | Apollo feeds leads automatically | ⬜ |
| **5** | Smarter (optional) | Richer personalization + learns from replies | ⬜ |

---

## ✅ PHASE 0 — Foundation (DONE)

The simple pipeline, built and tested.

| Ticket | What | Status |
|--------|------|--------|
| T-01 | Repo + project structure, pushed to GitHub | ✅ |
| T-02 | Python venv + minimal deps (anthropic, python-dotenv) | ✅ |
| T-03 | SQLite CRM — `database.py` | ✅ |
| T-04 | CSV loader with dedup — `csv_loader.py` | ✅ |
| T-05 | Scorer — one Claude call: score + draft email — `scorer.py` | ✅ |
| T-06 | Daily runner — `daily_runner.py` | ✅ |
| T-07 | Daily markdown report — `reporter.py` | ✅ |
| T-08 | Status tracking — `update_status.py` | ✅ |

**Milestone reached:** ✅ Live run works — 1 lead → scored + drafted → report, in 6.2s for $0.006.

---

## 🟡 PHASE 1 — First Real Drafts (READY — needs your input)

**Goal:** Real prospects in, real drafts out, send the best ones by hand.

| Ticket | What | Owner | Status |
|--------|------|-------|--------|
| T-09 | Sign up Apollo.io free tier (50 emails/mo) | **You** | ⬜ |
| T-10 | Export 5-10 real prospects to CSV | **You** | ⬜ |
| T-11 | Apollo CSV → our format — `scripts/apollo_to_prospects.py` | Me | ✅ Built |
| T-12 | Pass enrichment fields (industry, tech, headcount) through to scorer | Me | ⬜ Next |
| T-13 | Run pipeline against real leads | Me | ⬜ Blocked by T-10 |
| T-14 | Review report, send best drafts from Gmail/Outlook | **You** | ⬜ |

> **Note on T-12:** in testing, a lead with only name/title/company scored low (thin data).
> Apollo gives industry, tech stack, headcount — passing those through is the single biggest
> quality win. Small change, do it before the first real run.

**🎯 Milestone:** First personalized, AI-drafted email sent to a real prospect.

---

## 🟢 PHASE 2 — Autonomous Daily Runs (tooling built, needs turning on)

**Goal:** Pipeline runs itself every morning; you just read the report.

| Ticket | What | Owner | Status |
|--------|------|-------|--------|
| T-15 | Status tracking command (`update_status`) | Me | ✅ Built |
| T-16 | Windows Task Scheduler script | Me | ✅ Built (`scripts/schedule_daily.ps1`) |
| T-17 | Register the scheduled task on your laptop | **You** | ⬜ Run the .ps1 once |
| T-18 | Email the daily report to your inbox (optional) | Me | ⬜ |

**🎯 Milestone:** Wake up to a fresh report of drafts + pipeline status, zero manual effort.

---

## ⬜ PHASE 3 — Automated Email Sending

**Goal:** Pipeline sends emails itself. ⚠️ **The warmup has a 3-week lead time — start T-19/T-21 early.**

| Ticket | What | Owner |
|--------|------|-------|
| T-19 | Buy cold-outreach domain (~$12/yr) | You |
| T-20 | DNS auth: SPF, DKIM, DMARC | You + Me |
| T-21 | Start email warmup (Instantly.ai ~$30/mo, 3-week clock) | You |
| T-22 | SendGrid account + send function (direct API, no MCP) | Me |
| T-23 | Wire sending into daily_runner with guardrails + approval gate | Me |

**🎯 Milestone:** Pipeline sends personalized emails automatically, tracks opens/clicks.

---

## ⬜ PHASE 4 — Automated Lead Sourcing

**Goal:** Stop exporting CSVs by hand. The pipeline pulls leads itself.

| Ticket | What | Owner |
|--------|------|-------|
| T-24 | Apollo API integration (direct HTTP call, no MCP) | Me |
| T-25 | Daily auto-pull of N new ICP-matching leads | Me |
| T-26 | Intent signals — prioritize hiring/funded companies | Me |

**🎯 Milestone:** Fresh qualified leads flow in daily, hands-off.

> At this phase, consider **n8n or OpenClaw** as the automation/glue layer (trigger runs,
> watch inbox for replies, chat updates). The scoring/drafting code stays as-is — they wrap it.

---

## ⬜ PHASE 5 — Smarter (Optional, only if volume justifies it)

**Goal:** Better personalization and learning from what actually works.

| Ticket | What | Owner |
|--------|------|-------|
| T-27 | Multi-touch sequences (follow-up emails, not just first touch) | Me |
| T-28 | Learn from outcomes — feed winning email patterns back into the prompt | Me |
| T-29 | (Only if needed) richer company research before drafting | Me |

> We deliberately skipped vector DB / RAG / multi-agent. Revisit **only** if you have
> thousands of leads/docs and simple prompting stops being enough. Probably not for a long time.

**🎯 Milestone:** Reply rates climb over time without manual tuning.

---

## What To Do Right Now

You are here: **Phase 0 done. Phase 1 & 2 tooling built. Need real leads to go live.**

**Your next 3 steps:**
1. **T-09** — Sign up for Apollo free tier (5 min)
2. **T-10** — Export 5-10 real prospects to `data/apollo_export.csv` (15 min)
3. Tell me → I do **T-12** (enrichment passthrough) + **T-13** (run it) → you review + send (**T-14**)

**Start early if you want automated sending soon:**
- **T-19 + T-21** — buy the domain + start email warmup (3-week clock).

---

## Cost Summary

| Stage | One-time | Monthly |
|-------|----------|---------|
| Phase 0-2 (now) | $0 | ~$5-10 (Claude API only) |
| Phase 3 (auto send) | $12 (domain) | +$30 (warmup), SendGrid free tier |
| Phase 4 (auto sourcing) | $0 | +$49 (Apollo paid for API) |
| Phase 5 (optional) | $0 | minimal |
| **Fully automated** | **~$12** | **~$45-90/mo** |

vs. ~$3,000-5,000/mo for a junior SDR.
