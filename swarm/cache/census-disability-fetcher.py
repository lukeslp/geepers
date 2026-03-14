#!/usr/bin/env python3
"""
Census Bureau Disability Data Fetcher
Retrieves ACS 1-year disability estimates (S1810) and detailed demographic data (B18101)
for years 2010-2023 (excluding 2020 - no 1-year ACS released due to COVID).
"""

import json
import requests
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Census API Configuration
CENSUS_API_KEY = "56e280037b7fbf1788422653faa1cf2adf4276a7"
BASE_URL = "https://api.census.gov/data"

# Years to fetch (excluding 2020)
YEARS = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023]

# S1810 Subject Table - Disability Characteristics
S1810_VARIABLES = {
    "S1810_C01_001E": "Total civilian noninstitutionalized population",
    "S1810_C02_001E": "With a disability (total)",
    "S1810_C03_001E": "Percent with a disability",
    "S1810_C01_002E": "Under 18 years",
    "S1810_C02_002E": "Under 18 years - with disability",
    "S1810_C03_002E": "Under 18 years - percent with disability",
    "S1810_C01_003E": "18 to 64 years",
    "S1810_C02_003E": "18 to 64 years - with disability",
    "S1810_C03_003E": "18 to 64 years - percent with disability",
    "S1810_C01_004E": "65 years and over",
    "S1810_C02_004E": "65 years and over - with disability",
    "S1810_C03_004E": "65 years and over - percent with disability",
}

# B18101 Detail Table - Disability Status by Age and Sex
B18101_VARIABLES = {
    "B18101_001E": "Total population",
    "B18101_002E": "With a disability",
    "B18101_003E": "Male with a disability",
    "B18101_004E": "Under 5 years",
    "B18101_005E": "5 to 17 years",
    "B18101_006E": "18 to 34 years",
    "B18101_007E": "35 to 64 years",
    "B18101_008E": "65 to 74 years",
    "B18101_009E": "75 years and over",
}

class CensusFetcher:
    """Fetches and processes Census disability data."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.results = {
            "metadata": {
                "fetched_at": datetime.now().isoformat(),
                "api_key_masked": api_key[:8] + "..." + api_key[-8:],
            },
            "s1810_data": {},
            "b18101_data": {},
            "errors": [],
            "summary": {
                "total_requests": 0,
                "successful": 0,
                "failed": 0,
                "years_covered": [],
            }
        }

    def fetch_s1810(self, year: int) -> Optional[Dict]:
        """Fetch S1810 (Subject Table - Disability Characteristics) for a year."""
        try:
            # Build variable list
            variables = ["NAME"] + list(S1810_VARIABLES.keys())
            var_string = ",".join(variables)

            url = f"{BASE_URL}/{year}/acs/acs1/subject"
            params = {
                "get": var_string,
                "for": "us:*",
                "key": self.api_key
            }

            self.results["summary"]["total_requests"] += 1
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            self.results["summary"]["successful"] += 1

            return {
                "year": year,
                "table": "S1810",
                "data": data,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            error_msg = f"S1810 {year}: {str(e)}"
            self.results["errors"].append(error_msg)
            self.results["summary"]["failed"] += 1
            print(f"Error fetching S1810 {year}: {e}", file=sys.stderr)
            return None

    def fetch_b18101(self, year: int) -> Optional[Dict]:
        """Fetch B18101 (Detail Table - Disability by Age/Sex) for a year."""
        try:
            # Build variable list
            variables = ["NAME"] + list(B18101_VARIABLES.keys())
            var_string = ",".join(variables)

            url = f"{BASE_URL}/{year}/acs/acs1"
            params = {
                "get": var_string,
                "for": "us:*",
                "key": self.api_key
            }

            self.results["summary"]["total_requests"] += 1
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            self.results["summary"]["successful"] += 1

            return {
                "year": year,
                "table": "B18101",
                "data": data,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            error_msg = f"B18101 {year}: {str(e)}"
            self.results["errors"].append(error_msg)
            self.results["summary"]["failed"] += 1
            print(f"Error fetching B18101 {year}: {e}", file=sys.stderr)
            return None

    def fetch_all(self):
        """Fetch both tables for all years."""
        print(f"Starting Census disability data fetch for {len(YEARS)} years...")
        print(f"Years: {YEARS}")
        print()

        for year in YEARS:
            print(f"Fetching year {year}...")

            # Fetch S1810
            s1810_result = self.fetch_s1810(year)
            if s1810_result:
                self.results["s1810_data"][year] = s1810_result
                print(f"  ✓ S1810 ({len(s1810_result['data'])} rows)")

            # Fetch B18101
            b18101_result = self.fetch_b18101(year)
            if b18101_result:
                self.results["b18101_data"][year] = b18101_result
                print(f"  ✓ B18101 ({len(b18101_result['data'])} rows)")

            # Track successful years
            if s1810_result or b18101_result:
                self.results["summary"]["years_covered"].append(year)

        print()
        print("Fetch complete.")
        return self.results

    def save_results(self, output_path: str = None) -> str:
        """Save results to JSON file."""
        if output_path is None:
            output_path = f"/home/coolhand/geepers/swarm/cache/census-disability-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        return output_path

    def print_summary(self):
        """Print summary of fetch results."""
        summary = self.results["summary"]
        print("\n" + "="*70)
        print("CENSUS DISABILITY DATA FETCH SUMMARY")
        print("="*70)
        print(f"\nTimestamp: {self.results['metadata']['fetched_at']}")
        print(f"Total API Requests: {summary['total_requests']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Years Covered: {len(summary['years_covered'])} of {len(YEARS)}")
        print(f"Years: {sorted(summary['years_covered'])}")

        if self.results["errors"]:
            print(f"\nErrors ({len(self.results['errors'])}):")
            for error in self.results["errors"]:
                print(f"  - {error}")

        # Data summary
        print(f"\nS1810 Data Retrieved: {len(self.results['s1810_data'])} years")
        print(f"B18101 Data Retrieved: {len(self.results['b18101_data'])} years")

        print("\n" + "="*70 + "\n")


def main():
    """Main entry point."""
    fetcher = CensusFetcher(CENSUS_API_KEY)

    # Fetch all data
    fetcher.fetch_all()

    # Save to file
    output_file = fetcher.save_results()
    print(f"Results saved to: {output_file}")

    # Print summary
    fetcher.print_summary()

    # Return results dict for inspection
    return fetcher.results


if __name__ == "__main__":
    results = main()
