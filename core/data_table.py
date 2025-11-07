"""
Parent DataTable Class Architecture
Purpose: Unified CRUD operations and baseline checking for all data tables
- Parent class for all database tables
- Unified CRUD operations
- Validation hooks
- Baseline checking
- Connection tracking

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from abc import ABC, abstractmethod

from dotenv import load_dotenv

load_dotenv()

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
        logger.warning("Supabase not configured, DataTable operations disabled")
except Exception:
    HAS_SUPABASE = False
    supabase = None
    logger.warning("Supabase not available, DataTable operations disabled")


class DataTable(ABC):
    """
    Parent class for all data tables with unified CRUD operations.
    """
    
    def __init__(self, table_name: str):
        """
        Initialize data table.
        
        Args:
            table_name: Name of the database table
        """
        self.table_name = table_name
        self.supabase = supabase if HAS_SUPABASE else None
        logger.info(f"Initialized DataTable for {table_name}")
    
    def create(self, data: Dict[str, Any], validate: bool = True) -> Optional[Dict]:
        """
        Create a new record.
        
        Args:
            data: Dictionary with record data
            validate: Whether to validate before insertion
            
        Returns:
            Created record or None if failed
        """
        if not self.supabase:
            logger.error("Supabase not available")
            return None
        
        # Validate data
        if validate:
            validation_result = self.validate(data)
            if not validation_result['valid']:
                logger.error(f"Validation failed: {validation_result['errors']}")
                return None
        
        # Check baseline
        baseline_result = self.check_baseline(data)
        if baseline_result:
            data['baseline_id'] = baseline_result
        
        try:
            result = self.supabase.table(self.table_name).insert(data).execute()
            if result.data:
                record = result.data[0]
                # Track connection
                self.track_connection(record['id'], data)
                logger.info(f"Created record in {self.table_name}: {record.get('id')}")
                return record
            else:
                logger.error(f"Insert returned no data for {self.table_name}")
                return None
        except Exception as e:
            logger.error(f"Error creating record in {self.table_name}: {e}")
            return None
    
    def read(self, record_id: str) -> Optional[Dict]:
        """
        Read a record by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            Record or None if not found
        """
        if not self.supabase:
            return None
        
        try:
            result = self.supabase.table(self.table_name).select('*').eq('id', record_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error reading record from {self.table_name}: {e}")
            return None
    
    def update(self, record_id: str, data: Dict[str, Any], validate: bool = True) -> Optional[Dict]:
        """
        Update a record.
        
        Args:
            record_id: Record ID
            data: Dictionary with updated data
            validate: Whether to validate before update
            
        Returns:
            Updated record or None if failed
        """
        if not self.supabase:
            return None
        
        # Validate data
        if validate:
            validation_result = self.validate(data, record_id=record_id)
            if not validation_result['valid']:
                logger.error(f"Validation failed: {validation_result['errors']}")
                return None
        
        # Check baseline
        baseline_result = self.check_baseline(data)
        if baseline_result:
            data['baseline_id'] = baseline_result
        
        # Add updated_at timestamp
        data['updated_at'] = datetime.utcnow().isoformat()
        
        try:
            result = self.supabase.table(self.table_name).update(data).eq('id', record_id).execute()
            if result.data:
                record = result.data[0]
                # Track connection
                self.track_connection(record_id, data)
                logger.info(f"Updated record in {self.table_name}: {record_id}")
                return record
            return None
        except Exception as e:
            logger.error(f"Error updating record in {self.table_name}: {e}")
            return None
    
    def delete(self, record_id: str) -> bool:
        """
        Delete a record.
        
        Args:
            record_id: Record ID
            
        Returns:
            True if deleted, False otherwise
        """
        if not self.supabase:
            return False
        
        try:
            result = self.supabase.table(self.table_name).delete().eq('id', record_id).execute()
            logger.info(f"Deleted record from {self.table_name}: {record_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting record from {self.table_name}: {e}")
            return False
    
    def list(self, filters: Optional[Dict] = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        List records with optional filters.
        
        Args:
            filters: Dictionary with filter conditions
            limit: Maximum number of records
            offset: Offset for pagination
            
        Returns:
            List of records
        """
        if not self.supabase:
            return []
        
        try:
            query = self.supabase.table(self.table_name).select('*')
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        query = query.in_(key, value)
                    else:
                        query = query.eq(key, value)
            
            # Apply pagination
            query = query.limit(limit).offset(offset)
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error listing records from {self.table_name}: {e}")
            return []
    
    def count(self, filters: Optional[Dict] = None) -> int:
        """
        Count records with optional filters.
        
        Args:
            filters: Dictionary with filter conditions
            
        Returns:
            Number of records
        """
        if not self.supabase:
            return 0
        
        try:
            query = self.supabase.table(self.table_name).select('id', count='exact')
            
            # Apply filters
            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        query = query.in_(key, value)
                    else:
                        query = query.eq(key, value)
            
            result = query.execute()
            return result.count if hasattr(result, 'count') else 0
        except Exception as e:
            logger.error(f"Error counting records from {self.table_name}: {e}")
            return 0
    
    @abstractmethod
    def validate(self, data: Dict[str, Any], record_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate data before create/update.
        
        Args:
            data: Data to validate
            record_id: Record ID for updates (None for creates)
            
        Returns:
            Dictionary with 'valid' (bool) and 'errors' (list)
        """
        pass
    
    def check_baseline(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Check data against baselines.
        
        Args:
            data: Data to check
            
        Returns:
            Baseline ID if match found, None otherwise
        """
        if not self.supabase:
            return None
        
        try:
            # Check for matching baseline - select full baseline records from 'baselines' table
            result = self.supabase.table('baselines')\
                .select('id, value')\
                .eq('baseline_type', self.table_name)\
                .execute()
            
            if result.data:
                # Compare with baseline values
                for baseline in result.data:
                    # baseline['value'] contains the baseline data from the 'baselines' table
                    # No need to read from self.table_name - the baseline data is already in baseline['value']
                    if baseline.get('value') and self._compare_with_baseline(data, baseline):
                        return baseline['id']
            
            return None
        except Exception as e:
            logger.warning(f"Error checking baseline: {e}")
            return None
    
    def _compare_with_baseline(self, data: Dict, baseline: Dict) -> bool:
        """
        Compare data with baseline.
        
        Args:
            data: Data to compare
            baseline: Baseline data
            
        Returns:
            True if matches, False otherwise
        """
        # Simple comparison - can be overridden in subclasses
        return data == baseline.get('value', {})
    
    def track_connection(self, record_id: str, data: Dict[str, Any]):
        """
        Track connections to other records.
        
        Args:
            record_id: Record ID
            data: Record data
        """
        if not self.supabase:
            return
        
        try:
            # Extract foreign key references
            connections = []
            for key, value in data.items():
                if key.endswith('_id') and value:
                    connections.append({
                        'from_table': self.table_name,
                        'from_id': record_id,
                        'to_table': key.replace('_id', ''),
                        'to_id': value,
                        'created_at': datetime.utcnow().isoformat()
                    })
            
            # Store connections (if connections table exists)
            if connections:
                # This would insert into a connections table if it exists
                # For now, just log
                logger.info(f"Tracked {len(connections)} connections for {record_id}")
        except Exception as e:
            logger.warning(f"Error tracking connections: {e}")
    
    def batch_create(self, records: List[Dict[str, Any]], validate: bool = True, 
                     batch_size: int = 100) -> Tuple[int, List[str]]:
        """
        Create multiple records in batches.
        
        Args:
            records: List of record dictionaries
            validate: Whether to validate before insertion
            batch_size: Number of records per batch
            
        Returns:
            Tuple of (successful_count, error_messages)
        """
        if not self.supabase:
            return (0, ["Supabase not available"])
        
        successful = 0
        errors = []
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            
            # Validate batch
            if validate:
                validated_batch = []
                for record in batch:
                    validation_result = self.validate(record)
                    if validation_result['valid']:
                        validated_batch.append(record)
                    else:
                        errors.append(f"Validation failed: {validation_result['errors']}")
                batch = validated_batch
            
            if not batch:
                continue
            
            try:
                result = self.supabase.table(self.table_name).insert(batch).execute()
                if result.data:
                    successful += len(result.data)
                    # Track connections
                    for record in result.data:
                        self.track_connection(record['id'], record)
                else:
                    errors.append(f"Batch insert returned no data")
            except Exception as e:
                errors.append(f"Error inserting batch: {e}")
                logger.error(f"Error inserting batch: {e}")
        
        logger.info(f"Batch created {successful}/{len(records)} records in {self.table_name}")
        return (successful, errors)
    
    def search(self, query: str, fields: Optional[List[str]] = None, limit: int = 100) -> List[Dict]:
        """
        Search records by text query.
        
        Args:
            query: Search query
            fields: Fields to search (None for all text fields)
            limit: Maximum number of results
            
        Returns:
            List of matching records
        """
        if not self.supabase:
            return []
        
        try:
            # Simple text search - can be enhanced with full-text search
            result = self.supabase.table(self.table_name).select('*').limit(limit).execute()
            
            if not result.data:
                return []
            
            # Filter by query
            matches = []
            query_lower = query.lower()
            
            for record in result.data:
                if fields:
                    search_fields = fields
                else:
                    # Search all text fields
                    search_fields = [k for k, v in record.items() if isinstance(v, str)]
                
                for field in search_fields:
                    if field in record and query_lower in str(record[field]).lower():
                        matches.append(record)
                        break
            
            return matches
        except Exception as e:
            logger.error(f"Error searching {self.table_name}: {e}")
            return []


# Example implementation for Authors table
class AuthorsTable(DataTable):
    """Authors table implementation."""
    
    def __init__(self):
        super().__init__('authors')
    
    def validate(self, data: Dict[str, Any], record_id: Optional[str] = None) -> Dict[str, Any]:
        """Validate author data."""
        errors = []
        
        # Required fields
        if 'username' not in data or not data['username']:
            errors.append("username is required")
        
        if 'platform' not in data or not data['platform']:
            errors.append("platform is required")
        
        # Check uniqueness
        if not record_id:  # Only check on create
            if self.supabase:
                try:
                    existing = self.supabase.table(self.table_name)\
                        .select('id')\
                        .eq('username', data['username'])\
                        .eq('platform', data['platform'])\
                        .execute()
                    if existing.data:
                        errors.append(f"Author {data['username']} on {data['platform']} already exists")
                except Exception as e:
                    logger.warning(f"Could not check uniqueness: {e}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }


# Example implementation for Sources table
class SourcesTable(DataTable):
    """Sources table implementation."""
    
    def __init__(self):
        super().__init__('sources')
    
    def validate(self, data: Dict[str, Any], record_id: Optional[str] = None) -> Dict[str, Any]:
        """Validate source data."""
        errors = []
        
        # Required fields
        if 'url' not in data or not data['url']:
            errors.append("url is required")
        
        if 'source_type' not in data or not data['source_type']:
            errors.append("source_type is required")
        
        # Check URL uniqueness
        if not record_id:  # Only check on create
            if self.supabase:
                try:
                    existing = self.supabase.table(self.table_name)\
                        .select('id')\
                        .eq('url', data['url'])\
                        .execute()
                    if existing.data:
                        errors.append(f"Source with URL {data['url']} already exists")
                except Exception as e:
                    logger.warning(f"Could not check uniqueness: {e}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

