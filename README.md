# FundzWatch Python SDK

Real-time business event intelligence for AI agents and sales teams.

```bash
pip install fundzwatch
```

## Quick Start

```python
from fundzwatch import FundzWatch

fw = FundzWatch(api_key="fundz_test_...")  # or set FUNDZWATCH_API_KEY env var

# Get AI-scored leads matched to your ICP
leads = fw.get_leads(min_score=60, max_results=10)
for lead in leads["signals"]:
    print(f"{lead['company_name']}: {lead['score']}/100 - {lead['outreach_angle']}")

# Get real-time funding events
events = fw.get_events(types="funding", days=7)
for event in events["events"]:
    print(f"[{event['type']}] {event['title']}")

# Track companies and get their events
fw.add_to_watchlist(["stripe.com", "github.com", "openai.com"])
watchlist_events = fw.get_watchlist_events(days=30)

# Market intelligence
pulse = fw.get_market_pulse()
brief = fw.get_market_brief()
```

## Use with CrewAI

```bash
pip install fundzwatch[crewai]
```

```python
from fundzwatch import FundzWatch
from fundzwatch.tools.crewai import get_fundzwatch_tools
from crewai import Agent, Task, Crew

fw = FundzWatch()
tools = get_fundzwatch_tools(fw)

researcher = Agent(
    role="Sales Intelligence Analyst",
    goal="Find high-intent companies that match our ICP",
    backstory="You analyze business events to find sales opportunities.",
    tools=tools,
)

task = Task(
    description="Find the top 10 companies most likely to buy our product right now. "
    "Focus on companies with recent funding or leadership changes and a score above 60.",
    expected_output="A ranked list of companies with scores, buying stages, and outreach angles.",
    agent=researcher,
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
```

## Use with LangChain

```bash
pip install fundzwatch[langchain]
```

```python
from fundzwatch import FundzWatch
from fundzwatch.tools.langchain import get_fundzwatch_tools
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

fw = FundzWatch()
tools = get_fundzwatch_tools(fw)
llm = ChatAnthropic(model="claude-sonnet-4-20250514")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sales intelligence analyst with access to real-time business events."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "Find funded healthtech companies this week"})
```

## API Reference

### `FundzWatch(api_key=None, base_url=None, timeout=30.0)`

Initialize the client. API key falls back to `FUNDZWATCH_API_KEY` env var.

### Methods

| Method | Description |
|--------|-------------|
| `get_leads(min_score, max_results, buying_stages, industries)` | AI-scored leads |
| `get_events(types, days, limit, offset, industries, locations)` | Business events |
| `get_market_pulse()` | Market activity overview |
| `get_market_brief()` | AI strategic intelligence brief |
| `get_watchlist()` | List tracked companies |
| `add_to_watchlist(domains)` | Track companies |
| `remove_from_watchlist(domains)` | Untrack companies |
| `get_watchlist_events(days, types)` | Events for tracked companies |
| `get_usage()` | API usage and limits |

## Get a Free API Key

Sign up at [fundzwatch.ai/onboarding](https://fundzwatch.ai/onboarding) -- no credit card required.

## License

MIT
