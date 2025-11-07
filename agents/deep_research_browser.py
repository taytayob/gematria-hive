"""
Deep Research Browser Agent
Purpose: Build deep research browser agent for topic exploration
- Topic-based research
- Multi-source gathering
- Proof collection
- Importance scoring
- Research status tracking
- Lead generation

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime

from agents.orchestrator import AgentState
from agents.browser import BrowserAgent
from agents.perplexity_integrator import PerplexityIntegratorAgent

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


class DeepResearchBrowserAgent:
    """
    Deep Research Browser Agent - Conducts deep research on topics
    """
    
    def __init__(self):
        """Initialize deep research browser agent"""
        self.name = "deep_research_browser_agent"
        self.supabase = supabase if HAS_SUPABASE else None
        self.browser_agent = BrowserAgent()
        self.perplexity_agent = PerplexityIntegratorAgent()
        logger.info(f"Initialized {self.name}")
    
    def create_research_topic(self, topic_name: str, topic_description: str = '') -> Optional[str]:
        """
        Create a new research topic.
        
        Args:
            topic_name: Topic name
            topic_description: Topic description
            
        Returns:
            Research topic ID or None
        """
        if not self.supabase:
            return None
        
        try:
            topic_data = {
                'topic_name': topic_name,
                'topic_description': topic_description,
                'importance_score': 0.5,  # Default importance
                'proofs': {},
                'beliefs': {},
                'needs': {},
                'monitoring': {},
                'potential_leads': {},
                'sources': [],
                'key_terms': [],
                'patterns': [],
                'research_status': 'active',
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = self.supabase.table('research_topics').insert(topic_data).execute()
            
            if result.data:
                topic_id = result.data[0]['id']
                logger.info(f"Created research topic: {topic_name} (ID: {topic_id})")
                return topic_id
            
            return None
        except Exception as e:
            logger.error(f"Error creating research topic: {e}")
            return None
    
    def gather_sources(self, topic_id: str, query: str) -> List[Dict]:
        """
        Gather sources for a research topic.
        
        Args:
            topic_id: Research topic ID
            query: Search query
            
        Returns:
            List of source dictionaries
        """
        sources = []
        
        # Use Perplexity to search
        try:
            search_results = self.perplexity_agent.search(query)
            if search_results:
                citations = search_results.get('citations', [])
                for citation in citations:
                    if isinstance(citation, str):
                        url = citation
                    elif isinstance(citation, dict):
                        url = citation.get('url', '')
                    else:
                        continue
                    
                    if url:
                        source = {
                            'url': url,
                            'source_type': 'research',
                            'title': query,
                            'content': search_results.get('content', '')[:500],
                            'relevance_score': 0.8,  # Default relevance
                            'tags': ['research', 'perplexity'],
                            'metadata': {
                                'query': query,
                                'topic_id': topic_id
                            }
                        }
                        sources.append(source)
        except Exception as e:
            logger.error(f"Error gathering sources via Perplexity: {e}")
        
        # Use browser agent to scrape URLs
        for source in sources:
            url = source.get('url')
            if url:
                try:
                    # Scrape URL using browser agent
                    browser_state = {
                        'task': {'type': 'browser', 'url': url},
                        'data': [],
                        'context': {},
                        'results': [],
                        'cost': 0.0,
                        'status': 'pending',
                        'memory_id': None
                    }
                    browser_state = self.browser_agent.execute(browser_state)
                    
                    if browser_state.get('data'):
                        # Update source with scraped content
                        scraped_data = browser_state['data'][0] if browser_state['data'] else {}
                        source['content'] = scraped_data.get('content', source.get('content', ''))
                        source['images'] = scraped_data.get('images', [])
                        source['links'] = scraped_data.get('links', [])
                except Exception as e:
                    logger.warning(f"Error scraping {url}: {e}")
        
        return sources
    
    def collect_proofs(self, topic_id: str, sources: List[Dict]) -> List[Dict]:
        """
        Collect proofs from sources.
        
        Args:
            topic_id: Research topic ID
            sources: List of source dictionaries
            
        Returns:
            List of proof dictionaries
        """
        proofs = []
        
        for source in sources:
            # Extract proofs from source content
            content = source.get('content', '')
            if content:
                # Simple proof extraction (can be enhanced with NLP)
                proof = {
                    'proof_name': f"Proof from {source.get('url', 'unknown')}",
                    'proof_type': 'research',
                    'theorem': content[:200],  # First 200 chars as theorem
                    'evidence': {
                        'source_url': source.get('url'),
                        'content': content[:500],
                        'relevance_score': source.get('relevance_score', 0.5)
                    },
                    'sources': [source.get('id')] if source.get('id') else [],
                    'research_topic_id': topic_id
                }
                proofs.append(proof)
        
        return proofs
    
    def calculate_importance_score(self, topic_id: str) -> float:
        """
        Calculate importance score for a research topic.
        
        Args:
            topic_id: Research topic ID
            
        Returns:
            Importance score (0.0 to 1.0)
        """
        if not self.supabase:
            return 0.5
        
        try:
            # Get topic
            topic = self.supabase.table('research_topics')\
                .select('*')\
                .eq('id', topic_id)\
                .limit(1)\
                .execute()
            
            if not topic.data:
                return 0.5
            
            topic_data = topic.data[0]
            
            # Calculate importance based on:
            # - Number of sources
            # - Number of proofs
            # - Number of patterns
            # - Number of key terms
            sources_count = len(topic_data.get('sources', []))
            proofs_count = len(topic_data.get('proofs', {}).keys()) if isinstance(topic_data.get('proofs'), dict) else 0
            patterns_count = len(topic_data.get('patterns', []))
            key_terms_count = len(topic_data.get('key_terms', []))
            
            # Normalize scores
            sources_score = min(sources_count / 10.0, 1.0)  # Normalize to 10 sources
            proofs_score = min(proofs_count / 5.0, 1.0)  # Normalize to 5 proofs
            patterns_score = min(patterns_count / 3.0, 1.0)  # Normalize to 3 patterns
            key_terms_score = min(key_terms_count / 10.0, 1.0)  # Normalize to 10 terms
            
            # Weighted average
            importance = (sources_score * 0.3) + (proofs_score * 0.3) + (patterns_score * 0.2) + (key_terms_score * 0.2)
            
            return min(importance, 1.0)
        except Exception as e:
            logger.error(f"Error calculating importance score: {e}")
            return 0.5
    
    def generate_leads(self, topic_id: str) -> List[Dict]:
        """
        Generate potential leads for a research topic.
        
        Args:
            topic_id: Research topic ID
            
        Returns:
            List of lead dictionaries
        """
        leads = []
        
        if not self.supabase:
            return leads
        
        try:
            # Get topic
            topic = self.supabase.table('research_topics')\
                .select('*')\
                .eq('id', topic_id)\
                .limit(1)\
                .execute()
            
            if not topic.data:
                return leads
            
            topic_data = topic.data[0]
            key_terms = topic_data.get('key_terms', [])
            
            # Generate leads based on key terms
            for term_id in key_terms[:5]:  # Top 5 key terms
                try:
                    term = self.supabase.table('key_terms')\
                        .select('*')\
                        .eq('id', term_id)\
                        .limit(1)\
                        .execute()
                    
                    if term.data:
                        term_name = term.data[0].get('term', '')
                        if term_name:
                            # Search for related resources
                            lead = {
                                'term': term_name,
                                'type': 'key_term',
                                'description': f"Research lead based on key term: {term_name}",
                                'priority': 'medium'
                            }
                            leads.append(lead)
                except Exception as e:
                    logger.warning(f"Error generating lead for term {term_id}: {e}")
            
            return leads
        except Exception as e:
            logger.error(f"Error generating leads: {e}")
            return leads
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute deep research task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with research results
        """
        task = state.get("task", {})
        topic_name = task.get("topic_name", "")
        query = task.get("query", topic_name)
        
        if not topic_name:
            logger.error("No topic name provided for deep research")
            state["status"] = "failed"
            state["error"] = "No topic name provided"
            return state
        
        logger.info(f"Deep research browser agent: Researching topic {topic_name}")
        
        try:
            # Create research topic
            topic_id = self.create_research_topic(topic_name, task.get("description", ""))
            
            if not topic_id:
                logger.error(f"Failed to create research topic: {topic_name}")
                state["status"] = "failed"
                state["error"] = "Failed to create research topic"
                return state
            
            # Gather sources
            sources = self.gather_sources(topic_id, query)
            
            # Store sources
            source_ids = []
            for source in sources:
                try:
                    result = self.supabase.table('sources').upsert(source, on_conflict='url').execute()
                    if result.data:
                        source_ids.append(result.data[0]['id'])
                except Exception as e:
                    logger.warning(f"Error storing source: {e}")
            
            # Collect proofs
            proofs = self.collect_proofs(topic_id, sources)
            
            # Store proofs
            proof_ids = []
            for proof in proofs:
                try:
                    result = self.supabase.table('proofs').insert(proof).execute()
                    if result.data:
                        proof_ids.append(result.data[0]['id'])
                except Exception as e:
                    logger.warning(f"Error storing proof: {e}")
            
            # Calculate importance score
            importance_score = self.calculate_importance_score(topic_id)
            
            # Generate leads
            leads = self.generate_leads(topic_id)
            
            # Update research topic
            if self.supabase:
                self.supabase.table('research_topics')\
                    .update({
                        'sources': source_ids,
                        'importance_score': importance_score,
                        'potential_leads': leads,
                        'updated_at': datetime.utcnow().isoformat()
                    })\
                    .eq('id', topic_id)\
                    .execute()
            
            # Update state
            state["context"]["research_topic_id"] = topic_id
            state["context"]["sources_count"] = len(sources)
            state["context"]["proofs_count"] = len(proofs)
            state["context"]["importance_score"] = importance_score
            state["context"]["leads"] = leads
            state["results"].append({
                "agent": self.name,
                "action": "deep_research",
                "topic_name": topic_name,
                "topic_id": topic_id,
                "sources_count": len(sources),
                "proofs_count": len(proofs),
                "importance_score": importance_score
            })
            
            logger.info(f"Deep research complete: {topic_name} (importance: {importance_score:.2f})")
            
        except Exception as e:
            logger.error(f"Deep research error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

