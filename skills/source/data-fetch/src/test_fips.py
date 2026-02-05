
import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'lib'))

from data_fetching.census_client import CensusClient

def test_fips():
    client = CensusClient(use_cache=True)
    
    print("Testing State FIPS Lookup:")
    states = ["California", "CA", "texas", "New York"]
    for s in states:
        fips = client.get_state_fips(s)
        print(f"  {s} -> {fips}")
        if not fips:
            print(f"FAIL: Could not map {s}")
            return

    # Basic County Lookup (without API call if possible, or expect failure if no key)
    # We won't test full API fetch in this smoke test unless we know we have a key,
    # but we can test that the method exists and argument validation works.
    print("\nTesting County FIPS validation:")
    res = client.get_county_fips(None, None)
    if res is None:
         print("  ✓ Correctly handled None input")
    else:
         print("  FAIL: Should return None for empty input")

    print("\nVerification Complete.")

if __name__ == "__main__":
    test_fips()
