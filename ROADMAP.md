# AI Sales Pipeline — Practical Roadmap

> The simple, human-readable plan. Reflects where we actually are and what's next.
> For the granular 92-task version, see `project_management/AnalyticsGear_AI_Pipeline_Project_Plan.xlsx`.
>
> **Philosophy:** Manual-first, then automate. Get real value early, add sophistication later.
> Each phase ends in a milestone you can see and feel.

**Last updated:** 2026-04-19

---

## The Big Picture

```
PHASE 0          PHASE 1          PHASE 2          PHASE 3          PHASE 4          PHASE 5
Foundation  -->  First Real  -->  Autonomous  -->  Real Auto   -->  Auto Lead   -->  Deploy to
(DONE)           Drafts           Local Daily      Sending          Sourcing         Server 24/7
                                                                                         |
                                                                                         v
                                                                                    PHASE 6
                                                                                    Smarter (RAG)
```

| Phase | Goal | Milestone | Status |
|-------|------|-----------|--------|
| **0** | Foundation + working prototype | AI agent generates emails (fake data) | ✅ DONE |
| **1** | Real prospects → real drafts | First personalized draft for a real prospect | 🟡 In progress |
| **2** | Autonomous local runs | Pipeline runs daily on laptop, you get morning reports | ⬜ Next |
| **3** | Real automated email sending | Agent sends emails by itself | ⬜ (3-week lead time!) |
| **4** | Automated lead sourcing | No more manual CSV — Apollo auto-feeds leads | ⬜ |
| **5** | Deploy to server | Runs 24/7 in cloud without your laptop | ⬜ |
| **6** | Smarter system (RAG + memory) | Agent learns from what works, improves over time | ⬜ |

---

## ✅ PHASE 0 — Foundation (DONE)

| Ticket | What | Status |
|--------|------|--------|
| T-01 | Git repo + project structure, pushed to GitHub | ✅ |
| T-02 | Python venv + all dependencies installed | ✅ |
| T-03 | Working AI Outreach Agent prototype (tool use, scoring, email gen) | ✅ |
| T-04 | SQLite "CRM" database (prospects, outreach, activities, runs) | ✅ |
| T-05 | CSV loader with dedup logic | ✅ |
| T-06 | Daily pipeline runner (reads CSV → scores → drafts → saves) | ✅ |
| T-07 | Daily markdown report generator | ✅ |

**Milestone reached:** ✅ AI agent generates scored, personalized emails for sample prospects.

---

## 🟡 PHASE 1 — First Real Drafts (THIS WEEK)

**Goal:** Get real prospects into the system and generate drafts you'd actually send.

### T-08: Sign up for Apollo.io free tier
- **What:** Create Apollo account (50 free verified emails/month)
- **Why:** Need a source of real, verified prospect emails
- **How:** apollo.io → sign up → no credit card needed
- **Effort:** 5 min · **Owner:** You · **Status:** ⬜

### T-09: Export 5-10 real prospects from Apollo
- **What:** Search ICP (CTO/Head of Data, 50-1000 employees, Snowflake/Databricks users), export CSV
- **Why:** First batch of real targets
- **How:** Apollo Search → People → apply filters → Save Selected → Export CSV
- **Effort:** 15 min · **Owner:** You · **Status:** ⬜

### T-10: Build Apollo CSV adapter
- **What:** Convert Apollo's column format to our `prospects.csv` format
- **Why:** Apollo uses `first_name`/`last_name`; we use `name`
- **How:** Small Python script `scripts/apollo_to_prospects.py`
- **Effort:** 30 min · **Owner:** Me · **Status:** ⬜ · **Blocked by:** T-09

### T-11: Run pipeline against real prospects
- **What:** Execute daily_runner against real data, generate drafts
- **Why:** Validate the whole system works with real-world data
- **How:** `python -m src.pipeline.daily_runner`
- **Effort:** 5 min · **Cost:** ~$0.05-0.10 · **Owner:** Me · **Status:** ⬜ · **Blocked by:** T-10

### T-12: Review drafts + send first emails manually
- **What:** Read the daily report, pick the best drafts, send from your Gmail/Outlook
- **Why:** Get real outreach out the door without needing send infrastructure
- **How:** Open `data/reports/<date>.md`, copy-paste good drafts into your email client
- **Effort:** 20 min · **Owner:** You · **Status:** ⬜ · **Blocked by:** T-11

**🎯 Milestone:** First personalized, AI-generated email sent to a real prospect.

---

## ⬜ PHASE 2 — Autonomous Local Daily Runs

**Goal:** Pipeline runs by itself every morning; you wake up to a report.

### T-13: End-to-end test of daily runner
- **What:** Full run with error handling verified
- **Why:** Confidence before automating
- **Effort:** 30 min · **Owner:** Me · **Status:** ⬜

### T-14: Schedule daily run (Windows Task Scheduler)
- **What:** Auto-run pipeline every morning at 8 AM
- **Why:** True "set it and forget it" — no manual triggering
- **How:** PowerShell script + Task Scheduler entry (`scripts/schedule_daily.ps1`)
- **Effort:** 30 min · **Owner:** Me · **Status:** ⬜

### T-15: Email the daily report to yourself
- **What:** Pipeline emails you the morning report instead of just saving to disk
- **Why:** See results without opening the project
- **How:** Simple SMTP send to your inbox (uses Gmail app password, no warmup needed for self-email)
- **Effort:** 45 min · **Owner:** Me · **Status:** ⬜

### T-16: Reply / status tracking
- **What:** Simple way to mark a prospect as replied / meeting booked / lost
- **Why:** Keep the "existing bids" tracking you asked for
- **How:** CLI command `python -m src.pipeline.update_status <email> replied` + reflected in reports
- **Effort:** 1 hr · **Owner:** Me · **Status:** ⬜

**🎯 Milestone:** Wake up each morning to an email report of new drafts + pipeline status. Zero manual effort.

---

## ⬜ PHASE 3 — Real Automated Email Sending

**Goal:** Agent sends emails by itself. ⚠️ **Start the warmup ticket NOW — it has a 3-week lead time.**

### T-17: Buy cold-outreach domain ⏰ START EARLY
- **What:** Register a separate domain (e.g., `getanalyticsgear.com` or `outreach.analyticsgear.com`)
- **Why:** Protects your main `analyticsgear.com` reputation from cold-email risk
- **How:** Namecheap / Google Domains, ~$12/year
- **Effort:** 15 min · **Owner:** You · **Status:** ⬜

### T-18: DNS authentication (SPF, DKIM, DMARC)
- **What:** Set up email authentication records
- **Why:** Without these, your emails go straight to spam
- **How:** Add DNS records (I'll generate exact values)
- **Effort:** 30 min · **Owner:** You + Me · **Status:** ⬜ · **Blocked by:** T-17

### T-19: Start email warmup ⏰ 3-WEEK CLOCK
- **What:** Gradually ramp sending volume so inbox providers trust the domain
- **Why:** Brand-new domains that suddenly send 50 emails/day get blacklisted instantly
- **How:** Instantly.ai or Warmup Inbox, ~$30/mo. Set and forget for 3 weeks.
- **Effort:** 30 min setup, 3 weeks waiting · **Owner:** You · **Status:** ⬜ · **Blocked by:** T-17

### T-20: SendGrid account + integration
- **What:** Set up SendGrid, build the email-send tool
- **Why:** Reliable delivery + open/click tracking
- **How:** SendGrid free tier + `mcp-email` server
- **Effort:** 3 hrs · **Owner:** Me · **Status:** ⬜

### T-21: Wire agent to send (with safety guardrails)
- **What:** Agent sends approved drafts automatically; daily send caps, no-duplicate checks
- **Why:** The actual automation payoff
- **How:** Integrate send into daily_runner, add human-approval gate for first 2 weeks
- **Effort:** 2 hrs · **Owner:** Me · **Status:** ⬜ · **Blocked by:** T-19, T-20

**🎯 Milestone:** Agent sends personalized cold emails automatically, tracks opens/clicks.

---

## ⬜ PHASE 4 — Automated Lead Sourcing

**Goal:** Stop manually exporting CSVs. The system finds leads itself.

### T-22: Apollo API integration (mcp-apollo)
- **What:** Pull leads directly from Apollo via API instead of manual export
- **Why:** Fully hands-off lead discovery
- **How:** Build `mcp-apollo` server (Apollo paid tier $49/mo for API access)
- **Effort:** 4 hrs · **Owner:** Me · **Status:** ⬜

### T-23: Daily auto-prospecting
- **What:** Prospecting Agent finds 25 new ICP-matching leads each morning
- **Why:** Continuous top-of-funnel without your involvement
- **Effort:** 3 hrs · **Owner:** Me · **Status:** ⬜ · **Blocked by:** T-22

### T-24: Intent signals (job boards, funding news)
- **What:** Prioritize companies hiring data roles / recently funded
- **Why:** Higher-intent leads convert better
- **Effort:** 4 hrs · **Owner:** Me · **Status:** ⬜

**🎯 Milestone:** Fresh qualified leads flow in daily with zero manual work.

---

## ⬜ PHASE 5 — Deploy to Server (24/7)

**Goal:** Runs in the cloud, not your laptop. Works while you sleep / travel.

### T-25: Provision a VPS
- **What:** Small cloud server (Hetzner CX22 or DigitalOcean, ~$5-10/mo)
- **Why:** Laptop can't be the production host (off when closed)
- **How:** Create droplet/server, SSH, basic hardening
- **Effort:** 1 hr · **Owner:** You + Me · **Status:** ⬜

### T-26: Dockerize the application
- **What:** Package app + Qdrant into containers
- **Why:** Reproducible, portable deployment
- **How:** Dockerfile + docker-compose (already drafted in repo)
- **Effort:** 2 hrs · **Owner:** Me · **Status:** ⬜

### T-27: Deploy + schedule on server
- **What:** Run the pipeline on the VPS via cron, daily
- **Why:** True 24/7 autonomy
- **Effort:** 2 hrs · **Owner:** Me · **Status:** ⬜ · **Blocked by:** T-25, T-26

### T-28: Monitoring + alerts
- **What:** Get notified if a run fails or costs spike
- **Why:** Catch problems without babysitting
- **How:** Langfuse for traces + email/Slack alerts on failure
- **Effort:** 2 hrs · **Owner:** Me · **Status:** ⬜

**🎯 Milestone:** Pipeline runs in the cloud daily, unattended. You just read the reports.

---

## ⬜ PHASE 6 — Smarter System (RAG + Memory)

**Goal:** The system learns. Better personalization, learns what works, improves itself.

### T-29: Qdrant vector DB + embeddings
- **What:** Replace dict-lookup tools with real semantic search
- **Why:** Scales to thousands of companies + content; true RAG
- **How:** Qdrant (Docker) + Voyage AI embeddings
- **Effort:** 4 hrs · **Owner:** Me · **Status:** ⬜

### T-30: Ingest real knowledge base
- **What:** Embed AnalyticsGear blog posts, case studies, company profiles
- **Why:** Agent retrieves real, accurate content for personalization
- **Effort:** 3 hrs · **Owner:** Me · **Status:** ⬜ · **Blocked by:** T-29

### T-31: Memory — remember every interaction
- **What:** Agent recalls past touches per prospect, never repeats itself
- **Why:** Genuinely personal multi-touch sequences
- **Effort:** 4 hrs · **Owner:** Me · **Status:** ⬜

### T-32: Feedback loop — learn from outcomes
- **What:** Track which emails get replies, feed winning patterns back into generation
- **Why:** The system gets better every week automatically
- **Effort:** 5 hrs · **Owner:** Me · **Status:** ⬜

**🎯 Milestone:** Self-improving system. Reply rates climb over time without manual tuning.

---

## What To Do Right Now

You are here: **end of Phase 0, start of Phase 1.**

**Your immediate next 3 tickets:**
1. **T-08** — Sign up for Apollo free tier (5 min)
2. **T-09** — Export 5-10 real prospects (15 min)
3. Hand me the CSV → I do **T-10, T-11** → you get real drafts to review (**T-12**)

**Also start early (don't wait):**
- **T-17 + T-19** — Buy the domain and start email warmup. The 3-week warmup clock is the longest pole in the tent. If you start it this week, automated sending is ready by mid-May.

---

## Cost Summary

| Phase | One-time | Monthly |
|-------|----------|---------|
| 0-2 | $0 | ~$5-10 (Claude API) |
| 3 | $12 (domain) | +$30 (warmup) +$0 (SendGrid free tier) |
| 4 | $0 | +$49 (Apollo paid for API) |
| 5 | $0 | +$5-10 (VPS) |
| 6 | $0 | +$5 (embeddings) |
| **Full system** | **~$12** | **~$95-110/mo** |

vs. ~$3,000-5,000/mo for a junior SDR.
