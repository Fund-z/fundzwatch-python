---
title: "Build an AI SDR Agent with CrewAI + FundzWatch in 15 Minutes"
published: true
description: "Your AI agent is only as good as its data. Here's how to give it real-time funding rounds, buyer intent scores, and outreach angles."
tags: ai, crewai, sales, automation, python
cover_image: ""
canonical_url: ""
---

# Build an AI SDR Agent with CrewAI + FundzWatch in 15 Minutes

Your AI agent is only as good as its data. You can build the most sophisticated CrewAI pipeline in the world, but if it's working off stale CSVs or generic web scrapes, the output is useless.

Here's how to give your AI SDR agent real-time funding rounds, buyer intent scores, and personalized outreach angles -- in about 15 minutes.

## What We're Building

A CrewAI crew with two agents:

1. **Research Agent** -- pulls live business events and AI-scored leads from the FundzWatch API
2. **Outreach Agent** -- takes those leads and writes personalized cold emails using the intent signals

The end result: you run one command and get a batch of targeted, personalized outreach emails for companies that just raised funding, hired new executives, or hit other buying triggers.

## Prerequisites

- Python 3.9+
- A FundzWatch API key ([get one free here](https://fundzwatch.ai/onboarding) -- no credit card)
- An OpenAI API key (for CrewAI's LLM calls)

## Step 1: Install Dependencies

```bash
pip install fundzwatch[crewai] crewai crewai-tools
```

This installs the FundzWatch SDK with CrewAI tool bindings, plus CrewAI itself.

## Step 2: Set Your API Keys

```bash
export FUNDZWATCH_API_KEY="fundz_live_your_key_here"
export OPENAI_API_KEY="sk-your-openai-key-here"
```

## Step 3: Build the Crew

Create a file called `ai_sdr.py`:

```python
import os
import json
from fundzwatch import FundzWatch
from fundzwatch.tools.crewai import get_fundzwatch_tools
from crewai import Agent, Task, Crew, Process

# ── Initialize FundzWatch ────────────────────────────────────────────
fw = FundzWatch()  # reads FUNDZWATCH_API_KEY from env
tools = get_fundzwatch_tools(fw)

# ── Agent 1: Research Agent ──────────────────────────────────────────
researcher = Agent(
    role="Sales Intelligence Researcher",
    goal=(
        "Find companies that are actively in a buying cycle right now. "
        "Focus on companies with a buyer intent score above 60, recent "
        "funding rounds, or new executive hires. Return structured data "
        "including company name, score, buying stage, and pain points."
    ),
    backstory=(
        "You are a senior sales researcher at a B2B SaaS company. "
        "You have access to real-time business event data and AI-scored "
        "lead intelligence. You know that the best time to reach out is "
        "right after a funding round or leadership change."
    ),
    tools=tools,
    verbose=True,
)

# ── Agent 2: Outreach Writer ────────────────────────────────────────
writer = Agent(
    role="SDR Outreach Specialist",
    goal=(
        "Write personalized cold emails for each lead. Each email must "
        "reference a specific, real event (the funding round, the new "
        "hire, the product launch). Never write generic emails. Each "
        "email should be under 120 words."
    ),
    backstory=(
        "You are an elite SDR who consistently books 3x more meetings "
        "than your peers. Your secret: you never send a cold email that "
        "doesn't reference something specific about the prospect's "
        "company. You write short, direct emails with exactly one CTA."
    ),
    verbose=True,
)

# ── Task 1: Find High-Intent Leads ──────────────────────────────────
research_task = Task(
    description=(
        "Find the top 5 companies most likely to buy right now.\n\n"
        "1. Use get_scored_leads with min_score=60 and max_results=10\n"
        "2. Use get_business_events with types='funding,hiring' and days=7\n"
        "3. Cross-reference: prioritize leads that also have recent events\n"
        "4. For each lead, note the company name, score, buying stage, "
        "pain point, outreach angle, and the specific triggering event.\n\n"
        "Return a structured list of exactly 5 leads."
    ),
    expected_output=(
        "A numbered list of 5 leads, each with:\n"
        "- Company name and domain\n"
        "- Buyer intent score\n"
        "- Buying stage\n"
        "- Triggering event (funding round, exec hire, etc.)\n"
        "- Recommended outreach angle"
    ),
    agent=researcher,
)

# ── Task 2: Write Outreach Emails ───────────────────────────────────
outreach_task = Task(
    description=(
        "Using the research from the previous task, write a personalized "
        "cold email for each of the 5 leads.\n\n"
        "Rules:\n"
        "- Subject line under 8 words\n"
        "- Email body under 120 words\n"
        "- Must reference the specific triggering event by name\n"
        "- One clear CTA (15-min call, not a demo)\n"
        "- No fluff, no 'I hope this finds you well'\n"
        "- Tone: peer-to-peer, not salesy"
    ),
    expected_output=(
        "5 complete cold emails, each with:\n"
        "- Subject line\n"
        "- Email body\n"
        "- The lead info it was based on"
    ),
    agent=writer,
)

# ── Run the Crew ────────────────────────────────────────────────────
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, outreach_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()

print("\n" + "=" * 60)
print("AI SDR OUTPUT")
print("=" * 60)
print(result)
```

## Step 4: Run It

```bash
python ai_sdr.py
```

## What Happens Under the Hood

When the crew runs, here's the actual flow:

1. The Research Agent calls `get_scored_leads` via the FundzWatch API. This returns leads like:

```
Found 10 leads:
- Vanta (Score: 87/100, Stage: Active Evaluation): Reference their Series B
  and growing compliance team to position your security automation product
- Ramp (Score: 82/100, Stage: Decision): Their recent CFO hire signals
  budget process changes -- perfect timing for financial tooling
- Deel (Score: 78/100, Stage: Research): International expansion after
  Series D means they need localized infrastructure
```

2. The Research Agent then calls `get_business_events` to pull the last 7 days of funding and hiring events:

```
47 events found:
- [FUNDING] Vanta raises $150M Series C ($150.0M)
- [HIRING] Ramp hires new CFO from Goldman Sachs
- [FUNDING] Deel raises $425M Series D ($425.0M)
- [HIRING] Notion hires VP of Enterprise Sales
- [FUNDING] Wiz raises $300M Series D ($300.0M)
```

3. The Research Agent cross-references these, picking leads where intent score AND a fresh event line up.

4. The Outreach Writer takes those 5 leads and produces emails like:

```
Subject: Congrats on the Series C

Hi Sarah,

Saw Vanta just closed the $150M Series C -- congrats. That kind of
growth usually means the compliance surface area expands faster than
the team can keep up.

We help companies at your stage automate SOC 2 evidence collection
so your security team can focus on actual threats instead of
screenshot requests.

Worth a 15-min call next week to see if it fits?

Best,
[Your name]
```

That email works because it references a real event that happened this week. Not "I noticed your company is growing" -- a specific dollar amount, a specific round.

## Extending This

**Add a market pulse check.** Before researching leads, have the agent call `get_market_pulse` to understand the macro environment:

```python
context_task = Task(
    description=(
        "Get the current market pulse. How many funding rounds happened "
        "this week? Any large acquisitions? Use this context to inform "
        "which industries to focus on."
    ),
    expected_output="A brief market summary with focus areas.",
    agent=researcher,
)
```

**Track your target accounts.** Use the watchlist tool to monitor specific competitors or prospects:

```python
# In your research task description, add:
"First, add these domains to the watchlist: stripe.com, notion.so, "
"linear.app. Then check get_watchlist_events to see if any of them "
"had events this week."
```

**Run it on a cron.** Wrap the script, pipe the output to a Slack webhook, and run it every morning at 8am. Your SDR team gets a fresh batch of personalized outreach every day before they sit down.

## The Full API Surface

The FundzWatch CrewAI integration gives your agents four tools:

| Tool | What It Does |
|------|-------------|
| `get_scored_leads` | AI-scored leads with intent signals, buying stage, and outreach angles |
| `get_business_events` | Real-time funding, acquisitions, hires, contracts, product launches |
| `get_market_pulse` | 7-day and 30-day market activity totals and largest rounds |
| `manage_watchlist` | Track specific companies and get alerts on their events |

## Get Your API Key

FundzWatch has a free tier -- 100 API calls/month, no credit card required.

**[Get a free API key at fundzwatch.ai/onboarding](https://fundzwatch.ai/onboarding)**

The SDK is open source: [github.com/fundz/fundzwatch-python](https://github.com/fundz/fundzwatch-python)

```bash
pip install fundzwatch[crewai]
```

---

*Built something cool with FundzWatch + CrewAI? Drop a link in the comments. I'd like to see what people build with live business event data in their agent pipelines.*
