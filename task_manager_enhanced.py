"""
Enhanced Task Manager Module

Purpose: Manage tasks with phases, metadata, resources, tags, and role management.
Supports Project Manager, Product Manager, Developer Manager roles like Aha, Jira, ERP platforms.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Supabase client
try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    print("Warning: supabase not installed, task manager will use in-memory storage")

load_dotenv()

logger = logging.getLogger(__name__)


class EnhancedTaskManager:
    """
    Enhanced Task Manager - Manages tasks with phases, metadata, resources, tags, and roles
    
    Supports:
    - Phases (phase1_basic, phase2_deep, phase3_advanced, etc.)
    - Metadata (JSONB for flexible data)
    - Resources (URLs, files, documents, code, images, videos)
    - Tags (for categorization and filtering)
    - Roles (project_manager, product_manager, developer, etc.)
    - Priority (low, medium, high, critical)
    - Progress tracking (0-100%)
    - Dependencies and relationships
    - Comments and history
    """
    
    # Valid task statuses
    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_ARCHIVED = "archived"
    
    VALID_STATUSES = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED]
    
    # Valid phases
    PHASE_BASIC = "phase1_basic"
    PHASE_DEEP = "phase2_deep"
    PHASE_ADVANCED = "phase3_advanced"
    PHASE_SCALE = "phase4_scale"
    
    VALID_PHASES = [PHASE_BASIC, PHASE_DEEP, PHASE_ADVANCED, PHASE_SCALE]
    
    # Valid roles
    ROLE_PROJECT_MANAGER = "project_manager"
    ROLE_PRODUCT_MANAGER = "product_manager"
    ROLE_DEVELOPER = "developer"
    ROLE_DESIGNER = "designer"
    ROLE_QA = "qa"
    
    VALID_ROLES = [ROLE_PROJECT_MANAGER, ROLE_PRODUCT_MANAGER, ROLE_DEVELOPER, ROLE_DESIGNER, ROLE_QA]
    
    # Valid priorities
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CRITICAL = "critical"
    
    VALID_PRIORITIES = [PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH, PRIORITY_CRITICAL]
    
    def __init__(self, use_memory_fallback: bool = True):
        """
        Initialize Enhanced Task Manager
        
        Args:
            use_memory_fallback: If True, use in-memory storage when Supabase unavailable
        """
        self.use_memory = use_memory_fallback
        self.memory_store: Dict[str, Dict] = {}
        self.supabase: Optional[Client] = None
        
        # Initialize Supabase if available
        if HAS_SUPABASE:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            if supabase_url and supabase_key:
                try:
                    self.supabase = create_client(supabase_url, supabase_key)
                    logger.info("Enhanced Task Manager: Supabase connected")
                except Exception as e:
                    logger.error(f"Enhanced Task Manager: Failed to connect to Supabase: {e}")
                    if not use_memory_fallback:
                        raise
            else:
                logger.warning("Enhanced Task Manager: Supabase credentials not found")
                if not use_memory_fallback:
                    raise ValueError("Supabase credentials required but not found")
        else:
            logger.warning("Enhanced Task Manager: Supabase not available, using memory fallback")
    
    def create_task(
        self,
        content: str,
        status: str = STATUS_PENDING,
        phase: str = PHASE_BASIC,
        role: str = ROLE_DEVELOPER,
        priority: str = PRIORITY_MEDIUM,
        cost: float = 0.0,
        tags: Optional[List[str]] = None,
        resources: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        assigned_to: Optional[str] = None,
        project_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        due_date: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        progress: int = 0,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
        links: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """
        Create a new task with enhanced features
        
        Args:
            content: Task description/content
            status: Initial status (default: pending)
            phase: Project phase (default: phase1_basic)
            role: Role assignment (default: developer)
            priority: Task priority (default: medium)
            cost: Associated cost (default: 0.0)
            tags: List of tags for categorization
            resources: List of resource URLs/IDs
            labels: List of labels for organization
            assigned_to: User assigned to task
            project_id: Associated project ID
            parent_task_id: Parent task ID for subtasks
            due_date: Due date (ISO format)
            estimated_hours: Estimated hours to complete
            progress: Progress percentage (0-100)
            dependencies: List of task IDs this task depends on
            metadata: Additional metadata dictionary
            links: List of related URLs/IDs (legacy support)
            
        Returns:
            Created task dictionary with id, or None if creation failed
        """
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}. Must be one of {self.VALID_STATUSES}")
        if phase not in self.VALID_PHASES:
            raise ValueError(f"Invalid phase: {phase}. Must be one of {self.VALID_PHASES}")
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}. Must be one of {self.VALID_ROLES}")
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {self.VALID_PRIORITIES}")
        
        task_data = {
            "content": content,
            "status": status,
            "phase": phase,
            "role": role,
            "priority": priority,
            "cost": cost,
            "tags": tags or [],
            "resources": resources or [],
            "labels": labels or [],
            "assigned_to": assigned_to,
            "project_id": project_id,
            "parent_task_id": parent_task_id,
            "due_date": due_date,
            "estimated_hours": estimated_hours,
            "actual_hours": 0.0,
            "progress": max(0, min(100, progress)),
            "dependencies": dependencies or [],
            "metadata": metadata or {},
            "links": links or [],  # Legacy support
            "timestamp": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }
        
        if self.supabase:
            try:
                result = self.supabase.table("hunches").insert(task_data).execute()
                if result.data:
                    task_id = result.data[0].get('id')
                    # Create history entry
                    self._create_history_entry(task_id, "created", None, None, "system")
                    logger.info(f"Enhanced task created: {task_id}")
                    return result.data[0]
            except Exception as e:
                logger.error(f"Error creating enhanced task in Supabase: {e}")
                if not self.use_memory:
                    raise
        
        # Fallback to memory storage
        if self.use_memory:
            import uuid
            task_id = str(uuid.uuid4())
            task_data["id"] = task_id
            self.memory_store[task_id] = task_data
            logger.info(f"Enhanced task created in memory: {task_id}")
            return task_data
        
        return None
    
    def update_task(
        self,
        task_id: str,
        content: Optional[str] = None,
        status: Optional[str] = None,
        phase: Optional[str] = None,
        role: Optional[str] = None,
        priority: Optional[str] = None,
        cost: Optional[float] = None,
        tags: Optional[List[str]] = None,
        resources: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        assigned_to: Optional[str] = None,
        project_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        due_date: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        actual_hours: Optional[float] = None,
        progress: Optional[int] = None,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
        links: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """
        Update an existing task with enhanced features
        
        Returns:
            Updated task dictionary or None if update failed
        """
        update_data = {}
        
        # Validate inputs
        if status and status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        if phase and phase not in self.VALID_PHASES:
            raise ValueError(f"Invalid phase: {phase}")
        if role and role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role: {role}")
        if priority and priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}")
        if progress is not None:
            progress = max(0, min(100, progress))
        
        # Build update data
        if content is not None:
            update_data["content"] = content
        if status is not None:
            update_data["status"] = status
        if phase is not None:
            update_data["phase"] = phase
        if role is not None:
            update_data["role"] = role
        if priority is not None:
            update_data["priority"] = priority
        if cost is not None:
            update_data["cost"] = cost
        if tags is not None:
            update_data["tags"] = tags
        if resources is not None:
            update_data["resources"] = resources
        if labels is not None:
            update_data["labels"] = labels
        if assigned_to is not None:
            update_data["assigned_to"] = assigned_to
        if project_id is not None:
            update_data["project_id"] = project_id
        if parent_task_id is not None:
            update_data["parent_task_id"] = parent_task_id
        if due_date is not None:
            update_data["due_date"] = due_date
        if estimated_hours is not None:
            update_data["estimated_hours"] = estimated_hours
        if actual_hours is not None:
            update_data["actual_hours"] = actual_hours
        if progress is not None:
            update_data["progress"] = progress
        if dependencies is not None:
            update_data["dependencies"] = dependencies
        if metadata is not None:
            update_data["metadata"] = metadata
        if links is not None:
            update_data["links"] = links
        
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        if self.supabase:
            try:
                # Get old task for history
                old_task = self.get_task(task_id)
                
                result = self.supabase.table("hunches").update(update_data).eq("id", task_id).execute()
                if result.data:
                    # Create history entries for changed fields
                    for field, new_value in update_data.items():
                        if field != "updated_at":
                            old_value = old_task.get(field) if old_task else None
                            if old_value != new_value:
                                self._create_history_entry(
                                    task_id, "updated", field, 
                                    str(old_value), str(new_value), "system"
                                )
                    logger.info(f"Enhanced task updated: {task_id}")
                    return result.data[0]
            except Exception as e:
                logger.error(f"Error updating enhanced task in Supabase: {e}")
                if not self.use_memory:
                    raise
        
        # Fallback to memory
        if self.use_memory and task_id in self.memory_store:
            old_task = self.memory_store[task_id].copy()
            self.memory_store[task_id].update(update_data)
            logger.info(f"Enhanced task updated in memory: {task_id}")
            return self.memory_store[task_id]
        
        return None
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get a single task by ID"""
        if self.supabase:
            try:
                result = self.supabase.table("hunches").select("*").eq("id", task_id).execute()
                if result.data:
                    return result.data[0]
            except Exception as e:
                logger.error(f"Error fetching task from Supabase: {e}")
        
        if self.use_memory:
            return self.memory_store.get(task_id)
        
        return None
    
    def get_tasks_by_phase(self, phase: str) -> List[Dict]:
        """Get all tasks in a specific phase"""
        if self.supabase:
            try:
                result = self.supabase.table("hunches").select("*").eq("phase", phase).execute()
                return result.data or []
            except Exception as e:
                logger.error(f"Error fetching tasks by phase from Supabase: {e}")
        
        if self.use_memory:
            return [task for task in self.memory_store.values() if task.get("phase") == phase]
        
        return []
    
    def get_tasks_by_role(self, role: str) -> List[Dict]:
        """Get all tasks for a specific role"""
        if self.supabase:
            try:
                result = self.supabase.table("hunches").select("*").eq("role", role).execute()
                return result.data or []
            except Exception as e:
                logger.error(f"Error fetching tasks by role from Supabase: {e}")
        
        if self.use_memory:
            return [task for task in self.memory_store.values() if task.get("role") == role]
        
        return []
    
    def get_tasks_by_tag(self, tag: str) -> List[Dict]:
        """Get all tasks with a specific tag"""
        if self.supabase:
            try:
                result = self.supabase.table("hunches").select("*").contains("tags", [tag]).execute()
                return result.data or []
            except Exception as e:
                logger.error(f"Error fetching tasks by tag from Supabase: {e}")
        
        if self.use_memory:
            return [task for task in self.memory_store.values() if tag in (task.get("tags") or [])]
        
        return []
    
    def add_resource_to_task(self, task_id: str, resource_type: str, resource_name: str, 
                             resource_url: Optional[str] = None, resource_path: Optional[str] = None,
                             resource_content: Optional[str] = None, tags: Optional[List[str]] = None,
                             metadata: Optional[Dict] = None) -> Optional[Dict]:
        """Add a resource to a task"""
        resource_data = {
            "task_id": task_id,
            "resource_type": resource_type,
            "resource_name": resource_name,
            "resource_url": resource_url,
            "resource_path": resource_path,
            "resource_content": resource_content,
            "tags": tags or [],
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat()
        }
        
        if self.supabase:
            try:
                result = self.supabase.table("task_resources").insert(resource_data).execute()
                if result.data:
                    # Update task resources list
                    task = self.get_task(task_id)
                    if task:
                        resources = task.get("resources", [])
                        resources.append(result.data[0]["id"])
                        self.update_task(task_id, resources=resources)
                    return result.data[0]
            except Exception as e:
                logger.error(f"Error adding resource to task: {e}")
        
        return None
    
    def _create_history_entry(self, task_id: str, action: str, field_name: Optional[str] = None,
                             old_value: Optional[str] = None, new_value: Optional[str] = None,
                             changed_by: str = "system"):
        """Create a history entry for a task change"""
        if not self.supabase:
            return
        
        history_data = {
            "task_id": task_id,
            "action": action,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "changed_by": changed_by,
            "created_at": datetime.utcnow().isoformat()
        }
        
        try:
            self.supabase.table("task_history").insert(history_data).execute()
        except Exception as e:
            logger.error(f"Error creating history entry: {e}")
    
    def get_task_statistics(self) -> Dict:
        """Get enhanced statistics about tasks"""
        all_tasks = self.get_all_tasks()
        
        stats = {
            "total": len(all_tasks),
            "by_status": {
                self.STATUS_PENDING: 0,
                self.STATUS_IN_PROGRESS: 0,
                self.STATUS_COMPLETED: 0,
                self.STATUS_ARCHIVED: 0
            },
            "by_phase": {},
            "by_role": {},
            "by_priority": {},
            "total_cost": 0.0,
            "avg_cost": 0.0,
            "total_progress": 0.0,
            "avg_progress": 0.0
        }
        
        for task in all_tasks:
            # Status stats
            status = task.get("status", self.STATUS_PENDING)
            if status in stats["by_status"]:
                stats["by_status"][status] += 1
            
            # Phase stats
            phase = task.get("phase", self.PHASE_BASIC)
            stats["by_phase"][phase] = stats["by_phase"].get(phase, 0) + 1
            
            # Role stats
            role = task.get("role", self.ROLE_DEVELOPER)
            stats["by_role"][role] = stats["by_role"].get(role, 0) + 1
            
            # Priority stats
            priority = task.get("priority", self.PRIORITY_MEDIUM)
            stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
            
            # Cost stats
            cost = task.get("cost", 0.0) or 0.0
            stats["total_cost"] += cost
            
            # Progress stats
            progress = task.get("progress", 0) or 0
            stats["total_progress"] += progress
        
        if stats["total"] > 0:
            stats["avg_cost"] = stats["total_cost"] / stats["total"]
            stats["avg_progress"] = stats["total_progress"] / stats["total"]
        
        return stats
    
    def get_all_tasks(self, limit: Optional[int] = None, order_by: str = "timestamp", ascending: bool = False) -> List[Dict]:
        """Get all tasks"""
        if self.supabase:
            try:
                query = self.supabase.table("hunches").select("*")
                query = query.order(order_by, desc=not ascending)
                if limit:
                    query = query.limit(limit)
                result = query.execute()
                return result.data or []
            except Exception as e:
                logger.error(f"Error fetching all tasks from Supabase: {e}")
                if not self.use_memory:
                    return []
        
        if self.use_memory:
            tasks = list(self.memory_store.values())
            tasks.sort(key=lambda x: x.get(order_by, ""), reverse=not ascending)
            if limit:
                tasks = tasks[:limit]
            return tasks
        
        return []
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        if self.supabase:
            try:
                self.supabase.table("hunches").delete().eq("id", task_id).execute()
                logger.info(f"Task deleted: {task_id}")
                return True
            except Exception as e:
                logger.error(f"Error deleting task from Supabase: {e}")
                if not self.use_memory:
                    return False
        
        if self.use_memory and task_id in self.memory_store:
            del self.memory_store[task_id]
            logger.info(f"Task deleted from memory: {task_id}")
            return True
        
        return False


# Singleton instance
_enhanced_task_manager: Optional[EnhancedTaskManager] = None


def get_enhanced_task_manager(use_memory_fallback: bool = True) -> EnhancedTaskManager:
    """Get or create EnhancedTaskManager singleton instance"""
    global _enhanced_task_manager
    if _enhanced_task_manager is None:
        _enhanced_task_manager = EnhancedTaskManager(use_memory_fallback=use_memory_fallback)
    return _enhanced_task_manager

