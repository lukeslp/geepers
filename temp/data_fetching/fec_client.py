"""
Federal Election Commission API Client

Provides access to FEC campaign finance data:
- Candidate financial information
- Committee finances and disbursements
- Individual contributions
- Election results

Requires FEC_API_KEY environment variable.
Register at: https://api.open.fec.gov/developers/

Author: Luke Steuber
"""

import os
import requests
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class FECClient:
    """Client for Federal Election Commission API."""

    BASE_URL = "https://api.open.fec.gov/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize FEC client.

        Args:
            api_key: FEC API key (defaults to FEC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('FEC_API_KEY')
        if not self.api_key:
            raise ValueError("FEC_API_KEY required. Get one at https://api.open.fec.gov/developers/")
        self.session = requests.Session()
        self.session.headers.update({'X-Api-Key': self.api_key})

    def search_candidates(
        self,
        name: Optional[str] = None,
        office: Optional[str] = None,
        state: Optional[str] = None,
        party: Optional[str] = None,
        cycle: Optional[int] = None,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Search for candidates.

        Args:
            name: Candidate name (partial match)
            office: Office sought (H=House, S=Senate, P=President)
            state: Two-letter state code
            party: Party affiliation (DEM, REP, etc.)
            cycle: Election cycle year (e.g., 2024)
            per_page: Results per page (max 100)

        Returns:
            Dict with candidate results
        """
        try:
            params = {'per_page': min(per_page, 100)}
            
            if name:
                params['name'] = name
            if office:
                params['office'] = office
            if state:
                params['state'] = state
            if party:
                params['party'] = party
            if cycle:
                params['cycle'] = cycle

            response = self.session.get(
                f"{self.BASE_URL}/candidates/search/",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            return {
                "candidates": data.get("results", []),
                "total_count": data.get("pagination", {}).get("count", 0),
                "page": data.get("pagination", {}).get("page", 1)
            }
        except Exception as e:
            logger.error(f"FEC candidate search error: {e}")
            return {"error": str(e), "candidates": []}

    def get_candidate_totals(
        self,
        candidate_id: str,
        cycle: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get financial totals for a candidate.

        Args:
            candidate_id: FEC candidate ID (e.g., 'P80001571' for Trump)
            cycle: Election cycle year

        Returns:
            Dict with financial totals
        """
        try:
            params = {}
            if cycle:
                params['cycle'] = cycle

            response = self.session.get(
                f"{self.BASE_URL}/candidate/{candidate_id}/totals/",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:
                return {"error": "No financial data found"}

            totals = results[0]

            return {
                "candidate_id": candidate_id,
                "cycle": totals.get("cycle"),
                "receipts": totals.get("receipts", 0),
                "disbursements": totals.get("disbursements", 0),
                "cash_on_hand": totals.get("cash_on_hand_end_period", 0),
                "debts": totals.get("debts_owed_by_committee", 0),
                "individual_contributions": totals.get("individual_contributions", 0),
                "pac_contributions": totals.get("political_party_committee_contributions", 0)
            }
        except Exception as e:
            logger.error(f"FEC candidate totals error: {e}")
            return {"error": str(e)}

    def get_committee_info(self, committee_id: str) -> Dict[str, Any]:
        """
        Get information about a committee.

        Args:
            committee_id: FEC committee ID

        Returns:
            Dict with committee information
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/committee/{committee_id}/",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:
                return {"error": "Committee not found"}

            committee = results[0]

            return {
                "committee_id": committee.get("committee_id"),
                "name": committee.get("name"),
                "designation": committee.get("designation_full"),
                "type": committee.get("committee_type_full"),
                "party": committee.get("party_full"),
                "treasurer_name": committee.get("treasurer_name"),
                "state": committee.get("state"),
                "filing_frequency": committee.get("filing_frequency")
            }
        except Exception as e:
            logger.error(f"FEC committee info error: {e}")
            return {"error": str(e)}

    def get_committee_totals(
        self,
        committee_id: str,
        cycle: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get financial totals for a committee.

        Args:
            committee_id: FEC committee ID
            cycle: Election cycle year

        Returns:
            Dict with financial totals
        """
        try:
            params = {}
            if cycle:
                params['cycle'] = cycle

            response = self.session.get(
                f"{self.BASE_URL}/committee/{committee_id}/totals/",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:
                return {"error": "No financial data found"}

            totals = results[0]

            return {
                "committee_id": committee_id,
                "cycle": totals.get("cycle"),
                "receipts": totals.get("receipts", 0),
                "disbursements": totals.get("disbursements", 0),
                "cash_on_hand": totals.get("cash_on_hand_end_period", 0),
                "debts": totals.get("debts_owed", 0)
            }
        except Exception as e:
            logger.error(f"FEC committee totals error: {e}")
            return {"error": str(e)}

    def get_disbursements(
        self,
        committee_id: str,
        min_amount: Optional[float] = None,
        max_date: Optional[str] = None,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Get committee disbursements (spending).

        Args:
            committee_id: FEC committee ID
            min_amount: Minimum disbursement amount
            max_date: Maximum date (YYYY-MM-DD)
            per_page: Results per page (max 100)

        Returns:
            Dict with disbursement data
        """
        try:
            params = {
                'committee_id': committee_id,
                'per_page': min(per_page, 100)
            }

            if min_amount:
                params['min_amount'] = min_amount
            if max_date:
                params['max_date'] = max_date

            response = self.session.get(
                f"{self.BASE_URL}/schedules/schedule_b/",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            return {
                "disbursements": data.get("results", []),
                "total_count": data.get("pagination", {}).get("count", 0),
                "page": data.get("pagination", {}).get("page", 1)
            }
        except Exception as e:
            logger.error(f"FEC disbursements error: {e}")
            return {"error": str(e), "disbursements": []}

    def search_individual_contributions(
        self,
        contributor_name: Optional[str] = None,
        committee_id: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_date: Optional[str] = None,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Search individual contributions.

        Args:
            contributor_name: Name of contributor
            committee_id: Recipient committee ID
            min_amount: Minimum contribution amount
            max_date: Maximum date (YYYY-MM-DD)
            per_page: Results per page (max 100)

        Returns:
            Dict with contribution data
        """
        try:
            params = {'per_page': min(per_page, 100)}

            if contributor_name:
                params['contributor_name'] = contributor_name
            if committee_id:
                params['committee_id'] = committee_id
            if min_amount:
                params['min_amount'] = min_amount
            if max_date:
                params['max_date'] = max_date

            response = self.session.get(
                f"{self.BASE_URL}/schedules/schedule_a/",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            return {
                "contributions": data.get("results", []),
                "total_count": data.get("pagination", {}).get("count", 0),
                "page": data.get("pagination", {}).get("page", 1)
            }
        except Exception as e:
            logger.error(f"FEC contributions search error: {e}")
            return {"error": str(e), "contributions": []}
