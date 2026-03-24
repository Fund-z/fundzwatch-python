---
title: "Turn Claude into Your Business Intelligence Analyst with MCP"
published: true
description: "Ask Claude 'Who raised Series B this week?' and get a real answer. Here's how."
tags: claude, mcp, business-intelligence, no-code
cover_image: ""
canonical_url: ""
---

# Turn Claude into Your Business Intelligence Analyst with MCP

Ask Claude "Who raised Series B this week?" and get a real answer. Not a hallucination from training data. An actual list of companies that closed funding rounds in the last 7 days, with amounts, series, and dates.

This takes about 3 minutes to set up. No code. You just edit one JSON file.

## What is MCP?

Model Context Protocol (MCP) is an open standard that lets AI assistants like Claude connect to external tools and data sources. Instead of being limited to training data, Claude can call live APIs, query databases, and interact with services -- all through a standardized protocol.

The FundzWatch MCP server gives Claude access to real-time business event data: funding rounds, acquisitions, executive hires, government contracts, and AI-scored sales leads.

## Setup (3 Minutes)

### Step 1: Get Your API Key

Go to [fundzwatch.ai/onboarding](https://fundzwatch.ai/onboarding) and grab a free API key. No credit card required. It looks like `fundz_live_abc123...`.

### Step 2: Install the MCP Server

```bash
npm install -g @fundzwatch/mcp-server
```

That's it. One command.

### Step 3: Configure Claude Desktop

Open Claude Desktop, then go to **Settings** (gear icon) > **Developer** > **Edit Config**.

This opens your `claude_desktop_config.json` file. Add the FundzWatch server:

```json
{
  "mcpServers": {
    "fundzwatch": {
      "command": "fundzwatch-mcp",
      "env": {
        "FUNDZWATCH_API_KEY": "fundz_live_your_key_here"
      }
    }
  }
}
```

If you already have other MCP servers configured, just add the `"fundzwatch"` entry inside the existing `"mcpServers"` object.

### Step 4: Restart Claude Desktop

Quit and reopen Claude Desktop. You should see a hammer icon in the chat input area. Click it and you'll see the FundzWatch tools listed:

- `get_scored_leads`
- `get_events`
- `get_market_pulse`
- `get_market_brief`
- `manage_watchlist`
- `get_watchlist_events`
- `get_usage`

If you see those, you're set.

## The 7 Tools Explained

Here's what each tool does and when Claude will use it.

### 1. `get_scored_leads`

**What it does:** Returns AI-scored sales leads matched to your Ideal Customer Profile. Each lead comes with a buyer intent score (0-100), buying stage, pain points, and a recommended outreach angle.

**When Claude uses it:** When you ask about leads, prospects, who to sell to, or buying intent.

**Parameters:**
- `min_score` -- Minimum intent score (0-100)
- `max_results` -- How many leads (1-50)
- `buying_stages` -- Filter: "Active Evaluation", "Decision", "Research", "Awareness"
- `industries` -- Filter by industry: "SaaS", "FinTech", "HealthTech", etc.

### 2. `get_events`

**What it does:** Returns real-time business events: funding rounds, acquisitions, executive hires, government contracts, and product launches.

**When Claude uses it:** When you ask about funding, acquisitions, news, events, or what happened recently.

**Parameters:**
- `types` -- Event types: funding, acquisition, hiring, contract, product_launch
- `days` -- Lookback period (1-90)
- `limit` -- Max events (1-200)
- `industries` -- Industry filter
- `locations` -- Location filter

### 3. `get_market_pulse`

**What it does:** Returns a high-level market overview with 7-day and 30-day totals for all event types, plus the largest funding rounds of the week.

**When Claude uses it:** When you ask about market trends, overall activity, or "what's happening in the market."

### 4. `get_market_brief`

**What it does:** Returns today's AI-generated strategic intelligence brief -- a narrative analysis of the most important market movements, patterns, and opportunities.

**When Claude uses it:** When you ask for a briefing, summary, or strategic overview.

### 5. `manage_watchlist`

**What it does:** Add, remove, or list companies on your watchlist. You can track up to 25 companies (free tier) or 250 (Growth tier).

**When Claude uses it:** When you ask to track, watch, monitor, or follow specific companies.

### 6. `get_watchlist_events`

**What it does:** Returns events only for companies you're tracking. Useful for competitor monitoring and account-based sales.

**When Claude uses it:** When you ask about your tracked companies, competitors, or watchlist activity.

### 7. `get_usage`

**What it does:** Shows your current API usage, limits, and tier.

**When Claude uses it:** When you ask how many calls you've made or what your limits are.

## 10 Power Prompts

These are real prompts you can type into Claude Desktop once the MCP server is connected. Try them.

---

### Prompt 1: Daily Funding Scan

> "Show me every company that raised a funding round in the last 24 hours. Include the amount, series, and industry."

**What you'll see:** Claude calls `get_events` with `types: "funding"` and `days: 1`. You get back a clean table:

```
Here are today's funding rounds:

| Company | Amount | Series | Industry |
|---------|--------|--------|----------|
| Wiz | $300M | Series D | Cloud Security |
| Ramp | $150M | Series C | FinTech |
| Abridge | $75M | Series C | HealthTech |
| Vanta | $40M | Series B | Compliance |
| Weights & Biases | $50M | Series C | AI/ML |

5 funding events in the last 24 hours, totaling $615M.
```

---

### Prompt 2: Competitive Intelligence

> "Add salesforce.com, hubspot.com, and gong.io to my watchlist. Then tell me if any of them had events in the last 30 days."

**What you'll see:** Claude calls `manage_watchlist` to add the domains, then `get_watchlist_events` with `days: 30`. It reports back any funding, acquisitions, or exec hires for those specific companies.

---

### Prompt 3: Find Hot Leads

> "Who are my highest-scoring leads right now? I want companies in the Active Evaluation or Decision buying stage with a score above 70."

**What you'll see:** Claude calls `get_scored_leads` with `min_score: 70` and `buying_stages: ["Active Evaluation", "Decision"]`. Each lead comes with a company name, score, pain point, and a specific outreach angle you can use.

---

### Prompt 4: Weekly Market Briefing

> "Give me a market pulse for this week. How does it compare to the 30-day average?"

**What you'll see:** Claude calls `get_market_pulse` and does the math for you:

```
This week's market activity:

- Funding: 142 rounds ($4.2B raised) -- up 18% vs. 30-day weekly avg
- Acquisitions: 23 this week -- roughly in line with average
- Executive Moves: 87 -- down 8%
- Contracts: 34 -- up 12%

Largest rounds:
1. Wiz - $300M Series D
2. Ramp - $150M Series C
3. Abridge - $75M Series C

Takeaway: Funding velocity is accelerating, especially in security
and fintech. Good week to target recently-funded companies.
```

---

### Prompt 5: Industry Deep Dive

> "What's happening in HealthTech this month? Show me funding, acquisitions, and leadership changes."

**What you'll see:** Claude calls `get_events` with `industries: "HealthTech"` and `days: 30`, then organizes the results by event type. Useful for quarterly industry reports or board presentations.

---

### Prompt 6: Outreach Prep

> "I have a meeting with someone at Stripe tomorrow. What events has Stripe had recently? Also show me the market pulse so I have context."

**What you'll see:** Claude calls `manage_watchlist` to add stripe.com (if not already tracked), then `get_watchlist_events` and `get_market_pulse`. You get a pre-meeting briefing with company-specific intel and market context.

---

### Prompt 7: Strategic Brief

> "Give me today's strategic intelligence brief."

**What you'll see:** Claude calls `get_market_brief` and returns a narrative analysis. This is an AI-generated brief that covers the most important market movements, emerging patterns, and opportunities. Good for starting your day.

---

### Prompt 8: Geographic Focus

> "Show me all funding rounds and acquisitions in New York in the last 14 days."

**What you'll see:** Claude calls `get_events` with `types: "funding,acquisition"`, `days: 14`, and `locations: "New York"`. Useful if your sales team is territory-based.

---

### Prompt 9: Build a Target List

> "Find 10 SaaS companies with a buyer intent score above 50 that are in the Research or Awareness buying stage. Format as a CSV I can import into my CRM."

**What you'll see:** Claude calls `get_scored_leads` and formats the output as CSV:

```csv
company,domain,score,buying_stage,pain_point,outreach_angle
Vanta,vanta.com,87,Research,"Scaling compliance processes","Reference Series B and growing team"
Linear,linear.app,74,Awareness,"Outgrowing current project tools","Mention their recent enterprise push"
...
```

Copy, paste into your CRM. Done.

---

### Prompt 10: End-of-Week Recap

> "Summarize everything that happened this week: total funding raised, biggest deals, notable acquisitions, and any exec moves I should know about. Format it as a Slack message I can post to our #sales-intel channel."

**What you'll see:** Claude calls `get_market_pulse` and `get_events`, then formats everything using Slack-compatible markdown. You literally copy-paste it into Slack.

---

## Tips for Getting the Most Out of This

**Be specific about time ranges.** "This week" is fine, but "last 3 days" or "last 30 days" gives Claude a clear parameter to pass to the API.

**Name industries explicitly.** Instead of "tech companies," say "SaaS and FinTech." The API filters on specific industry names.

**Ask for specific formats.** "Format as a table," "Format as CSV," "Format as a Slack message." Claude is good at reformatting data when you tell it what you need.

**Combine tools in one prompt.** You can ask Claude to check events, pull leads, AND manage your watchlist in a single message. It will make multiple tool calls and synthesize the results.

**Use the watchlist for ongoing monitoring.** Add your top 20 target accounts once. Then every day, just ask "What happened with my watchlist companies today?" and you get a targeted briefing.

## Alternative Setup: Claude Code (CLI)

If you use Claude Code (the CLI version), you can also configure the MCP server there. Add this to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "fundzwatch": {
      "command": "fundzwatch-mcp",
      "env": {
        "FUNDZWATCH_API_KEY": "fundz_live_your_key_here"
      }
    }
  }
}
```

Then use the FundzWatch tools directly in your Claude Code sessions.

## Pricing

- **Free tier:** 100 API calls/month, 25 watchlist slots, no credit card
- **Growth tier:** 5,000 API calls/month, 250 watchlist slots, priority support

Each Claude message that triggers a tool call uses 1 API call. A typical "get me today's events" query is 1 call. A complex prompt that checks events, pulls leads, and checks the watchlist might use 3-4 calls.

## Get Started

1. Get your API key: [fundzwatch.ai/onboarding](https://fundzwatch.ai/onboarding)
2. Install: `npm install -g @fundzwatch/mcp-server`
3. Add to `claude_desktop_config.json`
4. Restart Claude Desktop
5. Ask: "Who raised funding this week?"

That's it. No code, no Python, no pipelines. Just Claude with live business intelligence.

**[Get a free API key at fundzwatch.ai/onboarding](https://fundzwatch.ai/onboarding)**

MCP server source: [github.com/fundz/fundzwatch-mcp](https://github.com/fundz/fundzwatch-mcp)

---

*Questions? Open an issue on GitHub or drop a comment below.*
