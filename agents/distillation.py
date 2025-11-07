"""
Distillation Agent

Purpose: Process and summarize extracted data, generate embeddings, and categorize relevance.
This agent can be used standalone or as part of the MCP orchestrator workflow.

Standalone Usage:
    from agents.distillation import DistillationAgent
    
    agent = DistillationAgent()
    processed = agent.process_data(extracted_data)
    print(f"Processed {len(processed)} items")

Orchestrator Usage:
    from agents import MCPOrchestrator
    
    orchestrator = MCPOrchestrator()
    result = orchestrator.execute({"type": "distillation", "data": [...]})

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
    AgentState = Dict

# Try to import ingestion utilities
try:
    from ingest_pass1 import categorize_relevance, embed_model
    HAS_INGESTION_UTILS = True
except ImportError:
    HAS_INGESTION_UTILS = False
    logger = logging.getLogger(__name__)
    logger.warning("ingest_pass1 not available, distillation limited")

logger = logging.getLogger(__name__)


class DistillationAgent:
    """
    Distillation Agent - Processes and summarizes data
    
    This agent processes extracted data by:
    - Generating embeddings using sentence transformers
    - Categorizing relevance (phase, score, tags)
    - Assigning tags based on content
    - Segmenting into phases (phase1_basic, phase2_deep)
    
    The agent can be used in two ways:
    1. Standalone: Direct method calls for processing
    2. Orchestrator: Part of MCP workflow via execute() method
    
    Attributes:
        name: Agent identifier
        logger: Logger instance
    
    Example:
        >>> agent = DistillationAgent()
        >>> processed = agent.process_data([{"url": "...", "summary": "..."}])
        >>> print(f"Processed {len(processed)} items")
    """
    
    def __init__(self):
        """
        Initialize distillation agent
        
        Sets up logging and prepares agent for processing operations.
        """
        self.name = "distillation_agent"
        logger.info(f"Initialized {self.name}")
    
    def process_data(self, data: List[Dict]) -> List[Dict]:
        """
        Process data (standalone method)
        
        This method can be called directly without the orchestrator.
        
        Args:
            data: List of extracted data dictionaries
            
        Returns:
            List of processed data dictionaries with embeddings, tags, phases
            
        Example:
            >>> agent = DistillationAgent()
            >>> processed = agent.process_data([{"url": "...", "summary": "..."}])
            >>> print(f"Processed {len(processed)} items")
        """
        if not data:
            logger.warning("No data to process")
            return []
        
        logger.info(f"Processing {len(data)} items")
        
        if not HAS_INGESTION_UTILS:
            logger.error("Ingestion utilities not available")
            return []
        
        try:
            # First pass: categorize all items and collect summaries
            items_with_metadata = []
            summaries = []
            summary_to_index = {}
            
            for idx, item in enumerate(data):
                # Categorize relevance (phase, score, tags)
                phase, score, tags = categorize_relevance(item)
                
                summary = item.get("summary", "")
                items_with_metadata.append({
                    "item": item,
                    "phase": phase,
                    "score": score,
                    "tags": tags,
                    "summary": summary
                })
                
                # Collect unique summaries for batch embedding
                if summary and summary not in summary_to_index:
                    summary_to_index[summary] = len(summaries)
                    summaries.append(summary)
            
            # Batch generate embeddings (5-10x faster than sequential)
            embedding_dict = {}
            if summaries:
                try:
                    logger.info(f"Generating embeddings for {len(summaries)} unique summaries in batch...")
                    # Use batch_size=32 for optimal performance
                    embeddings_batch = embed_model.encode(
                        summaries,
                        batch_size=32,
                        show_progress_bar=True,
                        convert_to_numpy=True
                    )
                    
                    # Map embeddings back to summaries
                    for summary, embedding in zip(summaries, embeddings_batch):
                        embedding_dict[summary] = embedding.tolist()
                    
                    logger.info(f"Batch embedding generation complete: {len(embeddings_batch)} embeddings")
                except Exception as e:
                    logger.error(f"Error in batch embedding generation: {e}")
                    # Fallback to sequential if batch fails
                    logger.warning("Falling back to sequential embedding generation")
                    for summary in summaries:
                        try:
                            embedding = embed_model.encode(summary).tolist()
                            embedding_dict[summary] = embedding
                        except Exception as e2:
                            logger.warning(f"Error generating embedding for summary: {e2}")
            
            # Second pass: create processed items with embeddings
            processed = []
            for metadata in items_with_metadata:
                item = metadata["item"]
                summary = metadata["summary"]
                
                # Get embedding from batch-generated dict
                embedding = embedding_dict.get(summary) if summary else None
                
                # Create processed item
                processed_item = {
                    "url": item.get("url", ""),
                    "summary": summary,
                    "embedding": embedding,
                    "tags": metadata["tags"],
                    "phase": metadata["phase"],
                    "relevance_score": metadata["score"]
                }
                
                processed.append(processed_item)
            
            logger.info(f"Processing complete: {len(processed)} items processed (batch embeddings: {len(embedding_dict)} unique)")
            return processed
            
        except Exception as e:
            logger.error(f"Processing error: {e}")
            return []
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute distillation task (orchestrator method)
        
        This method is called by the MCP orchestrator as part of a workflow.
        For standalone processing, use process_data() instead.
        
        Args:
            state: Agent state with extracted data
            
        Returns:
            Updated state with processed data
        """
        data = state.get("data", [])
        
        logger.info(f"Distillation agent: Processing {len(data)} items")
        
        try:
            # Use standalone processing method
            processed = self.process_data(data)
            
            # Update state for orchestrator
            if isinstance(state, dict):
                state["data"] = processed
                state.setdefault("context", {})["distillation_count"] = len(processed)
                state.setdefault("results", []).append({
                    "agent": self.name,
                    "action": "distill",
                    "count": len(processed),
                    "avg_relevance": sum(p.get("relevance_score", 0) for p in processed) / len(processed) if processed else 0.0
                })
            
            logger.info(f"Distillation complete: {len(processed)} items processed")
            
        except Exception as e:
            logger.error(f"Distillation error: {e}")
            if isinstance(state, dict):
                state["status"] = "failed"
                state["error"] = str(e)
        
        return state

