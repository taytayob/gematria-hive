"""
OneTab Links Scraper

Purpose: Parse OneTab shared page and scrape all links from it.
- Extract all 25 links from OneTab shared page
- Scrape each link with appropriate handlers
- Store in scraped_content table

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import re
from typing import List, Dict, Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from scraper import BaseScraper
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

# Logging setup
logging.basicConfig(
    filename='onetab_scraping_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

logger.info("OneTab scraper initialized")


class OneTabScraper:
    """
    Scraper for OneTab shared pages.
    """
    
    def __init__(self, onetab_url: str, delay: float = 2.0):
        """
        Initialize OneTab scraper.
        
        Args:
            onetab_url: URL of OneTab shared page
            delay: Delay between requests (seconds)
        """
        self.onetab_url = onetab_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'GematriaHive/1.0 (Educational Research)'})
        
        logger.info(f"Initialized OneTab scraper for {onetab_url}")
    
    def extract_links_from_onetab(self) -> List[str]:
        """
        Extract all links from OneTab shared page.
        
        Returns:
            List of URLs found on OneTab page
        """
        try:
            response = self.session.get(self.onetab_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            # OneTab pages typically have links in various formats
            # Look for anchor tags
            for tag in soup.find_all('a', href=True):
                href = tag['href']
                if href.startswith('http'):
                    links.append(href)
            
            # Also check for links in text content (OneTab sometimes embeds URLs)
            text = soup.get_text()
            url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
            found_urls = url_pattern.findall(text)
            links.extend(found_urls)
            
            # Remove duplicates and normalize
            unique_links = list(set(links))
            logger.info(f"Extracted {len(unique_links)} unique links from OneTab page")
            
            return unique_links
        
        except Exception as e:
            logger.error(f"Error extracting links from OneTab page: {e}")
            return []
    
    def scrape_link(self, url: str) -> Optional[Dict]:
        """
        Scrape a single link using BaseScraper.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with scraped data or None
        """
        try:
            # Parse domain for base scraper
            from urllib.parse import urlparse
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            
            # Create a temporary scraper for this domain
            scraper = BaseScraper(
                base_url=base_url,
                max_depth=1,  # Only scrape the specific page
                delay=self.delay,
                respect_robots=True
            )
            
            # Scrape the specific page
            scraped = scraper.scrape_page(url, depth=0)
            
            if scraped:
                # Determine source site
                domain = parsed.netloc
                scraped['source_site'] = domain
                
                return scraped
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
        
        return None
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for text content.
        
        Args:
            texts: List of text strings
            batch_size: Batch size for embedding generation
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_embeddings = embed_model.encode(batch, show_progress_bar=False)
            embeddings.extend(batch_embeddings.tolist())
        return embeddings
    
    def extract_tags(self, item: Dict) -> List[str]:
        """
        Extract tags from scraped item based on URL and content.
        
        Args:
            item: Scraped item dictionary
            
        Returns:
            List of tags
        """
        tags = ['onetab', 'scraped']
        url = item.get('url', '').lower()
        source = item.get('source_site', '').lower()
        
        # Tag based on domain
        if 'github' in source:
            tags.append('github')
        if 'wikipedia' in source:
            tags.append('wikipedia')
        if 'gematria' in url or 'gematria' in source:
            tags.append('gematria')
        if 'numerology' in url or 'numerology' in source:
            tags.append('numerology')
        if 'calculator' in url:
            tags.append('calculator')
        if 'bible' in url:
            tags.append('bible')
        if 'kabbalah' in url or 'kabbalah' in source:
            tags.append('kabbalah')
        
        return tags
    
    def store_scraped_content(self, scraped_data: List[Dict]) -> int:
        """
        Store scraped content in Supabase.
        
        Args:
            scraped_data: List of scraped page data
            
        Returns:
            Number of successfully stored items
        """
        if not scraped_data:
            return 0
        
        stored_count = 0
        
        # Prepare data for insertion
        insert_data = []
        for item in scraped_data:
            # Generate embedding for content
            content_text = f"{item.get('title', '')} {item.get('content', '')}"
            try:
                embedding = embed_model.encode(content_text).tolist()
            except Exception as e:
                logger.warning(f"Error generating embedding: {e}")
                embedding = None
            
            # Extract tags
            tags = self.extract_tags(item)
            
            insert_item = {
                'url': item['url'],
                'title': item.get('title', ''),
                'content': item.get('content', ''),
                'content_type': item.get('content_type', 'html'),
                'images': item.get('images', []),
                'links': item.get('links', []),
                'source_site': item.get('source_site', 'unknown'),
                'embedding': embedding,
                'tags': tags,
                'scraped_at': item.get('scraped_at', datetime.utcnow().isoformat())
            }
            
            insert_data.append(insert_item)
        
        # Insert in batches
        batch_size = 50
        for i in range(0, len(insert_data), batch_size):
            batch = insert_data[i:i+batch_size]
            try:
                result = supabase.table('scraped_content').insert(batch).execute()
                stored_count += len(batch)
                logger.info(f"Stored batch of {len(batch)} items to Supabase")
            except Exception as e:
                logger.error(f"Error inserting batch to Supabase: {e}")
                # Try individual inserts as fallback
                for item in batch:
                    try:
                        supabase.table('scraped_content').insert(item).execute()
                        stored_count += 1
                    except Exception as e2:
                        logger.error(f"Error inserting individual item: {e2}")
        
        return stored_count
    
    def scrape_all(self) -> Dict:
        """
        Scrape all links from OneTab page.
        
        Returns:
            Dictionary with scraping results
        """
        logger.info(f"Starting OneTab scraping from {self.onetab_url}")
        
        # Extract links from OneTab page
        links = self.extract_links_from_onetab()
        
        if not links:
            logger.warning("No links found on OneTab page")
            return {'success': False, 'error': 'No links found'}
        
        logger.info(f"Found {len(links)} links to scrape")
        
        # Scrape each link
        scraped_data = []
        for i, link in enumerate(links, 1):
            logger.info(f"Scraping link {i}/{len(links)}: {link}")
            scraped = self.scrape_link(link)
            if scraped:
                scraped_data.append(scraped)
        
        logger.info(f"Scraping complete: {len(scraped_data)}/{len(links)} links scraped successfully")
        
        # Store in database
        stored_count = self.store_scraped_content(scraped_data)
        
        # Log to hunches table
        try:
            hunch_content = f"OneTab scraping: {stored_count}/{len(scraped_data)} pages stored from {len(links)} links"
            supabase.table('hunches').insert({
                'content': hunch_content,
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'completed',
                'cost': 0.0
            }).execute()
        except Exception as e:
            logger.error(f"Error logging hunch: {e}")
        
        return {
            'success': True,
            'links_found': len(links),
            'links_scraped': len(scraped_data),
            'pages_stored': stored_count
        }


def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python scrape_onetab.py <onetab_url> [delay]")
        print("Example: python scrape_onetab.py https://www.one-tab.com/page/... 2.0")
        sys.exit(1)
    
    onetab_url = sys.argv[1]
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    
    print("=" * 60)
    print("Gematria Hive - OneTab Scraper")
    print("=" * 60)
    
    scraper = OneTabScraper(onetab_url=onetab_url, delay=delay)
    results = scraper.scrape_all()
    
    print("\n" + "=" * 60)
    print("Scraping Results:")
    print("=" * 60)
    print(f"Success: {results.get('success', False)}")
    print(f"Links Found: {results.get('links_found', 0)}")
    print(f"Links Scraped: {results.get('links_scraped', 0)}")
    print(f"Pages Stored: {results.get('pages_stored', 0)}")
    print("=" * 60)
    
    if results.get('success'):
        print("\n✅ OneTab scraping complete! Check onetab_scraping_log.txt for details.")
    else:
        print(f"\n❌ OneTab scraping failed: {results.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()

