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
        
        # Build graph if LangGraph available
        if HAS_LANGGRAPH:
            self._build_graph()
        else:
            logger.warning("LangGraph not available, using simple workflow")
    
    def _build_graph(self):
        """Build LangGraph state machine"""
        from .extraction import ExtractionAgent
        from .distillation import DistillationAgent
        from .ingestion import IngestionAgent
        from .inference import InferenceAgent
        from .proof import ProofAgent
        
        # Initialize agents
        self.agents['extraction'] = ExtractionAgent()
        self.agents['distillation'] = DistillationAgent()
        self.agents['ingestion'] = IngestionAgent()
        self.agents['inference'] = InferenceAgent()
        self.agents['proof'] = ProofAgent()
        
        # Create graph
        self.graph = StateGraph(AgentState)
        
        # Add nodes (agents)
        self.graph.add_node("extraction", self.agents['extraction'].execute)
        self.graph.add_node("distillation", self.agents['distillation'].execute)
        self.graph.add_node("ingestion", self.agents['ingestion'].execute)
        self.graph.add_node("inference", self.agents['inference'].execute)
        self.graph.add_node("proof", self.agents['proof'].execute)
        
        # Define workflow edges
        self.graph.set_entry_point("extraction")
        self.graph.add_edge("extraction", "distillation")
        self.graph.add_edge("distillation", "ingestion")
        self.graph.add_edge("ingestion", "inference")
        self.graph.add_edge("inference", "proof")
        self.graph.add_edge("proof", END)
        
        # Compile workflow
        self.workflow = self.graph.compile()
        logger.info("MCP Orchestrator graph built successfully")
    
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
        
        # Execute workflow
        if self.workflow:
            try:
                final_state = self.workflow.invoke(initial_state)
                final_state["status"] = "completed"
                logger.info(f"Workflow completed: {final_state['status']}")
            except Exception as e:
                logger.error(f"Workflow error: {e}")
                final_state = initial_state
                final_state["status"] = "failed"
                final_state["error"] = str(e)
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
        
        return final_state
    
    def _execute_sequential(self, state: AgentState) -> AgentState:
        """Fallback sequential execution without LangGraph"""
        from .extraction import ExtractionAgent
        from .distillation import DistillationAgent
        from .ingestion import IngestionAgent
        
        # Initialize agents
        extraction = ExtractionAgent()
        distillation = DistillationAgent()
        ingestion = IngestionAgent()
        
        # Execute sequentially
        try:
            state = extraction.execute(state)
            state = distillation.execute(state)
            state = ingestion.execute(state)
            state["status"] = "completed"
        except Exception as e:
            state["status"] = "failed"
            state["error"] = str(e)
        
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


# Singleton instance
_orchestrator = None

def get_orchestrator() -> MCPOrchestrator:
    """Get or create orchestrator singleton"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = MCPOrchestrator()
    return _orchestrator

