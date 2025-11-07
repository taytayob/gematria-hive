"""
MCP Tool Registry

Purpose: Centralized registry of tools available to all agents via MCP
- Agnostic tool availability
- Tool discovery and registration
- Tool execution interface
- Tool metadata and documentation
- Cross-agent tool sharing

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    category: str  # 'analysis', 'extraction', 'inference', 'visualization', etc.
    agent: str  # Agent that provides the tool
    execute_func: Callable  # Function to execute the tool
    parameters: Dict[str, Any] = field(default_factory=dict)  # Tool parameters
    returns: str = "Dict"  # Return type description
    requires_auth: bool = False
    cost_per_call: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class MCPToolRegistry:
    """
    MCP Tool Registry - Centralized tool registry for all agents
    
    All tools are available to all agents through this registry.
    Tools are agnostic and can be used by any agent.
    """
    
    def __init__(self):
        """Initialize tool registry"""
        self.tools: Dict[str, MCPTool] = {}
        self.tools_by_category: Dict[str, List[str]] = {}
        self.tools_by_agent: Dict[str, List[str]] = {}
        
        # Register default tools
        self._register_default_tools()
        
        logger.info(f"Initialized MCP Tool Registry with {len(self.tools)} tools")
    
    def register_tool(self, tool: MCPTool):
        """
        Register a tool in the registry
        
        Args:
            tool: MCPTool instance
        """
        self.tools[tool.name] = tool
        
        # Index by category
        if tool.category not in self.tools_by_category:
            self.tools_by_category[tool.category] = []
        self.tools_by_category[tool.category].append(tool.name)
        
        # Index by agent
        if tool.agent not in self.tools_by_agent:
            self.tools_by_agent[tool.agent] = []
        self.tools_by_agent[tool.agent].append(tool.name)
        
        logger.info(f"Registered tool: {tool.name} from {tool.agent}")
    
    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self, category: Optional[str] = None,
                   agent: Optional[str] = None) -> List[MCPTool]:
        """
        List tools, optionally filtered by category or agent
        
        Args:
            category: Optional category filter
            agent: Optional agent filter
            
        Returns:
            List of MCPTool instances
        """
        tools = list(self.tools.values())
        
        if category:
            tools = [t for t in tools if t.category == category]
        
        if agent:
            tools = [t for t in tools if t.agent == agent]
        
        return tools
    
    def execute_tool(self, name: str, **kwargs) -> Any:
        """
        Execute a tool by name
        
        Args:
            name: Tool name
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")
        
        try:
            logger.info(f"Executing tool: {name} with parameters: {kwargs}")
            result = tool.execute_func(**kwargs)
            logger.info(f"Tool {name} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            raise
    
    def _register_default_tools(self):
        """Register default tools from agents"""
        
        # Pattern detection tools
        try:
            from .pattern_detector import PatternDetectorAgent
            pattern_detector = PatternDetectorAgent()
            
            self.register_tool(MCPTool(
                name="detect_patterns",
                description="Detect patterns in data (cross-domain, temporal, symbolic, phonetic, gematria)",
                category="analysis",
                agent="pattern_detector",
                execute_func=lambda data: pattern_detector.execute({
                    "task": {},
                    "data": data,
                    "context": {},
                    "results": [],
                    "cost": 0.0,
                    "status": "pending",
                    "memory_id": None
                })
            ))
        except Exception as e:
            logger.warning(f"Could not register pattern detection tools: {e}")
        
        # Dark matter tracking tools
        try:
            from .dark_matter_tracker import DarkMatterTrackerAgent
            dark_matter_tracker = DarkMatterTrackerAgent()
            
            self.register_tool(MCPTool(
                name="track_dark_matter",
                description="Track hidden patterns and latent connections (dark matter)",
                category="analysis",
                agent="dark_matter_tracker",
                execute_func=lambda data: dark_matter_tracker.detect_latent_connections(data)
            ))
        except Exception as e:
            logger.warning(f"Could not register dark matter tracking tools: {e}")
        
        # Persona analysis tools
        try:
            from .persona_manager import PersonaManagerAgent
            persona_manager = PersonaManagerAgent()
            
            self.register_tool(MCPTool(
                name="analyze_with_persona",
                description="Analyze from a specific persona perspective (Einstein, Tesla, Pythagoras, etc.)",
                category="analysis",
                agent="persona_manager",
                execute_func=lambda query, persona_name: {
                    "persona": persona_manager.get_persona(persona_name),
                    "query": query,
                    "note": "Persona analysis tool"
                }
            ))
        except Exception as e:
            logger.warning(f"Could not register persona analysis tools: {e}")
        
        # Claude integration tools
        try:
            from .claude_integrator import ClaudeIntegratorAgent
            claude_integrator = ClaudeIntegratorAgent()
            
            self.register_tool(MCPTool(
                name="claude_analyze",
                description="Analyze using Claude API with first principles and highest persona thinking",
                category="analysis",
                agent="claude_integrator",
                execute_func=lambda query, context=None, persona=None: claude_integrator.analyze_with_claude(
                    query=query,
                    context=context or {},
                    persona=persona,
                    apply_first_principles=True
                ),
                cost_per_call=0.01  # Approximate cost per call
            ))
        except Exception as e:
            logger.warning(f"Could not register Claude integration tools: {e}")
        
        # Affinity analysis tools
        try:
            from .affinity import AffinityAgent
            affinity_agent = AffinityAgent()
            
            self.register_tool(MCPTool(
                name="explore_unknown_known",
                description="Explore latent patterns and unknown known connections",
                category="analysis",
                agent="affinity",
                execute_func=lambda state, query: affinity_agent.explore_unknown_known(state, query)
            ))
        except Exception as e:
            logger.warning(f"Could not register affinity analysis tools: {e}")
        
        # Gemini Deep Research tools
        try:
            from .gemini_research import GeminiResearchAgent
            gemini_research = GeminiResearchAgent()
            
            self.register_tool(MCPTool(
                name="gemini_research_report",
                description="Generate comprehensive research report using Google Gemini Deep Research",
                category="research",
                agent="gemini_research",
                execute_func=lambda url, query=None: gemini_research.generate_research_report(url, query),
                cost_per_call=0.01
            ))
        except Exception as e:
            logger.warning(f"Could not register Gemini Deep Research tools: {e}")
        
        # Google Drive integration tools
        try:
            from .google_drive_integrator import GoogleDriveIntegratorAgent
            google_drive = GoogleDriveIntegratorAgent()
            
            self.register_tool(MCPTool(
                name="list_drive_files",
                description="List files in Google Drive folder or search Drive",
                category="integration",
                agent="google_drive_integrator",
                execute_func=lambda folder_id=None, query=None: google_drive.list_files(folder_id, query)
            ))
            
            self.register_tool(MCPTool(
                name="extract_from_drive_file",
                description="Extract bookmarks and links from Google Drive file",
                category="integration",
                agent="google_drive_integrator",
                execute_func=lambda file_id: google_drive._extract_from_file(file_id)
            ))
        except Exception as e:
            logger.warning(f"Could not register Google Drive integration tools: {e}")
    
    def get_tool_documentation(self, name: str) -> Dict:
        """Get tool documentation"""
        tool = self.get_tool(name)
        if not tool:
            return {"error": f"Tool not found: {name}"}
        
        return {
            "name": tool.name,
            "description": tool.description,
            "category": tool.category,
            "agent": tool.agent,
            "parameters": tool.parameters,
            "returns": tool.returns,
            "requires_auth": tool.requires_auth,
            "cost_per_call": tool.cost_per_call,
            "metadata": tool.metadata
        }
    
    def list_all_tools(self) -> Dict:
        """List all tools with metadata"""
        return {
            "total_tools": len(self.tools),
            "tools_by_category": {
                category: len(tools) 
                for category, tools in self.tools_by_category.items()
            },
            "tools_by_agent": {
                agent: len(tools)
                for agent, tools in self.tools_by_agent.items()
            },
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "category": tool.category,
                    "agent": tool.agent
                }
                for tool in self.tools.values()
            ]
        }


# Singleton instance
_registry = None

def get_tool_registry() -> MCPToolRegistry:
    """Get or create tool registry singleton"""
    global _registry
    if _registry is None:
        _registry = MCPToolRegistry()
    return _registry

