"""
Gematrix.org Specific Scraper

Purpose: Scrape gematrix.org website including:
- Sitemap discovery
- Database/Numerology pages
- Statistics pages
- Gematria Types pages (Jewish, Hebrew, Latin, English, Simple)
- Calculator pages and documentation
- All subpages and linked content
- Image extraction and storage

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

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
    filename='gematrix_scraping_log.txt',
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

logger.info("Gematrix.org scraper initialized")


class GematrixScraper(BaseScraper):
    """
    Specialized scraper for gematrix.org
    """
    
    def __init__(self, max_depth: int = 5, delay: float = 2.0):
        """
        Initialize Gematrix scraper.
        
        Args:
            max_depth: Maximum crawling depth
            delay: Delay between requests (seconds)
        """
        super().__init__(
            base_url='https://www.gematrix.org',
            max_depth=max_depth,
            delay=delay,
            respect_robots=True,
            user_agent="GematriaHive/1.0 (Educational Research)"
        )
        
        # Priority pages to scrape first
        self.priority_pages = [
            '/',
            '/gematria-database',
            '/gematria-database-numerology',
            '/gematria-statistics',
            '/gematria-types',
            '/jewish-gematria',
            '/hebrew-gematria',
            '/latin-gematria',
            '/english-gematria',
            '/simple-gematria',
            '/peters-gematria-site',
            '/bible-codes',
            '/new-testament',
            '/hebrew-gematria-calculator',
            '/hebrew-gematria-wikipedia',
            '/jewish-kabbalah-hebrew',
            '/jewish-cabbala',
            '/chabad',
            '/numerology',
            '/about-gematria-calculator',
            '/gematria-calculator',
        ]
        
        logger.info("Gematrix scraper initialized with priority pages")
    
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
            
            # Extract tags from URL and content
            tags = self.extract_tags(item)
            
            insert_item = {
                'url': item['url'],
                'title': item.get('title', ''),
                'content': item.get('content', ''),
                'content_type': item.get('content_type', 'html'),
                'images': item.get('images', []),
                'links': item.get('links', []),
                'source_site': 'gematrix.org',
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
    
    def extract_tags(self, item: Dict) -> List[str]:
        """
        Extract tags from scraped item based on URL and content.
        
        Args:
            item: Scraped item dictionary
            
        Returns:
            List of tags
        """
        tags = ['gematrix.org', 'scraped']
        url = item.get('url', '').lower()
        
        # Tag based on URL patterns
        if 'database' in url or 'numerology' in url:
            tags.append('database')
            tags.append('numerology')
        if 'statistics' in url:
            tags.append('statistics')
        if 'jewish' in url:
            tags.append('jewish-gematria')
        if 'hebrew' in url:
            tags.append('hebrew-gematria')
        if 'latin' in url:
            tags.append('latin-gematria')
        if 'english' in url:
            tags.append('english-gematria')
        if 'simple' in url:
            tags.append('simple-gematria')
        if 'calculator' in url:
            tags.append('calculator')
        if 'bible' in url or 'testament' in url:
            tags.append('bible')
        if 'kabbalah' in url or 'cabbala' in url:
            tags.append('kabbalah')
        if 'chabad' in url:
            tags.append('chabad')
        if 'peter' in url:
            tags.append('peters-site')
        
        return tags
    
    def scrape_all(self) -> Dict:
        """
        Scrape all content from gematrix.org.
        
        Returns:
            Dictionary with scraping results
        """
        logger.info("Starting comprehensive scrape of gematrix.org")
        
        # Add priority pages to queue first
        for page in self.priority_pages:
            full_url = self.normalize_url(page)
            if full_url not in self.visited_urls:
                self.url_queue.append((full_url, 0))
        
        # Start crawling
        scraped_data = self.crawl(use_sitemap=True)
        
        logger.info(f"Scraping complete: {len(scraped_data)} pages scraped")
        logger.info(f"Total images found: {len(self.images)}")
        logger.info(f"Total links found: {len(self.links)}")
        
        # Store in database
        stored_count = self.store_scraped_content(scraped_data)
        
        # Log to hunches table
        try:
            hunch_content = f"Gematrix.org scraping: {stored_count}/{len(scraped_data)} pages stored, {len(self.images)} images, {len(self.links)} links"
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
            'pages_scraped': len(scraped_data),
            'pages_stored': stored_count,
            'images_found': len(self.images),
            'links_found': len(self.links),
            'visited_urls': len(self.visited_urls)
        }


def main():
    """Main function for command-line usage."""
    import sys
    
    max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    
    print("=" * 60)
    print("Gematria Hive - Gematrix.org Scraper")
    print("=" * 60)
    
    scraper = GematrixScraper(max_depth=max_depth, delay=delay)
    results = scraper.scrape_all()
    
    print("\n" + "=" * 60)
    print("Scraping Results:")
    print("=" * 60)
    print(f"Success: {results.get('success', False)}")
    print(f"Pages Scraped: {results.get('pages_scraped', 0)}")
    print(f"Pages Stored: {results.get('pages_stored', 0)}")
    print(f"Images Found: {results.get('images_found', 0)}")
    print(f"Links Found: {results.get('links_found', 0)}")
    print(f"Visited URLs: {results.get('visited_urls', 0)}")
    print("=" * 60)
    
    if results.get('success'):
        print("\n✅ Gematrix.org scraping complete! Check gematrix_scraping_log.txt for details.")
    else:
        print("\n❌ Gematrix.org scraping failed.")


if __name__ == "__main__":
    main()

