"""
Resource Discoverer Agent
Purpose: Find the highest fidelity data sets and repos and resources for us to explore
- Discover high-fidelity datasets, repos, papers
- Quality/reliability scoring
- Relevance to goals assessment
- Resource categorization
- Discovery tracking

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse

from agents.orchestrator import AgentState
from agents.perplexity_integrator import PerplexityIntegratorAgent
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


class ResourceDiscovererAgent(DataTable):
    """
    Resource Discoverer Agent - Discovers high-fidelity resources
    """
    
    def __init__(self):
        """Initialize resource discoverer agent"""
        super().__init__('discovered_resources')
        self.name = "resource_discoverer_agent"
        self.perplexity_agent = PerplexityIntegratorAgent()
        logger.info(f"Initialized {self.name}")
    
    def discover_resources(self, query: str, resource_type: str = 'dataset') -> List[Dict]:
        """
        Discover resources using Perplexity search.
        
        Args:
            query: Search query
            resource_type: Resource type ('dataset', 'repository', 'paper', 'library', etc.)
            
        Returns:
            List of discovered resource dictionaries
        """
        resources = []
        
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
                        # Determine resource type from URL
                        detected_type = self.detect_resource_type(url)
                        
                        resource = {
                            'resource_type': detected_type or resource_type,
                            'name': query,
                            'url': url,
                            'description': search_results.get('content', '')[:500],
                            'fidelity_score': self.calculate_fidelity_score(url, search_results),
                            'relevance_to_goals': {
                                'query': query,
                                'source': 'perplexity',
                                'resource_type': detected_type or resource_type
                            },
                            'tags': [resource_type, 'perplexity', 'discovered'],
                            'discovered_at': datetime.utcnow().isoformat(),
                            'ingested': False
                        }
                        resources.append(resource)
        except Exception as e:
            logger.error(f"Error discovering resources via Perplexity: {e}")
        
        return resources
    
    def detect_resource_type(self, url: str) -> Optional[str]:
        """
        Detect resource type from URL.
        
        Args:
            url: Resource URL
            
        Returns:
            Resource type or None
        """
        if not url:
            return None
        
        url_lower = url.lower()
        
        # Dataset repositories
        if 'kaggle.com' in url_lower or 'dataset' in url_lower:
            return 'dataset'
        
        # GitHub repositories
        if 'github.com' in url_lower:
            return 'repository'
        
        # Papers
        if 'arxiv.org' in url_lower or 'pdf' in url_lower or 'paper' in url_lower:
            return 'paper'
        
        # Libraries
        if 'pypi.org' in url_lower or 'npmjs.com' in url_lower or 'crates.io' in url_lower:
            return 'library'
        
        # Videos
        if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'video'
        
        # Images
        if any(url_lower.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            return 'image'
        
        # Default
        return 'article'
    
    def calculate_fidelity_score(self, url: str, search_results: Dict) -> float:
        """
        Calculate fidelity score for a resource.
        
        Args:
            url: Resource URL
            search_results: Search results dictionary
            
        Returns:
            Fidelity score (0.0 to 1.0)
        """
        score = 0.5  # Base score
        
        # Increase score based on URL domain
        url_lower = url.lower()
        
        # High-fidelity domains
        high_fidelity_domains = [
            'arxiv.org', 'github.com', 'kaggle.com', 'pypi.org',
            'scholar.google.com', 'ieee.org', 'acm.org', 'nature.com',
            'science.org', 'cell.com', 'springer.com', 'elsevier.com'
        ]
        
        for domain in high_fidelity_domains:
            if domain in url_lower:
                score += 0.3
                break
        
        # Increase score if in citations
        citations = search_results.get('citations', [])
        if url in citations:
            score += 0.2
        
        return min(score, 1.0)
    
    def assess_relevance_to_goals(self, resource: Dict) -> Dict:
        """
        Assess relevance to goals from PRD.
        
        Args:
            resource: Resource dictionary
            
        Returns:
            Relevance assessment dictionary
        """
        relevance = {
            'gematria': False,
            'numerology': False,
            'sacred_geometry': False,
            'esoteric': False,
            'mathematics': False,
            'physics': False,
            'quantum': False,
            'overall_relevance': 0.0
        }
        
        # Check resource content for keywords
        description = resource.get('description', '').lower()
        name = resource.get('name', '').lower()
        url = resource.get('url', '').lower()
        
        keywords = {
            'gematria': ['gematria', 'gematria', 'numerology', 'kabbalah'],
            'numerology': ['numerology', 'number', 'numerical'],
            'sacred_geometry': ['sacred geometry', 'geometry', 'metatron', 'tree of life'],
            'esoteric': ['esoteric', 'occult', 'mysticism', 'hermetic'],
            'mathematics': ['mathematics', 'math', 'mathematical', 'theorem'],
            'physics': ['physics', 'quantum', 'relativity', 'einstein'],
            'quantum': ['quantum', 'quantum mechanics', 'quantum physics']
        }
        
        text = f"{description} {name} {url}"
        
        for category, category_keywords in keywords.items():
            if any(keyword in text for keyword in category_keywords):
                relevance[category] = True
                relevance['overall_relevance'] += 0.15
        
        relevance['overall_relevance'] = min(relevance['overall_relevance'], 1.0)
        
        return relevance
    
    def store_discovered_resource(self, resource: Dict) -> Optional[str]:
        """
        Store discovered resource in database.
        
        Args:
            resource: Resource dictionary
            
        Returns:
            Resource ID or None
        """
        if not self.supabase:
            return None
        
        try:
            # Assess relevance
            relevance = self.assess_relevance_to_goals(resource)
            resource['relevance_to_goals'] = relevance
            
            # Check if resource already exists
            existing = self.supabase.table('discovered_resources')\
                .select('id')\
                .eq('url', resource['url'])\
                .limit(1)\
                .execute()
            
            if existing.data:
                # Update existing resource
                resource_id = existing.data[0]['id']
                self.supabase.table('discovered_resources')\
                    .update({
                        'fidelity_score': resource['fidelity_score'],
                        'relevance_to_goals': relevance,
                        'discovered_at': datetime.utcnow().isoformat()
                    })\
                    .eq('id', resource_id)\
                    .execute()
                
                logger.info(f"Updated discovered resource: {resource['url']}")
                return resource_id
            else:
                # Create new resource
                result = self.supabase.table('discovered_resources').insert(resource).execute()
                
                if result.data:
                    resource_id = result.data[0]['id']
                    logger.info(f"Discovered new resource: {resource['url']} (ID: {resource_id})")
                    return resource_id
            
            return None
        except Exception as e:
            logger.error(f"Error storing discovered resource: {e}")
            return None
    
    def get_high_fidelity_resources(self, min_fidelity: float = 0.7, limit: int = 100) -> List[Dict]:
        """
        Get high-fidelity resources.
        
        Args:
            min_fidelity: Minimum fidelity score
            limit: Maximum number of results
            
        Returns:
            List of resource dictionaries
        """
        if not self.supabase:
            return []
        
        try:
            result = self.supabase.table('discovered_resources')\
                .select('*')\
                .gte('fidelity_score', min_fidelity)\
                .order('fidelity_score', desc=True)\
                .limit(limit)\
                .execute()
            
            if result.data:
                return result.data
            
            return []
        except Exception as e:
            logger.error(f"Error getting high-fidelity resources: {e}")
            return []
    
    def validate(self, data: Dict, record_id: Optional[str] = None) -> Dict:
        """Validate resource data."""
        errors = []
        
        # Required fields
        if 'name' not in data or not data['name']:
            errors.append("name is required")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute resource discovery task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with discovered resources
        """
        task = state.get("task", {})
        query = task.get("query", "")
        resource_type = task.get("resource_type", "dataset")
        
        if not query:
            logger.error("No query provided for resource discovery")
            state["status"] = "failed"
            state["error"] = "No query provided"
            return state
        
        logger.info(f"Resource discoverer agent: Discovering resources for {query}")
        
        try:
            # Discover resources
            resources = self.discover_resources(query, resource_type)
            
            # Store discovered resources
            stored_resources = []
            for resource in resources:
                resource_id = self.store_discovered_resource(resource)
                if resource_id:
                    resource['id'] = resource_id
                    stored_resources.append(resource)
            
            # Update state
            state["data"] = stored_resources
            state["context"]["discovered_resources"] = stored_resources
            state["context"]["resources_count"] = len(stored_resources)
            state["results"].append({
                "agent": self.name,
                "action": "discover_resources",
                "query": query,
                "resources_count": len(stored_resources),
                "resources": stored_resources
            })
            
            logger.info(f"Resource discovery complete: {len(stored_resources)} resources discovered")
            
        except Exception as e:
            logger.error(f"Resource discovery error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

