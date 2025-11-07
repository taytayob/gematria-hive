"""
Gematria Calculator Module

Purpose: Gematria calculation and query interface
- Implement calculation methods from CSV data
- Support: Jewish, English, Simple, Hebrew variants
- Query interface for value-to-word lookups
- Relationship mapping (same value = related words)
- Semantic search integration

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from supabase import create_client, Client
from sentence_transformers import SentenceTransformer, util

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
    filename='gematria_calculator_log.txt',
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

# Embedding model for semantic search
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

logger.info("Gematria calculator initialized")


class GematriaCalculator:
    """
    Gematria calculation and query interface.
    """
    
    def __init__(self):
        """Initialize gematria calculator."""
        self.supabase = supabase
        self.embed_model = embed_model
        logger.info("Gematria calculator initialized")
    
    def find_words_by_value(
        self,
        value: int,
        gematria_type: str = 'jewish_gematria',
        limit: int = 100
    ) -> List[Dict]:
        """
        Find words/phrases by gematria value.
        
        Args:
            value: Gematria value to search for
            gematria_type: Type of gematria ('jewish_gematria', 'english_gematria', 'simple_gematria', etc.)
            limit: Maximum number of results
            
        Returns:
            List of word dictionaries with matching values
        """
        try:
            # Map gematria type to column name
            column_map = {
                'jewish': 'jewish_gematria',
                'english': 'english_gematria',
                'simple': 'simple_gematria',
                'hebrew_full': 'hebrew_full',
                'hebrew_musafi': 'hebrew_musafi',
                'hebrew_katan': 'hebrew_katan',
                'hebrew_ordinal': 'hebrew_ordinal',
                'hebrew_atbash': 'hebrew_atbash',
                'hebrew_kidmi': 'hebrew_kidmi',
                'hebrew_perati': 'hebrew_perati',
                'hebrew_shemi': 'hebrew_shemi',
            }
            
            column = column_map.get(gematria_type.lower(), gematria_type)
            
            # Query Supabase
            result = self.supabase.table('gematria_words')\
                .select('*')\
                .eq(column, value)\
                .limit(limit)\
                .execute()
            
            words = result.data if result.data else []
            logger.info(f"Found {len(words)} words with {gematria_type} value {value}")
            
            return words
        
        except Exception as e:
            logger.error(f"Error finding words by value: {e}")
            return []
    
    def find_related_words(
        self,
        phrase: str,
        gematria_type: str = 'jewish_gematria',
        limit: int = 100
    ) -> List[Dict]:
        """
        Find words with the same gematria value as the given phrase.
        
        Args:
            phrase: Phrase to find related words for
            gematria_type: Type of gematria to use for comparison
            limit: Maximum number of results
            
        Returns:
            List of related word dictionaries
        """
        try:
            # First, find the phrase and get its value
            result = self.supabase.table('gematria_words')\
                .select('*')\
                .ilike('phrase', f'%{phrase}%')\
                .limit(1)\
                .execute()
            
            if not result.data:
                logger.warning(f"Phrase '{phrase}' not found in database")
                return []
            
            word = result.data[0]
            
            # Get the gematria value
            column_map = {
                'jewish': 'jewish_gematria',
                'english': 'english_gematria',
                'simple': 'simple_gematria',
                'hebrew_full': 'hebrew_full',
                'hebrew_musafi': 'hebrew_musafi',
                'hebrew_katan': 'hebrew_katan',
                'hebrew_ordinal': 'hebrew_ordinal',
                'hebrew_atbash': 'hebrew_atbash',
                'hebrew_kidmi': 'hebrew_kidmi',
                'hebrew_perati': 'hebrew_perati',
                'hebrew_shemi': 'hebrew_shemi',
            }
            
            column = column_map.get(gematria_type.lower(), gematria_type)
            value = word.get(column)
            
            if value is None:
                logger.warning(f"No {gematria_type} value found for phrase '{phrase}'")
                return []
            
            # Find all words with the same value
            related = self.find_words_by_value(value, gematria_type, limit)
            
            # Filter out the original phrase
            related = [w for w in related if w.get('phrase', '').lower() != phrase.lower()]
            
            logger.info(f"Found {len(related)} related words for '{phrase}' (value: {value})")
            
            return related
        
        except Exception as e:
            logger.error(f"Error finding related words: {e}")
            return []
    
    def semantic_search(
        self,
        query: str,
        limit: int = 100,
        threshold: float = 0.5
    ) -> List[Dict]:
        """
        Semantic search for phrases using embeddings.
        
        Args:
            query: Search query text
            limit: Maximum number of results
            threshold: Minimum similarity threshold
            
        Returns:
            List of similar word dictionaries
        """
        try:
            # Generate embedding for query
            query_embedding = self.embed_model.encode(query).tolist()
            
            # Use Supabase vector similarity search
            # Note: This requires pgvector extension and proper index
            result = self.supabase.rpc(
                'match_gematria_words',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': threshold,
                    'match_count': limit
                }
            ).execute()
            
            if result.data:
                return result.data
            
            # Fallback: Use embedding similarity in Python if RPC not available
            logger.warning("Vector similarity RPC not available, using fallback method")
            
            # Get all words with embeddings (limited sample)
            all_words = self.supabase.table('gematria_words')\
                .select('*')\
                .not_.is_('embedding', 'null')\
                .limit(10000)\
                .execute()
            
            if not all_words.data:
                return []
            
            # Calculate similarities
            similarities = []
            for word in all_words.data:
                if word.get('embedding'):
                    similarity = util.cos_sim(query_embedding, word['embedding']).item()
                    if similarity >= threshold:
                        similarities.append((similarity, word))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[0], reverse=True)
            
            # Return top results
            results = [word for _, word in similarities[:limit]]
            
            logger.info(f"Found {len(results)} semantically similar words for '{query}'")
            
            return results
        
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    def get_value_statistics(
        self,
        gematria_type: str = 'jewish_gematria'
    ) -> Dict:
        """
        Get statistics about gematria values.
        
        Args:
            gematria_type: Type of gematria to analyze
            
        Returns:
            Dictionary with statistics
        """
        try:
            column_map = {
                'jewish': 'jewish_gematria',
                'english': 'english_gematria',
                'simple': 'simple_gematria',
            }
            
            column = column_map.get(gematria_type.lower(), gematria_type)
            
            # Get all values (this might be slow for large datasets)
            # Consider using a view or materialized view for better performance
            result = self.supabase.table('gematria_words')\
                .select(column)\
                .not_.is_(column, 'null')\
                .limit(100000)\
                .execute()
            
            if not result.data:
                return {}
            
            values = [row[column] for row in result.data if row.get(column) is not None]
            
            if not values:
                return {}
            
            # Calculate statistics
            stats = {
                'total_words': len(values),
                'unique_values': len(set(values)),
                'min_value': min(values),
                'max_value': max(values),
                'avg_value': sum(values) / len(values),
            }
            
            # Find most common values
            from collections import Counter
            value_counts = Counter(values)
            most_common = value_counts.most_common(10)
            stats['most_common_values'] = [{'value': val, 'count': count} for val, count in most_common]
            
            logger.info(f"Calculated statistics for {gematria_type}")
            
            return stats
        
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}
    
    def calculate_phrase_value(
        self,
        phrase: str,
        gematria_type: str = 'jewish_gematria'
    ) -> Optional[int]:
        """
        Calculate gematria value for a phrase (if it exists in database).
        
        Args:
            phrase: Phrase to calculate value for
            gematria_type: Type of gematria to use
            
        Returns:
            Gematria value or None if not found
        """
        try:
            # Look up phrase in database
            result = self.supabase.table('gematria_words')\
                .select('*')\
                .ilike('phrase', phrase)\
                .limit(1)\
                .execute()
            
            if not result.data:
                return None
            
            word = result.data[0]
            
            # Get the gematria value
            column_map = {
                'jewish': 'jewish_gematria',
                'english': 'english_gematria',
                'simple': 'simple_gematria',
                'hebrew_full': 'hebrew_full',
                'hebrew_musafi': 'hebrew_musafi',
                'hebrew_katan': 'hebrew_katan',
                'hebrew_ordinal': 'hebrew_ordinal',
                'hebrew_atbash': 'hebrew_atbash',
                'hebrew_kidmi': 'hebrew_kidmi',
                'hebrew_perati': 'hebrew_perati',
                'hebrew_shemi': 'hebrew_shemi',
            }
            
            column = column_map.get(gematria_type.lower(), gematria_type)
            value = word.get(column)
            
            return value
        
        except Exception as e:
            logger.error(f"Error calculating phrase value: {e}")
            return None


def main():
    """Main function for command-line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python gematria_calculator.py <command> [args...]")
        print("Commands:")
        print("  find <value> [type] [limit] - Find words by gematria value")
        print("  related <phrase> [type] [limit] - Find related words")
        print("  search <query> [limit] - Semantic search")
        print("  stats [type] - Get value statistics")
        print("  calculate <phrase> [type] - Calculate phrase value")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    calculator = GematriaCalculator()
    
    if command == 'find':
        if len(sys.argv) < 3:
            print("Usage: python gematria_calculator.py find <value> [type] [limit]")
            sys.exit(1)
        
        value = int(sys.argv[2])
        gematria_type = sys.argv[3] if len(sys.argv) > 3 else 'jewish_gematria'
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        
        words = calculator.find_words_by_value(value, gematria_type, limit)
        print(f"\nFound {len(words)} words with {gematria_type} value {value}:")
        for word in words[:10]:  # Show first 10
            print(f"  - {word.get('phrase', 'N/A')}")
    
    elif command == 'related':
        if len(sys.argv) < 3:
            print("Usage: python gematria_calculator.py related <phrase> [type] [limit]")
            sys.exit(1)
        
        phrase = sys.argv[2]
        gematria_type = sys.argv[3] if len(sys.argv) > 3 else 'jewish_gematria'
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100
        
        words = calculator.find_related_words(phrase, gematria_type, limit)
        print(f"\nFound {len(words)} related words for '{phrase}':")
        for word in words[:10]:  # Show first 10
            print(f"  - {word.get('phrase', 'N/A')}")
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Usage: python gematria_calculator.py search <query> [limit]")
            sys.exit(1)
        
        query = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        
        words = calculator.semantic_search(query, limit)
        print(f"\nFound {len(words)} semantically similar words for '{query}':")
        for word in words[:10]:  # Show first 10
            print(f"  - {word.get('phrase', 'N/A')}")
    
    elif command == 'stats':
        gematria_type = sys.argv[2] if len(sys.argv) > 2 else 'jewish_gematria'
        
        stats = calculator.get_value_statistics(gematria_type)
        print(f"\nStatistics for {gematria_type}:")
        print(f"  Total words: {stats.get('total_words', 0)}")
        print(f"  Unique values: {stats.get('unique_values', 0)}")
        print(f"  Min value: {stats.get('min_value', 'N/A')}")
        print(f"  Max value: {stats.get('max_value', 'N/A')}")
        print(f"  Avg value: {stats.get('avg_value', 'N/A'):.2f}")
    
    elif command == 'calculate':
        if len(sys.argv) < 3:
            print("Usage: python gematria_calculator.py calculate <phrase> [type]")
            sys.exit(1)
        
        phrase = sys.argv[2]
        gematria_type = sys.argv[3] if len(sys.argv) > 3 else 'jewish_gematria'
        
        value = calculator.calculate_phrase_value(phrase, gematria_type)
        if value is not None:
            print(f"\n'{phrase}' has {gematria_type} value: {value}")
        else:
            print(f"\n'{phrase}' not found in database")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

