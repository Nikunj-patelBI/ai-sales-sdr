# AnalyticsGear — AI-Powered Sales Pipeline Blueprint

> **Goal:** Replace a full-time sales hire with an automated, AI-driven pipeline that prospects, qualifies, reaches out, follows up, and logs everything — running a few hours each day on autopilot.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Pipeline Architecture Overview](#2-pipeline-architecture-overview)
3. [Phase 1 — Lead Discovery & Prospecting](#3-phase-1--lead-discovery--prospecting)
4. [Phase 2 — Lead Enrichment & Scoring](#4-phase-2--lead-enrichment--scoring)
5. [Phase 3 — Outreach Automation](#5-phase-3--outreach-automation)
6. [Phase 4 — Follow-Up & Nurturing](#6-phase-4--follow-up--nurturing)
7. [Phase 5 — CRM, Logging & Tracking](#7-phase-5--crm-logging--tracking)
8. [Phase 6 — Analytics & Optimization](#8-phase-6--analytics--optimization)
9. [Tech Stack & Tools](#9-tech-stack--tools)
10. [Daily Automation Schedule](#10-daily-automation-schedule)
11. [Implementation Roadmap](#11-implementation-roadmap)
12. [Cost Estimates](#12-cost-estimates)
13. [Risk Mitigation & Compliance](#13-risk-mitigation--compliance)
14. [Appendix — Prompt Templates & Scripts](#14-appendix--prompt-templates--scripts)

---

## 1. Executive Summary

AnalyticsGear offers Data Engineering, Analytics, AI, Cloud, and DevOps consulting services to mid-to-large enterprises across Banking, Retail, Healthcare, Manufacturing, Logistics, and SaaS verticals. Rather than hiring a sales team upfront, this blueprint designs a fully automated AI sales pipeline that:

- **Discovers** 50-100 new qualified leads per week from multiple sources
- **Enriches** each lead with company data, tech stack, hiring signals, and pain points
- **Reaches out** via personalized cold email, LinkedIn, and scheduled cold calls
- **Follows up** intelligently based on engagement signals
- **Logs everything** in a central CRM/spreadsheet with full audit trail
- **Runs 2-4 hours/day** on a scheduled basis with minimal human oversight

**Expected outcome:** 10-20 qualified conversations per month within 60 days of launch, with a fully traceable pipeline from first touch to booked call.

---

## 2. Pipeline Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     DAILY AUTOMATED PIPELINE                        │
│                      (Runs 2-4 hours/day)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │  PHASE 1  │──▶│  PHASE 2  │──▶│  PHASE 3  │──▶│  PHASE 4  │     │
│  │ Discovery │   │ Enrichment│   │ Outreach  │   │ Follow-Up │     │
│  │& Prospect │   │ & Scoring │   │ Automation│   │ & Nurture │     │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │
│       │              │              │              │                │
│       └──────────────┴──────────────┴──────────────┘                │
│                          │                                          │
│                    ┌─────▼─────┐                                    │
│                    │  PHASE 5   │                                    │
│                    │ CRM & Logs │                                    │
│                    └─────┬─────┘                                    │
│                          │                                          │
│                    ┌─────▼─────┐                                    │
│                    │  PHASE 6   │                                    │
│                    │ Analytics  │                                    │
│                    └───────────┘                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Phase 1 — Lead Discovery & Prospecting

### 3.1 Ideal Customer Profile (ICP)

Based on AnalyticsGear's service offerings, our ICP is:

| Attribute | Criteria |
|-----------|----------|
| **Company size** | 100-5000 employees |
| **Revenue** | $10M - $500M |
| **Industries** | Banking/Finance, Retail/CPG, Healthcare, Manufacturing, Logistics, SaaS |
| **Roles to target** | CTO, VP Engineering, Head of Data, Data Engineering Manager, VP Analytics, Chief Data Officer |
| **Geography** | US, UK, EU, Middle East, India, SEA |
| **Tech signals** | Uses Snowflake/Databricks/BigQuery, hiring data engineers, recent funding, data team growth |
| **Pain signals** | Job postings for data roles (they need help), legacy migration mentions, compliance requirements |

### 3.2 Lead Sources & Collection Methods

#### Source 1: LinkedIn Sales Navigator (Primary)
- **What:** Search for ICP-matching decision makers
- **How:** Use LinkedIn Sales Navigator API or scraping tools (Phantombuster, Apify)
- **Volume:** 20-30 leads/day
- **Data captured:** Name, title, company, LinkedIn URL, mutual connections
- **Automation:** Daily saved search export → CSV → pipeline

#### Source 2: Company Databases
- **Tools:** Apollo.io, ZoomInfo, Clearbit, or Hunter.io
- **What:** Bulk search companies matching ICP criteria
- **How:** API-based queries filtered by industry, size, tech stack, hiring signals
- **Volume:** 30-50 leads/day
- **Data captured:** Company info, decision maker contacts, emails, phone numbers

#### Source 3: Job Board Scraping (Intent Signal)
- **What:** Companies hiring for data engineers, analytics managers, ML engineers = companies with data needs
- **How:** Scrape LinkedIn Jobs, Indeed, Glassdoor for relevant job postings
- **Tool:** Custom Python scraper or Apify actor
- **Volume:** 10-20 companies/day
- **Signal strength:** HIGH — if they're hiring, they have budget and need

#### Source 4: Technology Signal Monitoring
- **What:** Track companies adopting or struggling with Snowflake, Databricks, dbt, Airflow, etc.
- **How:** Monitor BuiltWith, Wappalyzer, G2 reviews, GitHub activity
- **Signal:** Company recently adopted a data platform = needs help implementing it

#### Source 5: Event & Conference Attendees
- **What:** People attending data/cloud/AI conferences
- **How:** Scrape attendee lists from events, webinars, Meetup groups
- **Examples:** dbt Coalesce, Snowflake Summit, AWS re:Invent, DataEngBytes

#### Source 6: Inbound Website Leads
- **What:** Your existing Web3Forms contact form submissions
- **How:** Auto-forward form submissions to the pipeline for immediate follow-up
- **Priority:** HIGHEST — these leads are already warm

#### Source 7: Content & Social Listening
- **What:** People discussing data challenges on LinkedIn, Twitter/X, Reddit, HN
- **How:** Monitor keywords like "data pipeline broken", "need data engineer", "migrating to snowflake"
- **Tool:** Custom script using Reddit API, Twitter/X API, LinkedIn post monitoring

### 3.3 Prospecting Automation Script (Pseudocode)

```python
# daily_prospecting.py — runs every morning at 7 AM

def run_daily_prospecting():
    leads = []

    # 1. LinkedIn Sales Navigator export
    leads += linkedin_navigator.search(
        titles=["CTO", "VP Data", "Head of Engineering", "CDO"],
        industries=["Banking", "Retail", "Healthcare", "SaaS"],
        company_size="100-5000",
        geography=["US", "UK", "India", "EU"],
        limit=25
    )

    # 2. Apollo.io API search
    leads += apollo.search(
        job_titles=ICP_TITLES,
        industries=ICP_INDUSTRIES,
        technologies=["Snowflake", "Databricks", "BigQuery", "dbt"],
        company_headcount="100-5000",
        limit=30
    )

    # 3. Job board intent signals
    hiring_companies = job_scraper.search(
        keywords=["data engineer", "analytics engineer", "ML engineer"],
        posted_within_days=7
    )
    leads += enrich_from_hiring(hiring_companies)

    # 4. Deduplicate against existing CRM
    new_leads = deduplicate(leads, crm.get_all_contacts())

    # 5. Push to enrichment phase
    for lead in new_leads:
        enrichment_queue.add(lead)

    log(f"Discovered {len(new_leads)} new leads today")
```

---

## 4. Phase 2 — Lead Enrichment & Scoring

### 4.1 Enrichment Data Points

For each lead discovered, automatically gather:

| Data Point | Source | Purpose |
|-----------|--------|---------|
| Verified email | Hunter.io, Apollo, Clearbit | Email outreach |
| Phone number | Apollo, ZoomInfo | Cold calling |
| Company revenue & headcount | Clearbit, Apollo | Qualification |
| Tech stack | BuiltWith, Wappalyzer, job postings | Personalization |
| Recent funding | Crunchbase API | Budget signal |
| Recent job postings | LinkedIn, Indeed | Need signal |
| Company news | Google News API, press releases | Conversation starter |
| LinkedIn activity | LinkedIn | Engagement hooks |
| Mutual connections | LinkedIn | Warm intro paths |
| Existing vendors/partners | G2, case studies | Competitive positioning |

### 4.2 AI-Powered Lead Scoring

Use an LLM (Claude API) to score each lead 1-100 based on:

```python
def score_lead(lead: dict) -> int:
    prompt = f"""
    Score this lead 1-100 for AnalyticsGear (Data/AI/Cloud consultancy).

    Lead info:
    - Name: {lead['name']}
    - Title: {lead['title']}
    - Company: {lead['company']}
    - Industry: {lead['industry']}
    - Company size: {lead['headcount']}
    - Tech stack: {lead['tech_stack']}
    - Hiring data roles: {lead['hiring_data_roles']}
    - Recent funding: {lead['funding']}
    - Pain signals: {lead['pain_signals']}

    Scoring criteria:
    - Decision-making authority (title seniority): 0-25 points
    - Industry fit (Banking, Retail, Healthcare, SaaS, Manufacturing): 0-20 points
    - Tech stack alignment (Snowflake, Databricks, dbt, Airflow, cloud): 0-20 points
    - Intent signals (hiring, funding, job posts, tech adoption): 0-20 points
    - Company size fit (100-5000 employees): 0-15 points

    Return ONLY a JSON: {{"score": N, "tier": "HOT|WARM|COLD", "reason": "..."}}
    """
    return call_claude_api(prompt)
```

### 4.3 Lead Tiers & Actions

| Tier | Score | Daily Volume | Action |
|------|-------|-------------|--------|
| **HOT** | 75-100 | 5-10 | Personalized email + LinkedIn connect + phone call within 24h |
| **WARM** | 50-74 | 15-25 | Personalized email + LinkedIn connect within 48h |
| **COLD** | 25-49 | 10-20 | Template email + LinkedIn connect within 1 week |
| **DISCARD** | 0-24 | Variable | Archive, do not contact |

---

## 5. Phase 3 — Outreach Automation

### 5.1 Channel Strategy

```
                    ┌─────────────────────┐
                    │    QUALIFIED LEAD    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌───────────┐   ┌───────────┐   ┌───────────┐
        │   EMAIL    │   │  LINKEDIN  │   │   PHONE   │
        │  (Day 1)   │   │  (Day 1)   │   │  (Day 2)  │
        └───────────┘   └───────────┘   └───────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   MULTI-CHANNEL     │
                    │   FOLLOW-UP SEQ     │
                    └─────────────────────┘
```

### 5.2 Email Outreach

#### Tool Options
- **SendGrid / Mailgun** — Transactional email with tracking (opens, clicks)
- **Instantly.ai / Smartlead** — Cold email platform with warmup, rotation, deliverability
- **Custom SMTP** — For full control (use with email warmup service)

#### Email Deliverability Essentials
- Set up SPF, DKIM, DMARC records for analyticsgear.com
- Use a separate domain for cold outreach (e.g., `mail.analyticsgear.com` or `analyticsgear.io`)
- Warm up sending domain for 2-3 weeks before full volume
- Max 30-50 cold emails/day per email account
- Rotate across 3-5 email accounts
- Track bounce rates, keep below 3%

#### AI-Generated Personalized Emails

```python
def generate_outreach_email(lead: dict) -> str:
    prompt = f"""
    Write a cold outreach email from AnalyticsGear to this prospect.

    About AnalyticsGear:
    - Data Engineering, Analytics, AI & Cloud consultancy
    - Services: Data pipelines, Snowflake/Databricks/BigQuery platforms,
      GenAI/LLM engineering, MLOps, Cloud Migration, BI dashboards
    - Engagement models: Discovery Sprint (2-4 weeks), Delivery Program,
      Embedded Retainer, Platform Rescue
    - Based in India, serving global clients

    Prospect:
    - Name: {lead['name']}
    - Title: {lead['title']}
    - Company: {lead['company']}
    - Industry: {lead['industry']}
    - Tech stack: {lead['tech_stack']}
    - Pain signals: {lead['pain_signals']}
    - Recent news: {lead['recent_news']}

    Rules:
    - Keep under 120 words
    - No salesy language, no buzzwords
    - Reference something specific about their company
    - End with a soft CTA (not "book a call" — try "worth a quick chat?")
    - Tone: peer-to-peer, consultative, not vendor-pitch
    - Subject line: short, lowercase, feels personal
    """
    return call_claude_api(prompt)
```

#### Sample Email Sequences

**Sequence for HOT leads (5 emails over 14 days):**

| Day | Email | Purpose |
|-----|-------|---------|
| 1 | Personalized intro referencing their specific challenge | Open door |
| 3 | Share a relevant AnalyticsGear blog post (e.g., Lakehouse migration) | Add value |
| 6 | Brief case-study style proof point | Build credibility |
| 10 | "Did this land?" — short bump email | Re-engage |
| 14 | Breakup email — "Closing the loop, feel free to reach out anytime" | Final touch |

**Sequence for WARM leads (3 emails over 10 days):**

| Day | Email | Purpose |
|-----|-------|---------|
| 1 | Personalized intro | Open door |
| 5 | Share relevant insight or blog post | Add value |
| 10 | Breakup email | Final touch |

### 5.3 LinkedIn Outreach

#### Tools
- **Phantombuster** — LinkedIn automation (connect, message, visit profiles)
- **Dripify / Expandi** — LinkedIn drip campaigns
- **Manual + AI assist** — Use AI to draft messages, send manually (safest)

#### LinkedIn Sequence

| Step | Day | Action |
|------|-----|--------|
| 1 | Day 0 | View their profile (triggers "who viewed" notification) |
| 2 | Day 1 | Send connection request with personalized note (under 300 chars) |
| 3 | Day 2 | Like/comment on their recent post (if any) |
| 4 | Day 3 | Once connected, send intro message |
| 5 | Day 7 | Share a relevant article or insight |
| 6 | Day 14 | Follow up if no response |

#### AI-Generated LinkedIn Connection Note

```python
def generate_linkedin_note(lead: dict) -> str:
    prompt = f"""
    Write a LinkedIn connection request note (max 280 characters)
    for {lead['name']}, {lead['title']} at {lead['company']}.

    Context: AnalyticsGear does Data/AI/Cloud consulting.
    Their company uses: {lead['tech_stack']}
    Pain signal: {lead['pain_signals']}

    Rules:
    - No selling in the connection request
    - Reference a shared interest or their work
    - Be human, not corporate
    - Max 280 characters
    """
    return call_claude_api(prompt)
```

### 5.4 Cold Calling (Semi-Automated)

Cold calling can't be fully automated but can be heavily AI-assisted:

#### Pre-Call Automation
- AI generates a **call brief** for each lead: company background, pain points, talking points, objection handling
- Auto-schedule call blocks (e.g., 10 AM - 12 PM daily)
- Auto-dial through a list using **JustCall**, **Aircall**, or **Twilio**
- Call recordings auto-transcribed and summarized by AI

#### AI Call Brief Generator

```python
def generate_call_brief(lead: dict) -> str:
    prompt = f"""
    Generate a cold call brief for calling {lead['name']},
    {lead['title']} at {lead['company']}.

    Their company: {lead['company_description']}
    Industry: {lead['industry']}
    Tech stack: {lead['tech_stack']}
    Pain signals: {lead['pain_signals']}

    Generate:
    1. Opening hook (10 seconds, mention something relevant to them)
    2. Value proposition (tailored to their industry/tech)
    3. Three discovery questions
    4. Common objections + responses
    5. CTA: suggest a 20-min discovery call
    """
    return call_claude_api(prompt)
```

---

## 6. Phase 4 — Follow-Up & Nurturing

### 6.1 Engagement Signal Tracking

Track these signals to trigger intelligent follow-ups:

| Signal | Source | Follow-Up Action |
|--------|--------|-----------------|
| Email opened | SendGrid/Instantly | Wait for click or reply |
| Email link clicked | SendGrid/Instantly | Send follow-up within 2 hours |
| Email replied | Inbox monitoring | Alert founder, respond within 1 hour |
| LinkedIn connection accepted | LinkedIn | Send intro DM |
| LinkedIn message read | LinkedIn | Follow up after 3 days if no reply |
| Visited website | Google Analytics / Clearbit Reveal | Send contextual email |
| Downloaded content | Website tracking | Add to hot list |
| No response after full sequence | CRM | Move to monthly nurture list |

### 6.2 Nurture Campaigns (Long-Term)

For leads that don't convert immediately, run monthly nurture:

- **Monthly insight email:** Share a new AnalyticsGear blog post or case study
- **Quarterly check-in:** "Anything changed on the data front?"
- **Event invites:** Webinars, AMAs, community events
- **Re-engagement trigger:** If they change jobs, get funding, or post about data challenges

### 6.3 AI-Powered Response Handling

```python
def handle_email_reply(reply: str, lead: dict) -> dict:
    prompt = f"""
    Classify this email reply and draft a response.

    Original outreach: We pitched AnalyticsGear's data/AI consulting services.
    Their reply: "{reply}"

    Classify as one of:
    - INTERESTED: They want to learn more or book a call
    - OBJECTION: They have concerns (budget, timing, already have vendor)
    - NOT_NOW: Interested but not the right time
    - NOT_INTERESTED: Clear no
    - OUT_OF_OFFICE: Auto-reply
    - WRONG_PERSON: They're not the right contact

    For INTERESTED: Draft a reply proposing specific times for a 20-min call.
    For OBJECTION: Draft a reply addressing the specific objection.
    For NOT_NOW: Draft a reply asking when to follow up.
    For WRONG_PERSON: Draft a reply asking for the right contact.

    Return JSON: {{"classification": "...", "draft_reply": "...", "next_action": "..."}}
    """
    return call_claude_api(prompt)
```

---

## 7. Phase 5 — CRM, Logging & Tracking

### 7.1 CRM Options (Low-Cost)

| Option | Cost | Best For |
|--------|------|----------|
| **Google Sheets + Apps Script** | Free | Starting out, max flexibility |
| **Notion Database** | Free-$10/mo | Visual pipeline, collaboration |
| **HubSpot CRM (Free)** | Free | Proper CRM with email integration |
| **Airtable** | Free-$20/mo | Flexible database with automations |
| **Folk CRM** | $20/mo | Lightweight, LinkedIn-integrated |

**Recommendation:** Start with **Google Sheets** for speed, migrate to **HubSpot Free** once volume exceeds 200 leads.

### 7.2 CRM Schema (Google Sheets)

#### Sheet 1: Master Lead List

| Column | Description |
|--------|-------------|
| Lead ID | Auto-generated unique ID |
| First Name | |
| Last Name | |
| Email | Verified email |
| Phone | |
| LinkedIn URL | |
| Company | |
| Title/Role | |
| Industry | |
| Company Size | |
| Tech Stack | Detected technologies |
| Lead Source | LinkedIn / Apollo / Job Board / Inbound / etc. |
| Lead Score | 1-100 AI score |
| Lead Tier | HOT / WARM / COLD |
| Pain Signals | Detected challenges |
| Status | New / Contacted / Replied / Meeting Booked / Proposal / Won / Lost |
| Current Sequence | Which outreach sequence they're in |
| Sequence Step | Which step of the sequence |
| Date Added | |
| Last Contacted | |
| Next Follow-Up | |
| Notes | AI-generated + manual notes |
| Owner | Who's handling this lead |

#### Sheet 2: Activity Log

| Column | Description |
|--------|-------------|
| Timestamp | |
| Lead ID | |
| Channel | Email / LinkedIn / Phone / Website |
| Action | Sent / Opened / Clicked / Replied / Called / Connected |
| Details | Email subject, message content, call notes |
| Outcome | Positive / Neutral / Negative / No Response |

#### Sheet 3: Pipeline Dashboard

| Column | Description |
|--------|-------------|
| Stage | Discovery → Contacted → Engaged → Meeting → Proposal → Won/Lost |
| Count | Number of leads at each stage |
| Conversion Rate | Stage-over-stage conversion |
| Avg Days in Stage | |
| Revenue Potential | Estimated deal value |

### 7.3 Automated Logging

Every action in the pipeline auto-logs to the CRM:

```python
def log_activity(lead_id: str, channel: str, action: str, details: str):
    """Append to Activity Log sheet and update Master Lead List"""
    sheets_api.append("Activity Log", {
        "timestamp": datetime.now().isoformat(),
        "lead_id": lead_id,
        "channel": channel,
        "action": action,
        "details": details
    })

    # Update last contacted date and status
    sheets_api.update("Master Leads", lead_id, {
        "last_contacted": datetime.now().isoformat(),
        "next_follow_up": calculate_next_followup(action)
    })
```

---

## 8. Phase 6 — Analytics & Optimization

### 8.1 Key Metrics to Track

| Metric | Target | Frequency |
|--------|--------|-----------|
| Leads discovered/week | 50-100 | Weekly |
| Emails sent/day | 30-50 | Daily |
| Email open rate | >40% | Weekly |
| Email reply rate | >5% | Weekly |
| LinkedIn connection acceptance | >30% | Weekly |
| LinkedIn reply rate | >10% | Weekly |
| Meetings booked/week | 3-5 | Weekly |
| Meeting → Proposal rate | >40% | Monthly |
| Proposal → Close rate | >25% | Monthly |
| Cost per meeting | <$50 | Monthly |
| Pipeline value | Growing MoM | Monthly |

### 8.2 Weekly AI Analysis Report

```python
def generate_weekly_report():
    metrics = crm.get_weekly_metrics()
    prompt = f"""
    Analyze this week's sales pipeline performance for AnalyticsGear:

    {json.dumps(metrics, indent=2)}

    Generate:
    1. Executive summary (3 sentences)
    2. What's working (top performing channels, messages, industries)
    3. What's not working (low engagement areas)
    4. Specific recommendations for next week
    5. A/B test suggestions for email subject lines or messaging
    """
    report = call_claude_api(prompt)
    send_to_slack(report)  # or email to founders
```

---

## 9. Tech Stack & Tools

### 9.1 Recommended Stack

```
┌─────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                 │
│            Python + Cron / Prefect / n8n             │
├──────────┬──────────┬──────────┬────────────────────┤
│PROSPECTING│ENRICHMENT│ OUTREACH │    CRM/LOGGING     │
├──────────┼──────────┼──────────┼────────────────────┤
│Apollo.io  │Clearbit  │Instantly │Google Sheets       │
│LinkedIn   │Hunter.io │Phantombus│  (→ HubSpot Free)  │
│Apify      │Claude API│ter      │Google Apps Script   │
│Job scraper│Crunchbase│SendGrid  │                    │
│           │          │JustCall  │                    │
├──────────┴──────────┴──────────┴────────────────────┤
│                    AI LAYER                           │
│              Claude API (Anthropic)                   │
│   Lead scoring, email generation, reply handling,    │
│   call briefs, weekly analysis, A/B copy generation  │
└─────────────────────────────────────────────────────┘
```

### 9.2 Tool-by-Tool Breakdown

| Category | Tool | Purpose | Cost |
|----------|------|---------|------|
| **Orchestration** | Python + cron | Run daily pipeline scripts | Free |
| **Orchestration** | n8n (self-hosted) or Prefect | Visual workflow, error handling | Free (self-host) |
| **Prospecting** | Apollo.io | Lead database + emails + enrichment | $49/mo (Basic) |
| **Prospecting** | Apify | Web scraping (LinkedIn, job boards) | $49/mo |
| **Prospecting** | LinkedIn Sales Navigator | Advanced lead search | $80/mo |
| **Email** | Instantly.ai | Cold email sending + warmup | $30/mo |
| **Email** | Mailgun / SendGrid | Transactional email + tracking | Free tier |
| **LinkedIn** | Phantombuster | LinkedIn automation | $56/mo |
| **AI** | Claude API (Anthropic) | Personalization, scoring, analysis | ~$30-50/mo |
| **CRM** | Google Sheets | Lead tracking, logging | Free |
| **Phone** | JustCall / Twilio | Call scheduling, auto-dial | $19/mo |
| **Monitoring** | Google Analytics | Website visitor tracking | Free |
| **Domain** | Separate cold email domain | Protect main domain reputation | $12/yr |

**Estimated total: $350-450/month** (vs. $3,000-5,000/month for a junior sales hire)

---

## 10. Daily Automation Schedule

```
┌────────────────────────────────────────────────────────────────┐
│  DAILY PIPELINE SCHEDULE (Auto-runs via cron / task scheduler) │
├────────┬───────────────────────────────────────────────────────┤
│  TIME  │  TASK                                                 │
├────────┼───────────────────────────────────────────────────────┤
│ 06:00  │ PROSPECTING: Run lead discovery scripts               │
│        │ - Apollo.io API search                                │
│        │ - LinkedIn Sales Navigator export                     │
│        │ - Job board scraping                                  │
│        │ - Deduplicate against existing CRM                    │
├────────┼───────────────────────────────────────────────────────┤
│ 07:00  │ ENRICHMENT: Enrich new leads                          │
│        │ - Verify emails (Hunter.io)                           │
│        │ - Gather company data (Clearbit)                      │
│        │ - AI lead scoring (Claude API)                        │
│        │ - Assign tiers (HOT/WARM/COLD)                        │
├────────┼───────────────────────────────────────────────────────┤
│ 08:00  │ OUTREACH: Execute outreach sequences                  │
│        │ - Generate personalized emails (Claude API)           │
│        │ - Send cold emails (Instantly.ai)                     │
│        │ - Send LinkedIn connection requests (Phantombuster)   │
│        │ - Generate call briefs for phone block                │
├────────┼───────────────────────────────────────────────────────┤
│ 09:00  │ FOLLOW-UP: Process engagement signals                 │
│        │ - Check email opens/clicks/replies                    │
│        │ - Check LinkedIn acceptances/messages                 │
│        │ - Trigger follow-up sequences                         │
│        │ - AI-classify and draft replies to responses          │
├────────┼───────────────────────────────────────────────────────┤
│ 09:30  │ LOGGING: Update CRM                                   │
│        │ - Log all activities to Google Sheets                 │
│        │ - Update lead statuses                                │
│        │ - Calculate next follow-up dates                      │
├────────┼───────────────────────────────────────────────────────┤
│ 10:00  │ HUMAN REVIEW (15-30 mins)                             │
│        │ - Review AI-drafted replies before sending            │
│        │ - Make cold calls from generated call briefs          │
│        │ - Approve/modify outreach for HOT leads               │
├────────┼───────────────────────────────────────────────────────┤
│ 18:00  │ DAILY SUMMARY: AI generates end-of-day report         │
│        │ - Leads discovered, contacted, replied                │
│        │ - Meetings booked                                     │
│        │ - Tomorrow's priority actions                         │
└────────┴───────────────────────────────────────────────────────┘
```

---

## 11. Implementation Roadmap

### Week 1-2: Foundation

- [ ] Set up separate cold outreach domain (e.g., `outreach.analyticsgear.com`)
- [ ] Configure SPF, DKIM, DMARC for email deliverability
- [ ] Create Apollo.io account, configure ICP filters
- [ ] Set up Instantly.ai, begin email warmup (takes 2-3 weeks)
- [ ] Create Google Sheets CRM with schema from Section 7.2
- [ ] Set up Claude API key, test lead scoring prompts
- [ ] Write core Python scripts: prospecting, enrichment, scoring
- [ ] Define ICP and build target company list (200 companies)

### Week 3-4: Build Outreach Engine

- [ ] Write email generation prompts, test with 10 sample leads
- [ ] Set up Phantombuster for LinkedIn automation
- [ ] Build email sequence templates (HOT, WARM, COLD)
- [ ] Build LinkedIn sequence automation
- [ ] Write activity logging scripts → Google Sheets
- [ ] Create daily summary report generator
- [ ] Set up cron jobs for daily pipeline execution
- [ ] Test full pipeline end-to-end with 20 real leads

### Week 5-6: Launch & Iterate

- [ ] Begin sending cold emails (start at 10/day, ramp to 50/day)
- [ ] Begin LinkedIn outreach (10-20 connections/day)
- [ ] Monitor deliverability, open rates, reply rates
- [ ] Set up cold calling workflow with JustCall
- [ ] Start making 5-10 calls/day using AI call briefs
- [ ] Review and respond to replies daily
- [ ] Iterate on email copy based on performance

### Week 7-8: Optimize & Scale

- [ ] Analyze first month's data: what channels/messages work
- [ ] A/B test subject lines, email copy, LinkedIn messages
- [ ] Refine ICP based on actual engagement data
- [ ] Add new lead sources (events, social listening, intent data)
- [ ] Build monthly nurture campaign for non-responders
- [ ] Consider migrating to HubSpot Free CRM if volume grows
- [ ] Document SOPs for any manual steps

### Ongoing (Month 3+)

- [ ] Weekly: Review pipeline metrics, adjust targeting
- [ ] Monthly: AI-generated performance report + strategy recommendations
- [ ] Quarterly: Full pipeline audit, add new channels or sources
- [ ] Continuous: Improve AI prompts based on what converts

---

## 12. Cost Estimates

### Monthly Operating Costs

| Item | Cost/Month | Notes |
|------|-----------|-------|
| Apollo.io (Basic) | $49 | Lead database + email finder |
| Instantly.ai | $30 | Cold email platform + warmup |
| LinkedIn Sales Navigator | $80 | Advanced search |
| Phantombuster | $56 | LinkedIn automation |
| Claude API | $30-50 | ~100K tokens/day for personalization |
| JustCall (Essentials) | $19 | Cold calling |
| Apify (Starter) | $49 | Web scraping |
| Cold outreach domain | $1 | ~$12/year |
| **Total** | **$314-334/mo** | |

### Comparison: AI Pipeline vs. Sales Hire

| | AI Pipeline | Junior SDR Hire |
|-|------------|----------------|
| Monthly cost | ~$350 | $3,000-5,000 |
| Works 24/7 | Yes (scheduled) | No |
| Scales instantly | Add more accounts | Hire more people |
| Consistent quality | Yes | Variable |
| Personal touch | Lower (needs human review) | Higher |
| Relationship building | Limited | Strong |
| Annual cost | ~$4,200 | $36,000-60,000 |

**The AI pipeline costs ~90% less** and handles 80% of a sales person's tasks. The remaining 20% (calls, relationship building, closing) requires 30-60 minutes of founder time per day.

---

## 13. Risk Mitigation & Compliance

### 13.1 Email Compliance

- **CAN-SPAM (US):** Include unsubscribe link, physical address, no deceptive subjects
- **GDPR (EU):** Legitimate interest basis for B2B outreach, honor opt-outs within 30 days
- **CASL (Canada):** Requires implied or express consent — be cautious with Canadian leads
- **Best practice:** Include an easy opt-out in every email, honor immediately

### 13.2 LinkedIn Compliance

- **Daily limits:** Max 20-25 connection requests/day to avoid account restrictions
- **No automation detection:** Use human-like delays (random intervals between actions)
- **Profile quality:** Keep LinkedIn profile professional and complete
- **Fallback:** If automation gets restricted, switch to manual + AI-assisted approach

### 13.3 Reputation Protection

- **Use separate domain** for cold outreach to protect `analyticsgear.com` reputation
- **Monitor bounce rates** — remove invalid emails immediately
- **Warm up email accounts** for 2-3 weeks before sending at volume
- **Check blacklists** weekly (MXToolbox, Spamhaus)

### 13.4 Data Storage & Privacy

- Don't store sensitive personal data beyond what's needed for outreach
- Regular cleanup of old/unresponsive leads (90-day retention for non-engaged)
- Secure access to Google Sheets (limited to team members)

---

## 14. Appendix — Prompt Templates & Scripts

### A. Cold Email Templates

#### Template 1: Pain-Point Hook (Data Engineering)

```
Subject: {company}'s data stack

Hi {first_name},

Noticed {company} is hiring for data engineering roles — usually
means the pipeline backlog is growing faster than the team.

We've helped {similar_company_in_their_industry} clear a 6-month
backlog in 8 weeks by embedding senior data engineers alongside
their team (Snowflake + dbt + Airflow).

If the data engineering bottleneck is real, happy to share what
worked for them — 15 minutes, no pitch.

Best,
{sender_name}
AnalyticsGear
```

#### Template 2: Tech-Stack Specific (Snowflake/Databricks)

```
Subject: quick question about {tech_platform} at {company}

Hi {first_name},

Saw that {company} is running on {tech_platform}. We specialize in
optimizing {tech_platform} deployments — things like query cost
reduction, pipeline reliability, and proper data modeling.

One client cut their {tech_platform} spend by 40% after we
restructured their warehouse — took 4 weeks.

Worth a quick chat to see if there's a similar opportunity?

{sender_name}
```

#### Template 3: Industry-Specific (Banking/Finance)

```
Subject: data compliance at {company}

Hi {first_name},

Data teams in banking are dealing with a unique headache right
now — regulatory pressure to implement data lineage and quality
frameworks, while also shipping analytics faster.

We've worked with financial services firms to build compliant data
platforms that don't slow teams down. Happy to share the playbook
if that resonates.

{sender_name}
AnalyticsGear
```

### B. LinkedIn Message Templates

#### Connection Accepted — Intro Message

```
Thanks for connecting, {first_name}!

I work with {industry} companies on their data and AI platforms.
Your team's work at {company} caught my eye — particularly
{specific_detail}.

Would love to hear how you're thinking about {relevant_topic}
on your end. No pitch, genuinely curious.
```

#### Follow-Up After No Response

```
Hi {first_name} — don't want to be that person who sends
five follow-ups. Just wanted to share this quick read our
team published on {relevant_topic}:

{blog_link}

Thought it might be relevant given what {company} is building.
Either way, great to be connected.
```

### C. Project Directory Structure

```
sales_pipeline/
├── AI_SALES_PIPELINE_BLUEPRINT.md    ← This document
├── config/
│   ├── icp_config.yaml               ← ICP criteria, target roles, industries
│   ├── email_sequences.yaml          ← Email sequence definitions
│   ├── linkedin_sequences.yaml       ← LinkedIn sequence definitions
│   └── scoring_criteria.yaml         ← Lead scoring weights
├── scripts/
│   ├── 01_prospecting/
│   │   ├── apollo_search.py          ← Apollo.io API lead search
│   │   ├── linkedin_scraper.py       ← LinkedIn lead extraction
│   │   ├── job_board_scraper.py      ← Job posting intent signals
│   │   └── deduplicator.py           ← Cross-source deduplication
│   ├── 02_enrichment/
│   │   ├── email_verifier.py         ← Hunter.io email verification
│   │   ├── company_enricher.py       ← Clearbit/Apollo enrichment
│   │   └── ai_lead_scorer.py         ← Claude API lead scoring
│   ├── 03_outreach/
│   │   ├── email_generator.py        ← AI personalized email generation
│   │   ├── email_sender.py           ← Instantly.ai / SendGrid integration
│   │   ├── linkedin_automator.py     ← Phantombuster LinkedIn sequences
│   │   └── call_brief_generator.py   ← AI cold call brief generation
│   ├── 04_followup/
│   │   ├── engagement_tracker.py     ← Monitor opens, clicks, replies
│   │   ├── reply_classifier.py       ← AI reply classification + drafting
│   │   └── sequence_manager.py       ← Manage multi-step sequences
│   ├── 05_crm/
│   │   ├── sheets_logger.py          ← Google Sheets CRM logging
│   │   ├── status_updater.py         ← Update lead statuses
│   │   └── report_generator.py       ← Daily/weekly AI reports
│   └── orchestrator.py               ← Main pipeline runner (cron entry)
├── prompts/
│   ├── lead_scoring.txt              ← Lead scoring prompt template
│   ├── email_generation.txt          ← Email generation prompt template
│   ├── reply_classification.txt      ← Reply handling prompt template
│   ├── call_brief.txt                ← Call brief prompt template
│   └── weekly_report.txt             ← Weekly analysis prompt template
├── templates/
│   ├── email_templates/              ← Pre-built email templates by industry
│   └── linkedin_templates/           ← Pre-built LinkedIn message templates
├── data/
│   ├── target_companies.csv          ← Curated target company list
│   └── exclusion_list.csv            ← Companies/domains to never contact
├── .env                              ← API keys (Apollo, Claude, Hunter, etc.)
├── requirements.txt                  ← Python dependencies
└── README.md                         ← Setup and deployment instructions
```

---

## Quick Start Checklist

1. **Today:** Sign up for Apollo.io (free trial), Instantly.ai, Claude API
2. **This week:** Buy cold outreach domain, set up DNS (SPF/DKIM/DMARC), start email warmup
3. **This week:** Build Google Sheets CRM from Section 7.2 schema
4. **Week 2:** Write first Python scripts (prospecting + scoring)
5. **Week 2:** Generate first batch of 50 leads, score them, review quality
6. **Week 3:** Send first 10 cold emails (manually review AI-generated copy)
7. **Week 3:** Begin LinkedIn outreach (10 connections/day)
8. **Week 4:** Automate with cron, begin daily pipeline runs
9. **Month 2:** Optimize based on data — what's getting replies?
10. **Month 3:** Full autopilot with 30-minute daily founder review

---

*This blueprint was designed for AnalyticsGear's specific services, ICP, and growth stage. The pipeline should be treated as a living system — continuously improved based on real engagement data.*
