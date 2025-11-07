"""
Unified Database Conductor
Purpose: Unified database access, no silos, flow visualization, sequence tracking
- Unified database access
- No silos
- Flow visualization
- Sequence tracking
- n8n-style workflow view

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
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


class UnifiedConductor:
    """
    Unified Database Conductor - Manages all database operations without silos
    """
    
    def __init__(self):
        """Initialize unified conductor"""
        self.supabase = supabase if HAS_SUPABASE else None
        self.flow_history: List[Dict] = []
        self.sequence_tracking: OrderedDict = OrderedDict()
        logger.info("Unified conductor initialized")
    
    def execute_operation(self, operation: str, table: str, data: Dict, 
                          operation_type: str = 'read') -> Any:
        """
        Execute a database operation and track it.
        
        Args:
            operation: Operation name
            table: Table name
            data: Operation data
            operation_type: Operation type ('read', 'write', 'update', 'delete')
            
        Returns:
            Operation result
        """
        if not self.supabase:
            logger.warning("Supabase not available, operation not executed")
            return None
        
        try:
            # Track operation in flow history
            flow_entry = {
                'operation': operation,
                'table': table,
                'operation_type': operation_type,
                'timestamp': datetime.utcnow().isoformat(),
                'data': data
            }
            self.flow_history.append(flow_entry)
            
            # Track in sequence
            sequence_key = f"{table}_{operation}"
            self.sequence_tracking[sequence_key] = {
                'operation': operation,
                'table': table,
                'operation_type': operation_type,
                'timestamp': datetime.utcnow().isoformat(),
                'count': self.sequence_tracking.get(sequence_key, {}).get('count', 0) + 1
            }
            
            # Execute operation
            if operation_type == 'read':
                result = self._execute_read(table, data)
            elif operation_type == 'write':
                result = self._execute_write(table, data)
            elif operation_type == 'update':
                result = self._execute_update(table, data)
            elif operation_type == 'delete':
                result = self._execute_delete(table, data)
            else:
                result = None
            
            # Update flow entry with result
            flow_entry['result'] = result
            flow_entry['success'] = result is not None
            
            logger.info(f"Executed operation: {operation} on {table}")
            return result
            
        except Exception as e:
            logger.error(f"Error executing operation: {e}")
            flow_entry['error'] = str(e)
            flow_entry['success'] = False
            return None
    
    def _execute_read(self, table: str, data: Dict) -> Any:
        """Execute read operation."""
        try:
            query = self.supabase.table(table).select('*')
            
            # Apply filters
            if 'filters' in data:
                for key, value in data['filters'].items():
                    if isinstance(value, list):
                        query = query.in_(key, value)
                    else:
                        query = query.eq(key, value)
            
            # Apply pagination
            if 'limit' in data:
                query = query.limit(data['limit'])
            if 'offset' in data:
                query = query.offset(data['offset'])
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error executing read: {e}")
            return None
    
    def _execute_write(self, table: str, data: Dict) -> Any:
        """Execute write operation."""
        try:
            result = self.supabase.table(table).insert(data).execute()
            return result.data if result.data else None
        except Exception as e:
            logger.error(f"Error executing write: {e}")
            return None
    
    def _execute_update(self, table: str, data: Dict) -> Any:
        """Execute update operation."""
        try:
            record_id = data.get('id')
            update_data = {k: v for k, v in data.items() if k != 'id'}
            
            result = self.supabase.table(table).update(update_data).eq('id', record_id).execute()
            return result.data if result.data else None
        except Exception as e:
            logger.error(f"Error executing update: {e}")
            return None
    
    def _execute_delete(self, table: str, data: Dict) -> Any:
        """Execute delete operation."""
        try:
            record_id = data.get('id')
            result = self.supabase.table(table).delete().eq('id', record_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error executing delete: {e}")
            return None
    
    def get_flow_history(self, limit: int = 100) -> List[Dict]:
        """
        Get flow history.
        
        Args:
            limit: Maximum number of entries
            
        Returns:
            List of flow history entries
        """
        return self.flow_history[-limit:]
    
    def get_sequence_tracking(self) -> Dict:
        """
        Get sequence tracking data.
        
        Returns:
            Dictionary with sequence tracking data
        """
        return dict(self.sequence_tracking)
    
    def visualize_flow(self) -> Dict:
        """
        Generate flow visualization data (n8n-style).
        
        Returns:
            Dictionary with flow visualization data
        """
        nodes = []
        edges = []
        
        # Create nodes for each table
        tables = set()
        for entry in self.flow_history:
            tables.add(entry['table'])
        
        for i, table in enumerate(tables):
            nodes.append({
                'id': f"table_{i}",
                'label': table,
                'type': 'table',
                'position': {'x': i * 200, 'y': 0}
            })
        
        # Create edges for operations
        for i, entry in enumerate(self.flow_history):
            if i > 0:
                prev_entry = self.flow_history[i-1]
                edges.append({
                    'id': f"edge_{i}",
                    'source': f"table_{list(tables).index(prev_entry['table'])}",
                    'target': f"table_{list(tables).index(entry['table'])}",
                    'label': entry['operation']
                })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'flow_history': self.flow_history
        }


# Singleton instance
_unified_conductor = None

def get_unified_conductor() -> UnifiedConductor:
    """Get or create unified conductor singleton."""
    global _unified_conductor
    if _unified_conductor is None:
        _unified_conductor = UnifiedConductor()
    return _unified_conductor

