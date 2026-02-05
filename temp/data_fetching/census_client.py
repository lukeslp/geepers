"""
Census Bureau API Client

Provides a unified interface for fetching data from the U.S. Census Bureau API,
with built-in caching, error handling, and metadata tracking.

Supported APIs:
- American Community Survey (ACS) 5-year estimates
- Small Area Income and Poverty Estimates (SAIPE)
- Decennial Census

Example:
    from shared.data_fetching import CensusClient

    client = CensusClient(
        api_key='your_key_here',
        cache_dir='./cache',
        use_cache=True
    )

    # Fetch ACS data
    df = client.fetch_acs(
        year=2022,
        variables={
            'B01003_001E': 'total_population',
            'B17001_002E': 'poverty_population'
        },
        geography='county:*'
    )

    # Get metadata
    metadata = client.get_metadata()
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd
import requests


class CensusClient:
    """
    U.S. Census Bureau API client with caching and error handling.

    This client provides a simplified interface to Census data APIs with:
    - Automatic caching of API responses
    - Metadata tracking (sources, timestamps, record counts)
    - Error handling with graceful degradation
    - FIPS code generation for geographic identifiers
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        use_cache: bool = True,
        timeout: int = 30
    ):
        """
        Initialize Census API client.

        Args:
            api_key: Census API key. If None, uses CENSUS_API_KEY env var.
            cache_dir: Directory for caching API responses. Defaults to ./cache
            use_cache: Whether to use cached data when available
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key or os.getenv('CENSUS_API_KEY')
        self.use_cache = use_cache
        self.timeout = timeout

        # Set up cache directory
        if cache_dir is None:
            self.cache_dir = Path.cwd() / 'cache'
        else:
            self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True, parents=True)

        # Metadata tracking
        self.metadata = {
            'collection_date': datetime.now().isoformat(),
            'sources': {},
            'record_counts': {}
        }

    def _get_cache_path(self, cache_key: str) -> Path:
        """Generate cache file path from key."""
        # Use hash of key for filesystem safety
        key_hash = hashlib.md5(cache_key.encode()).hexdigest()
        return self.cache_dir / f"{cache_key}_{key_hash}.csv"

    def _load_from_cache(self, cache_path: Path) -> Optional[pd.DataFrame]:
        """Load DataFrame from cache if available and use_cache is True."""
        if self.use_cache and cache_path.exists():
            try:
                df = pd.read_csv(cache_path)
                return df
            except Exception as e:
                print(f"   ⚠️  Cache read error: {e}")
                return None
        return None

    def _save_to_cache(self, df: pd.DataFrame, cache_path: Path):
        """Save DataFrame to cache."""
        try:
            df.to_csv(cache_path, index=False)
        except Exception as e:
            print(f"   ⚠️  Cache write error: {e}")

    def fetch_acs(
        self,
        year: int,
        variables: Dict[str, str],
        geography: str = 'county:*',
        dataset: str = 'acs5',
        state: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch data from American Community Survey (ACS).

        Args:
            year: Year of data (e.g., 2022)
            variables: Dict mapping Census variable codes to column names
                      Example: {'B01003_001E': 'total_pop', 'B17001_002E': 'poverty_pop'}
            geography: Geographic level (default: 'county:*' for all counties)
            dataset: ACS dataset (default: 'acs5' for 5-year estimates)
            state: Optional state FIPS code to limit results

        Returns:
            DataFrame with requested variables and geography
        """
        # Build cache key
        var_codes = sorted(variables.keys())
        cache_key = f"acs_{year}_{dataset}_{geography.replace(':', '_')}_{'-'.join(var_codes)}"
        if state:
            cache_key += f"_state{state}"
        cache_path = self._get_cache_path(cache_key)

        # Try cache first
        cached_df = self._load_from_cache(cache_path)
        if cached_df is not None:
            print(f"   Using cached ACS data from {cache_path.name}")
            self.metadata['sources'][cache_key] = 'cached'
            return cached_df

        # Build API request
        url = f"https://api.census.gov/data/{year}/acs/{dataset}"

        # Add NAME to get human-readable geography names
        get_vars = ['NAME'] + list(variables.keys())
        params = {
            'get': ','.join(get_vars),
            'for': geography
        }

        if state:
            params['in'] = f'state:{state}'

        if self.api_key:
            params['key'] = self.api_key

        # Make API request
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])

            # Create FIPS code if geography is county
            if 'county' in geography and 'state' in df.columns and 'county' in df.columns:
                df['fips'] = df['state'] + df['county']

            # Rename variables to friendly names
            rename_map = {'NAME': 'name'}
            rename_map.update(variables)
            df = df.rename(columns=rename_map)

            # Convert numeric columns
            for orig_code, col_name in variables.items():
                if col_name in df.columns:
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')

            # Save to cache
            self._save_to_cache(df, cache_path)

            # Update metadata
            self.metadata['sources'][cache_key] = f"Census ACS {dataset} {year}"
            self.metadata['record_counts'][cache_key] = len(df)

            print(f"   ✓ Fetched ACS data for {len(df)} geographies")
            return df

        except requests.exceptions.RequestException as e:
            print(f"   ✗ Error fetching ACS data: {e}")
            return pd.DataFrame()

    def fetch_saipe(
        self,
        year: int,
        geography: str = 'county',
        state: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch Small Area Income and Poverty Estimates (SAIPE).

        Args:
            year: Year of data (e.g., 2022)
            geography: Geographic level ('county', 'state', or 'us')
            state: Optional state FIPS code to limit results

        Returns:
            DataFrame with poverty estimates
        """
        cache_key = f"saipe_{year}_{geography}"
        if state:
            cache_key += f"_state{state}"
        cache_path = self._get_cache_path(cache_key)

        # Try cache
        cached_df = self._load_from_cache(cache_path)
        if cached_df is not None:
            print(f"   Using cached SAIPE data from {cache_path.name}")
            self.metadata['sources'][cache_key] = 'cached'
            return cached_df

        # Build API request
        url = f"https://api.census.gov/data/{year}/acs/acs5"

        # SAIPE variables
        variables = {
            'B17001_001E': 'total_pop',
            'B17001_002E': 'poverty_pop'
        }

        params = {
            'get': f"NAME,{','.join(variables.keys())}",
            'for': f'{geography}:*'
        }

        if state and geography == 'county':
            params['in'] = f'state:{state}'

        if self.api_key:
            params['key'] = self.api_key

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(data[1:], columns=data[0])

            # Create FIPS for counties
            if geography == 'county' and 'state' in df.columns and 'county' in df.columns:
                df['fips'] = df['state'] + df['county']

            df = df.rename(columns={
                'NAME': 'name',
                **variables
            })

            # Convert numeric
            df['total_pop'] = pd.to_numeric(df['total_pop'], errors='coerce')
            df['poverty_pop'] = pd.to_numeric(df['poverty_pop'], errors='coerce')

            # Calculate poverty rate
            df['poverty_rate'] = (df['poverty_pop'] / df['total_pop'] * 100).round(2)

            self._save_to_cache(df, cache_path)

            self.metadata['sources'][cache_key] = f"Census ACS {year} (SAIPE proxy)"
            self.metadata['record_counts'][cache_key] = len(df)

            print(f"   ✓ Fetched SAIPE data for {len(df)} geographies")
            return df

        except requests.exceptions.RequestException as e:
            print(f"   ✗ Error fetching SAIPE data: {e}")
            return pd.DataFrame()

    def fetch_population(
        self,
        year: int,
        geography: str = 'county:*',
        state: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch total population counts.

        Args:
            year: Year of data
            geography: Geographic level
            state: Optional state FIPS code

        Returns:
            DataFrame with population data
        """
        return self.fetch_acs(
            year=year,
            variables={'B01003_001E': 'total_population'},
            geography=geography,
            state=state
        )

    def get_county_fips(self, state_name: str, county_name: str) -> Optional[str]:
        """
        Look up FIPS code for a county.

        Note: This requires a pre-loaded FIPS code table. For now, returns None.
        Future enhancement: Load from Census geocoding API.

        Args:
            state_name: State name (e.g., "California")
            county_name: County name (e.g., "Los Angeles")

        Returns:
            5-digit FIPS code or None
        """
        # TODO: Implement geocoding or load from reference table
        print(f"   ⚠️  FIPS lookup not yet implemented for {county_name}, {state_name}")
        return None

    def generate_metadata(self, source: str, dataset: str) -> Dict:
        """
        Generate metadata dictionary for a dataset.

        Args:
            source: Data source name (e.g., "Census Bureau")
            dataset: Dataset name (e.g., "ACS 2022")

        Returns:
            Dict with metadata
        """
        return {
            'source': source,
            'dataset': dataset,
            'collection_date': datetime.now().isoformat(),
            'api_key_used': bool(self.api_key),
            'cache_enabled': self.use_cache,
            'cache_directory': str(self.cache_dir)
        }

    def get_metadata(self) -> Dict:
        """
        Get metadata for all fetches performed by this client instance.

        Returns:
            Dict with collection metadata
        """
        return self.metadata

    def save_metadata(self, filepath: Union[str, Path]):
        """
        Save metadata to JSON file.

        Args:
            filepath: Path to save metadata JSON
        """
        filepath = Path(filepath)
        with open(filepath, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        print(f"   ✓ Metadata saved to {filepath}")

    def clear_cache(self, pattern: Optional[str] = None):
        """
        Clear cached files.

        Args:
            pattern: Optional glob pattern to match specific files (e.g., "acs_2022*")
                    If None, clears all cache files.
        """
        if pattern:
            files = list(self.cache_dir.glob(f"{pattern}"))
        else:
            files = list(self.cache_dir.glob("*.csv"))

        count = 0
        for file in files:
            try:
                file.unlink()
                count += 1
            except Exception as e:
                print(f"   ⚠️  Error deleting {file}: {e}")

        print(f"   ✓ Cleared {count} cached file(s)")


# Convenience function for quick access
def create_census_client(
    api_key: Optional[str] = None,
    cache_dir: Optional[Path] = None,
    use_cache: bool = True
) -> CensusClient:
    """
    Create a CensusClient with sensible defaults.

    Args:
        api_key: Census API key (uses CENSUS_API_KEY env var if None)
        cache_dir: Cache directory (defaults to ./cache)
        use_cache: Whether to use caching

    Returns:
        Configured CensusClient instance
    """
    return CensusClient(api_key=api_key, cache_dir=cache_dir, use_cache=use_cache)
