#!/usr/bin/env python3
"""
Kanban API Server

FastAPI backend for standalone HTML kanban board.
Provides REST API for task management operations.

Author: Gematria Hive Team
Date: January 6, 2025
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import get_task_manager, TaskManager
from task_manager_enhanced import get_enhanced_task_manager, EnhancedTaskManager
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Gematria Hive Kanban API",
    description="REST API for kanban task management with phases, metadata, resources, tags, and roles",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Task manager singleton (use enhanced version)
try:
    task_manager = get_enhanced_task_manager(use_memory_fallback=True)
    USE_ENHANCED = True
except:
    task_manager = get_task_manager(use_memory_fallback=True)
    USE_ENHANCED = False


# Pydantic models
class TaskCreate(BaseModel):
    content: str
    status: str = "pending"
    phase: str = "phase1_basic"
    role: str = "developer"
    priority: str = "medium"
    cost: float = 0.0
    tags: List[str] = []
    resources: List[str] = []
    labels: List[str] = []
    assigned_to: Optional[str] = None
    project_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    due_date: Optional[str] = None
    estimated_hours: Optional[float] = None
    progress: int = 0
    dependencies: List[str] = []
    metadata: Dict = {}
    links: List[str] = []  # Legacy support


class TaskUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[str] = None
    phase: Optional[str] = None
    role: Optional[str] = None
    priority: Optional[str] = None
    cost: Optional[float] = None
    tags: Optional[List[str]] = None
    resources: Optional[List[str]] = None
    labels: Optional[List[str]] = None
    assigned_to: Optional[str] = None
    project_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    due_date: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    progress: Optional[int] = None
    dependencies: Optional[List[str]] = None
    metadata: Optional[Dict] = None
    links: Optional[List[str]] = None


class TaskResponse(BaseModel):
    id: str
    content: str
    status: str
    phase: Optional[str] = None
    role: Optional[str] = None
    priority: Optional[str] = None
    cost: float
    tags: List[str] = []
    resources: List[str] = []
    labels: List[str] = []
    assigned_to: Optional[str] = None
    project_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    due_date: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    progress: int = 0
    dependencies: List[str] = []
    metadata: Dict = {}
    links: List[str] = []
    timestamp: str
    created_at: str


# Pipeline API models
class AgentExecutionRequest(BaseModel):
    agent: str
    task_type: Optional[str] = None
    query: Optional[str] = None
    url: Optional[str] = None
    topic_name: Optional[str] = None
    description: Optional[str] = None
    phase: Optional[str] = None
    metadata: Optional[Dict] = {}


class AgentExecutionResponse(BaseModel):
    success: bool
    task_id: Optional[str] = None
    agent: str
    status: str
    results: Optional[List] = []
    error: Optional[str] = None
    execution_time: Optional[float] = None


class OrchestratorExecutionRequest(BaseModel):
    task_type: str
    query: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    phase: Optional[str] = None
    metadata: Optional[Dict] = {}


class OrchestratorExecutionResponse(BaseModel):
    success: bool
    status: str
    results: List = []
    cost: float = 0.0
    agents_executed: List[str] = []
    execution_time: Optional[float] = None
    error: Optional[str] = None


# API Routes
@app.get("/")
async def root():
    """Root endpoint - serve kanban HTML"""
    html_path = os.path.join(os.path.dirname(__file__), "kanban.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as f:
            return HTMLResponse(content=f.read())
    return {"message": "Gematria Hive Kanban API", "version": "2.0.0"}


@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks(
    status: Optional[str] = None,
    phase: Optional[str] = None,
    limit: Optional[int] = None,
    order_by: str = "timestamp",
    ascending: bool = False
):
    """Get all tasks, optionally filtered by status or phase"""
    try:
        if USE_ENHANCED:
            if phase:
                tasks = task_manager.get_tasks_by_phase(phase)
            elif status:
                tasks = task_manager.get_tasks_by_status(
                    status=status,
                    limit=limit,
                    order_by=order_by,
                    ascending=ascending
                )
            else:
                tasks = task_manager.get_all_tasks(
                    limit=limit,
                    order_by=order_by,
                    ascending=ascending
                )
        else:
            if status:
                tasks = task_manager.get_tasks_by_status(
                    status=status,
                    limit=limit,
                    order_by=order_by,
                    ascending=ascending
                )
            else:
                tasks = task_manager.get_all_tasks(
                    limit=limit,
                    order_by=order_by,
                    ascending=ascending
                )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a single task by ID"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """Create a new task with enhanced features"""
    try:
        if USE_ENHANCED:
            created = task_manager.create_task(
                content=task.content,
                status=task.status,
                phase=task.phase,
                role=task.role,
                priority=task.priority,
                cost=task.cost,
                tags=task.tags,
                resources=task.resources,
                labels=task.labels,
                assigned_to=task.assigned_to,
                project_id=task.project_id,
                parent_task_id=task.parent_task_id,
                due_date=task.due_date,
                estimated_hours=task.estimated_hours,
                progress=task.progress,
                dependencies=task.dependencies,
                metadata=task.metadata,
                links=task.links
            )
        else:
            created = task_manager.create_task(
                content=task.content,
                status=task.status,
                cost=task.cost,
                links=task.links or []
            )
        if not created:
            raise HTTPException(status_code=500, detail="Failed to create task")
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task: TaskUpdate):
    """Update an existing task with enhanced features"""
    try:
        if USE_ENHANCED:
            updated = task_manager.update_task(
                task_id=task_id,
                content=task.content,
                status=task.status,
                phase=task.phase,
                role=task.role,
                priority=task.priority,
                cost=task.cost,
                tags=task.tags,
                resources=task.resources,
                labels=task.labels,
                assigned_to=task.assigned_to,
                project_id=task.project_id,
                parent_task_id=task.parent_task_id,
                due_date=task.due_date,
                estimated_hours=task.estimated_hours,
                actual_hours=task.actual_hours,
                progress=task.progress,
                dependencies=task.dependencies,
                metadata=task.metadata,
                links=task.links
            )
        else:
            updated = task_manager.update_task(
                task_id=task_id,
                content=task.content,
                status=task.status,
                cost=task.cost,
                links=task.links
            )
        if not updated:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/tasks/{task_id}/status")
async def update_task_status(task_id: str, status: str):
    """Update task status (quick update)"""
    try:
        updated = task_manager.update_task(task_id=task_id, status=status)
        if not updated:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    success = task_manager.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@app.get("/api/statistics")
async def get_statistics():
    """Get enhanced task statistics"""
    try:
        stats = task_manager.get_task_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/phases")
async def get_phases():
    """Get all available phases"""
    if USE_ENHANCED:
        return {
            "phases": [
                {"name": "phase1_basic", "display": "Phase 1: Foundation", "order": 1},
                {"name": "phase2_deep", "display": "Phase 2: Deep Analysis", "order": 2},
                {"name": "phase3_advanced", "display": "Phase 3: Advanced", "order": 3},
                {"name": "phase4_scale", "display": "Phase 4: Scale", "order": 4}
            ]
        }
    return {"phases": []}


@app.get("/api/roles")
async def get_roles():
    """Get all available roles"""
    if USE_ENHANCED:
        return {
            "roles": [
                {"name": "project_manager", "display": "Project Manager"},
                {"name": "product_manager", "display": "Product Manager"},
                {"name": "developer", "display": "Developer"},
                {"name": "designer", "display": "Designer"},
                {"name": "qa", "display": "QA Engineer"}
            ]
        }
    return {"roles": []}


@app.get("/api/priorities")
async def get_priorities():
    """Get all available priorities"""
    if USE_ENHANCED:
        return {
            "priorities": [
                {"name": "low", "display": "Low"},
                {"name": "medium", "display": "Medium"},
                {"name": "high", "display": "High"},
                {"name": "critical", "display": "Critical"}
            ]
        }
    return {"priorities": []}


@app.get("/api/tasks/phase/{phase}")
async def get_tasks_by_phase(phase: str):
    """Get tasks by phase"""
    if USE_ENHANCED:
        try:
            tasks = task_manager.get_tasks_by_phase(phase)
            return tasks
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=501, detail="Enhanced features not available")


@app.get("/api/tasks/role/{role}")
async def get_tasks_by_role(role: str):
    """Get tasks by role"""
    if USE_ENHANCED:
        try:
            tasks = task_manager.get_tasks_by_role(role)
            return tasks
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=501, detail="Enhanced features not available")


@app.get("/api/tasks/tag/{tag}")
async def get_tasks_by_tag(tag: str):
    """Get tasks by tag"""
    if USE_ENHANCED:
        try:
            tasks = task_manager.get_tasks_by_tag(tag)
            return tasks
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=501, detail="Enhanced features not available")


@app.post("/api/tasks/{task_id}/resources")
async def add_resource_to_task(
    task_id: str,
    resource_type: str,
    resource_name: str,
    resource_url: Optional[str] = None,
    resource_path: Optional[str] = None,
    resource_content: Optional[str] = None,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict] = None
):
    """Add a resource to a task"""
    if USE_ENHANCED:
        try:
            resource = task_manager.add_resource_to_task(
                task_id=task_id,
                resource_type=resource_type,
                resource_name=resource_name,
                resource_url=resource_url,
                resource_path=resource_path,
                resource_content=resource_content,
                tags=tags or [],
                metadata=metadata or {}
            )
            if not resource:
                raise HTTPException(status_code=500, detail="Failed to add resource")
            return resource
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(status_code=501, detail="Enhanced features not available")


# Pipeline API endpoints
@app.post("/api/pipeline/agent", response_model=AgentExecutionResponse)
async def execute_agent(request: AgentExecutionRequest):
    """Execute a single agent"""
    try:
        from agents.orchestrator import AgentState
        
        # Get the orchestrator
        from agents import get_orchestrator
        orchestrator = get_orchestrator()
        
        # Create agent state
        agent_state: AgentState = {
            "task": {
                "type": request.agent,
                "agent": request.agent,
                "query": request.query,
                "url": request.url,
                "topic_name": request.topic_name,
                "description": request.description,
                "phase": request.phase,
                **request.metadata
            },
            "data": [],
            "context": {},
            "results": [],
            "cost": 0.0,
            "status": "pending",
            "memory_id": None
        }
        
        # Execute agent
        if request.agent in orchestrator.agents:
            agent = orchestrator.agents[request.agent]
            result_state = agent.execute(agent_state)
            
            return AgentExecutionResponse(
                success=result_state.get("status") != "failed",
                task_id=request.metadata.get("task_id") if request.metadata else None,
                agent=request.agent,
                status=result_state.get("status", "completed"),
                results=result_state.get("results", []),
                error=result_state.get("error"),
                execution_time=None
            )
        else:
            raise HTTPException(status_code=404, detail=f"Agent {request.agent} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/pipeline/orchestrator", response_model=OrchestratorExecutionResponse)
async def execute_orchestrator(request: OrchestratorExecutionRequest):
    """Execute orchestrator (runs multiple agents)"""
    try:
        from agents import get_orchestrator
        orchestrator = get_orchestrator()
        
        # Create task for orchestrator
        task = {
            "type": request.task_type,
            "query": request.query,
            "url": request.url,
            "source": request.source,
            "phase": request.phase,
            **request.metadata
        }
        
        # Execute orchestrator
        result = orchestrator.execute(task)
        
        return OrchestratorExecutionResponse(
            success=result.get("status") != "failed",
            status=result.get("status", "completed"),
            results=result.get("results", []),
            cost=result.get("cost", 0.0),
            agents_executed=[r.get("agent", "unknown") for r in result.get("results", [])],
            execution_time=None,
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pipeline/agents")
async def get_agents():
    """Get list of available agents"""
    try:
        from agents import get_orchestrator
        orchestrator = get_orchestrator()
        agents = list(orchestrator.agents.keys())
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pipeline/status")
async def get_pipeline_status():
    """Get pipeline execution status"""
    try:
        # Get tasks by status
        all_tasks = task_manager.get_all_tasks()
        active = len([t for t in all_tasks if t.get("status") == "in_progress"])
        completed = len([t for t in all_tasks if t.get("status") == "completed"])
        failed = len([t for t in all_tasks if t.get("status") == "failed"])
        
        return {
            "active": active,
            "completed": completed,
            "failed": failed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
