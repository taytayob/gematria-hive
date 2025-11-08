#!/usr/bin/env python3
"""
Get API Keys Using Browser Agent

Purpose: Use browser agent to navigate to Google services and extract
API key setup information.

Usage:
    python scripts/get_api_keys_with_browser.py

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.browser import BrowserAgent
from agents.orchestrator import AgentState
from agents.gemini_research import GeminiResearchAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_google_ai_studio():
    """Scrape Google AI Studio for API key information"""
    logger.info("=" * 70)
    logger.info("Scraping Google AI Studio (https://ai.google.dev)")
    logger.info("=" * 70)
    
    browser = BrowserAgent()
    
    state = {
        'task': {
            'type': 'browser',
            'url': 'https://ai.google.dev',
            'max_depth': 2,
            'delay': 2.0,
            'use_sitemap': False,
            'respect_robots': True
        },
        'data': [],
        'context': {},
        'results': [],
        'cost': 0.0,
        'status': 'pending',
        'memory_id': None
    }
    
    result = browser.execute(state)
    
    if result.get('status') == 'success':
        logger.info(f"✅ Successfully scraped {len(result.get('data', []))} pages")
        return result.get('data', [])
    else:
        logger.error(f"❌ Failed to scrape: {result.get('error', 'Unknown error')}")
        return []


def scrape_google_cloud_console():
    """Scrape Google Cloud Console for OAuth setup information"""
    logger.info("=" * 70)
    logger.info("Scraping Google Cloud Console (https://console.cloud.google.com)")
    logger.info("=" * 70)
    
    browser = BrowserAgent()
    
    # Try to scrape the API library page
    state = {
        'task': {
            'type': 'browser',
            'url': 'https://console.cloud.google.com/apis/library',
            'max_depth': 1,
            'delay': 2.0,
            'use_sitemap': False,
            'respect_robots': True
        },
        'data': [],
        'context': {},
        'results': [],
        'cost': 0.0,
        'status': 'pending',
        'memory_id': None
    }
    
    result = browser.execute(state)
    
    if result.get('status') == 'success':
        logger.info(f"✅ Successfully scraped {len(result.get('data', []))} pages")
        return result.get('data', [])
    else:
        logger.warning(f"⚠️  May require authentication: {result.get('error', 'Unknown error')}")
        return []


def extract_api_key_info(scraped_data):
    """Extract API key setup information from scraped data"""
    logger.info("=" * 70)
    logger.info("Extracting API key setup information...")
    logger.info("=" * 70)
    
    info = {
        'links': [],
        'instructions': [],
        'keywords': []
    }
    
    for page in scraped_data:
        content = page.get('content', '').lower()
        title = page.get('title', '')
        url = page.get('url', '')
        
        # Look for API key related content
        if 'api key' in content or 'api key' in title.lower():
            info['links'].append(url)
            info['keywords'].append('api key')
        
        if 'get started' in content or 'get api key' in content:
            info['instructions'].append(f"Found setup info at: {url}")
    
    return info


def main():
    """Main function"""
    logger.info("=" * 70)
    logger.info("Getting API Keys Using Browser Agent")
    logger.info("=" * 70)
    logger.info()
    
    # Scrape Google AI Studio
    logger.info("Step 1: Scraping Google AI Studio...")
    ai_studio_data = scrape_google_ai_studio()
    logger.info()
    
    # Extract information
    if ai_studio_data:
        info = extract_api_key_info(ai_studio_data)
        logger.info(f"Found {len(info['links'])} relevant pages")
        for link in info['links'][:5]:  # Show first 5
            logger.info(f"  - {link}")
    logger.info()
    
    # Scrape Google Cloud Console (may require auth)
    logger.info("Step 2: Scraping Google Cloud Console...")
    cloud_data = scrape_google_cloud_console()
    logger.info()
    
    # Summary
    logger.info("=" * 70)
    logger.info("Summary")
    logger.info("=" * 70)
    logger.info()
    logger.info("✅ Browser agent can scrape public pages")
    logger.info("⚠️  Google Cloud Console may require authentication")
    logger.info()
    logger.info("Next Steps:")
    logger.info("1. Open https://ai.google.dev in your browser")
    logger.info("2. Click 'Get API Key' button")
    logger.info("3. Copy the API key")
    logger.info("4. Add to .env: GOOGLE_API_KEY=your-key-here")
    logger.info()
    logger.info("For Google Drive OAuth:")
    logger.info("1. Open https://console.cloud.google.com in your browser")
    logger.info("2. Create project and enable Drive API")
    logger.info("3. Create OAuth credentials")
    logger.info("4. See BROWSER_SETUP_GUIDE.md for detailed steps")
    logger.info()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

