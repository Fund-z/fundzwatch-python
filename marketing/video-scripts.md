# FundzWatch Short-Form Video Scripts

## Video 1: "Build an AI sales agent in 60 seconds"

**Format:** Screen recording -- terminal on left, code editor on right
**Duration:** 60 seconds
**Platform:** YouTube Shorts, TikTok, Instagram Reels

---

**[0:00-0:03] HOOK (text overlay + voiceover)**

"Build an AI sales agent in 60 seconds. No $500/mo tools."

**[0:03-0:10] Install**

*Terminal focus:*

```
pip install fundzwatch crewai
```

*Voiceover:* "Two packages. That's the entire stack. FundzWatch for real-time business data, CrewAI for the agent framework."

**[0:10-0:25] Code**

*Editor focus, typing fast (or pre-typed, revealing line by line):*

```python
from fundzwatch import FundzWatch
from fundzwatch.tools.crewai import get_fundzwatch_tools
from crewai import Agent, Task, Crew

fw = FundzWatch()
tools = get_fundzwatch_tools(fw)

agent = Agent(
    role="Sales Analyst",
    goal="Find high-intent companies",
    tools=tools
)

task = Task(
    description="Find 10 companies that raised funding this week with a buyer intent score above 60",
    expected_output="Ranked list with scores and outreach angles",
    agent=agent
)

Crew(agents=[agent], tasks=[task]).kickoff()
```

*Voiceover:* "Initialize the client, get the tools, create an agent, give it a task, run it. The agent calls FundzWatch's API -- funding events, AI-scored leads, market data -- and returns actual companies with intent scores and outreach recommendations."

**[0:25-0:45] Output**

*Terminal focus -- show the agent running and returning results:*

```
Found 10 leads:
- TechCorp (Score: 87/100, Stage: Active Evaluation): Just raised $25M Series B...
- HealthAI (Score: 74/100, Stage: Decision): New CRO hired + $12M round...
- DataStack (Score: 71/100, Stage: Research): Acquired competitor...
```

*Voiceover:* "Real companies. Real events. Real scores. Not hallucinated. Not from training data. These are actual business events from this week, scored by AI against your ideal customer profile."

**[0:45-0:55] Context**

*Text overlay with stats:*

"50M+ business events indexed since 2017"
"Funding, acquisitions, hires, contracts, launches"
"Free tier: 1,000 API calls/month"

*Voiceover:* "FundzWatch indexes over 50 million business events. The free tier gives you 1,000 API calls a month. No credit card."

**[0:55-0:60] CTA**

*Screen: fundzwatch.ai/onboarding*

*Voiceover:* "Link in bio. pip install fundzwatch. Go build something."

---

## Video 2: "I gave Claude real-time business intelligence"

**Format:** Screen recording -- Claude Desktop app
**Duration:** 75 seconds
**Platform:** YouTube Shorts, TikTok, Instagram Reels

---

**[0:00-0:04] HOOK**

*Text overlay on Claude Desktop:*

"I gave Claude access to 50M+ real-time business events. Watch what happens."

**[0:04-0:15] Setup**

*Show claude_desktop_config.json in editor:*

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

*Voiceover:* "Five lines in your Claude Desktop config. That's the entire setup. This uses MCP -- Model Context Protocol -- to give Claude access to the FundzWatch API."

**[0:15-0:30] First question**

*Claude Desktop -- type the question:*

"Who raised a Series B in the last 7 days?"

*Show Claude's response streaming in with real company names, amounts, investors.*

*Voiceover:* "I just asked Claude who raised a Series B this week. And it's giving me real answers. Not from training data. Not hallucinated. These are actual funding rounds that happened this week."

**[0:30-0:45] Follow-up**

*Type follow-up:*

"Which of those companies are in healthtech? What are their buyer intent scores?"

*Show response with filtered results and scores.*

*Voiceover:* "Follow-up question. Claude calls a different endpoint, filters the data, and gives me scored leads with buying stages. This is the kind of thing that used to require a $20K/year ZoomInfo subscription."

**[0:45-0:60] Power move**

*Type:*

"Draft a cold email to the CEO of the top-scored company referencing their funding round"

*Show Claude drafting a personalized email.*

*Voiceover:* "Now I ask it to draft outreach. It takes the real event data, the company context, and writes an email that references their actual funding round. Not a template. Not a guess. A personalized email based on something that actually happened."

**[0:60-0:70] Reaction**

*Text overlay:*

"Wait. Claude actually knows who raised funding THIS WEEK?"

*Voiceover:* "This is what happens when you connect AI to real-time data instead of hoping the training data is recent enough."

**[0:70-0:75] CTA**

*Text overlay: fundzwatch.ai/onboarding -- Free API key*

*Voiceover:* "Free API key, link in bio. Works with Claude Desktop, Cursor, any MCP client."

---

## Video 3: "The free API that replaces Crunchbase for AI agents"

**Format:** Split screen -- pricing page on left, terminal on right
**Duration:** 70 seconds
**Platform:** YouTube Shorts, TikTok, Instagram Reels

---

**[0:00-0:04] HOOK**

*Text overlay:*

"This free API gives AI agents what Crunchbase charges $10K+/year for."

**[0:04-0:18] The pricing problem**

*Left side: Crunchbase pricing page (or mockup showing tiers)*

*Voiceover:* "Crunchbase Pro: $49/month but the API is separate. Crunchbase Enterprise API: call for pricing, which means $10K to $30K per year. ZoomInfo: even more. And neither of them is designed for AI agents. You get rate-limited, the response format is messy, and good luck getting an API key without sitting through a sales demo."

*Right side shows: FundzWatch pricing*
- Free: 1,000 calls/month
- Pro: $49/month
- "No credit card for free tier"

**[0:18-0:35] The curl**

*Terminal focus:*

```bash
curl -s https://api.fundz.net/v1/watch/events\?types=funding\&days=7 \
  -H "Authorization: Bearer fundz_test_demo123" | python -m json.tool
```

*Show the JSON response:*

```json
{
  "total": 142,
  "events": [
    {
      "type": "funding",
      "title": "TechCorp raises $25M Series B",
      "amount": 25000000,
      "stage": "Series B",
      "date": "2026-03-22",
      "company": "TechCorp",
      "domain": "techcorp.com"
    }
  ]
}
```

*Voiceover:* "One curl command. Clean JSON. Funding rounds from the last 7 days with amounts, stages, dates, and company info. 142 events this week alone."

**[0:35-0:48] Python SDK**

*Editor focus:*

```python
from fundzwatch import FundzWatch

fw = FundzWatch()

# Scored leads -- not just events, actual buyer intent
leads = fw.get_leads(min_score=60)
for lead in leads["signals"]:
    print(f"{lead['company_name']}: {lead['score']}/100")
    print(f"  Stage: {lead['buying_stage']}")
    print(f"  Angle: {lead['outreach_angle']}")
```

*Voiceover:* "Or use the Python SDK. Three lines and you get AI-scored leads with buyer intent scores, buying stages, and outreach recommendations. Crunchbase gives you company profiles. This gives you actionable intelligence."

**[0:48-0:58] The numbers**

*Text overlay, appearing one at a time:*

- "50M+ events indexed since 2017"
- "Funding, acquisitions, hires, contracts, launches"
- "Python SDK, MCP server, REST API"
- "CrewAI + LangChain tool integrations"
- "Free tier: 1,000 calls/month, no credit card"

*Voiceover:* "50 million events. Goes back to 2017. Funding, acquisitions, executive hires, government contracts, product launches. Python SDK, MCP server for Claude, REST API, and built-in CrewAI and LangChain integrations."

**[0:58-0:65] The punchline**

*Terminal:*

```
pip install fundzwatch
```

*Voiceover:* "One line to install. Free to start. Built for AI agents, not for enterprise procurement committees."

**[0:65-0:70] CTA**

*Screen: fundzwatch.ai/onboarding*

*Voiceover:* "Free API key. Link in bio."
