"""
Cache Manager
Purpose: Manage caching for API responses, embeddings, calculations, etc.
- API response caching
- Embedding caching
- Gematria calculation caching
- Phonetic analysis caching
- TTL-based expiration
- Cache invalidation

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import hashlib
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from dotenv import load_dotenv
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


class CacheManager:
    """
    Cache Manager - Manages caching for all operations
    """
    
    def __init__(self):
        """Initialize cache manager"""
        self.supabase = supabase if HAS_SUPABASE else None
        logger.info("Initialized CacheManager")
    
    def generate_cache_key(self, cache_type: str, *args, **kwargs) -> str:
        """
        Generate cache key from arguments.
        
        Args:
            cache_type: Cache type ('api_response', 'embedding', 'gematria', etc.)
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Cache key string
        """
        # Create hash from arguments
        key_data = {
            'type': cache_type,
            'args': args,
            'kwargs': kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"{cache_type}_{key_hash}"
    
    def get(self, cache_key: str) -> Optional[Dict]:
        """
        Get cached data.
        
        Args:
            cache_key: Cache key
            
        Returns:
            Cached data dictionary or None
        """
        if not self.supabase:
            return None
        
        try:
            result = self.supabase.table('cache_logs')\
                .select('*')\
                .eq('cache_key', cache_key)\
                .gt('expires_at', datetime.utcnow().isoformat())\
                .limit(1)\
                .execute()
            
            if result.data:
                cached_data = result.data[0].get('cached_data', {})
                logger.debug(f"Cache hit: {cache_key}")
                return cached_data
            
            logger.debug(f"Cache miss: {cache_key}")
            return None
        except Exception as e:
            logger.warning(f"Error getting cache: {e}")
            return None
    
    def set(self, cache_key: str, cache_type: str, data: Dict, ttl_hours: int = 24):
        """
        Set cached data.
        
        Args:
            cache_key: Cache key
            cache_type: Cache type
            data: Data to cache
            ttl_hours: Time to live in hours
        """
        if not self.supabase:
            return
        
        try:
            expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
            
            self.supabase.table('cache_logs').upsert({
                'cache_key': cache_key,
                'cache_type': cache_type,
                'cached_data': data,
                'expires_at': expires_at.isoformat()
            }, on_conflict='cache_key').execute()
            
            logger.debug(f"Cached data: {cache_key}")
        except Exception as e:
            logger.warning(f"Error setting cache: {e}")
    
    def invalidate(self, cache_key: str):
        """
        Invalidate cache entry.
        
        Args:
            cache_key: Cache key
        """
        if not self.supabase:
            return
        
        try:
            self.supabase.table('cache_logs')\
                .delete()\
                .eq('cache_key', cache_key)\
                .execute()
            
            logger.info(f"Invalidated cache: {cache_key}")
        except Exception as e:
            logger.warning(f"Error invalidating cache: {e}")
    
    def invalidate_by_type(self, cache_type: str):
        """
        Invalidate all cache entries of a specific type.
        
        Args:
            cache_type: Cache type
        """
        if not self.supabase:
            return
        
        try:
            self.supabase.table('cache_logs')\
                .delete()\
                .eq('cache_type', cache_type)\
                .execute()
            
            logger.info(f"Invalidated all {cache_type} cache entries")
        except Exception as e:
            logger.warning(f"Error invalidating cache by type: {e}")
    
    def cleanup_expired(self):
        """Remove expired cache entries."""
        if not self.supabase:
            return
        
        try:
            self.supabase.table('cache_logs')\
                .delete()\
                .lt('expires_at', datetime.utcnow().isoformat())\
                .execute()
            
            logger.info("Cleaned up expired cache entries")
        except Exception as e:
            logger.warning(f"Error cleaning up expired cache: {e}")
    
    def get_cache_stats(self) -> Dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        if not self.supabase:
            return {}
        
        try:
            # Get all cache entries
            result = self.supabase.table('cache_logs')\
                .select('cache_type', count='exact')\
                .execute()
            
            # Count by type
            stats = {}
            if result.data:
                for entry in result.data:
                    cache_type = entry.get('cache_type', 'unknown')
                    stats[cache_type] = stats.get(cache_type, 0) + 1
            
            return stats
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}


# Singleton instance
_cache_manager = None

def get_cache_manager() -> CacheManager:
    """Get or create cache manager singleton."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager

