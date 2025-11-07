"""
Gematria Hive - Agent Framework

Self-scaffolding MCP-driven agent system for data triangulation,
unification, and eternal truth pursuit.

Author: Gematria Hive Team
Date: November 6, 2025
"""

from .orchestrator import MCPOrchestrator, AgentState
from .extraction import ExtractionAgent
from .distillation import DistillationAgent
from .ingestion import IngestionAgent
from .inference import InferenceAgent
from .proof import ProofAgent
from .generative import GenerativeAgent

__all__ = [
    'MCPOrchestrator',
    'AgentState',
    'ExtractionAgent',
    'DistillationAgent',
    'IngestionAgent',
    'InferenceAgent',
    'ProofAgent',
    'GenerativeAgent',
]

