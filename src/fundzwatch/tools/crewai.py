"""CrewAI tool integrations for FundzWatch.

Usage:
    from fundzwatch import FundzWatch
    from fundzwatch.tools.crewai import get_fundzwatch_tools

    fw = FundzWatch(api_key="fundz_test_...")
    tools = get_fundzwatch_tools(fw)

    # Use in a CrewAI agent:
    agent = Agent(role="Sales Researcher", tools=tools)
"""

from typing import List, Optional, Type

from pydantic import BaseModel, Field

try:
    from crewai.tools import BaseTool
except ImportError:
    raise ImportError(
        "crewai is required for CrewAI tools. Install with: pip install fundzwatch[crewai]"
    )

from fundzwatch.client import FundzWatch


# ── Input Schemas ────────────────────────────────────────────────────────

class ScoredLeadsInput(BaseModel):
    min_score: int = Field(default=0, description="Minimum buyer intent score (0-100)")
    max_results: int = Field(default=25, description="Max leads to return (1-50)")
    buying_stages: Optional[str] = Field(default=None, description="Comma-separated stages: Active Evaluation, Decision, Research, Awareness")
    industries: Optional[str] = Field(default=None, description="Comma-separated industries")


class EventsInput(BaseModel):
    types: Optional[str] = Field(default=None, description="Event types: funding, acquisition, hiring, contract, product_launch")
    days: int = Field(default=7, description="Look back days (1-90)")
    limit: int = Field(default=50, description="Max events (1-200)")
    industries: Optional[str] = Field(default=None, description="Comma-separated industries")
    locations: Optional[str] = Field(default=None, description="Comma-separated locations")


class WatchlistInput(BaseModel):
    action: str = Field(description="Action: 'list', 'add', or 'remove'")
    domains: Optional[str] = Field(default=None, description="Comma-separated domains for add/remove")


# ── Tools ────────────────────────────────────────────────────────────────

class GetScoredLeadsTool(BaseTool):
    name: str = "get_scored_leads"
    description: str = (
        "Get AI-scored sales leads matched to your ICP. Returns companies with "
        "buyer intent scores, buying stage, pain points, and outreach recommendations."
    )
    args_schema: Type[BaseModel] = ScoredLeadsInput
    fw_client: FundzWatch = None

    class Config:
        arbitrary_types_allowed = True

    def _run(self, min_score: int = 0, max_results: int = 25, buying_stages: Optional[str] = None, industries: Optional[str] = None) -> str:
        try:
            industry_list = [i.strip() for i in industries.split(",")] if industries else None
            stage_list = [s.strip() for s in buying_stages.split(",")] if buying_stages else None
            data = self.fw_client.get_leads(
                min_score=min_score,
                max_results=max_results,
                buying_stages=stage_list,
                industries=industry_list,
            )
            leads = data.get("signals", [])
            if not leads:
                return "No scored leads found matching your criteria."
            lines = []
            for lead in leads:
                lines.append(
                    f"- {lead['company_name']} (Score: {lead['score']}/100, "
                    f"Stage: {lead.get('buying_stage', 'N/A')}): "
                    f"{lead.get('outreach_angle', 'N/A')}"
                )
            return f"Found {data['signals_found']} leads:\n" + "\n".join(lines)
        except Exception as e:
            return f"Error fetching leads: {e}"


class GetEventsTool(BaseTool):
    name: str = "get_business_events"
    description: str = (
        "Get real-time business events: funding rounds, acquisitions, executive hires, "
        "government contracts, and product launches."
    )
    args_schema: Type[BaseModel] = EventsInput
    fw_client: FundzWatch = None

    class Config:
        arbitrary_types_allowed = True

    def _run(
        self,
        types: Optional[str] = None,
        days: int = 7,
        limit: int = 50,
        industries: Optional[str] = None,
        locations: Optional[str] = None,
    ) -> str:
        try:
            data = self.fw_client.get_events(
                types=types, days=days, limit=limit,
                industries=industries, locations=locations,
            )
            events = data.get("events", [])
            if not events:
                return "No events found matching your filters."
            lines = []
            for e in events:
                detail = f"- [{e['type'].upper()}] {e['title']}"
                if e.get("amount"):
                    detail += f" (${e['amount'] / 1_000_000:.1f}M)"
                lines.append(detail)
            return f"{data['total']} events found:\n" + "\n".join(lines)
        except Exception as e:
            return f"Error fetching events: {e}"


class GetMarketPulseTool(BaseTool):
    name: str = "get_market_pulse"
    description: str = (
        "Get a real-time market overview: funding totals, acquisition counts, "
        "executive moves, and largest rounds for the past week."
    )
    args_schema: Type[BaseModel] = BaseModel
    fw_client: FundzWatch = None

    class Config:
        arbitrary_types_allowed = True

    def _run(self) -> str:
        try:
            data = self.fw_client.get_market_pulse()
            p = data["pulse"]
            return (
                f"Market Pulse:\n"
                f"- Funding: {p['funding']['count_7d']} rounds, ${p['funding']['total_raised_7d'] / 1_000_000:.0f}M raised\n"
                f"- Acquisitions: {p['acquisitions']['count_7d']} this week\n"
                f"- Executive Moves: {p['executive_moves']['count_7d']} this week\n"
                f"- Contracts: {p['contracts']['count_7d']} this week"
            )
        except Exception as e:
            return f"Error fetching market pulse: {e}"


class ManageWatchlistTool(BaseTool):
    name: str = "manage_watchlist"
    description: str = (
        "Manage your company watchlist. Actions: 'list' to view, 'add' to track domains, "
        "'remove' to untrack. Provide comma-separated domains for add/remove."
    )
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
                    return "Watchlist is empty."
                lines = [f"- {c.get('name', c['domain'])} ({c['domain']})" for c in companies]
                return f"Watchlist ({data['total']}/{data['limit']}):\n" + "\n".join(lines)
            domain_list = [d.strip() for d in (domains or "").split(",") if d.strip()]
            if not domain_list:
                return "Provide comma-separated domains."
            if action == "add":
                data = self.fw_client.add_to_watchlist(domain_list)
                return f"Added {data['added']} companies. Total: {data['total_tracked']}"
            if action == "remove":
                data = self.fw_client.remove_from_watchlist(domain_list)
                return f"Removed {data['removed']} companies. Total: {data['total_tracked']}"
            return "Invalid action. Use 'list', 'add', or 'remove'."
        except Exception as e:
            return f"Error: {e}"


def get_fundzwatch_tools(client: FundzWatch) -> List[BaseTool]:
    """Get all FundzWatch tools configured with an API client.

    Args:
        client: An initialized FundzWatch client.

    Returns:
        List of CrewAI tools ready for use in agents.
    """
    return [
        GetScoredLeadsTool(fw_client=client),
        GetEventsTool(fw_client=client),
        GetMarketPulseTool(fw_client=client),
        ManageWatchlistTool(fw_client=client),
    ]
