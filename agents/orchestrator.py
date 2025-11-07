"""
MCP Orchestrator - LangGraph State Machine

Purpose: Orchestrate agent workflows, manage state, route tasks,
track costs, and maintain memory.

Author: Gematria Hive Team
Date: November 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional, TypedDict
from datetime import datetime
from dotenv import load_dotenv

# LangGraph imports
try:
    from langgraph.graph import StateGraph, END
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False
    print("Warning: langgraph not installed, orchestrator disabled")

# Supabase for memory
try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    print("Warning: supabase not installed, memory disabled")

load_dotenv()

logger = logging.getLogger(__name__)

# Agent State Definition
class AgentState(TypedDict):
    """State passed between agents in the workflow"""
    task: Dict  # Task description and parameters
    data: List[Dict]  # Processed data
    context: Dict  # Context and metadata
    results: List[Dict]  # Agent outputs
    cost: float  # Cumulative cost
    status: str  # Current status
    memory_id: Optional[str]  # Memory reference


class MCPOrchestrator:
    """
    MCP Orchestrator - Manages agent workflows and state
    
    Prompt Layers:
    - System: "Pursue truth with falsifiability. Unify gematria/esoteric with math—log leaps, measure costs."
    - MCP: "Triangulate data, segment phases, update master DB. Route tasks to appropriate agents."
    - Task: "Filter cosine >0.7; measure costs; flag for phase2 if score <0.5."
    """
    
    def __init__(self):
        """Initialize orchestrator with agents and state graph"""
        self.agents = {}
        self.graph = None
        self.workflow = None
        self.supabase = None
        
        # Initialize Supabase for memory
        if HAS_SUPABASE:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                logger.info("Supabase connected for agent memory")
        
        # Initialize observer, advisor, and mentor agents
        from .observer import ObserverAgent
        from .advisor import AdvisorAgent
        from .mentor import MentorAgent
        
        self.observer = ObserverAgent()
        self.advisor = AdvisorAgent(observer=self.observer)
        self.mentor = MentorAgent(observer=self.observer, advisor=self.advisor)
        
        # Initialize cost manager
        try:
            from .cost_manager import CostManagerAgent
            self.cost_manager = CostManagerAgent()
            logger.info("Cost manager initialized")
        except Exception as e:
            logger.warning(f"Cost manager not available: {e}")
            self.cost_manager = None
        
        # Add to agents dict for easy access
        self.agents['observer'] = self.observer
        self.agents['advisor'] = self.advisor
        self.agents['mentor'] = self.mentor
        if self.cost_manager:
            self.agents['cost_manager'] = self.cost_manager
        
        logger.info("Observer, Advisor, and Mentor agents initialized")
        
        # Build graph if LangGraph available
        if HAS_LANGGRAPH:
            self._build_graph()
        else:
            logger.warning("LangGraph not available, using simple workflow")
    
    def _build_graph(self):
        """Build LangGraph state machine - ALL AGENTS RUN SIMULTANEOUSLY"""
        from .extraction import ExtractionAgent
        from .distillation import DistillationAgent
        from .ingestion import IngestionAgent
        from .inference import InferenceAgent
        from .proof import ProofAgent
        from .browser import BrowserAgent
        from .affinity import AffinityAgent
        
        # Import new agents
        try:
            from .bookmark_ingestion import BookmarkIngestionAgent
            from .twitter_fetcher import TwitterFetcherAgent
            from .author_indexer import AuthorIndexerAgent
            from .symbol_extractor import SymbolExtractorAgent
            from .phonetic_analyzer import PhoneticAnalyzerAgent
            from .pattern_detector import PatternDetectorAgent
            from .gematria_integrator import GematriaIntegratorAgent
            from .cost_manager import CostManagerAgent
            from .perplexity_integrator import PerplexityIntegratorAgent
            from .deep_research_browser import DeepResearchBrowserAgent
            from .source_tracker import SourceTrackerAgent
            from .resource_discoverer import ResourceDiscovererAgent
        except ImportError as e:
            logger.warning(f"Some agents not available: {e}")
        
        # Initialize agents
        self.agents['extraction'] = ExtractionAgent()
        self.agents['distillation'] = DistillationAgent()
        self.agents['ingestion'] = IngestionAgent()
        self.agents['inference'] = InferenceAgent()
        self.agents['proof'] = ProofAgent()
        self.agents['browser'] = BrowserAgent()
        self.agents['affinity'] = AffinityAgent()
        
        # Initialize new agents
        try:
            self.agents['bookmark_ingestion'] = BookmarkIngestionAgent()
            self.agents['twitter_fetcher'] = TwitterFetcherAgent()
            self.agents['author_indexer'] = AuthorIndexerAgent()
            self.agents['symbol_extractor'] = SymbolExtractorAgent()
            self.agents['phonetic_analyzer'] = PhoneticAnalyzerAgent()
            self.agents['pattern_detector'] = PatternDetectorAgent()
            self.agents['gematria_integrator'] = GematriaIntegratorAgent()
            self.agents['cost_manager'] = CostManagerAgent()
            self.agents['perplexity_integrator'] = PerplexityIntegratorAgent()
            self.agents['deep_research_browser'] = DeepResearchBrowserAgent()
            self.agents['source_tracker'] = SourceTrackerAgent()
            self.agents['resource_discoverer'] = ResourceDiscovererAgent()
        except Exception as e:
            logger.warning(f"Error initializing new agents: {e}")
        
        # Create graph
        self.graph = StateGraph(AgentState)
        
        # Add nodes (agents) - ALL AGENTS
        self.graph.add_node("extraction", self.agents['extraction'].execute)
        self.graph.add_node("distillation", self.agents['distillation'].execute)
        self.graph.add_node("ingestion", self.agents['ingestion'].execute)
        self.graph.add_node("inference", self.agents['inference'].execute)
        self.graph.add_node("affinity", self.agents['affinity'].execute)
        self.graph.add_node("proof", self.agents['proof'].execute)
        self.graph.add_node("browser", self.agents['browser'].execute)
        
        # Add new agent nodes
        if 'bookmark_ingestion' in self.agents:
            self.graph.add_node("bookmark_ingestion", self.agents['bookmark_ingestion'].execute)
        if 'twitter_fetcher' in self.agents:
            self.graph.add_node("twitter_fetcher", self.agents['twitter_fetcher'].execute)
        if 'author_indexer' in self.agents:
            self.graph.add_node("author_indexer", self.agents['author_indexer'].execute)
        if 'symbol_extractor' in self.agents:
            self.graph.add_node("symbol_extractor", self.agents['symbol_extractor'].execute)
        if 'phonetic_analyzer' in self.agents:
            self.graph.add_node("phonetic_analyzer", self.agents['phonetic_analyzer'].execute)
        if 'pattern_detector' in self.agents:
            self.graph.add_node("pattern_detector", self.agents['pattern_detector'].execute)
        if 'gematria_integrator' in self.agents:
            self.graph.add_node("gematria_integrator", self.agents['gematria_integrator'].execute)
        if 'perplexity_integrator' in self.agents:
            self.graph.add_node("perplexity_integrator", self.agents['perplexity_integrator'].execute)
        if 'deep_research_browser' in self.agents:
            self.graph.add_node("deep_research_browser", self.agents['deep_research_browser'].execute)
        if 'source_tracker' in self.agents:
            self.graph.add_node("source_tracker", self.agents['source_tracker'].execute)
        if 'resource_discoverer' in self.agents:
            self.graph.add_node("resource_discoverer", self.agents['resource_discoverer'].execute)
        
        # Define workflow - ALL AGENTS RUN SIMULTANEOUSLY (parallel execution)
        self.graph.set_entry_point("extraction")
        
        # All analysis agents run in parallel after extraction
        # Use conditional edges to run all agents simultaneously
        def route_to_all_agents(state: AgentState) -> List[str]:
            """Route to all analysis agents simultaneously"""
            agents_to_run = []
            if 'distillation' in self.agents:
                agents_to_run.append("distillation")
            if 'ingestion' in self.agents:
                agents_to_run.append("ingestion")
            if 'inference' in self.agents:
                agents_to_run.append("inference")
            if 'affinity' in self.agents:
                agents_to_run.append("affinity")
            if 'symbol_extractor' in self.agents:
                agents_to_run.append("symbol_extractor")
            if 'phonetic_analyzer' in self.agents:
                agents_to_run.append("phonetic_analyzer")
            if 'pattern_detector' in self.agents:
                agents_to_run.append("pattern_detector")
            if 'gematria_integrator' in self.agents:
                agents_to_run.append("gematria_integrator")
            if 'author_indexer' in self.agents:
                agents_to_run.append("author_indexer")
            if 'source_tracker' in self.agents:
                agents_to_run.append("source_tracker")
            if 'deep_research_browser' in self.agents:
                agents_to_run.append("deep_research_browser")
            if 'resource_discoverer' in self.agents:
                agents_to_run.append("resource_discoverer")
            return agents_to_run
        
        # Add conditional edge to run all agents
        self.graph.add_conditional_edges(
            "extraction",
            route_to_all_agents,
            {agent: agent for agent in self.agents.keys() if agent != 'extraction'}
        )
        
        # All agents converge to proof
        for agent_name in self.agents.keys():
            if agent_name not in ['extraction', 'proof']:
                self.graph.add_edge(agent_name, "proof")
        
        self.graph.add_edge("proof", END)
        
        # Compile workflow
        self.workflow = self.graph.compile()
        logger.info("MCP Orchestrator graph built successfully - ALL AGENTS RUN SIMULTANEOUSLY")
    
    def execute(self, task: Dict) -> Dict:
        """
        Execute a task through the agent workflow
        
        Args:
            task: Task dictionary with 'type', 'source', 'query', etc.
            
        Returns:
            Dictionary with results, cost, and status
        """
        # Initialize state
        initial_state: AgentState = {
            "task": task,
            "data": [],
            "context": {
                "started_at": datetime.utcnow().isoformat(),
                "task_type": task.get("type", "unknown")
            },
            "results": [],
            "cost": 0.0,
            "status": "pending",
            "memory_id": None
        }
        
        # Save to memory
        if self.supabase:
            try:
                memory_result = self.supabase.table("agent_memory").insert({
                    "agent_id": "orchestrator",
                    "context": str(initial_state["context"]),
                    "state": initial_state,
                    "expires_at": (datetime.utcnow().timestamp() + 86400)  # 24h
                }).execute()
                if memory_result.data:
                    initial_state["memory_id"] = memory_result.data[0]["id"]
            except Exception as e:
                logger.error(f"Error saving to memory: {e}")
        
        # Check if this is a browser task - route directly to browser agent
        task_type = task.get("type", "")
        if task_type == "browser" or task.get("url"):
            logger.info("Routing to browser agent")
            if "browser" in self.agents:
                try:
                    final_state = self.agents["browser"].execute(initial_state)
                    # Optionally continue through pipeline if data was scraped
                    if final_state.get("status") != "failed" and final_state.get("data"):
                        # Continue through extraction/distillation/ingestion
                        if "extraction" in self.agents:
                            final_state = self.agents["extraction"].execute(final_state)
                        if "distillation" in self.agents:
                            final_state = self.agents["distillation"].execute(final_state)
                        if "ingestion" in self.agents:
                            final_state = self.agents["ingestion"].execute(final_state)
                    final_state["status"] = "completed"
                    logger.info(f"Browser task completed: {final_state['status']}")
                except Exception as e:
                    logger.error(f"Browser task error: {e}")
                    final_state = initial_state
                    final_state["status"] = "failed"
                    final_state["error"] = str(e)
            else:
                # Fallback to sequential execution
                final_state = self._execute_sequential(initial_state)
        # Execute workflow
        elif self.workflow:
            try:
                # Track execution start
                if self.observer:
                    self.observer.observe("execution_start", {
                        "task": task,
                        "task_type": task_type
                    }, "orchestrator")
                
                import time
                start_time = time.time()
                
                final_state = self.workflow.invoke(initial_state)
                execution_time = time.time() - start_time
                
                final_state["status"] = "completed"
                
                # Track execution completion
                if self.observer:
                    self.observer.track_execution("orchestrator", final_state, execution_time)
                
                logger.info(f"Workflow completed: {final_state['status']}")
            except Exception as e:
                logger.error(f"Workflow error: {e}")
                final_state = initial_state
                final_state["status"] = "failed"
                final_state["error"] = str(e)
                
                # Track error
                if self.observer:
                    self.observer.record_error("orchestrator", e, {"task": task})
        else:
            # Fallback: simple sequential execution
            logger.warning("Using fallback sequential execution")
            final_state = self._execute_sequential(initial_state)
        
        # Update memory
        if self.supabase and initial_state["memory_id"]:
            try:
                self.supabase.table("agent_memory").update({
                    "state": final_state,
                    "context": str(final_state["context"])
                }).eq("id", initial_state["memory_id"]).execute()
            except Exception as e:
                logger.error(f"Error updating memory: {e}")
        
        # Track costs
        if self.cost_manager and final_state.get("cost", 0) > 0:
            try:
                self.cost_manager.track_cost(
                    cost_type="api",
                    api_name="orchestrator",
                    operation="workflow_execution",
                    cost_amount=final_state.get("cost", 0),
                    metadata={
                        "task_type": task.get("type", "unknown"),
                        "agents_executed": len(final_state.get("results", [])),
                        "status": final_state.get("status", "unknown")
                    }
                )
            except Exception as e:
                logger.warning(f"Error tracking cost: {e}")
        
        return final_state
    
    def _execute_sequential(self, state: AgentState) -> AgentState:
        """Fallback sequential execution - ALL AGENTS RUN SIMULTANEOUSLY"""
        import concurrent.futures
        from .extraction import ExtractionAgent
        from .distillation import DistillationAgent
        from .ingestion import IngestionAgent
        from .browser import BrowserAgent
        
        # Initialize agents
        extraction = ExtractionAgent()
        distillation = DistillationAgent()
        ingestion = IngestionAgent()
        browser = BrowserAgent()
        
        # Import new agents
        try:
            from .bookmark_ingestion import BookmarkIngestionAgent
            from .twitter_fetcher import TwitterFetcherAgent
            from .author_indexer import AuthorIndexerAgent
            from .symbol_extractor import SymbolExtractorAgent
            from .phonetic_analyzer import PhoneticAnalyzerAgent
            from .pattern_detector import PatternDetectorAgent
            from .gematria_integrator import GematriaIntegratorAgent
        except ImportError as e:
            logger.warning(f"Some agents not available: {e}")
        
        # Check if task is a browser/scraping task
        task_type = state.get("task", {}).get("type", "")
        if task_type == "browser" or state.get("task", {}).get("url"):
            # Execute browser agent first, then continue with pipeline
            try:
                state = browser.execute(state)
                if state.get("status") == "failed":
                    return state
            except Exception as e:
                logger.error(f"Browser agent error: {e}")
        
        # Execute extraction first
        try:
            state = extraction.execute(state)
        except Exception as e:
            logger.error(f"Extraction agent error: {e}")
        
        # Execute ALL analysis agents SIMULTANEOUSLY (parallel execution)
        agents_to_run = [
            ('distillation', distillation),
            ('ingestion', ingestion),
        ]
        
        # Add new agents if available
        try:
            agents_to_run.extend([
                ('author_indexer', AuthorIndexerAgent()),
                ('symbol_extractor', SymbolExtractorAgent()),
                ('phonetic_analyzer', PhoneticAnalyzerAgent()),
                ('pattern_detector', PatternDetectorAgent()),
                ('gematria_integrator', GematriaIntegratorAgent()),
            ])
            
            # Add additional agents
            try:
                from .source_tracker import SourceTrackerAgent
                from .deep_research_browser import DeepResearchBrowserAgent
                from .resource_discoverer import ResourceDiscovererAgent
                agents_to_run.extend([
                    ('source_tracker', SourceTrackerAgent()),
                    ('deep_research_browser', DeepResearchBrowserAgent()),
                    ('resource_discoverer', ResourceDiscovererAgent()),
                ])
            except ImportError as e:
                logger.warning(f"Some agents not available: {e}")
        except Exception as e:
            logger.warning(f"Error adding new agents: {e}")
        
        # Run all agents in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents_to_run)) as executor:
            futures = {executor.submit(agent.execute, state): name for name, agent in agents_to_run}
            
            for future in concurrent.futures.as_completed(futures):
                agent_name = futures[future]
                try:
                    result_state = future.result()
                    # Merge results from all agents
                    if result_state.get("results"):
                        state["results"].extend(result_state["results"])
                    if result_state.get("context"):
                        state["context"].update(result_state["context"])
                except Exception as e:
                    logger.error(f"Agent {agent_name} error: {e}")
        
        state["status"] = "completed"
        return state
    
    def get_memory(self, memory_id: str) -> Optional[Dict]:
        """Retrieve agent memory by ID"""
        if not self.supabase:
            return None
        
        try:
            result = self.supabase.table("agent_memory").select("*").eq("id", memory_id).execute()
            if result.data:
                return result.data[0]
        except Exception as e:
            logger.error(f"Error retrieving memory: {e}")
        
        return None
    
    def log_hunch(self, content: str, links: List[str] = None, cost: float = 0.0):
        """Log a hunch to the database"""
        if not self.supabase:
            logger.warning("Supabase not available, hunch not logged")
            return
        
        try:
            self.supabase.table("hunches").insert({
                "content": content,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pending",
                "cost": cost,
                "links": links or []
            }).execute()
            logger.info(f"Hunch logged: {content[:50]}...")
        except Exception as e:
            logger.error(f"Error logging hunch: {e}")
    
    def execute_browser_task(self, url: str, max_depth: int = 3, delay: float = 1.0, 
                            use_sitemap: bool = True, respect_robots: bool = True) -> Dict:
        """
        Execute a browser/scraping task directly
        
        Args:
            url: URL to scrape
            max_depth: Maximum crawl depth
            delay: Delay between requests (seconds)
            use_sitemap: Whether to use sitemap if available
            respect_robots: Whether to respect robots.txt
            
        Returns:
            Dictionary with scraping results
        """
        from .browser import BrowserAgent
        
        task = {
            "type": "browser",
            "url": url,
            "max_depth": max_depth,
            "delay": delay,
            "use_sitemap": use_sitemap,
            "respect_robots": respect_robots
        }
        
        initial_state: AgentState = {
            "task": task,
            "data": [],
            "context": {
                "started_at": datetime.utcnow().isoformat(),
                "task_type": "browser"
            },
            "results": [],
            "cost": 0.0,
            "status": "pending",
            "memory_id": None
        }
        
        browser = BrowserAgent()
        final_state = browser.execute(initial_state)
        
        return {
            "status": final_state.get("status", "unknown"),
            "pages_scraped": final_state.get("context", {}).get("browser_pages_scraped", 0),
            "images_found": final_state.get("context", {}).get("browser_images_found", 0),
            "links_found": final_state.get("context", {}).get("browser_links_found", 0),
            "data": final_state.get("data", []),
            "results": final_state.get("results", []),
            "error": final_state.get("error")
        }


# Singleton instance
_orchestrator = None

def get_orchestrator() -> MCPOrchestrator:
    """Get or create orchestrator singleton"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = MCPOrchestrator()
    return _orchestrator

