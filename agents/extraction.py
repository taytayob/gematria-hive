"""
Extraction Agent

Purpose: Extract data from various sources (Dewey, OCR, URLs)

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
from ingest_pass1 import pull_data

logger = logging.getLogger(__name__)


class ExtractionAgent:
    """
    Extraction Agent - Extracts data from various sources
    
    Sources:
    - Dewey API (X/Instagram bookmarks)
    - OCR (photos/images)
    - Web scraping (URLs)
    - JSON files
    """
    
    def __init__(self):
        """Initialize extraction agent"""
        self.name = "extraction_agent"
        logger.info(f"Initialized {self.name}")
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute extraction task
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with extracted data
        """
        task = state["task"]
        source = task.get("source", "dewey_json.json")
        
        logger.info(f"Extraction agent: Extracting from {source}")
        
        try:
            # Use pull_data from ingest_pass1.py
            data = pull_data(source)
            
            state["data"] = data
            state["context"]["extraction_source"] = source
            state["context"]["extraction_count"] = len(data)
            state["results"].append({
                "agent": self.name,
                "action": "extract",
                "count": len(data),
                "source": source
            })
            
            logger.info(f"Extraction complete: {len(data)} items extracted")
            
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

