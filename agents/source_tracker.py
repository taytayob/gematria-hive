"""
Source Tracker Agent
Purpose: Create source repository tracking with extraction metadata
- Track all sources with extraction metadata
- Link sources to authors, patterns, proofs
- Track extraction reasons and PRD alignment
- Monitor source relevance and importance
- Update source status and processing

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

from agents.orchestrator import AgentState
from core.data_table import DataTable

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


class SourceTrackerAgent(DataTable):
    """
    Source Tracker Agent - Tracks sources with extraction metadata
    """
    
    def __init__(self):
        """Initialize source tracker agent"""
        super().__init__('sources')
        self.name = "source_tracker_agent"
        logger.info(f"Initialized {self.name}")
    
    def track_source(self, url: str, source_type: str, title: str = '', 
                     content: str = '', extracted_data: Dict = None,
                     extraction_reason: str = '', prd_alignment: Dict = None,
                     author_id: Optional[str] = None, tags: List[str] = None) -> Optional[str]:
        """
        Track a source with extraction metadata.
        
        Args:
            url: Source URL
            source_type: Source type ('bookmark', 'tweet', 'thread', 'article', etc.)
            title: Source title
            content: Source content
            extracted_data: Extracted data dictionary
            extraction_reason: Reason for extraction
            prd_alignment: PRD alignment dictionary
            author_id: Author ID
            tags: List of tags
            
        Returns:
            Source ID or None
        """
        if not self.supabase:
            return None
        
        try:
            source_data = {
                'url': url,
                'source_type': source_type,
                'title': title,
                'content': content,
                'extracted_data': extracted_data or {},
                'extraction_reason': extraction_reason,
                'prd_alignment': prd_alignment or {},
                'author_id': author_id,
                'tags': tags or [],
                'relevance_score': 0.5,  # Default relevance
                'metadata': {},
                'ingested_at': datetime.utcnow().isoformat()
            }
            
            # Check if source already exists
            existing = self.supabase.table('sources')\
                .select('id')\
                .eq('url', url)\
                .limit(1)\
                .execute()
            
            if existing.data:
                # Update existing source
                source_id = existing.data[0]['id']
                self.supabase.table('sources')\
                    .update({
                        'extracted_data': source_data['extracted_data'],
                        'extraction_reason': extraction_reason,
                        'prd_alignment': prd_alignment or {},
                        'relevance_score': source_data['relevance_score'],
                        'processed_at': datetime.utcnow().isoformat()
                    })\
                    .eq('id', source_id)\
                    .execute()
                
                logger.info(f"Updated source: {url}")
                return source_id
            else:
                # Create new source
                result = self.supabase.table('sources').insert(source_data).execute()
                
                if result.data:
                    source_id = result.data[0]['id']
                    logger.info(f"Tracked new source: {url} (ID: {source_id})")
                    return source_id
            
            return None
        except Exception as e:
            logger.error(f"Error tracking source: {e}")
            return None
    
    def calculate_relevance_score(self, source_id: str) -> float:
        """
        Calculate relevance score for a source.
        
        Args:
            source_id: Source ID
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        if not self.supabase:
            return 0.5
        
        try:
            # Get source
            source = self.read(source_id)
            
            if not source:
                return 0.5
            
            # Calculate relevance based on:
            # - Extraction data quality
            # - PRD alignment
            # - Number of tags
            # - Author presence
            extracted_data = source.get('extracted_data', {})
            prd_alignment = source.get('prd_alignment', {})
            tags = source.get('tags', [])
            author_id = source.get('author_id')
            
            # Score components
            extraction_score = 0.3 if extracted_data else 0.0
            prd_score = 0.3 if prd_alignment else 0.0
            tags_score = min(len(tags) / 5.0, 0.2)  # Normalize to 5 tags
            author_score = 0.2 if author_id else 0.0
            
            relevance = extraction_score + prd_score + tags_score + author_score
            
            return min(relevance, 1.0)
        except Exception as e:
            logger.error(f"Error calculating relevance score: {e}")
            return 0.5
    
    def update_prd_alignment(self, source_id: str, prd_alignment: Dict):
        """
        Update PRD alignment for a source.
        
        Args:
            source_id: Source ID
            prd_alignment: PRD alignment dictionary
        """
        if not self.supabase:
            return
        
        try:
            self.supabase.table('sources')\
                .update({
                    'prd_alignment': prd_alignment,
                    'relevance_score': self.calculate_relevance_score(source_id),
                    'updated_at': datetime.utcnow().isoformat()
                })\
                .eq('id', source_id)\
                .execute()
            
            logger.info(f"Updated PRD alignment for source: {source_id}")
        except Exception as e:
            logger.error(f"Error updating PRD alignment: {e}")
    
    def link_to_patterns(self, source_id: str, pattern_ids: List[str]):
        """
        Link source to patterns.
        
        Args:
            source_id: Source ID
            pattern_ids: List of pattern IDs
        """
        if not self.supabase:
            return
        
        try:
            # Get source
            source = self.read(source_id)
            
            if source:
                # Update patterns in source metadata
                metadata = source.get('metadata', {})
                metadata['pattern_ids'] = pattern_ids
                
                self.update(source_id, {'metadata': metadata})
                
                logger.info(f"Linked source {source_id} to {len(pattern_ids)} patterns")
        except Exception as e:
            logger.error(f"Error linking source to patterns: {e}")
    
    def link_to_proofs(self, source_id: str, proof_ids: List[str]):
        """
        Link source to proofs.
        
        Args:
            source_id: Source ID
            proof_ids: List of proof IDs
        """
        if not self.supabase:
            return
        
        try:
            # Get source
            source = self.read(source_id)
            
            if source:
                # Update proofs in source metadata
                metadata = source.get('metadata', {})
                metadata['proof_ids'] = proof_ids
                
                self.update(source_id, {'metadata': metadata})
                
                logger.info(f"Linked source {source_id} to {len(proof_ids)} proofs")
        except Exception as e:
            logger.error(f"Error linking source to proofs: {e}")
    
    def get_sources_by_relevance(self, min_relevance: float = 0.7, limit: int = 100) -> List[Dict]:
        """
        Get sources by relevance score.
        
        Args:
            min_relevance: Minimum relevance score
            limit: Maximum number of results
            
        Returns:
            List of source dictionaries
        """
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table('sources')\
                .select('*')\
                .gte('relevance_score', min_relevance)\
                .order('relevance_score', desc=True)\
                .limit(limit)\
                .execute()
            
            if result.data:
                return result.data
            
            return []
        except Exception as e:
            logger.error(f"Error getting sources by relevance: {e}")
            return []
    
    def validate(self, data: Dict, record_id: Optional[str] = None) -> Dict:
        """Validate source data."""
        errors = []
        
        # Required fields
        if 'url' not in data or not data['url']:
            errors.append("url is required")
        
        if 'source_type' not in data or not data['source_type']:
            errors.append("source_type is required")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute source tracking task.
        
        Args:
            state: Agent state with source data
            
        Returns:
            Updated state with tracking results
        """
        data = state.get("data", [])
        
        if not data:
            logger.warning("No data provided for source tracking")
            return state
        
        logger.info(f"Source tracker agent: Processing {len(data)} sources")
        
        try:
            tracked_sources = []
            
            for source in data:
                if not isinstance(source, dict):
                    continue
                
                url = source.get('url')
                if not url:
                    continue
                
                # Track source
                source_id = self.track_source(
                    url=url,
                    source_type=source.get('source_type', 'unknown'),
                    title=source.get('title', ''),
                    content=source.get('content', ''),
                    extracted_data=source.get('extracted_data', {}),
                    extraction_reason=source.get('extraction_reason', ''),
                    prd_alignment=source.get('prd_alignment', {}),
                    author_id=source.get('author_id'),
                    tags=source.get('tags', [])
                )
                
                if source_id:
                    # Calculate relevance score
                    relevance_score = self.calculate_relevance_score(source_id)
                    
                    # Update relevance score
                    self.update(source_id, {'relevance_score': relevance_score})
                    
                    tracked_sources.append({
                        'source_id': source_id,
                        'url': url,
                        'relevance_score': relevance_score
                    })
            
            # Update state
            state["context"]["tracked_sources"] = tracked_sources
            state["context"]["sources_count"] = len(tracked_sources)
            state["results"].append({
                "agent": self.name,
                "action": "track_sources",
                "count": len(tracked_sources),
                "sources": tracked_sources
            })
            
            logger.info(f"Source tracking complete: {len(tracked_sources)} sources tracked")
            
        except Exception as e:
            logger.error(f"Source tracking error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

