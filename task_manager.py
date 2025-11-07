"""
Task Manager Module

Purpose: Manage tasks/hunches in a kanban-style system with status tracking,
cost monitoring, and full CRUD operations.

This module provides a clean interface for:
- Creating, reading, updating, and deleting tasks
- Managing task status (pending, in_progress, completed, archived)
- Tracking costs and links
- Querying tasks by status, date range, or other criteria

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


class TaskManager:
    """
    Task Manager - Manages tasks/hunches in kanban-style system
    
    Provides full CRUD operations for tasks stored in the 'hunches' table.
    Tasks can be in one of four statuses:
    - pending: Newly created tasks
    - in_progress: Tasks currently being worked on
    - completed: Finished tasks
    - archived: Old/completed tasks moved to archive
    
    Attributes:
        supabase: Supabase client instance (if available)
        use_memory: Whether to use in-memory storage as fallback
        memory_store: In-memory task storage (dict)
    """
    
    # Valid task statuses
    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_ARCHIVED = "archived"
    
    VALID_STATUSES = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_ARCHIVED]
    
    def __init__(self, use_memory_fallback: bool = True):
        """
        Initialize Task Manager
        
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
                    logger.info("Task Manager: Supabase connected")
                except Exception as e:
                    logger.error(f"Task Manager: Failed to connect to Supabase: {e}")
                    if not use_memory_fallback:
                        raise
            else:
                logger.warning("Task Manager: Supabase credentials not found")
                if not use_memory_fallback:
                    raise ValueError("Supabase credentials required but not found")
        else:
            logger.warning("Task Manager: Supabase not available, using memory fallback")
    
    def create_task(
        self,
        content: str,
        status: str = STATUS_PENDING,
        cost: float = 0.0,
        links: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Create a new task/hunch
        
        Args:
            content: Task description/content
            status: Initial status (default: pending)
            cost: Associated cost (default: 0.0)
            links: List of related URLs/IDs (default: None)
            metadata: Additional metadata dictionary (default: None)
            
        Returns:
            Created task dictionary with id, or None if creation failed
            
        Raises:
            ValueError: If status is invalid
        """
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}. Must be one of {self.VALID_STATUSES}")
        
        task_data = {
            "content": content,
            "status": status,
            "cost": cost,
            "links": links or [],
            "timestamp": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Add metadata if provided
        if metadata:
            task_data.update(metadata)
        
        if self.supabase:
            try:
                result = self.supabase.table("hunches").insert(task_data).execute()
                if result.data:
                    logger.info(f"Task created: {result.data[0].get('id')}")
                    return result.data[0]
            except Exception as e:
                logger.error(f"Error creating task in Supabase: {e}")
                if not self.use_memory:
                    raise
        
        # Fallback to memory storage
        if self.use_memory:
            import uuid
            task_id = str(uuid.uuid4())
            task_data["id"] = task_id
            self.memory_store[task_id] = task_data
            logger.info(f"Task created in memory: {task_id}")
            return task_data
        
        return None
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """
        Get a single task by ID
        
        Args:
            task_id: Task UUID
            
        Returns:
            Task dictionary or None if not found
        """
        if self.supabase:
            try:
                result = self.supabase.table("hunches").select("*").eq("id", task_id).execute()
                if result.data:
                    return result.data[0]
            except Exception as e:
                logger.error(f"Error fetching task from Supabase: {e}")
        
        # Fallback to memory
        if self.use_memory:
            return self.memory_store.get(task_id)
        
        return None
    
    def update_task(
        self,
        task_id: str,
        content: Optional[str] = None,
        status: Optional[str] = None,
        cost: Optional[float] = None,
        links: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Update an existing task
        
        Args:
            task_id: Task UUID
            content: New content (optional)
            status: New status (optional)
            links: New links list (optional)
            cost: New cost (optional)
            metadata: Additional metadata to update (optional)
            
        Returns:
            Updated task dictionary or None if update failed
            
        Raises:
            ValueError: If status is invalid
        """
        if status and status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}. Must be one of {self.VALID_STATUSES}")
        
        update_data = {}
        if content is not None:
            update_data["content"] = content
        if status is not None:
            update_data["status"] = status
        if cost is not None:
            update_data["cost"] = cost
        if links is not None:
            update_data["links"] = links
        if metadata:
            update_data.update(metadata)
        
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        if self.supabase:
            try:
                result = self.supabase.table("hunches").update(update_data).eq("id", task_id).execute()
                if result.data:
                    logger.info(f"Task updated: {task_id}")
                    return result.data[0]
            except Exception as e:
                logger.error(f"Error updating task in Supabase: {e}")
                if not self.use_memory:
                    raise
        
        # Fallback to memory
        if self.use_memory and task_id in self.memory_store:
            self.memory_store[task_id].update(update_data)
            logger.info(f"Task updated in memory: {task_id}")
            return self.memory_store[task_id]
        
        return None
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task
        
        Args:
            task_id: Task UUID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        if self.supabase:
            try:
                self.supabase.table("hunches").delete().eq("id", task_id).execute()
                logger.info(f"Task deleted: {task_id}")
                return True
            except Exception as e:
                logger.error(f"Error deleting task from Supabase: {e}")
                if not self.use_memory:
                    return False
        
        # Fallback to memory
        if self.use_memory and task_id in self.memory_store:
            del self.memory_store[task_id]
            logger.info(f"Task deleted from memory: {task_id}")
            return True
        
        return False
    
    def get_tasks_by_status(
        self,
        status: str,
        limit: Optional[int] = None,
        order_by: str = "timestamp",
        ascending: bool = False
    ) -> List[Dict]:
        """
        Get all tasks with a specific status
        
        Args:
            status: Task status to filter by
            limit: Maximum number of tasks to return (optional)
            order_by: Field to order by (default: timestamp)
            ascending: Whether to sort ascending (default: False)
            
        Returns:
            List of task dictionaries
        """
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}. Must be one of {self.VALID_STATUSES}")
        
        if self.supabase:
            try:
                query = self.supabase.table("hunches").select("*").eq("status", status)
                query = query.order(order_by, desc=not ascending)
                if limit:
                    query = query.limit(limit)
                result = query.execute()
                return result.data or []
            except Exception as e:
                logger.error(f"Error fetching tasks from Supabase: {e}")
                if not self.use_memory:
                    return []
        
        # Fallback to memory
        if self.use_memory:
            tasks = [task for task in self.memory_store.values() if task.get("status") == status]
            tasks.sort(key=lambda x: x.get(order_by, ""), reverse=not ascending)
            if limit:
                tasks = tasks[:limit]
            return tasks
        
        return []
    
    def get_all_tasks(
        self,
        limit: Optional[int] = None,
        order_by: str = "timestamp",
        ascending: bool = False
    ) -> List[Dict]:
        """
        Get all tasks
        
        Args:
            limit: Maximum number of tasks to return (optional)
            order_by: Field to order by (default: timestamp)
            ascending: Whether to sort ascending (default: False)
            
        Returns:
            List of all task dictionaries
        """
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
        
        # Fallback to memory
        if self.use_memory:
            tasks = list(self.memory_store.values())
            tasks.sort(key=lambda x: x.get(order_by, ""), reverse=not ascending)
            if limit:
                tasks = tasks[:limit]
            return tasks
        
        return []
    
    def get_tasks_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        Get tasks within a date range
        
        Args:
            start_date: Start datetime
            end_date: End datetime
            status: Optional status filter
            
        Returns:
            List of task dictionaries in date range
        """
        if self.supabase:
            try:
                query = self.supabase.table("hunches").select("*")
                query = query.gte("timestamp", start_date.isoformat())
                query = query.lte("timestamp", end_date.isoformat())
                if status:
                    query = query.eq("status", status)
                query = query.order("timestamp", desc=True)
                result = query.execute()
                return result.data or []
            except Exception as e:
                logger.error(f"Error fetching tasks by date range from Supabase: {e}")
                if not self.use_memory:
                    return []
        
        # Fallback to memory
        if self.use_memory:
            tasks = [
                task for task in self.memory_store.values()
                if start_date.isoformat() <= task.get("timestamp", "") <= end_date.isoformat()
            ]
            if status:
                tasks = [task for task in tasks if task.get("status") == status]
            tasks.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return tasks
        
        return []
    
    def get_task_statistics(self) -> Dict:
        """
        Get statistics about tasks
        
        Returns:
            Dictionary with counts by status, total cost, etc.
        """
        all_tasks = self.get_all_tasks()
        
        stats = {
            "total": len(all_tasks),
            "by_status": {
                self.STATUS_PENDING: 0,
                self.STATUS_IN_PROGRESS: 0,
                self.STATUS_COMPLETED: 0,
                self.STATUS_ARCHIVED: 0
            },
            "total_cost": 0.0,
            "avg_cost": 0.0
        }
        
        for task in all_tasks:
            status = task.get("status", self.STATUS_PENDING)
            if status in stats["by_status"]:
                stats["by_status"][status] += 1
            cost = task.get("cost", 0.0) or 0.0
            stats["total_cost"] += cost
        
        if stats["total"] > 0:
            stats["avg_cost"] = stats["total_cost"] / stats["total"]
        
        return stats


# Singleton instance
_task_manager: Optional[TaskManager] = None


def get_task_manager(use_memory_fallback: bool = True) -> TaskManager:
    """
    Get or create TaskManager singleton instance
    
    Args:
        use_memory_fallback: If True, use in-memory storage when Supabase unavailable
        
    Returns:
        TaskManager instance
    """
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManager(use_memory_fallback=use_memory_fallback)
    return _task_manager


# Convenience functions for direct usage
def create_task(content: str, **kwargs) -> Optional[Dict]:
    """Create a task (convenience function)"""
    return get_task_manager().create_task(content, **kwargs)


def get_tasks_by_status(status: str, **kwargs) -> List[Dict]:
    """Get tasks by status (convenience function)"""
    return get_task_manager().get_tasks_by_status(status, **kwargs)


def update_task_status(task_id: str, status: str) -> Optional[Dict]:
    """Update task status (convenience function)"""
    return get_task_manager().update_task(task_id, status=status)

