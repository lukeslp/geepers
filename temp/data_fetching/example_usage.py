"""
Example usage of CensusClient

This shows common patterns for fetching Census data.
"""

from census_client import CensusClient
from pathlib import Path


def main():
    # Initialize client (uses CENSUS_API_KEY env var)
    client = CensusClient(
        cache_dir=Path('./cache'),
        use_cache=True
    )

    print("=" * 70)
    print("Census API Client - Example Usage")
    print("=" * 70)

    # Example 1: Fetch population data
    print("\n📊 Example 1: Fetch county populations")
    pop_df = client.fetch_population(year=2022)
    print(pop_df.head())
    print(f"Total counties: {len(pop_df)}")

    # Example 2: Fetch custom variables
    print("\n📊 Example 2: Fetch uninsured rates")
    health_df = client.fetch_acs(
        year=2022,
        variables={
            'B27001_001E': 'total_pop',
            'B27001_005E': 'uninsured_pop'
        }
    )
    # Calculate rate
    health_df['uninsured_rate'] = (
        health_df['uninsured_pop'] / health_df['total_pop'] * 100
    ).round(2)
    print(health_df[['name', 'uninsured_rate']].head())

    # Example 3: Fetch poverty data
    print("\n📊 Example 3: Fetch poverty estimates")
    poverty_df = client.fetch_saipe(year=2022)
    print(poverty_df[['name', 'poverty_rate']].head())

    # Example 4: State-specific data
    print("\n📊 Example 4: Fetch California counties only")
    ca_df = client.fetch_population(year=2022, state='06')  # California FIPS: 06
    print(f"California counties: {len(ca_df)}")

    # Save metadata
    print("\n📄 Saving metadata...")
    client.save_metadata('census_metadata.json')

    # Get metadata
    print("\n📊 Metadata summary:")
    metadata = client.get_metadata()
    print(f"Collection date: {metadata['collection_date']}")
    print(f"Sources: {len(metadata['sources'])}")
    print(f"Total records: {sum(metadata['record_counts'].values())}")


if __name__ == '__main__':
    main()
