# FundzWatch dev.to Posts

---

## Post 1: I Built a Free Alternative to ZoomInfo's API for AI Agents

```yaml
---
title: I Built a Free Alternative to ZoomInfo's API for AI Agents
published: true
tags: python, ai, salestech, api
cover_image: # add a relevant image URL
canonical_url: https://fundzwatch.ai/blog/free-alternative-zoominfo-api
---
```

If you've ever tried to add real-time business intelligence to an AI agent, you've probably hit the same wall I did: enterprise APIs cost a fortune and aren't designed for the way developers actually build today.

ZoomInfo: $15K-30K/year, requires a sales call to even see pricing.
Crunchbase Enterprise API: $10K+/year, rate limits that don't work for agents.
PitchBook: $20K+/year, gated behind institutional access.

I needed something different. A developer-first API that gives AI agents access to real-time business events -- funding rounds, acquisitions, executive hires, contracts -- with actual AI scoring on top. And ideally, a free tier that's actually useful.

So we built FundzWatch.

### What it does

FundzWatch indexes 50M+ business events going back to 2017. The API returns structured JSON for:

- **Funding rounds** -- amount, stage, investors, date
- **Acquisitions** -- acquirer, target, terms
- **Executive moves** -- person, role, company
- **Government contracts** -- agency, value, awardee
- **Product launches** -- company, product, category

On top of the raw events, there's an AI scoring engine that analyzes signals and returns buyer intent scores (0-100), buying stages, inferred pain points, and specific outreach angles.

### The pricing comparison

| Feature | ZoomInfo | Crunchbase Enterprise | FundzWatch Free | FundzWatch Pro |
|---------|----------|-----------------------|-----------------|----------------|
| Annual cost | $15K-30K | $10K+ | $0 | $588/yr |
| API calls | Varies | Varies | 1,000/mo | 10,000/mo |
| AI scoring | No | No | Yes | Yes |
| Buyer intent | Pageview-based | No | Event-based | Event-based |
| MCP server | No | No | Yes | Yes |
| CrewAI/LangChain tools | No | No | Yes | Yes |
| Credit card required | Yes | Yes | No | Yes |
| Sales call required | Yes | Yes | No | No |
| Event types | Limited | Funding only | 5 types | 5 types |
| Historical data | Varies | 2013+ | 2017+ | 2017+ |

### Python SDK

```bash
pip install fundzwatch
```

```python
from fundzwatch import FundzWatch

fw = FundzWatch()  # uses FUNDZWATCH_API_KEY env var

# Get AI-scored leads
leads = fw.get_leads(min_score=60, max_results=10)
for lead in leads["signals"]:
    print(f"{lead['company_name']}: {lead['score']}/100")
    print(f"  Buying stage: {lead['buying_stage']}")
    print(f"  Outreach angle: {lead['outreach_angle']}")

# Get raw events
events = fw.get_events(types="funding", days=7)
for event in events["events"]:
    print(f"[{event['type']}] {event['title']}")

# Market overview
pulse = fw.get_market_pulse()
p = pulse["pulse"]
print(f"This week: {p['funding']['count_7d']} rounds, "
      f"${p['funding']['total_raised_7d'] / 1_000_000:.0f}M raised")
```

### MCP Server (for Claude Desktop, Cursor, etc.)

If you use Claude Desktop or any MCP-compatible client, you can give your AI assistant direct access to FundzWatch data. No code needed.

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fundzwatch": {
      "command": "npx",
      "args": ["-y", "@fundzwatch/mcp-server"],
      "env": {
        "FUNDZWATCH_API_KEY": "your_key_here"
      }
    }
  }
}
```

Then just ask Claude: "Who raised a Series B this week?" and get real, accurate answers from live data.

### CrewAI Integration

```python
from fundzwatch import FundzWatch
from fundzwatch.tools.crewai import get_fundzwatch_tools
from crewai import Agent, Task, Crew

fw = FundzWatch()
tools = get_fundzwatch_tools(fw)

researcher = Agent(
    role="Sales Intelligence Analyst",
    goal="Find high-intent companies that match our ICP",
    tools=tools,
)

task = Task(
    description="Find the top 10 companies most likely to buy right now. "
    "Focus on recent funding or leadership changes, score above 60.",
    expected_output="Ranked list with scores, stages, and outreach angles.",
    agent=researcher,
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
print(result)
```

The SDK also includes LangChain tool integrations (`pip install fundzwatch[langchain]`).

### REST API

If you're not using Python, the REST API works with anything:

```bash
# Get funding events from the last 7 days
curl https://api.fundz.net/v1/watch/events?types=funding&days=7 \
  -H "Authorization: Bearer YOUR_API_KEY"

# Get AI-scored leads
curl -X POST https://api.fundz.net/v1/watch/signals \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"min_score": 60, "max_results": 10}'
```

### Why I built this

Most business intelligence APIs were designed for enterprise sales teams with big budgets and long procurement cycles. They don't work well for:

- **AI agents** that need structured, real-time data via simple API calls
- **Solo developers** who can't justify $10K+/year for business data
- **Startups** that need sales intelligence but aren't enterprise-scale yet

FundzWatch is built API-first for the AI agent era. The MCP server, CrewAI tools, and LangChain integrations exist because that's how developers are actually building sales intelligence today.

### Get started

Free API key (no credit card): [fundzwatch.ai/onboarding](https://fundzwatch.ai/onboarding)

Python SDK: `pip install fundzwatch`

MCP server: `npx -y @fundzwatch/mcp-server`

GitHub:
- [Python SDK](https://github.com/fundz/fundzwatch-python)
- [MCP Server](https://github.com/fundz/fundzwatch-mcp)
- [AI SDR Example](https://github.com/fundz/fundzwatch-ai-sdr)

If you have questions or feature requests, drop a comment. I read all of them.

---

## Post 2: How to Add Real-Time Business Events to Your AI Agent (Python)

```yaml
---
title: How to Add Real-Time Business Events to Your AI Agent (Python)
published: true
tags: python, ai, tutorial, beginners
cover_image: # add a relevant image URL
canonical_url: https://fundzwatch.ai/blog/add-business-events-ai-agent-python
---
```

AI agents are great at reasoning but terrible at knowing what happened yesterday. If your agent needs to answer questions like "who raised funding this week?" or "which companies in fintech are hiring a CRO?", it's going to hallucinate unless you give it access to real data.

This tutorial shows how to connect your Python-based AI agent to real-time business events using FundzWatch. Takes about 5 minutes to get the basics working.

### What you'll need

- Python 3.9+
- A free FundzWatch API key ([get one here](https://fundzwatch.ai/onboarding), no credit card)
- That's it for the basic setup. CrewAI or LangChain if you want agent tool integration.

### Step 1: Install and authenticate

```bash
pip install fundzwatch
export FUNDZWATCH_API_KEY="fundz_test_your_key_here"
```

```python
from fundzwatch import FundzWatch

fw = FundzWatch()  # picks up the API key from the env var
```

The client handles auth, retries, and error handling. If the key is invalid or the rate limit is hit, you get clear exception types (`AuthenticationError`, `RateLimitError`) instead of cryptic HTTP errors.

### Step 2: Fetch events

```python
# All events from the last 7 days
events = fw.get_events(days=7)
print(f"Total events: {events['total']}")

# Just funding rounds
funding = fw.get_events(types="funding", days=7)
for event in funding["events"]:
    print(f"{event['title']} - ${event.get('amount', 0) / 1e6:.1f}M")

# Acquisitions in healthtech
acquisitions = fw.get_events(
    types="acquisition",
    days=30,
    industries="HealthTech"
)
```

Event types: `funding`, `acquisition`, `hiring`, `contract`, `product_launch`

You can filter by industry, location, and time range (up to 90 days back).

### Step 3: Get AI-scored leads

This is where it gets useful. Instead of raw events, the scoring engine analyzes signals and returns leads ranked by buyer intent:

```python
leads = fw.get_leads(min_score=50, max_results=10)

for lead in leads["signals"]:
    print(f"\n{lead['company_name']} ({lead['domain']})")
    print(f"  Score: {lead['score']}/100")
    print(f"  Stage: {lead['buying_stage']}")
    print(f"  Why now: {lead['outreach_angle']}")
```

The score combines multiple signals: recent funding, executive changes, growth indicators, and timing. A score of 70+ means the company has strong buying signals right now.

### Step 4: Track companies

```python
# Add companies to your watchlist
fw.add_to_watchlist(["stripe.com", "openai.com", "github.com"])

# Get events for tracked companies
watchlist_events = fw.get_watchlist_events(days=30)
for event in watchlist_events["events"]:
    print(f"[{event['type']}] {event['title']}")

# Check your watchlist
watchlist = fw.get_watchlist()
print(f"Tracking {watchlist['total']} companies")
```

### Step 5: Market intelligence

```python
# Quick market overview
pulse = fw.get_market_pulse()
p = pulse["pulse"]
print(f"Funding this week: {p['funding']['count_7d']} rounds")
print(f"Total raised: ${p['funding']['total_raised_7d'] / 1e6:.0f}M")
print(f"Acquisitions: {p['acquisitions']['count_7d']}")
print(f"Executive moves: {p['executive_moves']['count_7d']}")

# AI-generated market brief
brief = fw.get_market_brief()
print(brief["brief"])
```

### Quick wins: 5 things you can do in under 5 minutes

Here are practical things you can build immediately with just a few lines each:

**1. Slack alert for competitor funding**

```python
import os, requests
from fundzwatch import FundzWatch

fw = FundzWatch()
competitors = ["competitor1.com", "competitor2.com", "competitor3.com"]
fw.add_to_watchlist(competitors)

events = fw.get_watchlist_events(days=1, types="funding")
for event in events["events"]:
    requests.post(os.environ["SLACK_WEBHOOK"], json={
        "text": f"Competitor alert: {event['title']}"
    })
```

Run this as a daily cron job and you'll never miss a competitor funding round again.

**2. Weekly lead report**

```python
from fundzwatch import FundzWatch

fw = FundzWatch()
leads = fw.get_leads(min_score=60, max_results=20)

print("This Week's Top Leads")
print("=" * 50)
for i, lead in enumerate(leads["signals"], 1):
    print(f"\n{i}. {lead['company_name']} - Score: {lead['score']}/100")
    print(f"   Stage: {lead['buying_stage']}")
    print(f"   Outreach: {lead['outreach_angle']}")
```

**3. Industry-specific event monitor**

```python
from fundzwatch import FundzWatch

fw = FundzWatch()

# What's happening in fintech this week?
fintech = fw.get_events(days=7, industries="FinTech", limit=20)
print(f"FinTech events this week: {fintech['total']}")
for e in fintech["events"]:
    print(f"  [{e['type']}] {e['title']}")
```

**4. Give Claude real-time data (no code needed)**

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fundzwatch": {
      "command": "npx",
      "args": ["-y", "@fundzwatch/mcp-server"],
      "env": {
        "FUNDZWATCH_API_KEY": "your_key_here"
      }
    }
  }
}
```

Restart Claude Desktop. Ask: "What are the biggest funding rounds this week?" Get real answers.

**5. CrewAI sales research agent**

```python
from fundzwatch import FundzWatch
from fundzwatch.tools.crewai import get_fundzwatch_tools
from crewai import Agent, Task, Crew

fw = FundzWatch()
tools = get_fundzwatch_tools(fw)

agent = Agent(
    role="Sales Researcher",
    goal="Find companies ready to buy",
    tools=tools
)

task = Task(
    description="Find 5 SaaS companies that raised Series A or B this month",
    expected_output="Company list with scores and outreach recommendations",
    agent=agent
)

result = Crew(agents=[agent], tasks=[task]).kickoff()
print(result)
```

### Error handling

The SDK raises typed exceptions so you can handle issues cleanly:

```python
from fundzwatch import FundzWatch, AuthenticationError, RateLimitError

try:
    fw = FundzWatch()
    leads = fw.get_leads(min_score=60)
except AuthenticationError:
    print("Bad API key. Get one at fundzwatch.ai/onboarding")
except RateLimitError:
    print("Monthly limit hit. Upgrade at fundzwatch.ai/dashboard/upgrade")
```

### Check your usage

```python
usage = fw.get_usage()
print(f"Used: {usage['calls_used']}/{usage['calls_limit']} this month")
print(f"Resets: {usage['resets_at']}")
```

### What's next

Once you have the basics working, a few directions to explore:

- **Build a full AI SDR**: The [fundzwatch-ai-sdr](https://github.com/fundz/fundzwatch-ai-sdr) repo shows a complete pipeline that finds leads, scores them, and drafts personalized outreach
- **Add to your existing agent**: The CrewAI and LangChain tool integrations drop into any existing agent setup
- **Set up the MCP server**: If you use Claude Desktop or Cursor, the MCP server gives your AI assistant access to all this data through natural language

### Links

- Free API key: [fundzwatch.ai/onboarding](https://fundzwatch.ai/onboarding)
- Python SDK: `pip install fundzwatch` ([PyPI](https://pypi.org/project/fundzwatch/))
- MCP server: `npx -y @fundzwatch/mcp-server` ([npm](https://www.npmjs.com/package/@fundzwatch/mcp-server))
- [Python SDK source](https://github.com/fundz/fundzwatch-python)
- [MCP server source](https://github.com/fundz/fundzwatch-mcp)
- [AI SDR example](https://github.com/fundz/fundzwatch-ai-sdr)

Questions? Drop a comment, happy to help.
