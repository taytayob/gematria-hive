"""
Gematria Integrator Agent
Purpose: Run key terms through gematria calculator
- Extract key terms from content
- Calculate gematria values (Jewish, English, Simple, Hebrew variants)
- Store gematria results in key_terms table
- Find related terms by gematria value
- Detect gematria patterns and connections

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import re
from typing import Dict, List, Optional
from datetime import datetime

from agents.orchestrator import AgentState
from core.gematria_engine import get_gematria_engine

# Load environment variables
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


class GematriaIntegratorAgent:
    """
    Gematria Integrator Agent - Integrates gematria calculations with key terms
    """
    
    def __init__(self):
        """Initialize gematria integrator agent"""
        self.name = "gematria_integrator_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        self.gematria_engine = get_gematria_engine()
        logger.info(f"Initialized {self.name}")
    
    def extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key terms from text.
        
        Args:
            text: Text to extract terms from
            
        Returns:
            List of key terms
        """
        # Simple extraction - can be enhanced with NLP
        # Extract words (3+ characters, alphanumeric)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        
        # Filter common words
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        key_terms = [word.lower() for word in words if word.lower() not in common_words]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_terms = []
        for term in key_terms:
            if term not in seen:
                seen.add(term)
                unique_terms.append(term)
        
        return unique_terms
    
    def calculate_gematria_for_term(self, term: str) -> Dict:
        """
        Calculate all gematria values for a term.
        
        Args:
            term: Term to calculate
            
        Returns:
            Dictionary with all gematria values
        """
        return self.gematria_engine.calculate_all(term)
    
    def find_related_terms(self, gematria_values: Dict, method: str = 'jewish_gematria') -> List[Dict]:
        """
        Find related terms by gematria value.
        
        Args:
            gematria_values: Dictionary with gematria values
            method: Method to use for matching
            
        Returns:
            List of related term dictionaries
        """
        if not self.supabase:
            return []
        
        try:
            value = gematria_values.get(method)
            if value is None:
                return []
            
            # Map method to column name
            column_map = {
                'jewish_gematria': 'jewish_gematria',
                'english_gematria': 'english_gematria',
                'simple_gematria': 'simple_gematria',
                'hebrew_full': 'hebrew_full',
                'hebrew_musafi': 'hebrew_musafi',
                'hebrew_katan': 'hebrew_katan',
                'hebrew_ordinal': 'hebrew_ordinal',
                'hebrew_atbash': 'hebrew_atbash',
                'hebrew_kidmi': 'hebrew_kidmi',
                'hebrew_perati': 'hebrew_perati',
                'hebrew_shemi': 'hebrew_shemi'
            }
            
            column = column_map.get(method, method)
            
            # Find words with same gematria value
            result = self.supabase.table('gematria_words')\
                .select('*')\
                .eq(column, value)\
                .limit(100)\
                .execute()
            
            if result.data:
                return result.data
            
            return []
        except Exception as e:
            logger.error(f"Error finding related terms: {e}")
            return []
    
    def store_key_term(self, term: str, gematria_values: Dict, source_ids: List[str] = None, 
                       context: str = '') -> Optional[str]:
        """
        Store key term with gematria values.
        
        Args:
            term: Term to store
            gematria_values: Dictionary with gematria values
            source_ids: List of source IDs
            context: Context for the term
            
        Returns:
            Key term ID or None
        """
        if not self.supabase:
            return None
        
        try:
            # Check if term already exists
            existing = self.supabase.table('key_terms')\
                .select('id')\
                .eq('term', term)\
                .limit(1)\
                .execute()
            
            term_data = {
                'term': term,
                'term_type': 'gematria',
                'gematria_values': gematria_values,
                'context': context,
                'frequency': 1,
                'first_seen_at': datetime.utcnow().isoformat(),
                'last_seen_at': datetime.utcnow().isoformat()
            }
            
            if source_ids:
                term_data['source_ids'] = source_ids
            
            if existing.data:
                # Update existing term
                term_id = existing.data[0]['id']
                
                # Merge gematria values
                existing_gematria = existing.data[0].get('gematria_values', {})
                if isinstance(existing_gematria, dict):
                    merged_gematria = {**existing_gematria, **gematria_values}
                else:
                    merged_gematria = gematria_values
                
                # Merge source IDs
                existing_source_ids = existing.data[0].get('source_ids', [])
                if isinstance(existing_source_ids, list):
                    merged_source_ids = list(set(existing_source_ids + (source_ids or [])))
                else:
                    merged_source_ids = source_ids or []
                
                self.supabase.table('key_terms')\
                    .update({
                        'gematria_values': merged_gematria,
                        'source_ids': merged_source_ids,
                        'last_seen_at': datetime.utcnow().isoformat(),
                        'frequency': existing.data[0].get('frequency', 0) + 1
                    })\
                    .eq('id', term_id)\
                    .execute()
                
                logger.info(f"Updated key term: {term}")
                return term_id
            else:
                # Create new term
                result = self.supabase.table('key_terms').insert(term_data).execute()
                
                if result.data:
                    term_id = result.data[0]['id']
                    logger.info(f"Created key term: {term}")
                    return term_id
            
            return None
        except Exception as e:
            logger.error(f"Error storing key term: {e}")
            return None
    
    def process_source(self, source: Dict) -> Dict:
        """
        Process a source and extract/calculate gematria for key terms.
        
        Args:
            source: Source dictionary
            
        Returns:
            Dictionary with processed terms
        """
        content = source.get('content', '') or source.get('title', '') or source.get('description', '')
        source_id = source.get('id')
        
        if not content:
            return {'terms': [], 'related_terms': []}
        
        # Extract key terms
        key_terms = self.extract_key_terms(content)
        
        # Calculate gematria for each term
        processed_terms = []
        all_related_terms = []
        
        for term in key_terms:
            # Calculate gematria values
            gematria_values = self.calculate_gematria_for_term(term)
            
            # Store key term
            term_id = self.store_key_term(term, gematria_values, [source_id] if source_id else None, content)
            
            if term_id:
                processed_terms.append({
                    'term': term,
                    'term_id': term_id,
                    'gematria_values': gematria_values
                })
                
                # Find related terms
                related_terms = self.find_related_terms(gematria_values, 'jewish_gematria')
                all_related_terms.extend(related_terms)
        
        return {
            'terms': processed_terms,
            'related_terms': all_related_terms
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute gematria integration task.
        
        Args:
            state: Agent state with source data
            
        Returns:
            Updated state with gematria calculations
        """
        data = state.get("data", [])
        
        if not data:
            logger.warning("No data provided for gematria integration")
            return state
        
        logger.info(f"Gematria integrator agent: Processing {len(data)} sources")
        
        try:
            all_processed = []
            total_terms = 0
            total_related = 0
            
            for source in data:
                if not isinstance(source, dict):
                    continue
                
                # Process source
                processed = self.process_source(source)
                all_processed.append({
                    'source_id': source.get('id'),
                    'processed': processed
                })
                
                total_terms += len(processed['terms'])
                total_related += len(processed['related_terms'])
            
            # Update state
            state["context"]["gematria_processed"] = all_processed
            state["context"]["total_terms"] = total_terms
            state["context"]["total_related_terms"] = total_related
            state["results"].append({
                "agent": self.name,
                "action": "integrate_gematria",
                "sources_processed": len(all_processed),
                "total_terms": total_terms,
                "total_related_terms": total_related
            })
            
            logger.info(f"Gematria integration complete: {total_terms} terms processed, {total_related} related terms found")
            
        except Exception as e:
            logger.error(f"Gematria integration error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

