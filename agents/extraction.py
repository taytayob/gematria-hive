"""
Extraction Agent

Purpose: Extract data from various sources (Dewey, OCR, URLs, JSON files).
This agent can be used standalone or as part of the MCP orchestrator workflow.

Standalone Usage:
    from agents.extraction import ExtractionAgent
    
    agent = ExtractionAgent()
    data = agent.extract_from_source("dewey_json.json")
    print(f"Extracted {len(data)} items")

Orchestrator Usage:
    from agents import MCPOrchestrator
    
    orchestrator = MCPOrchestrator()
    result = orchestrator.execute({"type": "extraction", "source": "data.json"})

Author: Gematria Hive Team
Date: November 6, 2025
"""

import logging
import sys
import os
from typing import Dict, List, Optional, Union

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import orchestrator types (optional for standalone use)
try:
    from agents.orchestrator import AgentState
    HAS_ORCHESTRATOR = True
except ImportError:
    HAS_ORCHESTRATOR = False
    # Define minimal AgentState for standalone use
    AgentState = Dict

# Try to import ingestion utilities
try:
    from ingest_pass1 import pull_data
    HAS_INGESTION_UTILS = True
except ImportError:
    HAS_INGESTION_UTILS = False
    logger = logging.getLogger(__name__)
    logger.warning("ingest_pass1 not available, extraction limited")

logger = logging.getLogger(__name__)


class ExtractionAgent:
    """
    Extraction Agent - Extracts data from various sources
    
    This agent extracts data from multiple sources:
    - Dewey API (X/Instagram bookmarks)
    - OCR (photos/images) - Future implementation
    - Web scraping (URLs) - Future implementation
    - JSON files (current implementation)
    
    The agent can be used in two ways:
    1. Standalone: Direct method calls for extraction
    2. Orchestrator: Part of MCP workflow via execute() method
    
    Attributes:
        name: Agent identifier
        logger: Logger instance
    
    Example:
        >>> agent = ExtractionAgent()
        >>> data = agent.extract_from_source("bookmarks.json")
        >>> print(f"Extracted {len(data)} items")
    """
    
    def __init__(self):
        """
        Initialize extraction agent
        
        Sets up logging and prepares agent for extraction operations.
        """
        self.name = "extraction_agent"
        logger.info(f"Initialized {self.name}")
    
    def extract_from_source(self, source: Union[str, Dict]) -> List[Dict]:
        """
        Extract data from a source (standalone method)
        
        This method can be called directly without the orchestrator.
        
        Args:
            source: Source identifier (file path, URL, or dict with source info)
            
        Returns:
            List of extracted data dictionaries
            
        Example:
            >>> agent = ExtractionAgent()
            >>> data = agent.extract_from_source("dewey_json.json")
            >>> print(f"Extracted {len(data)} items")
        """
        if isinstance(source, dict):
            source = source.get("source", source.get("file", ""))
        
        if not source:
            logger.error("No source provided")
            return []
        
        logger.info(f"Extracting from source: {source}")
        
        try:
            if HAS_INGESTION_UTILS:
                data = pull_data(source)
                logger.info(f"Extraction complete: {len(data)} items extracted")
                return data
            else:
                logger.error("Ingestion utilities not available")
                return []
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            return []
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute extraction task (orchestrator method)
        
        This method is called by the MCP orchestrator as part of a workflow.
        For standalone extraction, use extract_from_source() instead.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with extracted data
        """
        task = state.get("task", {})
        source = task.get("source", "dewey_json.json")
        
        logger.info(f"Extraction agent: Extracting from {source}")
        
        try:
            # Use standalone extraction method
            data = self.extract_from_source(source)
            
            # Update state for orchestrator
            if isinstance(state, dict):
                state["data"] = data
                state.setdefault("context", {})["extraction_source"] = source
                state["context"]["extraction_count"] = len(data)
                state.setdefault("results", []).append({
                    "agent": self.name,
                    "action": "extract",
                    "count": len(data),
                    "source": source
                })
            
            logger.info(f"Extraction complete: {len(data)} items extracted")
            
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            if isinstance(state, dict):
                state["status"] = "failed"
                state["error"] = str(e)
        
        return state

