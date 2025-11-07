#!/usr/bin/env python3
"""
Execute All Ingestions Concurrently

Purpose: Pull data from all available sources and ingest concurrently
- Pull from database
- Scrape websites
- Import CSV files
- Process bookmarks
- Run all ingestion agents concurrently

Author: Gematria Hive Team
Date: November 7, 2025
"""

import sys
import os
import asyncio
import concurrent.futures
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ingestion_execution.log')
    ]
)
logger = logging.getLogger(__name__)


def pull_from_database() -> List[Dict]:
    """Pull all data from database tables"""
    logger.info("📊 Pulling data from database...")
    
    try:
        from supabase import create_client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            logger.error("❌ Supabase credentials not configured")
            return []
        
        supabase = create_client(supabase_url, supabase_key)
        
        all_data = []
        
        # Pull from all tables concurrently
        tables = ['bookmarks', 'gematria_words', 'sources', 'patterns', 'hunches']
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(tables)) as executor:
            futures = {}
            for table in tables:
                future = executor.submit(
                    lambda t: supabase.table(t).select('*').limit(1000).execute(),
                    table
                )
                futures[future] = table
            
            for future in concurrent.futures.as_completed(futures):
                table = futures[future]
                try:
                    result = future.result()
                    data = result.data if result.data else []
                    for item in data:
                        item['_source'] = table
                        all_data.append(item)
                    logger.info(f"✅ Pulled {len(data)} items from {table}")
                except Exception as e:
                    logger.warning(f"⚠️  Error pulling from {table}: {e}")
        
        logger.info(f"✅ Total data pulled: {len(all_data)} items")
        return all_data
        
    except Exception as e:
        logger.error(f"❌ Error pulling from database: {e}")
        return []


def scrape_websites() -> List[Dict]:
    """Scrape gematria-related websites concurrently"""
    logger.info("🌐 Scraping websites...")
    
    try:
        from agents.browser import BrowserAgent
        
        browser = BrowserAgent()
        
        # List of gematria-related URLs to scrape
        urls = [
            "https://www.gematrix.org",
            "https://www.gematrinator.com",
        ]
        
        scraped_data = []
        
        # Scrape all URLs concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
            futures = {}
            for url in urls:
                future = executor.submit(browser.scrape_url, url, max_depth=2, delay=1.0)
                futures[future] = url
            
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                try:
                    result = future.result()
                    if result:
                        scraped_data.extend(result)
                        logger.info(f"✅ Scraped {len(result)} pages from {url}")
                except Exception as e:
                    logger.warning(f"⚠️  Error scraping {url}: {e}")
        
        logger.info(f"✅ Total scraped: {len(scraped_data)} pages")
        return scraped_data
        
    except Exception as e:
        logger.error(f"❌ Error scraping websites: {e}")
        return []


def ingest_csv_files() -> List[Dict]:
    """Ingest CSV files concurrently"""
    logger.info("📄 Ingesting CSV files...")
    
    try:
        from agents.ingestion import IngestionAgent
        
        ingestion = IngestionAgent()
        
        # Find CSV files in current directory
        csv_files = list(Path('.').glob('*.csv'))
        
        if not csv_files:
            logger.info("ℹ️  No CSV files found")
            return []
        
        all_data = []
        
        # Ingest all CSV files concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(csv_files)) as executor:
            futures = {}
            for csv_file in csv_files:
                future = executor.submit(ingestion.ingest_csv_file, str(csv_file))
                futures[future] = csv_file
            
            for future in concurrent.futures.as_completed(futures):
                csv_file = futures[future]
                try:
                    result = future.result()
                    if result.get('success'):
                        ingested = result.get('total_ingested', 0)
                        all_data.append({
                            'file': str(csv_file),
                            'ingested': ingested,
                            'status': 'success'
                        })
                        logger.info(f"✅ Ingested {ingested} rows from {csv_file}")
                except Exception as e:
                    logger.warning(f"⚠️  Error ingesting {csv_file}: {e}")
        
        logger.info(f"✅ Total CSV files processed: {len(all_data)}")
        return all_data
        
    except Exception as e:
        logger.error(f"❌ Error ingesting CSV files: {e}")
        return []


def process_bookmarks() -> List[Dict]:
    """Process bookmarks concurrently"""
    logger.info("🔖 Processing bookmarks...")
    
    try:
        from agents.bookmark_ingestion import BookmarkIngestionAgent
        
        bookmark_agent = BookmarkIngestionAgent()
        
        # Process bookmarks
        result = bookmark_agent.process_bookmarks()
        
        if result.get('success'):
            processed = result.get('bookmarks_processed', 0)
            logger.info(f"✅ Processed {processed} bookmarks")
            return result.get('bookmarks', [])
        else:
            logger.warning(f"⚠️  Bookmark processing failed: {result.get('error')}")
            return []
        
    except Exception as e:
        logger.error(f"❌ Error processing bookmarks: {e}")
        return []


def run_all_ingestions_concurrently() -> Dict:
    """Run all ingestion methods concurrently"""
    logger.info("=" * 60)
    logger.info("EXECUTING ALL INGESTIONS CONCURRENTLY")
    logger.info("=" * 60)
    
    start_time = datetime.now()
    
    # Run all ingestion methods concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(pull_from_database): "database",
            executor.submit(scrape_websites): "websites",
            executor.submit(ingest_csv_files): "csv_files",
            executor.submit(process_bookmarks): "bookmarks"
        }
        
        results = {}
        for future in concurrent.futures.as_completed(futures):
            source = futures[future]
            try:
                data = future.result()
                results[source] = data
                logger.info(f"✅ {source} completed: {len(data)} items")
            except Exception as e:
                logger.error(f"❌ {source} failed: {e}")
                results[source] = []
    
    # Combine all results
    all_data = []
    for source, data in results.items():
        for item in data:
            if isinstance(item, dict):
                item['_ingestion_source'] = source
                all_data.append(item)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("INGESTION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"⏱️  Duration: {duration:.2f} seconds")
    logger.info(f"📊 Total Items: {len(all_data)}")
    for source, data in results.items():
        logger.info(f"   - {source}: {len(data)} items")
    logger.info("")
    
    return {
        "total_items": len(all_data),
        "sources": results,
        "all_data": all_data,
        "duration": duration,
        "timestamp": datetime.now().isoformat()
    }


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("CONCURRENT INGESTION EXECUTION")
    logger.info("=" * 60)
    logger.info("")
    
    # Run all ingestions concurrently
    results = run_all_ingestions_concurrently()
    
    # Save results
    results_file = f"ingestion_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"📄 Results saved to: {results_file}")
    except Exception as e:
        logger.warning(f"⚠️  Could not save results: {e}")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("✅ INGESTION EXECUTION COMPLETE!")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

