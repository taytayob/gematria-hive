"""
Browser Agent

Purpose: Web scraping and browser automation using BaseScraper
- Sitemap discovery and parsing
- Recursive page crawling with depth limits
- Image extraction and storage
- Link discovery and queue management
- Rate limiting and respectful scraping

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import os
import sys
from typing import Dict, List, Optional
from agents.orchestrator import AgentState

# Import BaseScraper from scraper.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from scraper import BaseScraper
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False
    print("Warning: scraper module not available, browser agent disabled")

logger = logging.getLogger(__name__)


class BrowserAgent:
    """
    Browser Agent - Web scraping and browser automation
    
    Operations:
    - Scrape websites using BaseScraper
    - Discover and parse sitemaps
    - Extract images, links, and text content
    - Respect robots.txt and rate limits
    - Crawl recursively with depth limits
    """
    
    def __init__(self):
        """Initialize browser agent"""
        self.name = "browser_agent"
        self.scraper: Optional[BaseScraper] = None
        logger.info(f"Initialized {self.name}")
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute browser/scraping task
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with scraped data
        """
        if not HAS_SCRAPER:
            logger.error("Scraper module not available")
            state["status"] = "failed"
            state["error"] = "Scraper module not available"
            return state
        
        task = state.get("task", {})
        url = task.get("url", "")
        max_depth = task.get("max_depth", 3)
        delay = task.get("delay", 1.0)
        use_sitemap = task.get("use_sitemap", True)
        respect_robots = task.get("respect_robots", True)
        
        if not url:
            logger.error("No URL provided in task")
            state["status"] = "failed"
            state["error"] = "No URL provided"
            return state
        
        logger.info(f"Browser agent: Scraping {url} (depth: {max_depth}, delay: {delay})")
        
        try:
            # Initialize scraper
            self.scraper = BaseScraper(
                base_url=url,
                max_depth=max_depth,
                delay=delay,
                respect_robots=respect_robots,
                user_agent="GematriaHive/1.0 (Educational Research)"
            )
            
            # Start crawling
            scraped_data = self.scraper.crawl(start_url=url, use_sitemap=use_sitemap)
            
            # Convert scraped data to format compatible with ingestion pipeline
            formatted_data = []
            for item in scraped_data:
                formatted_item = {
                    'url': item.get('url', ''),
                    'summary': item.get('content', ''),
                    'title': item.get('title', ''),
                    'content_type': item.get('content_type', 'html'),
                    'images': item.get('images', []),
                    'links': item.get('links', []),
                    'tags': [],  # Will be categorized by ingestion
                    'scraped_at': item.get('scraped_at', '')
                }
                formatted_data.append(formatted_item)
            
            # Add to state data
            existing_data = state.get("data", [])
            state["data"] = existing_data + formatted_data
            
            # Update context
            state["context"]["browser_url"] = url
            state["context"]["browser_pages_scraped"] = len(scraped_data)
            state["context"]["browser_images_found"] = len(self.scraper.images)
            state["context"]["browser_links_found"] = len(self.scraper.links)
            
            # Add results
            state["results"].append({
                "agent": self.name,
                "action": "scrape",
                "url": url,
                "pages_scraped": len(scraped_data),
                "images_found": len(self.scraper.images),
                "links_found": len(self.scraper.links),
                "max_depth": max_depth
            })
            
            logger.info(f"Browser scraping complete: {len(scraped_data)} pages scraped, "
                       f"{len(self.scraper.images)} images, {len(self.scraper.links)} links")
            
        except Exception as e:
            logger.error(f"Browser scraping error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state
    
    def scrape_url(self, url: str, max_depth: int = 3, delay: float = 1.0, 
                   use_sitemap: bool = True, respect_robots: bool = True) -> List[Dict]:
        """
        Convenience method to scrape a single URL
        
        Args:
            url: URL to scrape
            max_depth: Maximum crawl depth
            delay: Delay between requests
            use_sitemap: Whether to use sitemap if available (default: True)
            respect_robots: Whether to respect robots.txt (default: True)
            
        Returns:
            List of scraped data dictionaries
        """
        if not HAS_SCRAPER:
            logger.error("Scraper module not available")
            return []
        
        try:
            scraper = BaseScraper(
                base_url=url,
                max_depth=max_depth,
                delay=delay,
                respect_robots=respect_robots,
                user_agent="GematriaHive/1.0 (Educational Research)"
            )
            return scraper.crawl(start_url=url, use_sitemap=use_sitemap)
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return []
    
    def find_sitemap(self, url: str) -> Optional[str]:
        """
        Find sitemap for a given URL
        
        Args:
            url: Base URL to check for sitemap
            
        Returns:
            Sitemap URL or None
        """
        if not HAS_SCRAPER:
            return None
        
        try:
            scraper = BaseScraper(base_url=url)
            return scraper.find_sitemap()
        except Exception as e:
            logger.error(f"Error finding sitemap for {url}: {e}")
            return None
    
    def parse_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Parse sitemap and extract URLs
        
        Args:
            sitemap_url: URL of sitemap
            
        Returns:
            List of URLs from sitemap
        """
        if not HAS_SCRAPER:
            return []
        
        try:
            scraper = BaseScraper(base_url=sitemap_url)
            return scraper.parse_sitemap(sitemap_url)
        except Exception as e:
            logger.error(f"Error parsing sitemap {sitemap_url}: {e}")
            return []

