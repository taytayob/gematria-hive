"""
Inference Agent

Purpose: Generate insights, patterns, and hunches from data

Author: Gematria Hive Team
Date: November 6, 2025
"""

import logging
import os
from typing import Dict, List
from agents.orchestrator import AgentState
from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
    from sentence_transformers import SentenceTransformer, util
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False
    print("Warning: Inference agent dependencies not available")

logger = logging.getLogger(__name__)


class InferenceAgent:
    """
    Inference Agent - Generates insights and patterns
    
    Operations:
    - Vector similarity search
    - Pattern discovery
    - Hunch generation
    - Synergy detection
    """
    
    def __init__(self):
        """Initialize inference agent"""
        self.name = "inference_agent"
        
        if HAS_DEPENDENCIES:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
            else:
                self.supabase = None
                self.embed_model = None
        else:
            self.supabase = None
            self.embed_model = None
        
        logger.info(f"Initialized {self.name}")
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute inference task
        
        Args:
            state: Agent state with ingested data
            
        Returns:
            Updated state with insights and hunches
        """
        task = state.get("task", {})
        query = task.get("query", "")
        
        logger.info(f"Inference agent: Generating insights for query: {query}")
        
        if not self.supabase or not self.embed_model:
            logger.warning("Inference agent: Dependencies not available, skipping")
            return state
        
        try:
            insights = []
            hunches = []
            
            # If query provided, search for similar bookmarks
            if query:
                query_embedding = self.embed_model.encode(query)
                
                # Get similar bookmarks (vector similarity search)
                # Note: This requires pgvector extension and proper indexing
                result = self.supabase.table("bookmarks").select("*").limit(10).execute()
                
                if result.data:
                    # Generate insights from similar items
                    for item in result.data:
                        if item.get("embedding"):
                            # Calculate similarity
                            item_emb = item["embedding"]
                            similarity = util.cos_sim(query_embedding, [item_emb])[0][0].item()
                            
                            if similarity > 0.7:  # High relevance threshold
                                insight = {
                                    "type": "similarity",
                                    "bookmark_id": item.get("id"),
                                    "similarity": float(similarity),
                                    "summary": item.get("summary", "")[:100]
                                }
                                insights.append(insight)
                                
                                # Generate hunch
                                hunch = f"High similarity ({similarity:.2f}) found: {item.get('summary', '')[:50]}..."
                                hunches.append(hunch)
            
            # Log hunches to database
            for hunch in hunches:
                try:
                    self.supabase.table("hunches").insert({
                        "content": hunch,
                        "status": "pending",
                        "cost": 0.0
                    }).execute()
                except Exception as e:
                    logger.error(f"Error logging hunch: {e}")
            
            state["results"].append({
                "agent": self.name,
                "action": "infer",
                "insights_count": len(insights),
                "hunches_count": len(hunches),
                "insights": insights
            })
            
            logger.info(f"Inference complete: {len(insights)} insights, {len(hunches)} hunches")
            
        except Exception as e:
            logger.error(f"Inference error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

