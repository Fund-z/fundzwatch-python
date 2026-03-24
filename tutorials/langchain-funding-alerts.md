---
title: "Real-Time Funding Alerts with LangChain + FundzWatch"
published: true
description: "What if your Slack bot could tell you every time a competitor raised funding? Let's build that."
tags: langchain, python, slack, funding, ai-agents
cover_image: ""
canonical_url: ""
---

# Real-Time Funding Alerts with LangChain + FundzWatch

What if your Slack bot could tell you every time a competitor raised funding? Or alert you when a prospect in your pipeline just hired a new VP of Engineering?

We're going to build that. A LangChain agent that monitors business events from FundzWatch, formats them into actionable intelligence, and posts them to Slack. The whole thing is about 80 lines of Python.

## What We're Building

A Python script that:

1. Queries the FundzWatch API for the latest funding rounds, acquisitions, and executive hires
2. Uses a LangChain agent to analyze and summarize those events
3. Posts formatted alerts to a Slack channel via webhook

You can run it manually, on a cron, or as part of a larger pipeline.

## Prerequisites

- Python 3.9+
- A FundzWatch API key ([get one free](https://fundzwatch.ai/onboarding))
- An Anthropic or OpenAI API key (for the LLM)
- A Slack webhook URL ([create one here](https://api.slack.com/messaging/webhooks))

## Step 1: Install

```bash
pip install fundzwatch[langchain] langchain-anthropic httpx
```

If you prefer OpenAI:

```bash
pip install fundzwatch[langchain] langchain-openai httpx
```

## Step 2: Set Environment Variables

```bash
export FUNDZWATCH_API_KEY="fundz_live_your_key_here"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T00/B00/xxxx"
```

## Step 3: Build the Agent

Create `funding_alerts.py`:

```python
import os
import json
import httpx
from fundzwatch import FundzWatch
from fundzwatch.tools.langchain import get_fundzwatch_tools
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# ── Config ───────────────────────────────────────────────────────────
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL")
INDUSTRIES_TO_WATCH = ["SaaS", "FinTech", "HealthTech", "AI"]
DAYS_LOOKBACK = 1  # check daily

# ── Initialize ───────────────────────────────────────────────────────
fw = FundzWatch()
tools = get_fundzwatch_tools(fw)
llm = ChatAnthropic(model="claude-sonnet-4-20250514")

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a business intelligence analyst. You monitor real-time "
     "business events and produce concise Slack-ready summaries. "
     "Format output using Slack mrkdwn syntax: *bold*, _italic_, "
     "and use bullet points. Keep summaries actionable -- tell the "
     "reader what they should DO with this information."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def build_query(industries: list[str], days: int) -> str:
    """Build the agent query string."""
    industry_str = ", ".join(industries)
    return (
        f"Get business events from the last {days} day(s). "
        f"Focus on these industries: {industry_str}. "
        f"Include funding rounds, acquisitions, and executive hires.\n\n"
        f"Then format them as a Slack-ready briefing with these sections:\n"
        f"1. *Funding Rounds* -- list each with company, amount, series\n"
        f"2. *Acquisitions* -- who acquired who and why it matters\n"
        f"3. *Executive Moves* -- new hires that signal buying intent\n"
        f"4. *Action Items* -- 2-3 specific things our sales team should do today\n\n"
        f"Skip any section that has zero events. Be concise."
    )


def post_to_slack(text: str) -> None:
    """Post a message to Slack via webhook."""
    if not SLACK_WEBHOOK:
        print("No SLACK_WEBHOOK_URL set. Printing to stdout instead:\n")
        print(text)
        return

    response = httpx.post(
        SLACK_WEBHOOK,
        json={"text": text},
        headers={"Content-Type": "application/json"},
    )
    if response.status_code == 200:
        print("Posted to Slack.")
    else:
        print(f"Slack error {response.status_code}: {response.text}")


# ── Run ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    query = build_query(INDUSTRIES_TO_WATCH, DAYS_LOOKBACK)
    result = executor.invoke({"input": query})
    output = result["output"]

    # Add a header
    slack_message = (
        ":newspaper: *Daily Business Intelligence Briefing*\n"
        f"_{DAYS_LOOKBACK}-day lookback | "
        f"{', '.join(INDUSTRIES_TO_WATCH)}_\n\n"
        f"{output}"
    )

    post_to_slack(slack_message)
```

## Step 4: Run It

```bash
python funding_alerts.py
```

## What the Output Looks Like

Here's a real example of what the agent produces. The LangChain agent calls `fundzwatch_events` behind the scenes and gets back raw event data, then formats it:

```
:newspaper: Daily Business Intelligence Briefing
1-day lookback | SaaS, FinTech, HealthTech, AI

*Funding Rounds*
- *Wiz* raised $300M Series D -- cloud security, post-money valuation ~$10B.
  They'll be hiring aggressively and evaluating new vendor contracts.
- *Ramp* raised $150M Series C -- corporate cards & expense management.
  New CFO starts next month, expect budget re-evaluation across all tools.
- *Abridge* raised $75M Series C -- AI medical documentation.
  Expanding from hospitals into private practice. New territory = new tooling needs.

*Executive Moves*
- *Notion* hired VP Enterprise Sales from Salesforce.
  Signal: they're moving upmarket hard. Enterprise deals need enterprise integrations.
- *Linear* hired Head of Revenue from Datadog.
  Signal: transitioning from PLG to sales-led. They'll need outbound tooling.

*Action Items*
1. Reach out to Ramp -- new CFO = fresh budget review. Reference the raise.
2. Add Notion to watchlist -- enterprise push means they'll evaluate vendors in the next 90 days.
3. Check if Wiz is on our target account list. $300M raise means they're spending.
```

That's what lands in your Slack channel. Every morning. Automatically.

## Adding Watchlist Monitoring

Want to track specific companies? The FundzWatch tools include a watchlist manager. Add this before the main query:

```python
# Track your competitors and key prospects
setup_query = (
    "Add these companies to my watchlist: "
    "salesforce.com, hubspot.com, gong.io, outreach.io, zoominfo.com. "
    "Then check if any of them had events in the last 7 days. "
    "If so, format as a separate *Competitor Watch* section."
)

watchlist_result = executor.invoke({"input": setup_query})
competitor_section = watchlist_result["output"]
```

Then append it to your Slack message:

```python
slack_message = (
    ":newspaper: *Daily Business Intelligence Briefing*\n\n"
    f"{output}\n\n"
    f"---\n\n"
    f":eyes: *Competitor Watch*\n{competitor_section}"
)
```

## Running on a Schedule

### Option A: Cron (Linux/Mac)

```bash
crontab -e
```

```cron
# Run at 8:00 AM ET every weekday
0 8 * * 1-5 cd /path/to/project && /path/to/python funding_alerts.py
```

### Option B: GitHub Actions (free)

```yaml
# .github/workflows/funding-alerts.yml
name: Daily Funding Alerts
on:
  schedule:
    - cron: '0 12 * * 1-5'  # 12:00 UTC = 8:00 AM ET
  workflow_dispatch:  # manual trigger

jobs:
  alert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install fundzwatch[langchain] langchain-anthropic httpx
      - run: python funding_alerts.py
        env:
          FUNDZWATCH_API_KEY: ${{ secrets.FUNDZWATCH_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Using the SDK Directly (Without LangChain)

If you don't need the LLM analysis and just want raw event data pushed to Slack, you can skip LangChain entirely:

```python
import os
import httpx
from fundzwatch import FundzWatch

fw = FundzWatch()
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK_URL"]

# Pull today's funding rounds
events = fw.get_events(types="funding", days=1, limit=20)

if not events["events"]:
    print("No funding events today.")
    exit()

lines = [":moneybag: *Today's Funding Rounds*\n"]
for e in events["events"]:
    amount = f"${e['amount'] / 1_000_000:.1f}M" if e.get("amount") else "undisclosed"
    series = f" ({e['series']})" if e.get("series") else ""
    lines.append(f"- *{e['title']}*{series} -- {amount}")

lines.append(f"\n_{events['total']} total events today_")

httpx.post(SLACK_WEBHOOK, json={"text": "\n".join(lines)})
```

That's 20 lines. No LLM costs, no agent overhead. Just data into Slack.

## The Full LangChain Tool Set

The FundzWatch LangChain integration provides four tools:

| Tool Name | What It Does |
|-----------|-------------|
| `fundzwatch_scored_leads` | AI-scored leads with buyer intent, buying stage, outreach angle |
| `fundzwatch_events` | Funding, acquisitions, hires, contracts, product launches |
| `fundzwatch_market_pulse` | 7-day/30-day market totals, largest rounds |
| `fundzwatch_watchlist` | Add/remove/list tracked companies |

The agent decides which tools to call based on your prompt. Ask it "who raised funding this week?" and it'll call `fundzwatch_events`. Ask it "who should I sell to right now?" and it'll call `fundzwatch_scored_leads`.

## Get Your API Key

Free tier: 100 API calls/month, no credit card.

**[Get a free API key at fundzwatch.ai/onboarding](https://fundzwatch.ai/onboarding)**

```bash
pip install fundzwatch[langchain]
```

Source: [github.com/fundz/fundzwatch-python](https://github.com/fundz/fundzwatch-python)

---

*If you build something with this, I'd like to hear about it. Drop a comment or find me on Twitter.*
