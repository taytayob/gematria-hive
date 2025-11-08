#!/usr/bin/env python3
"""
Extract Words from Gematrix.org Pages

Purpose: Extract words and gematria values directly from gematrix.org pages
- Scrape gematrix.org word pages
- Extract words and their gematria values
- Store in gematria_words table

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
import re
import logging
import requests
import time
from typing import Dict, List, Set
from datetime import datetime
from bs4 import BeautifulSoup

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from core.gematria_engine import get_gematria_engine

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

# Gematria engine
gematria_engine = get_gematria_engine()


def extract_words_from_gematrix_page(url: str) -> List[Dict]:
    """
    Extract words and gematria values from a gematrix.org page.
    
    Args:
        url: URL of gematrix.org page
        
    Returns:
        List of word dictionaries with gematria values
    """
    words = []
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'GematriaHive/1.0 (Educational Research)'
        })
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for word tables or lists
        # Gematrix.org typically has tables with words and their values
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    # Try to extract word and value
                    word_text = cells[0].get_text(strip=True)
                    value_text = cells[1].get_text(strip=True)
                    
                    # Clean word
                    word = re.sub(r'[^a-zA-Z\s]', '', word_text).strip().lower()
                    
                    if word and len(word) >= 3:
                        # Try to parse gematria value
                        try:
                            value = int(re.sub(r'[^\d]', '', value_text))
                        except:
                            value = None
                        
                        # Calculate gematria if we have the word
                        gematria_values = gematria_engine.calculate_all(word)
                        
                        word_data = {
                            'phrase': word,
                            'jewish_gematria': gematria_values.get('jewish_gematria') or value,
                            'english_gematria': gematria_values.get('english_gematria'),
                            'simple_gematria': gematria_values.get('simple_gematria'),
                            'hebrew_full': gematria_values.get('hebrew_full'),
                            'hebrew_musafi': gematria_values.get('hebrew_musafi'),
                            'hebrew_katan': gematria_values.get('hebrew_katan'),
                            'hebrew_ordinal': gematria_values.get('hebrew_ordinal'),
                            'hebrew_atbash': gematria_values.get('hebrew_atbash'),
                            'hebrew_kidmi': gematria_values.get('hebrew_kidmi'),
                            'hebrew_perati': gematria_values.get('hebrew_perati'),
                            'hebrew_shemi': gematria_values.get('hebrew_shemi'),
                            'source': 'gematrix.org'
                        }
                        
                        words.append(word_data)
        
        # Also extract words from text content
        text = soup.get_text()
        # Find words in the text (3+ characters)
        text_words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter common words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was',
            'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may',
            'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'let', 'put',
            'say', 'she', 'too', 'use', 'this', 'that', 'with', 'from', 'have', 'been',
            'will', 'than', 'more', 'some', 'time', 'very', 'what', 'know', 'just', 'like'
        }
        
        unique_text_words = set(text_words) - stop_words
        
        for word in unique_text_words:
            # Check if we already have this word
            if not any(w['phrase'] == word for w in words):
                gematria_values = gematria_engine.calculate_all(word)
                
                word_data = {
                    'phrase': word,
                    'jewish_gematria': gematria_values.get('jewish_gematria'),
                    'english_gematria': gematria_values.get('english_gematria'),
                    'simple_gematria': gematria_values.get('simple_gematria'),
                    'hebrew_full': gematria_values.get('hebrew_full'),
                    'hebrew_musafi': gematria_values.get('hebrew_musafi'),
                    'hebrew_katan': gematria_values.get('hebrew_katan'),
                    'hebrew_ordinal': gematria_values.get('hebrew_ordinal'),
                    'hebrew_atbash': gematria_values.get('hebrew_atbash'),
                    'hebrew_kidmi': gematria_values.get('hebrew_kidmi'),
                    'hebrew_perati': gematria_values.get('hebrew_perati'),
                    'hebrew_shemi': gematria_values.get('hebrew_shemi'),
                    'source': 'gematrix.org'
                }
                
                words.append(word_data)
        
        logger.info(f"✅ Extracted {len(words)} words from {url}")
        
    except Exception as e:
        logger.error(f"Error extracting words from {url}: {e}")
    
    return words


def scrape_gematrix_words(limit: int = 100) -> int:
    """
    Scrape words from gematrix.org pages.
    
    Args:
        limit: Maximum number of pages to scrape
        
    Returns:
        Number of words extracted and stored
    """
    if not supabase:
        logger.error("Supabase not available")
        return 0
    
    logger.info(f"🌐 Scraping words from gematrix.org (limit: {limit} pages)...")
    
    # List of gematrix.org pages to scrape
    pages = [
        "https://www.gematrix.org",
        "https://www.gematrix.org/gematria-database",
        "https://www.gematrix.org/gematria-database-numerology",
    ]
    
    all_words: Dict[str, Dict] = {}  # phrase -> word_data
    
    for page_url in pages[:limit]:
        logger.info(f"📄 Scraping {page_url}...")
        words = extract_words_from_gematrix_page(page_url)
        
        for word_data in words:
            phrase = word_data['phrase']
            if phrase not in all_words:
                all_words[phrase] = word_data
            # If word already exists, keep the first one (or merge if needed)
        
        time.sleep(2)  # Be respectful
    
    logger.info(f"✅ Extracted {len(all_words)} unique words")
    
    # Check which words already exist
    logger.info("🔍 Checking existing words in database...")
    existing_words = set()
    if all_words:
        word_list = list(all_words.keys())
        batch_size = 100
        for i in range(0, len(word_list), batch_size):
            batch = word_list[i:i+batch_size]
            try:
                result = supabase.table('gematria_words')\
                    .select('phrase')\
                    .in_('phrase', batch)\
                    .execute()
                if result.data:
                    existing_words.update([w['phrase'] for w in result.data])
            except Exception as e:
                logger.warning(f"Error checking existing words: {e}")
    
    new_words = {k: v for k, v in all_words.items() if k not in existing_words}
    logger.info(f"✅ Found {len(new_words)} new words to insert (out of {len(all_words)} total)")
    
    # Insert new words
    if new_words:
        logger.info(f"💾 Inserting {len(new_words)} words into database...")
        words_to_insert = list(new_words.values())
        batch_size = 100
        inserted_count = 0
        
        for i in range(0, len(words_to_insert), batch_size):
            batch = words_to_insert[i:i+batch_size]
            try:
                result = supabase.table('gematria_words').insert(batch).execute()
                inserted_count += len(batch)
                logger.info(f"✅ Inserted batch of {len(batch)} words ({inserted_count}/{len(words_to_insert)})")
            except Exception as e:
                logger.error(f"Error inserting batch: {e}")
                # Try individual inserts
                for word_data in batch:
                    try:
                        supabase.table('gematria_words').insert(word_data).execute()
                        inserted_count += 1
                    except Exception as e2:
                        logger.error(f"Error inserting word '{word_data.get('phrase')}': {e2}")
        
        logger.info(f"✅ Successfully inserted {inserted_count}/{len(words_to_insert)} words")
        return inserted_count
    else:
        logger.info("ℹ️  No new words to insert")
        return 0


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("EXTRACT WORDS FROM GEMATRIX.ORG")
    logger.info("=" * 60)
    logger.info("")
    
    if not HAS_SUPABASE:
        logger.error("❌ Supabase not configured. Cannot extract words.")
        return 1
    
    # Scrape words from gematrix.org
    word_count = scrape_gematrix_words(limit=10)
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("EXTRACTION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"📊 Words extracted and stored: {word_count}")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

