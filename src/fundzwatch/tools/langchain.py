"""LangChain tool integrations for FundzWatch.

Usage:
    from fundzwatch import FundzWatch
    from fundzwatch.tools.langchain import get_fundzwatch_tools

    fw = FundzWatch(api_key="fundz_test_...")
    tools = get_fundzwatch_tools(fw)

    # Use in a LangChain agent:
    agent = create_tool_calling_agent(llm, tools, prompt)
"""

from typing import List, Optional, Type

from pydantic import BaseModel, Field

try:
    from langchain_core.tools import BaseTool
except ImportError:
    raise ImportError(
        "langchain-core is required for LangChain tools. Install with: pip install fundzwatch[langchain]"
    )

from fundzwatch.client import FundzWatch


# ── Input Schemas ────────────────────────────────────────────────────────

class ScoredLeadsInput(BaseModel):
    min_score: int = Field(default=0, description="Minimum buyer intent score (0-100)")
    max_results: int = Field(default=25, description="Max leads to return (1-50)")
    industries: Optional[str] = Field(default=None, description="Comma-separated industries")


class EventsInput(BaseModel):
    types: Optional[str] = Field(default=None, description="Event types: funding, acquisition, hiring, contract, product_launch")
    days: int = Field(default=7, description="Look back days (1-90)")
    limit: int = Field(default=50, description="Max events (1-200)")


class WatchlistInput(BaseModel):
    action: str = Field(description="Action: 'list', 'add', or 'remove'")
    domains: Optional[str] = Field(default=None, description="Comma-separated domains for add/remove")


# ── Tools ────────────────────────────────────────────────────────────────

class FundzWatchScoredLeads(BaseTool):
    name: str = "fundzwatch_scored_leads"
    description: str = (
        "Get AI-scored sales leads matched to your ICP. Returns companies with "
        "buyer intent scores, buying stage, and outreach recommendations."
    )
    args_schema: Type[BaseModel] = ScoredLeadsInput
    fw_client: FundzWatch = None

    class Config:
        arbitrary_types_allowed = True

    def _run(self, min_score: int = 0, max_results: int = 25, industries: Optional[str] = None) -> str:
        try:
            industry_list = [i.strip() for i in industries.split(",")] if industries else None
            data = self.fw_client.get_leads(min_score=min_score, max_results=max_results, industries=industry_list)
            leads = data.get("signals", [])
            if not leads:
                return "No scored leads found."
            lines = []
            for lead in leads:
                lines.append(
                    f"- {lead['company_name']} (Score: {lead['score']}/100, "
                    f"Stage: {lead.get('buying_stage', 'N/A')}): "
                    f"{lead.get('outreach_angle', 'N/A')}"
                )
            return f"Found {data['signals_found']} leads:\n" + "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"


class FundzWatchEvents(BaseTool):
    name: str = "fundzwatch_events"
    description: str = (
        "Get real-time business events: funding, acquisitions, hires, contracts, launches."
    )
    args_schema: Type[BaseModel] = EventsInput
    fw_client: FundzWatch = None

    class Config:
        arbitrary_types_allowed = True

    def _run(self, types: Optional[str] = None, days: int = 7, limit: int = 50) -> str:
        try:
            data = self.fw_client.get_events(types=types, days=days, limit=limit)
            events = data.get("events", [])
            if not events:
                return "No events found."
            lines = []
            for e in events:
                detail = f"- [{e['type'].upper()}] {e['title']}"
                if e.get("amount"):
                    detail += f" (${e['amount'] / 1_000_000:.1f}M)"
                lines.append(detail)
            return f"{data['total']} events:\n" + "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"


class FundzWatchMarketPulse(BaseTool):
    name: str = "fundzwatch_market_pulse"
    description: str = "Get real-time market overview: funding totals, acquisitions, exec moves."
    args_schema: Type[BaseModel] = BaseModel
    fw_client: FundzWatch = None

    class Config:
        arbitrary_types_allowed = True

    def _run(self) -> str:
        try:
            data = self.fw_client.get_market_pulse()
            p = data["pulse"]
            return (
                f"Funding: {p['funding']['count_7d']} rounds (${p['funding']['total_raised_7d'] / 1_000_000:.0f}M) | "
                f"Acquisitions: {p['acquisitions']['count_7d']} | "
                f"Exec Moves: {p['executive_moves']['count_7d']} | "
                f"Contracts: {p['contracts']['count_7d']}"
            )
        except Exception as e:
            return f"Error: {e}"


class FundzWatchWatchlist(BaseTool):
    name: str = "fundzwatch_watchlist"
    description: str = "Manage company watchlist: 'list', 'add' domains, or 'remove' domains."
    args_schema: Type[BaseModel] = WatchlistInput
    fw_client: FundzWatch = None

    class Config:
        arbitrary_types_allowed = True

    def _run(self, action: str, domains: Optional[str] = None) -> str:
        try:
            if action == "list":
                data = self.fw_client.get_watchlist()
                companies = data.get("companies", [])
                if not companies:
                    return "Watchlist empty."
                return "\n".join(f"- {c.get('name', c['domain'])}" for c in companies)
            domain_list = [d.strip() for d in (domains or "").split(",") if d.strip()]
            if not domain_list:
                return "Provide domains."
            if action == "add":
                data = self.fw_client.add_to_watchlist(domain_list)
                return f"Added {data['added']}. Total: {data['total_tracked']}"
            if action == "remove":
                data = self.fw_client.remove_from_watchlist(domain_list)
                return f"Removed {data['removed']}. Total: {data['total_tracked']}"
            return "Use 'list', 'add', or 'remove'."
        except Exception as e:
            return f"Error: {e}"


def get_fundzwatch_tools(client: FundzWatch) -> List[BaseTool]:
    """Get all FundzWatch tools for LangChain agents.

    Args:
        client: An initialized FundzWatch client.

    Returns:
        List of LangChain tools.
    """
    return [
        FundzWatchScoredLeads(fw_client=client),
        FundzWatchEvents(fw_client=client),
        FundzWatchMarketPulse(fw_client=client),
        FundzWatchWatchlist(fw_client=client),
    ]
