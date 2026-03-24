# FundzWatch Twitter/X Thread Scripts

## Thread 1: "I replaced our $2K/mo sales intelligence tool with 3 lines of Python"

**Tweet 1/6:**
I replaced our $2K/mo sales intelligence tool with 3 lines of Python.

Same data. Better scoring. Free tier included.

Here's exactly what I did (thread):

**Tweet 2/6:**
The tool we were paying for: ZoomInfo + Crunchbase Pro.

$800/mo + $1,200/mo = $2K/mo for funding alerts, company data, and "intent signals" that were basically web scraping dressed up.

We needed: who raised funding this week + their contact info + a reason to reach out.

**Tweet 3/6:**
The replacement:

```python
from fundzwatch import FundzWatch

fw = FundzWatch()  # API key via env var
leads = fw.get_leads(min_score=60, max_results=10)

for lead in leads["signals"]:
    print(f"{lead['company_name']}: {lead['score']}/100")
    print(f"  Why now: {lead['outreach_angle']}")
```

That's it. AI-scored leads with buyer intent, buying stage, and a specific outreach angle. Not "this company visited your website."

**Tweet 4/6:**
What comes back:

- Company name, domain, industry
- Buyer intent score (0-100)
- Buying stage (Research, Active Evaluation, Decision)
- Pain points tied to real events
- A specific outreach angle

The score is based on actual business events: funding rounds, exec hires, acquisitions. Not pageview guessing.

**Tweet 5/6:**
The math:

Old stack: $2,000/mo ($24K/yr)
FundzWatch free tier: $0/mo (1,000 API calls)
FundzWatch Pro: $49/mo if you need more

We're getting better leads because the scoring is based on real signals, not "they downloaded a whitepaper 6 months ago."

**Tweet 6/6:**
Free API key, no credit card:
https://fundzwatch.ai/onboarding

Python SDK:
pip install fundzwatch

50M+ business events indexed since 2017. Funding, acquisitions, hires, contracts, product launches.

Also has an MCP server if you want Claude to query it directly. But that's a thread for another day.

---

## Thread 2: "The AI SDR stack that actually works (no $500/mo tools needed)"

**Tweet 1/7:**
The AI SDR stack that actually works:

- FundzWatch for real-time data ($0-49/mo)
- CrewAI for the agent framework (free)
- Claude for analysis and email drafting ($0-20/mo)

Total: under $70/mo vs $500+/mo for "AI SDR" SaaS tools.

Here's the architecture:

**Tweet 2/7:**
The problem with most AI SDR tools:

They charge $500/mo to wrap GPT around stale data and send templated emails.

The "AI" is just "Dear {first_name}, I noticed {company} is growing..."

That's not intelligence. That's a mail merge with extra steps.

**Tweet 3/7:**
Layer 1: Real-time data (FundzWatch)

```python
from fundzwatch import FundzWatch
fw = FundzWatch()

# AI-scored leads matched to your ICP
leads = fw.get_leads(min_score=60)

# This week's funding rounds
events = fw.get_events(types="funding", days=7)

# Market overview
pulse = fw.get_market_pulse()
```

This gives you the raw intelligence. Who raised, who got acquired, who hired a new CRO.

**Tweet 4/7:**
Layer 2: Agent framework (CrewAI)

```python
from crewai import Agent, Task, Crew
from fundzwatch.tools.crewai import get_fundzwatch_tools

tools = get_fundzwatch_tools(fw)

researcher = Agent(
    role="Sales Intelligence Analyst",
    goal="Find high-intent companies",
    tools=tools
)
```

The agent decides which API calls to make based on your query. "Find healthtech companies that just raised Series B" -- it knows what to do.

**Tweet 5/7:**
Layer 3: Outreach (Claude)

The agent takes the scored leads + their events and drafts outreach that references specific things:

"Saw you closed your $15M Series B last week. Companies at your stage typically hit [pain point]. We help with [specific solution]."

Not "I noticed your company is doing great things." Actual context.

**Tweet 6/7:**
The full pipeline in ~30 lines:

1. FundzWatch scores leads against your ICP
2. CrewAI agent filters and prioritizes
3. Claude drafts personalized emails tied to real events
4. You review and send

No $500/mo SaaS. No 12-month contracts. No "enterprise pricing" calls.

**Tweet 7/7:**
Everything you need to build this:

pip install fundzwatch crewai

Free API key: https://fundzwatch.ai/onboarding

Full AI SDR example repo:
github.com/fundz/fundzwatch-ai-sdr

The FundzWatch SDK also has LangChain tools if that's your stack. Same idea, different framework.

---

## Thread 3: "I asked Claude 'who raised Series B this week?' and it gave me real answers"

**Tweet 1/6:**
I asked Claude "who raised Series B this week?" and it gave me real, accurate answers.

Not hallucinated. Not from training data. Actual funding rounds from this week.

Here's the 30-second setup:

**Tweet 2/6:**
The trick: MCP (Model Context Protocol).

It lets Claude call external tools. FundzWatch has an MCP server that gives Claude access to 50M+ business events.

Setup in claude_desktop_config.json:

```json
{
  "mcpServers": {
    "fundzwatch": {
      "command": "npx",
      "args": ["-y", "@fundzwatch/mcp-server"],
      "env": {
        "FUNDZWATCH_API_KEY": "fundz_test_..."
      }
    }
  }
}
```

**Tweet 3/6:**
Now I just ask Claude in natural language:

Me: "Who raised a Series B in healthtech this week?"

Claude calls the FundzWatch API, gets real events, and responds with actual companies, amounts, and investors.

No prompt engineering. No RAG pipeline. Just a config file and a question.

**Tweet 4/6:**
It gets better. You can ask follow-up questions:

"Which of those companies are hiring a VP of Sales?"
"Add the top 3 to my watchlist"
"What does the funding market look like this month vs last?"

Claude calls different FundzWatch endpoints as needed. It figures out the right API calls on its own.

**Tweet 5/6:**
Why this matters:

LLMs hallucinate facts. That's a problem when you need accurate business data.

MCP solves this by letting the model call verified data sources instead of guessing.

FundzWatch returns structured, timestamped events from real sources. Claude presents them. No hallucination possible for the data part.

**Tweet 6/6:**
To set this up:

1. Get a free API key: https://fundzwatch.ai/onboarding
2. Add the config block above to your Claude Desktop settings
3. Restart Claude
4. Ask it anything about business events

Works with any MCP-compatible client (Claude Desktop, Cursor, etc.)

npm package: @fundzwatch/mcp-server

---

## Thread 4: "Every AI agent has the same problem: stale data"

**Tweet 1/7:**
Every AI agent has the same problem: stale data.

Your agent is brilliant at reasoning but clueless about what happened yesterday.

Training cutoffs, static RAG, cached results -- they all lead to the same failure mode.

Here's how to fix it for business intelligence:

**Tweet 2/7:**
The failure mode:

You: "Which companies raised funding this week?"
Agent: *confidently lists companies from 2023*

You: "Is Acme Corp a good prospect right now?"
Agent: *analyzes based on 18-month-old data*

For sales, stale data isn't just wrong -- it's actively harmful. You're pitching based on situations that no longer exist.

**Tweet 3/7:**
The root cause:

- LLM training data: months to years old
- RAG over documents: only as fresh as your last ingestion
- Web search: unstructured, noisy, unreliable for structured queries
- Manual research: doesn't scale

What you need: a structured, real-time API that your agent can call.

**Tweet 4/7:**
What "real-time business events" actually means:

FundzWatch indexes 50M+ events going back to 2017, with new events added continuously:

- Funding rounds (amount, stage, investors)
- Acquisitions (acquirer, target, terms)
- Executive hires (who, what role, from where)
- Government contracts (agency, value)
- Product launches

Structured JSON. Not scraped web pages.

**Tweet 5/7:**
Integration takes minutes, not sprints:

REST API:
```bash
curl https://api.fundz.net/v1/watch/events?types=funding&days=7 \
  -H "Authorization: Bearer fundz_test_..."
```

Python:
```python
from fundzwatch import FundzWatch
fw = FundzWatch()
events = fw.get_events(types="funding", days=7)
```

MCP: just add 5 lines to your claude_desktop_config.json.

**Tweet 6/7:**
The key difference: AI-scored leads.

FundzWatch doesn't just give you raw events. It scores companies against your ICP:

- Buyer intent score (0-100)
- Buying stage detection
- Pain point inference from events
- Specific outreach angles

Your agent gets pre-analyzed intelligence, not just data.

**Tweet 7/7:**
If you're building AI agents that need business data:

pip install fundzwatch

Free tier: 1,000 API calls/month
No credit card. No sales call.

https://fundzwatch.ai/onboarding

Also: CrewAI tools, LangChain tools, and an MCP server. All included in the package.

---

## Thread 5: "We index 50M+ business events. Here's what the data shows."

**Tweet 1/6:**
We index 50M+ business events going back to 2017.

Funding rounds. Acquisitions. Executive moves. Contracts. Product launches.

Here's what the data shows about how companies actually signal they're ready to buy:

**Tweet 2/6:**
Signal #1: New executive + funding within 90 days.

When a company raises a round AND hires a new VP/C-suite within 90 days, they're in active buying mode.

The new exec has budget, mandate, and pressure to show results fast. They're evaluating tools in their first 60 days.

This is the highest-intent signal in our data.

**Tweet 3/6:**
Signal #2: Series B is the sweet spot.

Seed/A companies are building, not buying. Series C+ have already locked in their stack.

Series B companies have enough budget to buy real tools but are still actively building their go-to-market infrastructure.

If you're selling B2B SaaS, Series B companies that raised in the last 30 days are your best prospects.

**Tweet 4/6:**
Signal #3: Acquisitions create immediate pain.

When Company A acquires Company B, the combined entity needs to:
- Consolidate tools
- Re-evaluate vendors
- Onboard new teams

The 30-60 day window after an acquisition announcement is prime time for outreach. Existing contracts are being reviewed. Everything is on the table.

**Tweet 5/6:**
Signal #4: Government contracts signal growth capacity.

Companies that win federal contracts are about to scale operations. They need tools, infrastructure, and people.

The contract award data is public but hard to aggregate. We index it alongside private sector events so you can see the full picture.

**Tweet 6/6:**
All of this data is available through the FundzWatch API.

The AI scoring engine combines these signals automatically -- you don't need to build the logic yourself.

```python
from fundzwatch import FundzWatch
fw = FundzWatch()
leads = fw.get_leads(min_score=70)
# High-intent companies, pre-scored
```

Free API key: https://fundzwatch.ai/onboarding
50M+ events. Real-time updates. No hallucinations.
