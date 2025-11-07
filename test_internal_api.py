#!/usr/bin/env python3
"""
Test Internal API

Test script for internal API endpoints.

Usage:
    python test_internal_api.py [--base-url URL] [--api-key KEY]

Author: Gematria Hive Team
Date: January 6, 2025
"""

import argparse
import requests
import json
import sys
import os
from typing import Optional

def test_health_check(base_url: str) -> bool:
    """Test health check endpoint (no auth required)"""
    try:
        response = requests.get(f"{base_url}/internal/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Components: {data.get('components', {})}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_list_agents(base_url: str, api_key: str) -> bool:
    """Test list agents endpoint"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{base_url}/internal/agents", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            agents = data.get("agents", [])
            print(f"✅ List agents passed: {len(agents)} agents found")
            for agent in agents[:5]:  # Show first 5
                print(f"   - {agent.get('name')}: {agent.get('description', '')[:50]}")
            return True
        else:
            print(f"❌ List agents failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ List agents error: {e}")
        return False

def test_list_tools(base_url: str, api_key: str) -> bool:
    """Test list tools endpoint"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{base_url}/internal/tools", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            tools = data.get("tools", [])
            print(f"✅ List tools passed: {len(tools)} tools found")
            for tool in tools[:5]:  # Show first 5
                print(f"   - {tool.get('name')}: {tool.get('description', '')[:50]}")
            return True
        else:
            print(f"❌ List tools failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ List tools error: {e}")
        return False

def test_get_cost(base_url: str, api_key: str) -> bool:
    """Test get current cost endpoint"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{base_url}/internal/cost/current", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Get cost passed")
            print(f"   Total cost: ${data.get('total_cost', 0):.2f}")
            print(f"   Daily cost: ${data.get('daily_cost', 0):.2f}")
            print(f"   Remaining budget: ${data.get('remaining_budget', 0):.2f}")
            return True
        else:
            print(f"❌ Get cost failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Get cost error: {e}")
        return False

def main():
    """Main test function"""
    parser = argparse.ArgumentParser(description="Test Internal API")
    parser.add_argument(
        "--base-url",
        type=str,
        default=os.getenv("INTERNAL_API_URL", "http://localhost:8001"),
        help="Base URL for internal API (default: http://localhost:8001)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.getenv("INTERNAL_API_KEY", "internal-api-key-change-in-production"),
        help="API key for authentication"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧪 Testing Internal API")
    print("=" * 60)
    print(f"Base URL: {args.base_url}")
    print(f"API Key: {'*' * 20}")
    print("=" * 60)
    print()
    
    results = []
    
    # Test health check (no auth)
    print("1. Testing health check (no auth)...")
    results.append(("Health Check", test_health_check(args.base_url)))
    print()
    
    # Test list agents (requires auth)
    print("2. Testing list agents (requires auth)...")
    results.append(("List Agents", test_list_agents(args.base_url, args.api_key)))
    print()
    
    # Test list tools (requires auth)
    print("3. Testing list tools (requires auth)...")
    results.append(("List Tools", test_list_tools(args.base_url, args.api_key)))
    print()
    
    # Test get cost (requires auth)
    print("4. Testing get cost (requires auth)...")
    results.append(("Get Cost", test_get_cost(args.base_url, args.api_key)))
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())

