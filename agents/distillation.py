"""
Distillation Agent

Purpose: Process and summarize extracted data, generate embeddings

Author: Gematria Hive Team
Date: November 6, 2025
"""

import logging
from typing import Dict, List
from agents.orchestrator import AgentState

# Import from main ingestion script
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ingest_pass1 import categorize_relevance, embed_model

logger = logging.getLogger(__name__)


class DistillationAgent:
    """
    Distillation Agent - Processes and summarizes data
    
    Operations:
    - Generate embeddings
    - Categorize relevance
    - Assign tags
    - Segment phases
    """
    
    def __init__(self):
        """Initialize distillation agent"""
        self.name = "distillation_agent"
        logger.info(f"Initialized {self.name}")
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute distillation task
        
        Args:
            state: Agent state with extracted data
            
        Returns:
            Updated state with processed data
        """
        data = state.get("data", [])
        
        logger.info(f"Distillation agent: Processing {len(data)} items")
        
        try:
            processed = []
            
            for item in data:
                # Categorize relevance (phase, score, tags)
                phase, score, tags = categorize_relevance(item)
                
                # Generate embedding
                if item.get("summary"):
                    embedding = embed_model.encode(item["summary"]).tolist()
                else:
                    embedding = None
                
                # Create processed item
                processed_item = {
                    "url": item.get("url", ""),
                    "summary": item.get("summary", ""),
                    "embedding": embedding,
                    "tags": tags,
                    "phase": phase,
                    "relevance_score": score
                }
                
                processed.append(processed_item)
            
            state["data"] = processed
            state["context"]["distillation_count"] = len(processed)
            state["results"].append({
                "agent": self.name,
                "action": "distill",
                "count": len(processed),
                "avg_relevance": sum(p["relevance_score"] for p in processed) / len(processed) if processed else 0.0
            })
            
            logger.info(f"Distillation complete: {len(processed)} items processed")
            
        except Exception as e:
            logger.error(f"Distillation error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

