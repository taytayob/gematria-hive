"""
Baseline Manager
Purpose: Manage baseline tracking for validation and comparison
- Create and manage baselines
- Baseline validation
- Baseline comparison
- Baseline updates
- Baseline history

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

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


class BaselineManager:
    """
    Baseline Manager - Manages baselines for validation
    """
    
    def __init__(self):
        """Initialize baseline manager"""
        self.supabase = supabase if HAS_SUPABASE else None
        logger.info("Initialized BaselineManager")
    
    def create_baseline(self, baseline_type: str, value: Dict, source: str = '') -> Optional[str]:
        """
        Create a new baseline.
        
        Args:
            baseline_type: Baseline type (e.g., 'gematria', 'phonetic', 'symbol')
            value: Baseline value dictionary
            source: Source of baseline
            
        Returns:
            Baseline ID or None
        """
        if not self.supabase:
            return None
        
        try:
            baseline_data = {
                'baseline_type': baseline_type,
                'value': value,
                'source': source,
                'validated': False,
                'validation_notes': '',
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('baselines').insert(baseline_data).execute()
            
            if result.data:
                baseline_id = result.data[0]['id']
                logger.info(f"Created baseline: {baseline_type} (ID: {baseline_id})")
                return baseline_id
            
            return None
        except Exception as e:
            logger.error(f"Error creating baseline: {e}")
            return None
    
    def get_baseline(self, baseline_type: str) -> Optional[Dict]:
        """
        Get baseline by type.
        
        Args:
            baseline_type: Baseline type
            
        Returns:
            Baseline dictionary or None
        """
        if not self.supabase:
            return None
        
        try:
            result = self.supabase.table('baselines')\
                .select('*')\
                .eq('baseline_type', baseline_type)\
                .eq('validated', True)\
                .order('created_at', desc=True)\
                .limit(1)\
                .execute()
            
            if result.data:
                return result.data[0]
            
            return None
        except Exception as e:
            logger.error(f"Error getting baseline: {e}")
            return None
    
    def validate_baseline(self, baseline_id: str, validation_notes: str = ''):
        """
        Validate a baseline.
        
        Args:
            baseline_id: Baseline ID
            validation_notes: Validation notes
        """
        if not self.supabase:
            return
        
        try:
            self.supabase.table('baselines')\
                .update({
                    'validated': True,
                    'validation_notes': validation_notes,
                    'updated_at': datetime.utcnow().isoformat()
                })\
                .eq('id', baseline_id)\
                .execute()
            
            logger.info(f"Validated baseline: {baseline_id}")
        except Exception as e:
            logger.error(f"Error validating baseline: {e}")
    
    def compare_with_baseline(self, baseline_type: str, value: Dict) -> Dict:
        """
        Compare value with baseline.
        
        Args:
            baseline_type: Baseline type
            value: Value to compare
            
        Returns:
            Comparison result dictionary
        """
        baseline = self.get_baseline(baseline_type)
        
        if not baseline:
            return {
                'matches': False,
                'similarity': 0.0,
                'notes': 'No baseline found'
            }
        
        baseline_value = baseline.get('value', {})
        
        # Calculate similarity
        similarity = self._calculate_similarity(value, baseline_value)
        
        return {
            'matches': similarity >= 0.8,  # 80% similarity threshold
            'similarity': similarity,
            'baseline_id': baseline['id'],
            'notes': f"Similarity: {similarity:.2f}"
        }
    
    def _calculate_similarity(self, value1: Dict, value2: Dict) -> float:
        """
        Calculate similarity between two values.
        
        Args:
            value1: First value dictionary
            value2: Second value dictionary
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not isinstance(value1, dict) or not isinstance(value2, dict):
            return 0.0
        
        # Count matching keys
        keys1 = set(value1.keys())
        keys2 = set(value2.keys())
        common_keys = keys1.intersection(keys2)
        
        if not common_keys:
            return 0.0
        
        # Count matching values
        matches = 0
        for key in common_keys:
            if value1[key] == value2[key]:
                matches += 1
        
        # Calculate similarity
        similarity = matches / max(len(keys1), len(keys2), 1)
        
        return similarity
    
    def update_baseline(self, baseline_id: str, value: Dict):
        """
        Update baseline value.
        
        Args:
            baseline_id: Baseline ID
            value: New baseline value
        """
        if not self.supabase:
            return
        
        try:
            self.supabase.table('baselines')\
                .update({
                    'value': value,
                    'validated': False,  # Re-validate after update
                    'updated_at': datetime.utcnow().isoformat()
                })\
                .eq('id', baseline_id)\
                .execute()
            
            logger.info(f"Updated baseline: {baseline_id}")
        except Exception as e:
            logger.error(f"Error updating baseline: {e}")
    
    def get_all_baselines(self) -> List[Dict]:
        """
        Get all baselines.
        
        Returns:
            List of baseline dictionaries
        """
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table('baselines')\
                .select('*')\
                .order('created_at', desc=True)\
                .execute()
            
            if result.data:
                return result.data
            
            return []
        except Exception as e:
            logger.error(f"Error getting all baselines: {e}")
            return []


# Singleton instance
_baseline_manager = None

def get_baseline_manager() -> BaselineManager:
    """Get or create baseline manager singleton."""
    global _baseline_manager
    if _baseline_manager is None:
        _baseline_manager = BaselineManager()
    return _baseline_manager

