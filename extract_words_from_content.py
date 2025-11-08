#!/usr/bin/env python3
"""
Extract Words from Scraped Content

Purpose: Extract words from scraped content, calculate gematria values, and store in gematria_words table
- Pull scraped content from database
- Extract words from content
- Calculate gematria values
- Store in gematria_words table

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import sys
import re
import logging
from typing import Dict, List, Set
from datetime import datetime
from collections import Counter

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


def extract_words(text: str, min_length: int = 3) -> List[str]:
    """
    Extract words from text.
    
    Args:
        text: Text to extract words from
        min_length: Minimum word length
        
    Returns:
        List of unique words
    """
    if not text:
        return []
    
    # Extract words (alphanumeric, min_length+ characters)
    words = re.findall(r'\b[a-zA-Z]{' + str(min_length) + r',}\b', text.lower())
    
    # Filter common stop words
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 
        'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 
        'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'let', 'put', 
        'say', 'she', 'too', 'use', 'this', 'that', 'with', 'from', 'have', 'been', 
        'will', 'than', 'more', 'some', 'time', 'very', 'what', 'know', 'just', 'like',
        'into', 'them', 'these', 'their', 'there', 'other', 'which', 'make', 'when',
        'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'first', 'well'
    }
    
    # Remove stop words and get unique words
    unique_words = []
    seen = set()
    for word in words:
        if word not in stop_words and word not in seen:
            seen.add(word)
            unique_words.append(word)
    
    return unique_words


def calculate_gematria_for_word(word: str) -> Dict:
    """
    Calculate all gematria values for a word.
    
    Args:
        word: Word to calculate
        
    Returns:
        Dictionary with gematria values
    """
    return gematria_engine.calculate_all(word)


def process_scraped_content(limit: int = 1000) -> int:
    """
    Process scraped content and extract words.
    
    Args:
        limit: Maximum number of content items to process
        
    Returns:
        Number of words extracted and stored
    """
    if not supabase:
        logger.error("Supabase not available")
        return 0
    
    logger.info(f"📊 Pulling scraped content (limit: {limit})...")
    
    try:
        # Pull scraped content from database
        result = supabase.table('scraped_content')\
            .select('id, title, content, url')\
            .limit(limit)\
            .execute()
        
        if not result.data:
            logger.warning("No scraped content found")
            return 0
        
        content_items = result.data
        logger.info(f"✅ Found {len(content_items)} content items")
        
        # Extract all words
        all_words: Set[str] = set()
        word_sources: Dict[str, List[str]] = {}  # word -> list of source URLs
        
        logger.info("🔍 Extracting words from content...")
        for item in content_items:
            content = item.get('content', '') or item.get('title', '')
            url = item.get('url', '')
            
            if not content:
                continue
            
            words = extract_words(content)
            for word in words:
                all_words.add(word)
                if word not in word_sources:
                    word_sources[word] = []
                word_sources[word].append(url)
        
        logger.info(f"✅ Extracted {len(all_words)} unique words")
        
        # Check which words already exist in database
        logger.info("🔍 Checking existing words in database...")
        existing_words = set()
        if all_words:
            # Query in batches
            word_list = list(all_words)
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
        
        new_words = all_words - existing_words
        logger.info(f"✅ Found {len(new_words)} new words to process (out of {len(all_words)} total)")
        
        # Calculate gematria for new words
        logger.info(f"🧮 Calculating gematria values for {len(new_words)} words...")
        words_to_insert = []
        
        for word in new_words:
            try:
                gematria_values = calculate_gematria_for_word(word)
                
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
                    'sources': word_sources.get(word, []),
                    'extracted_at': datetime.utcnow().isoformat()
                }
                
                words_to_insert.append(word_data)
            except Exception as e:
                logger.warning(f"Error calculating gematria for '{word}': {e}")
        
        # Insert words in batches
        if words_to_insert:
            logger.info(f"💾 Inserting {len(words_to_insert)} words into database...")
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
        
    except Exception as e:
        logger.error(f"Error processing scraped content: {e}")
        return 0


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("WORD EXTRACTION FROM SCRAPED CONTENT")
    logger.info("=" * 60)
    logger.info("")
    
    if not HAS_SUPABASE:
        logger.error("❌ Supabase not configured. Cannot extract words.")
        return 1
    
    # Process scraped content
    word_count = process_scraped_content(limit=1000)
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("EXTRACTION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"📊 Words extracted and stored: {word_count}")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

