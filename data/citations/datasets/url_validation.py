#!/usr/bin/env python3
"""
URL Citation Validator for Datasets
Checks all source URLs in README files for accessibility
"""

import requests
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urlparse

# Government domains that should always be valid
CRITICAL_DOMAINS = [
    'data.census.gov',
    'nasa.gov',
    'noaa.gov',
    'usgs.gov',
    'census.gov',
    'bls.gov',
    'eeoc.gov',
    'ed.gov',
    'who.int',
    'data.cms.gov',
    'ssa.gov',
    'va.gov'
]

def extract_urls(text: str) -> List[str]:
    """Extract all URLs from markdown text"""
    # Match markdown links [text](url)
    md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
    urls = [url for _, url in md_links]

    # Match bare URLs
    bare_urls = re.findall(r'https?://[^\s\)]+', text)
    urls.extend(bare_urls)

    return list(set(urls))  # Deduplicate

def check_url(url: str, timeout: int = 10) -> Tuple[bool, int, str]:
    """
    Check if URL is accessible
    Returns (success, status_code, message)
    """
    try:
        # Skip anchor links
        if url.startswith('#'):
            return True, 0, "Anchor link"

        # Handle relative paths
        if not url.startswith('http'):
            return True, 0, "Relative path (skipped)"

        response = requests.head(url, timeout=timeout, allow_redirects=True)

        if response.status_code == 200:
            return True, 200, "OK"
        elif response.status_code in [301, 302, 307, 308]:
            return True, response.status_code, f"Redirect to {response.headers.get('Location', 'unknown')}"
        elif response.status_code == 405:
            # HEAD not allowed, try GET
            response = requests.get(url, timeout=timeout, allow_redirects=True, stream=True)
            if response.status_code == 200:
                return True, 200, "OK (GET)"

        return False, response.status_code, f"HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        return False, 0, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, 0, "Connection error"
    except Exception as e:
        return False, 0, f"Error: {str(e)[:50]}"

def validate_dataset_citations(dataset_dir: Path) -> Dict:
    """Validate all citations in a dataset's README"""
    readme = dataset_dir / "README.md"

    if not readme.exists():
        return {
            "dataset": dataset_dir.name,
            "status": "no_readme",
            "urls_checked": 0,
            "urls_valid": 0,
            "urls_invalid": 0
        }

    content = readme.read_text()
    urls = extract_urls(content)

    results = {
        "dataset": dataset_dir.name,
        "status": "checked",
        "urls_checked": len(urls),
        "urls_valid": 0,
        "urls_invalid": 0,
        "urls": []
    }

    for url in urls:
        success, status, message = check_url(url)

        url_result = {
            "url": url,
            "valid": success,
            "status_code": status,
            "message": message,
            "is_critical": any(domain in url for domain in CRITICAL_DOMAINS)
        }

        results["urls"].append(url_result)

        if success:
            results["urls_valid"] += 1
        else:
            results["urls_invalid"] += 1

    return results

def main():
    datasets_dir = Path("/home/coolhand/datasets")

    all_results = []

    # Check each dataset directory
    for dataset_path in sorted(datasets_dir.iterdir()):
        if dataset_path.is_dir() and not dataset_path.name.startswith('.'):
            print(f"Checking {dataset_path.name}...")
            result = validate_dataset_citations(dataset_path)
            all_results.append(result)

    # Save results
    output_dir = Path("/home/coolhand/geepers/data/citations/datasets")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "validation_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to {output_file}")

    # Summary
    total_urls = sum(r["urls_checked"] for r in all_results)
    total_valid = sum(r["urls_valid"] for r in all_results)
    total_invalid = sum(r["urls_invalid"] for r in all_results)

    print(f"\nTotal URLs checked: {total_urls}")
    print(f"Valid: {total_valid}")
    print(f"Invalid: {total_invalid}")

    # Show critical failures
    critical_failures = []
    for result in all_results:
        for url_data in result.get("urls", []):
            if url_data.get("is_critical") and not url_data.get("valid"):
                critical_failures.append({
                    "dataset": result["dataset"],
                    "url": url_data["url"],
                    "message": url_data["message"]
                })

    if critical_failures:
        print(f"\n⚠️  {len(critical_failures)} CRITICAL FAILURES (government sources):")
        for failure in critical_failures[:10]:
            print(f"  - {failure['dataset']}: {failure['url']} ({failure['message']})")

if __name__ == "__main__":
    main()
