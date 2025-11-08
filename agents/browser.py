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
from datetime import datetime
from agents.orchestrator import AgentState
from dotenv import load_dotenv

# Import BaseScraper from scraper.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from scraper import BaseScraper
    HAS_SCRAPER = True
except ImportError:
    HAS_SCRAPER = False
    print("Warning: scraper module not available, browser agent disabled")

# Supabase for data persistence
load_dotenv()
try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        HAS_SUPABASE = True
    else:
        HAS_SUPABASE = False
        supabase = None
except Exception:
    HAS_SUPABASE = False
    supabase = None

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
        self.supabase = supabase if HAS_SUPABASE else None
        if not self.supabase:
            logger.warning(f"{self.name}: Supabase not available - data will NOT be persisted!")
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
            
            # SYSTEM-LEVEL RULE: ALL SCRAPED DATA MUST BE STORED IN DATABASE
            # This is a critical requirement - data cannot be lost
            stored_count = self._store_scraped_data(formatted_data, url)
            
            if stored_count == 0 and len(formatted_data) > 0:
                logger.error(f"CRITICAL: Failed to store {len(formatted_data)} scraped pages! Data will be lost!")
                state["status"] = "failed"
                state["error"] = f"Failed to store scraped data - {len(formatted_data)} pages not persisted"
                return state
            
            # Update context
            state["context"]["browser_url"] = url
            state["context"]["browser_pages_scraped"] = len(scraped_data)
            state["context"]["browser_pages_stored"] = stored_count
            state["context"]["browser_images_found"] = len(self.scraper.images)
            state["context"]["browser_links_found"] = len(self.scraper.links)
            
            # Add results
            state["results"].append({
                "agent": self.name,
                "action": "scrape",
                "url": url,
                "pages_scraped": len(scraped_data),
                "pages_stored": stored_count,
                "images_found": len(self.scraper.images),
                "links_found": len(self.scraper.links),
                "max_depth": max_depth,
                "storage_success": stored_count == len(formatted_data)
            })
            
            logger.info(f"Browser scraping complete: {len(scraped_data)} pages scraped, "
                       f"{stored_count} pages stored, {len(self.scraper.images)} images, {len(self.scraper.links)} links")
            
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
    
    def _store_scraped_data(self, formatted_data: List[Dict], base_url: str) -> int:
        """
        Store scraped data in database.
        
        SYSTEM-LEVEL RULE: This method MUST succeed or the entire operation fails.
        Data cannot be scraped without being stored - this wastes resources.
        
        Args:
            formatted_data: List of scraped page data
            base_url: Base URL that was scraped
            
        Returns:
            Number of successfully stored items
        """
        if not self.supabase:
            logger.error("CRITICAL: Supabase not available - cannot store scraped data!")
            return 0
        
        if not formatted_data:
            return 0
        
        stored_count = 0
        
        # Prepare data for insertion into scraped_content table
        insert_data = []
        for item in formatted_data:
            insert_item = {
                'url': item.get('url', ''),
                'title': item.get('title', ''),
                'content': item.get('summary', ''),
                'content_type': item.get('content_type', 'html'),
                'images': item.get('images', []),
                'links': item.get('links', []),
                'source_site': base_url,
                'tags': item.get('tags', []),
                'scraped_at': item.get('scraped_at', datetime.utcnow().isoformat())
            }
            insert_data.append(insert_item)
        
        # Insert in batches
        batch_size = 50
        for i in range(0, len(insert_data), batch_size):
            batch = insert_data[i:i+batch_size]
            try:
                # Use upsert to avoid duplicates (on conflict with url)
                result = self.supabase.table('scraped_content').upsert(
                    batch,
                    on_conflict='url'
                ).execute()
                stored_count += len(batch)
                logger.info(f"✅ Stored batch of {len(batch)} scraped pages ({stored_count}/{len(insert_data)})")
            except Exception as e:
                logger.error(f"Error inserting batch to scraped_content: {e}")
                # Try individual inserts as fallback
                for item in batch:
                    try:
                        self.supabase.table('scraped_content').upsert(
                            item,
                            on_conflict='url'
                        ).execute()
                        stored_count += 1
                    except Exception as e2:
                        logger.error(f"Error inserting individual scraped page {item.get('url', 'unknown')}: {e2}")
        
        if stored_count != len(insert_data):
            logger.error(f"CRITICAL: Only stored {stored_count}/{len(insert_data)} pages! Data loss occurred!")
        
        return stored_count
    
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

