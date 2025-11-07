"""
Ingestion Agent

Purpose: Store processed data in database

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
from ingest_pass1 import ingest_to_db

logger = logging.getLogger(__name__)


class IngestionAgent:
    """
    Ingestion Agent - Stores data in database
    
    Operations:
    - Batch insert to Supabase
    - Log hunches
    - Track ingestion metrics
    """
    
    def __init__(self):
        """Initialize ingestion agent"""
        self.name = "ingestion_agent"
        logger.info(f"Initialized {self.name}")
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute ingestion task
        
        Args:
            state: Agent state with processed data
            
        Returns:
            Updated state with ingestion results
        """
        data = state.get("data", [])
        
        logger.info(f"Ingestion agent: Ingesting {len(data)} items")
        
        try:
            # Use ingest_to_db from ingest_pass1.py
            ingested_count = ingest_to_db(data)
            
            state["context"]["ingestion_count"] = ingested_count
            state["results"].append({
                "agent": self.name,
                "action": "ingest",
                "count": ingested_count,
                "total": len(data)
            })
            
            logger.info(f"Ingestion complete: {ingested_count}/{len(data)} items ingested")
            
        except Exception as e:
            logger.error(f"Ingestion error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

