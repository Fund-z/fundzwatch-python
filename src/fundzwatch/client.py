"""FundzWatch API client."""

import os
from typing import Any, Dict, List, Optional

import httpx

from fundzwatch import __version__
from fundzwatch.exceptions import (
    APIError,
    AuthenticationError,
    FundzWatchError,
    RateLimitError,
    ValidationError,
)


class FundzWatch:
    """Client for the FundzWatch.ai API.

    Args:
        api_key: Your FundzWatch API key. Falls back to FUNDZWATCH_API_KEY env var.
        base_url: API base URL. Defaults to https://api.fundz.net/v1/watch.
        timeout: Request timeout in seconds. Default: 30.
    """

    DEFAULT_BASE_URL = "https://api.fundz.net/v1/watch"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.api_key = api_key or os.environ.get("FUNDZWATCH_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "API key required. Pass api_key= or set FUNDZWATCH_API_KEY env var. "
                "Get a free key at https://fundzwatch.ai/onboarding"
            )
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": f"fundzwatch-python/{__version__}",
            },
            timeout=timeout,
            transport=httpx.HTTPTransport(retries=2),
        )

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        try:
            response = self._client.request(method, path, **kwargs)
        except httpx.ConnectError as e:
            raise APIError(f"Connection failed: {e}") from e
        except httpx.TimeoutException as e:
            raise APIError(f"Request timed out: {e}") from e

        if response.status_code == 401:
            raise AuthenticationError("Invalid API key", status_code=401)
        if response.status_code == 429:
            raise RateLimitError(
                "Monthly API call limit exceeded. Upgrade at https://fundzwatch.ai/dashboard/upgrade",
                status_code=429,
            )
        if response.status_code == 400:
            data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
            raise ValidationError(data.get("message", "Bad request"), status_code=400)
        if response.status_code >= 400:
            data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
            raise APIError(
                data.get("message", f"API error {response.status_code}"),
                status_code=response.status_code,
                error_code=data.get("error"),
            )

        return response.json()

    # ── Scored Leads ─────────────────────────────────────────────────────

    def get_leads(
        self,
        min_score: int = 0,
        max_results: int = 25,
        buying_stages: Optional[List[str]] = None,
        industries: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Get AI-scored leads matched to your ICP.

        Args:
            min_score: Minimum buyer intent score (0-100).
            max_results: Max leads to return (1-50).
            buying_stages: Filter by stage (e.g., ['Active Evaluation', 'Decision']).
            industries: Filter by industry (e.g., ['SaaS', 'HealthTech']).

        Returns:
            Dict with 'signals_found', 'signals' (list of scored leads), and metadata.
        """
        body: Dict[str, Any] = {"min_score": min_score, "max_results": max_results}
        if buying_stages:
            body["buying_stages"] = buying_stages
        if industries:
            body["industries"] = industries
        return self._request("POST", "/signals", json=body)

    # ── Events ───────────────────────────────────────────────────────────

    def get_events(
        self,
        types: Optional[str] = None,
        days: int = 7,
        limit: int = 50,
        offset: int = 0,
        industries: Optional[str] = None,
        locations: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get real-time business events.

        Args:
            types: Comma-separated: funding, acquisition, hiring, contract, product_launch.
            days: Look back period (1-90).
            limit: Max events (1-200).
            offset: Pagination offset.
            industries: Comma-separated industry filter.
            locations: Comma-separated location filter.

        Returns:
            Dict with 'events' list and 'total' count.
        """
        params: Dict[str, Any] = {"days": days, "limit": limit, "offset": offset}
        if types:
            params["types"] = types
        if industries:
            params["industries"] = industries
        if locations:
            params["locations"] = locations
        return self._request("GET", "/events", params=params)

    # ── Market Intelligence ──────────────────────────────────────────────

    def get_market_pulse(self) -> Dict[str, Any]:
        """Get market activity overview (7d and 30d totals, largest rounds)."""
        return self._request("GET", "/market/pulse")

    def get_market_brief(self) -> Dict[str, Any]:
        """Get today's AI-generated strategic intelligence brief."""
        return self._request("GET", "/market/brief")

    # ── Watchlist ────────────────────────────────────────────────────────

    def get_watchlist(self) -> Dict[str, Any]:
        """List all companies on your watchlist."""
        return self._request("GET", "/watchlist")

    def add_to_watchlist(self, domains: List[str]) -> Dict[str, Any]:
        """Add companies to your watchlist by domain.

        Args:
            domains: List of domains (e.g., ['stripe.com', 'github.com']).

        Returns:
            Dict with add/match results and total tracked count.
        """
        return self._request("POST", "/watchlist", json={"domains": domains})

    def remove_from_watchlist(self, domains: List[str]) -> Dict[str, Any]:
        """Remove companies from your watchlist."""
        return self._request("DELETE", "/watchlist", json={"domains": domains})

    def get_watchlist_events(
        self, days: int = 7, types: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get events for tracked companies.

        Args:
            days: Look back period (1-90).
            types: Comma-separated event types.
        """
        params: Dict[str, Any] = {"days": days}
        if types:
            params["types"] = types
        return self._request("GET", "/watchlist/events", params=params)

    # ── Usage ────────────────────────────────────────────────────────────

    def get_usage(self) -> Dict[str, Any]:
        """Get current API usage and limits."""
        return self._request("GET", "/usage")

    # ── Cleanup ──────────────────────────────────────────────────────────

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
