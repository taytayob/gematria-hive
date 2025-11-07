#!/usr/bin/env python3
"""
Internal API Server

FastAPI backend for internal agent-to-agent communication and system operations.
Separate from public-facing kanban API, optimized for internal system operations.

Author: Gematria Hive Team
Date: January 6, 2025
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
import sys
import logging
import uuid

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Gematria Hive Internal API",
    description="Internal API for agent-to-agent communication and system operations",
    version="1.0.0"
)

# CORS middleware (restrictive for internal API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("INTERNAL_API_ORIGINS", "http://localhost:8000,http://localhost:8001").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Internal API key validation
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "internal-api-key-change-in-production")

def verify_internal_api_key(authorization: str = Header(None)):
    """Verify internal API key"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    if token != INTERNAL_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return token

# Import agent components
try:
    from agents.orchestrator import MCPOrchestrator, AgentState
    from agents.mcp_tool_registry import get_tool_registry
    from agents.cost_manager import CostManagerAgent
    HAS_AGENTS = True
except Exception as e:
    logger.warning(f"Agents not available: {e}")
    HAS_AGENTS = False

# Initialize components
orchestrator = None
tool_registry = None
cost_manager = None

if HAS_AGENTS:
    try:
        orchestrator = MCPOrchestrator()
        tool_registry = get_tool_registry()
        cost_manager = CostManagerAgent()
        logger.info("Internal API components initialized")
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")

# Pydantic models
class AgentExecuteRequest(BaseModel):
    state: Dict[str, Any]
    async_execution: bool = False

class AgentExecuteResponse(BaseModel):
    result: Dict[str, Any]
    execution_time: float
    cost: float

class WorkflowExecuteRequest(BaseModel):
    task: Dict[str, Any]
    agents: List[str]
    parallel: bool = True

class WorkflowExecuteResponse(BaseModel):
    workflow_id: str
    status: str
    estimated_completion: Optional[str] = None

class ToolExecuteRequest(BaseModel):
    parameters: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class ToolExecuteResponse(BaseModel):
    result: Dict[str, Any]
    execution_time: float
    cost: float

# Agent Communication API
@app.get("/internal/agents")
async def list_agents(api_key: str = Depends(verify_internal_api_key)):
    """List all available agents"""
    if not HAS_AGENTS or not orchestrator:
        raise HTTPException(status_code=503, detail="Agents not available")
    
    agents = []
    for name, agent in orchestrator.agents.items():
        agents.append({
            "name": name,
            "description": getattr(agent, "__doc__", "No description"),
            "status": "active",
            "capabilities": getattr(agent, "capabilities", []),
            "cost_per_call": getattr(agent, "cost_per_call", 0.0)
        })
    
    return {"agents": agents}

@app.get("/internal/agents/{agent_name}")
async def get_agent(agent_name: str, api_key: str = Depends(verify_internal_api_key)):
    """Get agent details"""
    if not HAS_AGENTS or not orchestrator:
        raise HTTPException(status_code=503, detail="Agents not available")
    
    if agent_name not in orchestrator.agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    agent = orchestrator.agents[agent_name]
    return {
        "name": agent_name,
        "description": getattr(agent, "__doc__", "No description"),
        "status": "active",
        "capabilities": getattr(agent, "capabilities", []),
        "health": "healthy",
        "cost_per_call": getattr(agent, "cost_per_call", 0.0)
    }

@app.post("/internal/agents/{agent_name}/execute", response_model=AgentExecuteResponse)
async def execute_agent(
    agent_name: str,
    request: AgentExecuteRequest,
    api_key: str = Depends(verify_internal_api_key)
):
    """Execute agent with state"""
    if not HAS_AGENTS or not orchestrator:
        raise HTTPException(status_code=503, detail="Agents not available")
    
    if agent_name not in orchestrator.agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    agent = orchestrator.agents[agent_name]
    start_time = datetime.now()
    
    try:
        # Convert request state to AgentState
        state: AgentState = {
            "task": request.state.get("task", {}),
            "data": request.state.get("data", []),
            "context": request.state.get("context", {}),
            "results": request.state.get("results", []),
            "cost": request.state.get("cost", 0.0),
            "status": "running",
            "memory_id": request.state.get("memory_id")
        }
        
        # Execute agent
        result_state = agent.execute(state)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        cost = result_state.get("cost", 0.0) - state.get("cost", 0.0)
        
        return AgentExecuteResponse(
            result={
                "state": result_state,
                "execution_time": execution_time,
                "cost": cost
            },
            execution_time=execution_time,
            cost=cost
        )
    except Exception as e:
        logger.error(f"Agent execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Orchestrator API
@app.post("/internal/orchestrator/execute", response_model=WorkflowExecuteResponse)
async def execute_workflow(
    request: WorkflowExecuteRequest,
    api_key: str = Depends(verify_internal_api_key)
):
    """Execute workflow"""
    if not HAS_AGENTS or not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not available")
    
    workflow_id = str(uuid.uuid4())
    
    try:
        # Execute workflow
        result = orchestrator.execute(request.task)
        
        return WorkflowExecuteResponse(
            workflow_id=workflow_id,
            status="completed",
            estimated_completion=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Workflow execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Tool Registry API
@app.get("/internal/tools")
async def list_tools(api_key: str = Depends(verify_internal_api_key)):
    """List all available tools"""
    if not HAS_AGENTS or not tool_registry:
        raise HTTPException(status_code=503, detail="Tool registry not available")
    
    tools = []
    for tool_name, tool in tool_registry.tools.items():
        tools.append({
            "name": tool_name,
            "description": tool.description,
            "category": tool.category,
            "agent": tool.agent,
            "cost_per_call": tool.cost_per_call
        })
    
    return {"tools": tools}

@app.get("/internal/tools/{tool_name}")
async def get_tool(tool_name: str, api_key: str = Depends(verify_internal_api_key)):
    """Get tool details"""
    if not HAS_AGENTS or not tool_registry:
        raise HTTPException(status_code=503, detail="Tool registry not available")
    
    if tool_name not in tool_registry.tools:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
    
    tool = tool_registry.tools[tool_name]
    return {
        "name": tool_name,
        "description": tool.description,
        "category": tool.category,
        "agent": tool.agent,
        "parameters": tool.parameters,
        "returns": tool.returns,
        "cost_per_call": tool.cost_per_call
    }

@app.post("/internal/tools/{tool_name}/execute", response_model=ToolExecuteResponse)
async def execute_tool(
    tool_name: str,
    request: ToolExecuteRequest,
    api_key: str = Depends(verify_internal_api_key)
):
    """Execute tool"""
    if not HAS_AGENTS or not tool_registry:
        raise HTTPException(status_code=503, detail="Tool registry not available")
    
    if tool_name not in tool_registry.tools:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
    
    start_time = datetime.now()
    
    try:
        result = tool_registry.execute_tool(tool_name, request.parameters, request.context)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        tool = tool_registry.tools[tool_name]
        cost = tool.cost_per_call
        
        return ToolExecuteResponse(
            result=result,
            execution_time=execution_time,
            cost=cost
        )
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Cost Management API
@app.get("/internal/cost/current")
async def get_current_cost(api_key: str = Depends(verify_internal_api_key)):
    """Get current cost"""
    if not HAS_AGENTS or not cost_manager:
        raise HTTPException(status_code=503, detail="Cost manager not available")
    
    total_cost = cost_manager.get_total_cost()
    daily_cost = cost_manager.get_daily_cost()
    budget_cap = cost_manager.budget_cap
    
    return {
        "total_cost": total_cost,
        "daily_cost": daily_cost,
        "remaining_budget": budget_cap - total_cost,
        "budget_cap": budget_cap,
        "alerts": []
    }

# Health Check API
@app.get("/internal/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy" if HAS_AGENTS else "degraded",
        "components": {
            "orchestrator": "healthy" if orchestrator else "unavailable",
            "tool_registry": "healthy" if tool_registry else "unavailable",
            "cost_manager": "healthy" if cost_manager else "unavailable",
            "agents": "healthy" if HAS_AGENTS else "unavailable"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/internal/health/agents")
async def agent_health(api_key: str = Depends(verify_internal_api_key)):
    """Agent health check"""
    if not HAS_AGENTS or not orchestrator:
        return {"agents": {}, "status": "unavailable"}
    
    agent_status = {}
    for name in orchestrator.agents.keys():
        agent_status[name] = "healthy"
    
    return {"agents": agent_status}

# --- MCP Tool Registry Endpoints (Aliases for clarity) ---

@app.get("/internal/mcp/tools", summary="List All MCP Tools")
async def list_mcp_tools(
    category: Optional[str] = None,
    agent: Optional[str] = None,
    api_key: str = Depends(verify_internal_api_key)
):
    """
    List all available MCP tools, optionally filtered by category or agent.
    This is an alias for /internal/tools with MCP-specific naming.
    """
    if not HAS_AGENTS or not tool_registry:
        raise HTTPException(status_code=503, detail="MCP tool registry not available")
    
    try:
        tools = tool_registry.list_tools(category=category, agent=agent)
        all_tools = tool_registry.list_all_tools()
        return {
            "total": len(tools),
            "tools_by_category": all_tools.get("tools_by_category", {}),
            "tools_by_agent": all_tools.get("tools_by_agent", {}),
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "category": tool.category,
                    "agent": tool.agent,
                    "cost_per_call": tool.cost_per_call
                }
                for tool in tools
            ]
        }
    except Exception as e:
        logger.error(f"Error listing MCP tools: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")

@app.get("/internal/mcp/tools/{tool_name}", summary="Get MCP Tool Details")
async def get_mcp_tool(
    tool_name: str,
    api_key: str = Depends(verify_internal_api_key)
):
    """
    Get details about a specific MCP tool.
    This is an alias for /internal/tools/{tool_name} with MCP-specific naming.
    """
    if not HAS_AGENTS or not tool_registry:
        raise HTTPException(status_code=503, detail="MCP tool registry not available")
    
    try:
        tool = tool_registry.get_tool(tool_name)
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_name}")
        
        return tool_registry.get_tool_documentation(tool_name)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting MCP tool: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting tool: {str(e)}")

@app.post("/internal/mcp/tools/{tool_name}/execute", summary="Execute MCP Tool")
async def execute_mcp_tool(
    tool_name: str,
    parameters: Dict[str, Any],
    api_key: str = Depends(verify_internal_api_key)
):
    """
    Execute an MCP tool with provided parameters.
    This is an alias for /internal/tools/{tool_name}/execute with MCP-specific naming.
    """
    if not HAS_AGENTS or not tool_registry:
        raise HTTPException(status_code=503, detail="MCP tool registry not available")
    
    start_time = datetime.now()
    
    try:
        result = tool_registry.execute_tool(tool_name, **parameters)
        execution_time = (datetime.now() - start_time).total_seconds()
        
        tool = tool_registry.get_tool(tool_name)
        cost = tool.cost_per_call if tool else 0.0
        
        return {
            "tool": tool_name,
            "result": result,
            "execution_time": execution_time,
            "cost": cost,
            "success": True
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing MCP tool: {e}")
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")

@app.get("/internal/mcp/tools/categories", summary="List Tool Categories")
async def list_tool_categories(api_key: str = Depends(verify_internal_api_key)):
    """
    List all available tool categories from MCP registry.
    """
    if not HAS_AGENTS or not tool_registry:
        raise HTTPException(status_code=503, detail="MCP tool registry not available")
    
    try:
        all_tools = tool_registry.list_all_tools()
        return {
            "categories": list(all_tools.get("tools_by_category", {}).keys()),
            "counts": all_tools.get("tools_by_category", {}),
            "agents": list(all_tools.get("tools_by_agent", {}).keys())
        }
    except Exception as e:
        logger.error(f"Error listing categories: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing categories: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("INTERNAL_API_PORT", "8001"))
    host = os.getenv("INTERNAL_API_HOST", "0.0.0.0")
    
    print("=" * 60)
    print("🐝 Gematria Hive - Internal API")
    print("=" * 60)
    print(f"Starting internal API on http://{host}:{port}")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "internal_api:app",
        host=host,
        port=port,
        reload=True
    )

