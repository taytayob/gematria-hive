"""
Floating Index System
Purpose: Quick lookup index for fast access without full database queries
- In-memory index for frequently accessed data
- Key-based lookups
- Automatic cache updates
- TTL-based expiration
- Background refresh

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from threading import Lock
from collections import OrderedDict

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


class FloatingIndex:
    """
    Floating Index - In-memory index for quick lookups
    """
    
    def __init__(self, max_size: int = 10000, ttl_seconds: int = 3600):
        """
        Initialize floating index.
        
        Args:
            max_size: Maximum number of entries
            ttl_seconds: Time to live in seconds
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.supabase = supabase if HAS_SUPABASE else None
        
        # In-memory index: {key: {entity_type, entity_id, metadata, last_accessed, created_at}}
        self.index: OrderedDict[str, Dict] = OrderedDict()
        self.lock = Lock()
        
        logger.info(f"Initialized FloatingIndex with max_size={max_size}, ttl={ttl_seconds}s")
    
    def _generate_key(self, entity_type: str, entity_id: str, **kwargs) -> str:
        """
        Generate index key.
        
        Args:
            entity_type: Entity type
            entity_id: Entity ID
            **kwargs: Additional key components
            
        Returns:
            Index key
        """
        key_parts = [entity_type, entity_id]
        if kwargs:
            key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
        return "|".join(key_parts)
    
    def get(self, key: str) -> Optional[Dict]:
        """
        Get entry from index.
        
        Args:
            key: Index key
            
        Returns:
            Entry dictionary or None
        """
        with self.lock:
            if key in self.index:
                entry = self.index[key]
                
                # Check TTL
                last_accessed = entry.get('last_accessed', 0)
                if time.time() - last_accessed > self.ttl_seconds:
                    # Expired, remove from index
                    del self.index[key]
                    return None
                
                # Update last accessed
                entry['last_accessed'] = time.time()
                entry['access_count'] = entry.get('access_count', 0) + 1
                
                # Move to end (LRU)
                self.index.move_to_end(key)
                
                return entry
            
            return None
    
    def set(self, key: str, entity_type: str, entity_id: str, metadata: Optional[Dict] = None):
        """
        Set entry in index.
        
        Args:
            key: Index key
            entity_type: Entity type
            entity_id: Entity ID
            metadata: Additional metadata
        """
        with self.lock:
            # Check if we need to evict
            if len(self.index) >= self.max_size and key not in self.index:
                # Evict oldest entry (LRU)
                oldest_key = next(iter(self.index))
                del self.index[oldest_key]
            
            # Add/update entry
            self.index[key] = {
                'entity_type': entity_type,
                'entity_id': entity_id,
                'metadata': metadata or {},
                'last_accessed': time.time(),
                'created_at': time.time(),
                'access_count': 1
            }
            
            # Move to end (LRU)
            self.index.move_to_end(key)
    
    def lookup(self, entity_type: str, entity_id: str, **kwargs) -> Optional[Dict]:
        """
        Lookup entity in index.
        
        Args:
            entity_type: Entity type
            entity_id: Entity ID
            **kwargs: Additional key components
            
        Returns:
            Entry dictionary or None
        """
        key = self._generate_key(entity_type, entity_id, **kwargs)
        return self.get(key)
    
    def store(self, entity_type: str, entity_id: str, metadata: Optional[Dict] = None, **kwargs):
        """
        Store entity in index.
        
        Args:
            entity_type: Entity type
            entity_id: Entity ID
            metadata: Additional metadata
            **kwargs: Additional key components
        """
        key = self._generate_key(entity_type, entity_id, **kwargs)
        self.set(key, entity_type, entity_id, metadata)
        
        # Also store in database for persistence
        if self.supabase:
            try:
                self.supabase.table('floating_index').upsert({
                    'key': key,
                    'entity_type': entity_type,
                    'entity_id': entity_id,
                    'metadata': metadata or {},
                    'last_accessed': datetime.utcnow().isoformat(),
                    'access_count': 1
                }, on_conflict='key').execute()
            except Exception as e:
                logger.warning(f"Error storing in database: {e}")
    
    def load_from_database(self, limit: int = 1000):
        """
        Load entries from database into memory.
        
        Args:
            limit: Maximum number of entries to load
        """
        if not self.supabase:
            return
        
        try:
            result = self.supabase.table('floating_index')\
                .select('*')\
                .order('last_accessed', desc=True)\
                .limit(limit)\
                .execute()
            
            if result.data:
                with self.lock:
                    for entry in result.data:
                        key = entry.get('key')
                        if key:
                            self.index[key] = {
                                'entity_type': entry.get('entity_type'),
                                'entity_id': entry.get('entity_id'),
                                'metadata': entry.get('metadata', {}),
                                'last_accessed': time.time(),
                                'created_at': time.time(),
                                'access_count': entry.get('access_count', 1)
                            }
                
                logger.info(f"Loaded {len(result.data)} entries from database")
        except Exception as e:
            logger.error(f"Error loading from database: {e}")
    
    def cleanup_expired(self):
        """Remove expired entries from index."""
        with self.lock:
            current_time = time.time()
            expired_keys = []
            
            for key, entry in self.index.items():
                last_accessed = entry.get('last_accessed', 0)
                if current_time - last_accessed > self.ttl_seconds:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.index[key]
            
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired entries")
    
    def get_stats(self) -> Dict:
        """
        Get index statistics.
        
        Returns:
            Dictionary with statistics
        """
        with self.lock:
            total_entries = len(self.index)
            total_accesses = sum(entry.get('access_count', 0) for entry in self.index.values())
            
            # Get most accessed entries
            sorted_entries = sorted(
                self.index.items(),
                key=lambda x: x[1].get('access_count', 0),
                reverse=True
            )
            most_accessed = [
                {
                    'key': key,
                    'entity_type': entry.get('entity_type'),
                    'entity_id': entry.get('entity_id'),
                    'access_count': entry.get('access_count', 0)
                }
                for key, entry in sorted_entries[:10]
            ]
            
            return {
                'total_entries': total_entries,
                'max_size': self.max_size,
                'total_accesses': total_accesses,
                'ttl_seconds': self.ttl_seconds,
                'most_accessed': most_accessed
            }


# Singleton instance
_floating_index = None

def get_floating_index() -> FloatingIndex:
    """Get or create floating index singleton."""
    global _floating_index
    if _floating_index is None:
        _floating_index = FloatingIndex()
        # Load from database on initialization
        _floating_index.load_from_database()
    return _floating_index

