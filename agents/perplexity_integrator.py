"""
Perplexity Integrator Agent
Purpose: Integrate Perplexity API for enhanced search capabilities
- Add Perplexity API for search
- Integrate with research workflows
- Source attribution
- Quality scoring

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import requests
import time
from typing import Dict, List, Optional
from datetime import datetime

from agents.orchestrator import AgentState
from agents.cost_manager import CostManagerAgent

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

# Perplexity API configuration
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY', '')
PERPLEXITY_API_URL = 'https://api.perplexity.ai/chat/completions'
PERPLEXITY_MODEL = 'llama-3.1-sonar-large-128k-online'


class PerplexityIntegratorAgent:
    """
    Perplexity Integrator Agent - Integrates Perplexity API for search
    """
    
    def __init__(self):
        """Initialize Perplexity integrator agent"""
        self.name = "perplexity_integrator_agent"
        self.api_key = PERPLEXITY_API_KEY
        self.api_url = PERPLEXITY_API_URL
        self.model = PERPLEXITY_MODEL
        self.supabase = supabase if HAS_SUPABASE else None
        self.cost_manager = CostManagerAgent()
        self.rate_limit_delay = 1.0
        self.last_request_time = 0
        logger.info(f"Initialized {self.name}")
    
    def rate_limit(self):
        """Apply rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def check_cache(self, query: str) -> Optional[Dict]:
        """
        Check cache for search results.
        
        Args:
            query: Search query
            
        Returns:
            Cached search results or None
        """
        if not self.supabase:
            return None
        
        try:
            cache_key = f"perplexity_search_{hash(query)}"
            result = self.supabase.table('cache_logs')\
                .select('*')\
                .eq('cache_key', cache_key)\
                .gt('expires_at', datetime.utcnow().isoformat())\
                .limit(1)\
                .execute()
            
            if result.data:
                cached_data = result.data[0].get('cached_data', {})
                logger.info(f"Found cached search results for query: {query[:50]}")
                return cached_data
            
            return None
        except Exception as e:
            logger.warning(f"Error checking cache: {e}")
            return None
    
    def save_cache(self, query: str, search_results: Dict, ttl_hours: int = 24):
        """
        Save search results to cache.
        
        Args:
            query: Search query
            search_results: Search results dictionary
            ttl_hours: Time to live in hours
        """
        if not self.supabase:
            return
        
        try:
            cache_key = f"perplexity_search_{hash(query)}"
            expires_at = datetime.utcnow().timestamp() + (ttl_hours * 3600)
            
            self.supabase.table('cache_logs').upsert({
                'cache_key': cache_key,
                'cache_type': 'api_response',
                'cached_data': search_results,
                'expires_at': datetime.fromtimestamp(expires_at).isoformat()
            }, on_conflict='cache_key').execute()
            
            logger.info(f"Cached search results for query: {query[:50]}")
        except Exception as e:
            logger.warning(f"Error saving cache: {e}")
    
    def search(self, query: str, max_results: int = 10) -> Optional[Dict]:
        """
        Search using Perplexity API.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Search results dictionary or None
        """
        if not self.api_key:
            logger.error("Perplexity API key not configured")
            return None
        
        # Check cache first
        cached_results = self.check_cache(query)
        if cached_results:
            return cached_results
        
        # Check cost before proceeding
        can_proceed, message = self.cost_manager.can_proceed(estimated_cost=0.01)  # Estimate $0.01 per search
        if not can_proceed:
            logger.error(f"Cannot proceed with search: {message}")
            return None
        
        # Apply rate limiting
        self.rate_limit()
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': query
                    }
                ],
                'max_tokens': 4000,
                'temperature': 0.1
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract search results
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # Extract citations/sources
                citations = []
                if 'citations' in result:
                    citations = result['citations']
                
                search_results = {
                    'query': query,
                    'content': content,
                    'citations': citations,
                    'sources': citations,
                    'model': self.model,
                    'searched_at': datetime.utcnow().isoformat()
                }
                
                # Save to cache
                self.save_cache(query, search_results)
                
                # Track cost
                # Estimate cost (Perplexity pricing may vary)
                estimated_cost = 0.01  # $0.01 per search (adjust based on actual pricing)
                self.cost_manager.track_cost('api', 'perplexity', 'search', estimated_cost, {
                    'query': query,
                    'model': self.model
                })
                
                logger.info(f"Searched Perplexity: {query[:50]}")
                return search_results
            else:
                logger.error(f"Unexpected Perplexity API response format: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching Perplexity API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error searching Perplexity: {e}")
            return None
    
    def store_search_results(self, search_results: Dict) -> Optional[str]:
        """
        Store search results as discovered resources.
        
        Args:
            search_results: Search results dictionary
            
        Returns:
            Resource ID or None
        """
        if not self.supabase:
            return None
        
        try:
            query = search_results.get('query', '')
            citations = search_results.get('citations', [])
            
            # Store each citation as a discovered resource
            resource_ids = []
            
            for citation in citations:
                if isinstance(citation, str):
                    url = citation
                elif isinstance(citation, dict):
                    url = citation.get('url', '')
                else:
                    continue
                
                if not url:
                    continue
                
                resource_data = {
                    'resource_type': 'paper' if 'arxiv' in url.lower() or 'pdf' in url.lower() else 'article',
                    'name': query,
                    'url': url,
                    'description': search_results.get('content', '')[:500],
                    'fidelity_score': 0.8,  # Default fidelity score
                    'relevance_to_goals': {
                        'query': query,
                        'source': 'perplexity'
                    },
                    'tags': ['perplexity', 'search'],
                    'discovered_at': datetime.utcnow().isoformat(),
                    'ingested': False
                }
                
                result = self.supabase.table('discovered_resources').upsert(
                    resource_data,
                    on_conflict='url'
                ).execute()
                
                if result.data:
                    resource_ids.append(result.data[0]['id'])
            
            logger.info(f"Stored {len(resource_ids)} resources from Perplexity search")
            return resource_ids[0] if resource_ids else None
            
        except Exception as e:
            logger.error(f"Error storing search results: {e}")
            return None
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute Perplexity search task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with search results
        """
        task = state.get("task", {})
        query = task.get("query", "")
        
        if not query:
            logger.error("No query provided for Perplexity search")
            state["status"] = "failed"
            state["error"] = "No query provided"
            return state
        
        logger.info(f"Perplexity integrator agent: Searching for {query}")
        
        try:
            # Search Perplexity
            search_results = self.search(query)
            
            if not search_results:
                logger.error(f"Failed to get search results for {query}")
                state["status"] = "failed"
                state["error"] = "Failed to get search results"
                return state
            
            # Store search results
            resource_id = self.store_search_results(search_results)
            
            # Update state
            state["data"] = [search_results]
            state["context"]["search_results"] = search_results
            state["context"]["resource_id"] = resource_id
            state["context"]["query"] = query
            state["results"].append({
                "agent": self.name,
                "action": "search",
                "query": query,
                "citations_count": len(search_results.get('citations', [])),
                "resource_id": resource_id
            })
            
            logger.info(f"Perplexity search complete: {query}")
            
        except Exception as e:
            logger.error(f"Perplexity search error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

