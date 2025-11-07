"""
Base Agent Class with MCP Support

Purpose: Base class for all agents with MCP tool registry integration
- MCP tool discovery
- MCP tool execution
- Tool registration
- Agent state management

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

from agents.orchestrator import AgentState

logger = logging.getLogger(__name__)

# Import MCP tool registry
try:
    from agents.mcp_tool_registry import get_tool_registry, MCPTool
    HAS_MCP = True
except ImportError:
    HAS_MCP = False
    logger.warning("MCP tool registry not available")


class BaseAgent(ABC):
    """
    Base Agent Class with MCP Support
    
    All agents should inherit from this class to get:
    - MCP tool registry access
    - Tool discovery and execution
    - Standard agent interface
    """
    
    def __init__(self, name: str):
        """
        Initialize base agent
        
        Args:
            name: Agent name
        """
        self.name = name
        self.tool_registry = None
        
        # Initialize MCP tool registry if available
        if HAS_MCP:
            try:
                self.tool_registry = get_tool_registry()
                logger.info(f"Agent {self.name} initialized with MCP tool registry")
            except Exception as e:
                logger.warning(f"Could not initialize MCP tool registry for {self.name}: {e}")
        
        logger.info(f"Initialized {self.name}")
    
    @abstractmethod
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute agent task (must be implemented by subclasses)
        
        Args:
            state: Agent state
            
        Returns:
            Updated agent state
        """
        pass
    
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Use a tool from the MCP registry
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        if not self.tool_registry:
            logger.warning(f"Tool registry not available for {self.name}")
            return None
        
        try:
            logger.info(f"Agent {self.name} using tool: {tool_name}")
            result = self.tool_registry.execute_tool(tool_name, **kwargs)
            logger.info(f"Tool {tool_name} executed successfully by {self.name}")
            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_name} in {self.name}: {e}")
            return None
    
    def discover_tools(self, category: Optional[str] = None, agent: Optional[str] = None) -> List[MCPTool]:
        """
        Discover available tools from MCP registry
        
        Args:
            category: Optional category filter
            agent: Optional agent filter
            
        Returns:
            List of available tools
        """
        if not self.tool_registry:
            logger.warning(f"Tool registry not available for {self.name}")
            return []
        
        try:
            tools = self.tool_registry.list_tools(category=category, agent=agent)
            logger.info(f"Agent {self.name} discovered {len(tools)} tools")
            return tools
        except Exception as e:
            logger.error(f"Error discovering tools in {self.name}: {e}")
            return []
    
    def register_tool(self, tool: MCPTool):
        """
        Register a tool with the MCP registry
        
        Args:
            tool: MCPTool instance to register
        """
        if not self.tool_registry:
            logger.warning(f"Tool registry not available for {self.name}")
            return
        
        try:
            self.tool_registry.register_tool(tool)
            logger.info(f"Agent {self.name} registered tool: {tool.name}")
        except Exception as e:
            logger.error(f"Error registering tool in {self.name}: {e}")
    
    def get_tool(self, tool_name: str) -> Optional[MCPTool]:
        """
        Get a tool from the MCP registry
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            MCPTool instance or None
        """
        if not self.tool_registry:
            return None
        
        return self.tool_registry.get_tool(tool_name)
    
    def has_tool_access(self) -> bool:
        """
        Check if agent has access to MCP tool registry
        
        Returns:
            True if tool registry is available
        """
        return self.tool_registry is not None

