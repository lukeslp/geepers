#!/usr/bin/env python3
"""
Wolfram Alpha Computational Knowledge Engine Client

Description: Client for querying Wolfram Alpha's computational knowledge engine with
             support for multiple response formats (plaintext, image, MathML) and
             both JSON and XML parsing.

Use Cases:
- Mathematical computations and equation solving
- Scientific calculations and unit conversions
- Data lookups and fact queries
- Knowledge base integration for AI applications

Dependencies:
- requests

Notes:
- Requires Wolfram Alpha App ID (free tier available)
- Supports plaintext, image, and MathML output formats
- Handles both JSON and XML API responses
- Includes simplified result extraction for quick answers
- Pod structure preserves categorized results (Input, Result, Solution, etc.)

Related Snippets:
- api-clients/multi_provider_abstraction.py

Source Attribution:
- Extracted from: /home/coolhand/inbox/apis/llamni/utils/wolfram_alpha.py
- Author: Luke Steuber
"""

import logging
import requests
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


def query_wolfram_alpha(query: str, app_id: str, format: str = 'plaintext') -> Dict[str, Any]:
    """
    Query the Wolfram Alpha computational knowledge engine.

    Args:
        query: Query to send to Wolfram Alpha
        app_id: Wolfram Alpha Application ID/API Key
        format: Result format ('plaintext', 'image', 'mathml')

    Returns:
        Dictionary with query results containing:
        - query: Original query string
        - success: Boolean indicating if query succeeded
        - results: List of pods with title and values
        - warnings: Optional list of warnings
        - assumptions: Optional list of query assumptions
    """
    if not app_id:
        raise ValueError("Wolfram Alpha App ID is required")

    valid_formats = {'plaintext', 'image', 'mathml'}
    if format not in valid_formats:
        format = 'plaintext'

    base_url = "https://api.wolframalpha.com/v2/query"
    params = {
        'input': query,
        'appid': app_id,
        'format': format,
        'output': 'json' if format == 'plaintext' else 'xml',
        'podtimeout': 5
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()

        if format == 'plaintext' and params['output'] == 'json':
            data = response.json()
            return _parse_json_response(data, query)
        else:
            root = ET.fromstring(response.content)
            return _parse_xml_response(root, query, format)

    except requests.RequestException as e:
        logger.error(f"Error querying Wolfram Alpha: {str(e)}")
        return {
            "query": query,
            "success": False,
            "error": f"API request failed: {str(e)}",
            "results": []
        }
    except Exception as e:
        logger.error(f"Error processing Wolfram Alpha response: {str(e)}")
        return {
            "query": query,
            "success": False,
            "error": f"Response processing failed: {str(e)}",
            "results": []
        }


def _parse_json_response(data: Dict[str, Any], query: str) -> Dict[str, Any]:
    """Parse JSON response from Wolfram Alpha API."""
    result = {
        "query": query,
        "success": False,
        "results": []
    }

    if 'queryresult' in data:
        queryresult = data['queryresult']
        result['success'] = queryresult.get('success', False)

        if 'pods' in queryresult:
            for pod in queryresult['pods']:
                pod_data = {
                    "title": pod.get('title', ''),
                    "values": []
                }

                if 'subpods' in pod:
                    for subpod in pod['subpods']:
                        if 'plaintext' in subpod:
                            text = subpod.get('plaintext', '')
                            if text:
                                pod_data['values'].append(text)

                if pod_data['values']:
                    result['results'].append(pod_data)

        if 'warnings' in queryresult:
            result['warnings'] = queryresult['warnings']

        if 'assumptions' in queryresult:
            result['assumptions'] = queryresult['assumptions']

    return result


def _parse_xml_response(root: ET.Element, query: str, format: str) -> Dict[str, Any]:
    """Parse XML response from Wolfram Alpha API."""
    result = {
        "query": query,
        "success": False,
        "results": []
    }

    success = root.get('success')
    result['success'] = success == 'true'

    for pod in root.findall('.//pod'):
        pod_data = {
            "title": pod.get('title', ''),
            "values": []
        }

        for subpod in pod.findall('.//subpod'):
            if format == 'plaintext':
                plaintext = subpod.find('.//plaintext')
                if plaintext is not None and plaintext.text:
                    pod_data['values'].append(plaintext.text)

            elif format == 'mathml':
                mathml = subpod.find('.//mathml')
                if mathml is not None:
                    mathml_str = ET.tostring(mathml, encoding='unicode')
                    pod_data['values'].append(mathml_str)

            elif format == 'image':
                img = subpod.find('.//img')
                if img is not None:
                    img_src = img.get('src', '')
                    if img_src:
                        pod_data['values'].append(img_src)

        if pod_data['values']:
            result['results'].append(pod_data)

    # Extract warnings
    warnings = root.find('.//warnings')
    if warnings is not None:
        result['warnings'] = []
        for warning in warnings.findall('.//warning'):
            text = warning.find('.//text')
            if text is not None and text.text:
                result['warnings'].append(text.text)

    # Extract assumptions
    assumptions = root.find('.//assumptions')
    if assumptions is not None:
        result['assumptions'] = []
        for assumption in assumptions.findall('.//assumption'):
            assumption_data = {
                "type": assumption.get('type', ''),
                "values": []
            }
            for value in assumption.findall('.//value'):
                assumption_data['values'].append({
                    "name": value.get('name', ''),
                    "description": value.get('desc', '')
                })
            result['assumptions'].append(assumption_data)

    return result


def get_simple_result(query: str, app_id: str) -> str:
    """
    Get a simplified result from Wolfram Alpha, with just the primary output.

    Args:
        query: Query to send to Wolfram Alpha
        app_id: Wolfram Alpha Application ID/API Key

    Returns:
        Primary result as string, or error message
    """
    try:
        result = query_wolfram_alpha(query, app_id)

        if result['success'] and result['results']:
            # Look for Result or Solution pod first
            for pod in result['results']:
                if pod['title'] in ['Result', 'Solution', 'Value']:
                    return pod['values'][0]

            # Fall back to first pod
            return result['results'][0]['values'][0]
        else:
            if 'error' in result:
                return f"Error: {result['error']}"
            else:
                return "No results found"
    except Exception as e:
        logger.error(f"Error getting simple result: {str(e)}")
        return f"Error: {str(e)}"


# Usage example
if __name__ == "__main__":
    import os

    # Get API key from environment
    app_id = os.environ.get('WOLFRAM_ALPHA_APP_ID', 'DEMO')

    # Example queries
    queries = [
        "2+2",
        "derivative of x^2",
        "population of France",
        "convert 100 miles to km"
    ]

    print("Wolfram Alpha Client Demo")
    print("=" * 50)

    if app_id == 'DEMO':
        print("Note: Set WOLFRAM_ALPHA_APP_ID environment variable for actual queries")
        print("Demo mode - showing expected output structure:\n")

        # Show expected structure
        demo_result = {
            "query": "2+2",
            "success": True,
            "results": [
                {"title": "Input", "values": ["2 + 2"]},
                {"title": "Result", "values": ["4"]}
            ]
        }
        print(f"Query: {demo_result['query']}")
        print(f"Success: {demo_result['success']}")
        for pod in demo_result['results']:
            print(f"  {pod['title']}: {pod['values']}")
    else:
        for query in queries:
            print(f"\nQuery: {query}")

            # Full result
            result = query_wolfram_alpha(query, app_id)
            if result['success']:
                for pod in result['results']:
                    print(f"  {pod['title']}: {pod['values']}")
            else:
                print(f"  Error: {result.get('error', 'Unknown error')}")

            # Simple result
            simple = get_simple_result(query, app_id)
            print(f"  Simple answer: {simple}")
