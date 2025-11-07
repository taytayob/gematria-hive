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
from .browser import BrowserAgent
from .autonomous import AutonomousAgent
from .observer import ObserverAgent
from .affinity import AffinityAgent
from .reviewer import ReviewerAgent
try:
    from .advisor import AdvisorAgent
except ImportError:
    AdvisorAgent = None
try:
    from .mentor import MentorAgent
except ImportError:
    MentorAgent = None
try:
    from .notes import NoteTakingSystem, get_note_system
except ImportError:
    NoteTakingSystem = None
    get_note_system = None
from .knowledge_registry import (
    KnowledgeRegistry,
    get_registry,
    ClaudeSkill,
    Domain,
    Bookmark,
    GitRepository,
    ProcessingStatus,
    Priority,
    DomainCategory
)

# Import new agents
try:
    from .bookmark_ingestion import BookmarkIngestionAgent
except ImportError:
    BookmarkIngestionAgent = None

try:
    from .twitter_fetcher import TwitterFetcherAgent
except ImportError:
    TwitterFetcherAgent = None

try:
    from .author_indexer import AuthorIndexerAgent
except ImportError:
    AuthorIndexerAgent = None

try:
    from .symbol_extractor import SymbolExtractorAgent
except ImportError:
    SymbolExtractorAgent = None

try:
    from .phonetic_analyzer import PhoneticAnalyzerAgent
except ImportError:
    PhoneticAnalyzerAgent = None

try:
    from .pattern_detector import PatternDetectorAgent
except ImportError:
    PatternDetectorAgent = None

try:
    from .gematria_integrator import GematriaIntegratorAgent
except ImportError:
    GematriaIntegratorAgent = None

try:
    from .cost_manager import CostManagerAgent
except ImportError:
    CostManagerAgent = None

try:
    from .perplexity_integrator import PerplexityIntegratorAgent
except ImportError:
    PerplexityIntegratorAgent = None

try:
    from .deep_research_browser import DeepResearchBrowserAgent
except ImportError:
    DeepResearchBrowserAgent = None

try:
    from .source_tracker import SourceTrackerAgent
except ImportError:
    SourceTrackerAgent = None

try:
    from .resource_discoverer import ResourceDiscovererAgent
except ImportError:
    ResourceDiscovererAgent = None

try:
    from .persona_manager import PersonaManagerAgent
except ImportError:
    PersonaManagerAgent = None

try:
    from .alphabet_manager import AlphabetManagerAgent
except ImportError:
    AlphabetManagerAgent = None

try:
    from .validation_engine import ValidationEngineAgent
except ImportError:
    ValidationEngineAgent = None

try:
    from .project_manager import ProjectManagerAgent
except ImportError:
    ProjectManagerAgent = None

__all__ = [
    'MCPOrchestrator',
    'AgentState',
    'ExtractionAgent',
    'DistillationAgent',
    'IngestionAgent',
    'InferenceAgent',
    'ProofAgent',
    'GenerativeAgent',
    'BrowserAgent',
    'AutonomousAgent',
    'ObserverAgent',
    'AffinityAgent',
    'ReviewerAgent',
    'AdvisorAgent',
    'MentorAgent',
    'NoteTakingSystem',
    'get_note_system',
    'KnowledgeRegistry',
    'get_registry',
    'ClaudeSkill',
    'Domain',
    'Bookmark',
    'GitRepository',
    'ProcessingStatus',
    'Priority',
    'DomainCategory',
    # New agents
    'BookmarkIngestionAgent',
    'TwitterFetcherAgent',
    'AuthorIndexerAgent',
    'SymbolExtractorAgent',
    'PhoneticAnalyzerAgent',
    'PatternDetectorAgent',
    'GematriaIntegratorAgent',
    'CostManagerAgent',
    'PerplexityIntegratorAgent',
    'DeepResearchBrowserAgent',
    'SourceTrackerAgent',
    'ResourceDiscovererAgent',
    'PersonaManagerAgent',
    'AlphabetManagerAgent',
    'ValidationEngineAgent',
    'ProjectManagerAgent',
]

