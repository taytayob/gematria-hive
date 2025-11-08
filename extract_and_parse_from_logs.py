#!/usr/bin/env python3
"""
Extract URLs from Logs and Parse Gematrix Pages

Purpose: Extract URLs from log files, fetch pages, and parse structured data
- Extract URLs from ingestion_execution.log
- Fetch pages from gematrix.org
- Parse structured data (words, values, tables, page numbers)
- Store in database

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
import re
import logging
import requests
import urllib.parse
import time
from typing import Dict, List, Set, Optional
from datetime import datetime
from bs4 import BeautifulSoup

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from parse_gematrix_pages import parse_gematrix_page

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Supabase client
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
        logger.warning("Supabase not configured")
except Exception:
    HAS_SUPABASE = False
    supabase = None
    logger.warning("Supabase not available")


def extract_urls_from_log(log_file: str) -> List[str]:
    """
    Extract URLs from log file.
    
    Args:
        log_file: Path to log file
        
    Returns:
        List of unique URLs
    """
    urls = []
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                # Look for "Fetched https://..." lines
                match = re.search(r'Fetched (https://[^\s]+)', line)
                if match:
                    url = match.group(1)
                    if 'gematrix.org' in url:
                        urls.append(url)
    except Exception as e:
        logger.error(f"Error reading log file {log_file}: {e}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    return unique_urls


def fetch_and_parse_url(url: str, delay: float = 1.0) -> Optional[Dict]:
    """
    Fetch a URL and parse it.
    
    Args:
        url: URL to fetch
        delay: Delay between requests
        
    Returns:
        Parsed data dictionary or None
    """
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'GematriaHive/1.0 (Educational Research)'
        })
        response.raise_for_status()
        
        # Parse the page
        parsed_data = parse_gematrix_page(response.text, url)
        
        # Store in scraped_content table
        if supabase:
            try:
                supabase.table('scraped_content').upsert({
                    'url': url,
                    'title': parsed_data.get('search_term', ''),
                    'content': response.text,
                    'content_type': 'html',
                    'source_site': 'gematrix.org',
                    'scraped_at': datetime.utcnow().isoformat()
                }, on_conflict='url').execute()
            except Exception as e:
                logger.warning(f"Error storing scraped content for {url}: {e}")
        
        time.sleep(delay)  # Be respectful
        return parsed_data
        
    except Exception as e:
        logger.error(f"Error fetching/parsing {url}: {e}")
        return None


def process_urls_from_logs(log_file: str, limit: int = 100, delay: float = 1.0) -> Dict:
    """
    Process URLs from log file.
    
    Args:
        log_file: Path to log file
        limit: Maximum number of URLs to process
        delay: Delay between requests
        
    Returns:
        Dictionary with processing results
    """
    logger.info(f"📄 Extracting URLs from {log_file}...")
    urls = extract_urls_from_log(log_file)
    
    if not urls:
        logger.warning("No URLs found in log file")
        return {'success': False, 'error': 'No URLs found'}
    
    logger.info(f"✅ Found {len(urls)} unique URLs")
    
    # Limit number of URLs to process
    urls_to_process = urls[:limit]
    logger.info(f"📊 Processing {len(urls_to_process)} URLs (limit: {limit})...")
    
    parsed_count = 0
    words_to_insert = []
    all_search_terms = set()
    
    for i, url in enumerate(urls_to_process, 1):
        logger.info(f"📄 Processing {i}/{len(urls_to_process)}: {url[:80]}...")
        
        parsed_data = fetch_and_parse_url(url, delay=delay)
        
        if not parsed_data:
            continue
        
        parsed_count += 1
        
        # Extract search term
        search_term = parsed_data.get('search_term')
        if search_term:
            all_search_terms.add(search_term)
            
            # Store the main search term
            if parsed_data.get('jewish_gematria'):
                word_data = {
                    'phrase': search_term,
                    'jewish_gematria': parsed_data.get('jewish_gematria'),
                    'english_gematria': parsed_data.get('english_gematria'),
                    'simple_gematria': parsed_data.get('simple_gematria'),
                    'source': 'gematrix.org',
                    'search_value': parsed_data.get('search_value'),
                    'page_number': parsed_data.get('page_number'),
                    'max_page': parsed_data.get('max_page')
                }
                words_to_insert.append(word_data)
        
        # Store equal words from Jewish table
        for equal_word in parsed_data.get('equal_words_jewish', []):
            if equal_word.get('word'):
                word_data = {
                    'phrase': equal_word['word'],
                    'jewish_gematria': equal_word.get('jewish_gematria'),
                    'english_gematria': equal_word.get('english_gematria'),
                    'simple_gematria': equal_word.get('simple_gematria'),
                    'source': 'gematrix.org',
                    'searches': equal_word.get('searches')
                }
                words_to_insert.append(word_data)
        
        # Store equal words from English table
        for equal_word in parsed_data.get('equal_words_english', []):
            if equal_word.get('word'):
                word_data = {
                    'phrase': equal_word['word'],
                    'jewish_gematria': equal_word.get('jewish_gematria'),
                    'english_gematria': equal_word.get('english_gematria'),
                    'simple_gematria': equal_word.get('simple_gematria'),
                    'source': 'gematrix.org',
                    'searches': equal_word.get('searches')
                }
                words_to_insert.append(word_data)
    
    logger.info(f"✅ Parsed {parsed_count}/{len(urls_to_process)} pages")
    logger.info(f"📊 Extracted {len(words_to_insert)} words from {len(all_search_terms)} unique search terms")
    
    # Insert words in batches
    inserted_count = 0
    if words_to_insert and supabase:
        logger.info(f"💾 Inserting {len(words_to_insert)} words into database...")
        batch_size = 100
        
        for i in range(0, len(words_to_insert), batch_size):
            batch = words_to_insert[i:i+batch_size]
            try:
                supabase.table('gematria_words').upsert(
                    batch,
                    on_conflict='phrase'
                ).execute()
                inserted_count += len(batch)
                logger.info(f"✅ Inserted batch of {len(batch)} words ({inserted_count}/{len(words_to_insert)})")
            except Exception as e:
                logger.error(f"Error inserting batch: {e}")
                # Try individual inserts
                for word_data in batch:
                    try:
                        supabase.table('gematria_words').upsert(
                            word_data,
                            on_conflict='phrase'
                        ).execute()
                        inserted_count += 1
                    except Exception as e2:
                        logger.error(f"Error inserting word '{word_data.get('phrase')}': {e2}")
    
    return {
        'success': True,
        'urls_found': len(urls),
        'urls_processed': len(urls_to_process),
        'pages_parsed': parsed_count,
        'words_extracted': len(words_to_insert),
        'words_inserted': inserted_count,
        'search_terms': list(all_search_terms)
    }


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("EXTRACT AND PARSE FROM LOGS")
    logger.info("=" * 60)
    logger.info("")
    
    if not HAS_SUPABASE:
        logger.error("❌ Supabase not configured. Cannot process URLs.")
        return 1
    
    # Process URLs from ingestion_execution.log
    log_file = 'ingestion_execution.log'
    
    if not os.path.exists(log_file):
        logger.error(f"❌ Log file not found: {log_file}")
        return 1
    
    # Process URLs (limit to 50 for now to avoid overwhelming the server)
    results = process_urls_from_logs(log_file, limit=50, delay=2.0)
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("PROCESSING SUMMARY")
    logger.info("=" * 60)
    logger.info(f"📊 URLs found: {results.get('urls_found', 0)}")
    logger.info(f"📄 URLs processed: {results.get('urls_processed', 0)}")
    logger.info(f"✅ Pages parsed: {results.get('pages_parsed', 0)}")
    logger.info(f"📝 Words extracted: {results.get('words_extracted', 0)}")
    logger.info(f"💾 Words inserted: {results.get('words_inserted', 0)}")
    logger.info(f"🔍 Search terms: {len(results.get('search_terms', []))}")
    logger.info("=" * 60)
    
    # Note about terminal history
    logger.info("")
    logger.info("ℹ️  NOTE: Terminal history is limited by shell buffer size (typically 500-1000 lines).")
    logger.info("    Log files contain the full history of all operations.")
    logger.info("    Use 'tail -n 1000 ingestion_execution.log' to see recent activity.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

