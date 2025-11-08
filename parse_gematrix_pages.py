#!/usr/bin/env python3
"""
Parse Gematrix.org Pages - Extract Structured Data

Purpose: Parse scraped gematrix.org pages and extract:
- Search word/phrase
- URL
- Gematria values (Jewish, English, Simple)
- Search value
- Tables of words with equal values
- Page numbers showing depth

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
import re
import logging
import urllib.parse
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from bs4 import BeautifulSoup

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

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


def extract_search_term_from_url(url: str) -> Optional[str]:
    """Extract search term from gematrix.org URL"""
    try:
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        if 'word' in params:
            return urllib.parse.unquote(params['word'][0])
    except Exception as e:
        logger.warning(f"Error extracting search term from URL {url}: {e}")
    return None


def extract_page_number_from_url(url: str) -> Optional[int]:
    """Extract page number from gematrix.org URL"""
    try:
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        if 'page' in params:
            return int(params['page'][0])
    except Exception:
        pass
    return None


def parse_gematrix_page(html: str, url: str) -> Dict:
    """
    Parse a gematrix.org page and extract structured data.
    
    Args:
        html: HTML content of the page
        url: URL of the page
        
    Returns:
        Dictionary with extracted data
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract search term from URL
    search_term = extract_search_term_from_url(url)
    page_number = extract_page_number_from_url(url)
    
    # Extract gematria values from top section
    # Look for: "in Hebrew Gematria equals 779"
    jewish_value = None
    english_value = None
    simple_value = None
    
    # Find the main calculation section
    text = soup.get_text()
    
    # Extract Jewish Gematria value
    jewish_match = re.search(r'in Hebrew Gematria equals (\d+)', text)
    if jewish_match:
        jewish_value = int(jewish_match.group(1))
    
    # Extract English Gematria value
    english_match = re.search(r'in English Gematria equals (\d+)', text)
    if english_match:
        english_value = int(english_match.group(1))
    
    # Extract Simple Gematria value
    simple_match = re.search(r'in Simple Gematria equals (\d+)', text)
    if simple_match:
        simple_value = int(simple_match.group(1))
    
    # Extract search value (if present)
    search_value = None
    search_match = re.search(r'search.*?(\d+)', text, re.IGNORECASE)
    if search_match:
        try:
            search_value = int(search_match.group(1))
        except:
            pass
    
    # Extract tables of words with equal values
    # Find tables with headers: Word | Jewish | English | Simple | Searches
    equal_words_jewish = []
    equal_words_english = []
    
    # Find Jewish Gematria table
    tables = soup.find_all('table')
    for table in tables:
        headers = table.find_all('th')
        header_texts = [h.get_text(strip=True).lower() for h in headers]
        
        # Check if this is a results table
        if 'word' in header_texts and 'jewish' in header_texts:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 4:
                    word_link = cells[0].find('a')
                    if word_link:
                        word_text = word_link.get_text(strip=True)
                        word_url = word_link.get('href', '')
                        
                        # Extract values
                        try:
                            jewish_val = int(cells[1].get_text(strip=True)) if cells[1].get_text(strip=True).isdigit() else None
                            english_val = int(cells[2].get_text(strip=True)) if len(cells) > 2 and cells[2].get_text(strip=True).isdigit() else None
                            simple_val = int(cells[3].get_text(strip=True)) if len(cells) > 3 and cells[3].get_text(strip=True).isdigit() else None
                            searches = int(cells[-1].get_text(strip=True)) if cells[-1].get_text(strip=True).isdigit() else None
                        except:
                            continue
                        
                        if 'jewish' in header_texts[0] or 'Results by Jewish' in table.get_text():
                            equal_words_jewish.append({
                                'word': word_text,
                                'url': word_url,
                                'jewish_gematria': jewish_val,
                                'english_gematria': english_val,
                                'simple_gematria': simple_val,
                                'searches': searches
                            })
                        elif 'english' in header_texts[0] or 'Results by English' in table.get_text():
                            equal_words_english.append({
                                'word': word_text,
                                'url': word_url,
                                'jewish_gematria': jewish_val,
                                'english_gematria': english_val,
                                'simple_gematria': simple_val,
                                'searches': searches
                            })
    
    # Extract page numbers (showing depth)
    page_numbers = []
    page_links = soup.find_all('a', href=re.compile(r'page=\d+'))
    for link in page_links:
        page_text = link.get_text(strip=True)
        if page_text.isdigit():
            page_numbers.append(int(page_text))
    
    max_page = max(page_numbers) if page_numbers else None
    
    return {
        'search_term': search_term,
        'url': url,
        'page_number': page_number,
        'jewish_gematria': jewish_value,
        'english_gematria': english_value,
        'simple_gematria': simple_value,
        'search_value': search_value,
        'equal_words_jewish': equal_words_jewish,
        'equal_words_english': equal_words_english,
        'page_numbers': sorted(set(page_numbers)),
        'max_page': max_page,
        'total_pages': max_page,
        'parsed_at': datetime.utcnow().isoformat()
    }


def parse_scraped_content_from_db(limit: int = 1000) -> int:
    """
    Parse scraped content from database and extract structured data.
    
    Args:
        limit: Maximum number of items to process
        
    Returns:
        Number of pages parsed
    """
    if not supabase:
        logger.error("Supabase not available")
        return 0
    
    logger.info(f"📊 Fetching scraped content (limit: {limit})...")
    
    try:
        # Get scraped content from database
        result = supabase.table('scraped_content')\
            .select('id, url, content, title')\
            .like('url', '%gematrix.org%')\
            .limit(limit)\
            .execute()
        
        if not result.data:
            logger.warning("No scraped content found")
            return 0
        
        items = result.data
        logger.info(f"✅ Found {len(items)} gematrix.org pages to parse")
        
        parsed_count = 0
        words_to_insert = []
        
        for item in items:
            url = item.get('url', '')
            content = item.get('content', '') or item.get('title', '')
            
            if not content:
                continue
            
            try:
                # Parse the page
                parsed_data = parse_gematrix_page(content, url)
                
                # Store parsed data
                if parsed_data.get('search_term'):
                    # Store the main search term
                    if parsed_data.get('jewish_gematria'):
                        word_data = {
                            'phrase': parsed_data['search_term'],
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
                
                parsed_count += 1
                
            except Exception as e:
                logger.error(f"Error parsing page {url}: {e}")
                continue
        
        logger.info(f"✅ Parsed {parsed_count} pages, extracted {len(words_to_insert)} words")
        
        # Insert words in batches
        if words_to_insert:
            logger.info(f"💾 Inserting {len(words_to_insert)} words into database...")
            batch_size = 100
            inserted_count = 0
            
            for i in range(0, len(words_to_insert), batch_size):
                batch = words_to_insert[i:i+batch_size]
                try:
                    result = supabase.table('gematria_words').upsert(
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
            
            logger.info(f"✅ Successfully inserted {inserted_count}/{len(words_to_insert)} words")
            return inserted_count
        else:
            logger.info("ℹ️  No words to insert")
            return 0
        
    except Exception as e:
        logger.error(f"Error parsing scraped content: {e}")
        return 0


def extract_urls_from_logs(log_file: str) -> List[str]:
    """
    Extract URLs from log files.
    
    Args:
        log_file: Path to log file
        
    Returns:
        List of URLs
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
    
    return urls


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("PARSE GEMATRIX.ORG PAGES")
    logger.info("=" * 60)
    logger.info("")
    
    if not HAS_SUPABASE:
        logger.error("❌ Supabase not configured. Cannot parse pages.")
        return 1
    
    # First, try to parse from database
    logger.info("📊 Parsing scraped content from database...")
    word_count = parse_scraped_content_from_db(limit=1000)
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("PARSING SUMMARY")
    logger.info("=" * 60)
    logger.info(f"📊 Words extracted and stored: {word_count}")
    logger.info("=" * 60)
    
    # Note about terminal history
    logger.info("")
    logger.info("ℹ️  NOTE: Terminal history is limited by shell buffer size.")
    logger.info("    Use log files (ingestion_execution.log, scraping_log.txt) for full history.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

