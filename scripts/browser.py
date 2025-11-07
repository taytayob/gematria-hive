#!/usr/bin/env python3
"""
Browser Agent CLI Script

Purpose: Standalone CLI script for running the browser agent.
Scrapes websites and extracts content.

Usage:
    python scripts/browser.py --url https://example.com
    python scripts/browser.py --url https://example.com --max-depth 2 --output scraped.json

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import json
import argparse
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.browser import BrowserAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Scrape websites using Browser Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape a single URL
  python scripts/browser.py --url https://example.com
  
  # Scrape with custom depth and save output
  python scripts/browser.py --url https://example.com --max-depth 2 --output scraped.json
        """
    )
    
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL to scrape"
    )
    
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum crawl depth (default: 3)"
    )
    
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output JSON file path (optional)"
    )
    
    parser.add_argument(
        "--no-use-sitemap",
        action="store_false",
        dest="use_sitemap",
        default=True,
        help="Disable sitemap usage (default: enabled)"
    )
    
    parser.add_argument(
        "--no-respect-robots",
        action="store_false",
        dest="respect_robots",
        default=True,
        help="Disable robots.txt respect (default: enabled)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize agent
    logger.info("Initializing Browser Agent...")
    agent = BrowserAgent()
    
    # Scrape URL
    logger.info(f"Scraping {args.url} (max_depth: {args.max_depth}, delay: {args.delay}, "
                f"use_sitemap: {args.use_sitemap}, respect_robots: {args.respect_robots})")
    scraped_data = agent.scrape_url(
        url=args.url,
        max_depth=args.max_depth,
        delay=args.delay,
        use_sitemap=args.use_sitemap,
        respect_robots=args.respect_robots
    )
    
    if not scraped_data:
        logger.error("No data scraped")
        sys.exit(1)
    
    logger.info(f"Successfully scraped {len(scraped_data)} pages")
    
    # Save output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(scraped_data, f, indent=2)
        
        logger.info(f"Scraped data written to {args.output}")
    else:
        # Print to stdout
        print(json.dumps(scraped_data, indent=2))
    
    logger.info("Browser scraping complete")


if __name__ == "__main__":
    main()

