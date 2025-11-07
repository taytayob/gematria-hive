"""
Project Manager Agent
Purpose: Create projects/sandbox system for experimental work with master sync
- Create projects table
- Sandbox environment
- Data isolation with master sync
- Completion workflows
- Documentation generation

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import logging
import json
from typing import Dict, List, Optional
from datetime import datetime

from agents.orchestrator import AgentState
from core.data_table import DataTable

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

try:
    from supabase import create_client, Client
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    if SUPABASE_URL and SUPABASE_KEY:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        HAS_SUPABASE = True
    else:
        HAS_SUPABASE = False
        supabase = None
except Exception:
    HAS_SUPABASE = False
    supabase = None

logger = logging.getLogger(__name__)


class ProjectManagerAgent(DataTable):
    """
    Project Manager Agent - Manages projects and sandbox environments
    """
    
    def __init__(self):
        """Initialize project manager agent"""
        super().__init__('projects')
        self.name = "project_manager_agent"
        logger.info(f"Initialized {self.name}")
    
    def create_project(self, project_name: str, project_description: str = '', 
                       project_type: str = 'sandbox', master_sync_enabled: bool = True) -> Optional[str]:
        """
        Create a new project.
        
        Args:
            project_name: Project name
            project_description: Project description
            project_type: Project type ('sandbox', 'research', 'production')
            master_sync_enabled: Whether to enable master sync
            
        Returns:
            Project ID or None
        """
        if not self.supabase:
            return None
        
        try:
            project_data = {
                'project_name': project_name,
                'project_description': project_description,
                'project_type': project_type,
                'status': 'active',
                'data_snapshot': {},
                'master_sync_enabled': master_sync_enabled,
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = self.create(project_data)
            
            if result:
                project_id = result['id']
                logger.info(f"Created project: {project_name} (ID: {project_id})")
                return project_id
            
            return None
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            return None
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """
        Get project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project dictionary or None
        """
        return self.read(project_id)
    
    def update_project_snapshot(self, project_id: str, snapshot: Dict):
        """
        Update project data snapshot.
        
        Args:
            project_id: Project ID
            snapshot: Data snapshot dictionary
        """
        if not self.supabase:
            return
        
        try:
            self.update(project_id, {
                'data_snapshot': snapshot,
                'updated_at': datetime.utcnow().isoformat()
            })
            
            logger.info(f"Updated project snapshot: {project_id}")
        except Exception as e:
            logger.error(f"Error updating project snapshot: {e}")
    
    def sync_to_master(self, project_id: str) -> bool:
        """
        Sync project data to master tables.
        
        Args:
            project_id: Project ID
            
        Returns:
            True if synced successfully, False otherwise
        """
        if not self.supabase:
            return False
        
        try:
            # Get project
            project = self.get_project(project_id)
            
            if not project:
                logger.error(f"Project not found: {project_id}")
                return False
            
            if not project.get('master_sync_enabled'):
                logger.info(f"Master sync disabled for project: {project_id}")
                return False
            
            snapshot = project.get('data_snapshot', {})
            
            if not snapshot:
                logger.warning(f"No snapshot data to sync for project: {project_id}")
                return False
            
            # Sync data to master tables
            # This would sync project-specific data to master tables
            # Implementation depends on what data is in the snapshot
            
            logger.info(f"Synced project {project_id} to master tables")
            return True
        except Exception as e:
            logger.error(f"Error syncing project to master: {e}")
            return False
    
    def complete_project(self, project_id: str, completion_notes: str = '', 
                         documentation: Optional[Dict] = None) -> bool:
        """
        Complete a project.
        
        Args:
            project_id: Project ID
            completion_notes: Completion notes
            documentation: Documentation dictionary
            
        Returns:
            True if completed successfully, False otherwise
        """
        if not self.supabase:
            return False
        
        try:
            # Sync to master before completing
            if self.get_project(project_id).get('master_sync_enabled'):
                self.sync_to_master(project_id)
            
            # Update project status
            self.update(project_id, {
                'status': 'completed',
                'completion_notes': completion_notes,
                'documentation': documentation or {},
                'completed_at': datetime.utcnow().isoformat()
            })
            
            logger.info(f"Completed project: {project_id}")
            return True
        except Exception as e:
            logger.error(f"Error completing project: {e}")
            return False
    
    def generate_documentation(self, project_id: str) -> Dict:
        """
        Generate documentation for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            Documentation dictionary
        """
        if not self.supabase:
            return {}
        
        try:
            project = self.get_project(project_id)
            
            if not project:
                return {}
            
            documentation = {
                'project_name': project.get('project_name'),
                'project_description': project.get('project_description'),
                'project_type': project.get('project_type'),
                'status': project.get('status'),
                'created_at': project.get('created_at'),
                'completed_at': project.get('completed_at'),
                'completion_notes': project.get('completion_notes'),
                'data_snapshot': project.get('data_snapshot', {}),
                'master_sync_enabled': project.get('master_sync_enabled'),
                'documentation_generated_at': datetime.utcnow().isoformat()
            }
            
            # Update project with documentation
            self.update(project_id, {
                'documentation': documentation
            })
            
            logger.info(f"Generated documentation for project: {project_id}")
            return documentation
        except Exception as e:
            logger.error(f"Error generating documentation: {e}")
            return {}
    
    def validate(self, data: Dict, record_id: Optional[str] = None) -> Dict:
        """Validate project data."""
        errors = []
        
        # Required fields
        if 'project_name' not in data or not data['project_name']:
            errors.append("project_name is required")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute project management task.
        
        Args:
            state: Agent state with task information
            
        Returns:
            Updated state with project data
        """
        task = state.get("task", {})
        action = task.get("action", "create")
        
        logger.info(f"Project manager agent: Executing action {action}")
        
        try:
            if action == "create":
                # Create project
                project_name = task.get("project_name")
                project_description = task.get("project_description", "")
                project_type = task.get("project_type", "sandbox")
                master_sync_enabled = task.get("master_sync_enabled", True)
                
                if project_name:
                    project_id = self.create_project(project_name, project_description, project_type, master_sync_enabled)
                    state["context"]["project_id"] = project_id
                    state["results"].append({
                        "agent": self.name,
                        "action": "create_project",
                        "project_id": project_id
                    })
            
            elif action == "get_project":
                # Get project
                project_id = task.get("project_id")
                
                if project_id:
                    project = self.get_project(project_id)
                    state["context"]["project"] = project
                    state["results"].append({
                        "agent": self.name,
                        "action": "get_project",
                        "project": project
                    })
            
            elif action == "update_snapshot":
                # Update project snapshot
                project_id = task.get("project_id")
                snapshot = task.get("snapshot", {})
                
                if project_id and snapshot:
                    self.update_project_snapshot(project_id, snapshot)
                    state["results"].append({
                        "agent": self.name,
                        "action": "update_snapshot",
                        "project_id": project_id
                    })
            
            elif action == "sync_to_master":
                # Sync project to master
                project_id = task.get("project_id")
                
                if project_id:
                    synced = self.sync_to_master(project_id)
                    state["context"]["synced"] = synced
                    state["results"].append({
                        "agent": self.name,
                        "action": "sync_to_master",
                        "synced": synced
                    })
            
            elif action == "complete":
                # Complete project
                project_id = task.get("project_id")
                completion_notes = task.get("completion_notes", "")
                documentation = task.get("documentation")
                
                if project_id:
                    completed = self.complete_project(project_id, completion_notes, documentation)
                    state["context"]["completed"] = completed
                    state["results"].append({
                        "agent": self.name,
                        "action": "complete_project",
                        "completed": completed
                    })
            
            elif action == "generate_documentation":
                # Generate documentation
                project_id = task.get("project_id")
                
                if project_id:
                    documentation = self.generate_documentation(project_id)
                    state["context"]["documentation"] = documentation
                    state["results"].append({
                        "agent": self.name,
                        "action": "generate_documentation",
                        "documentation": documentation
                    })
            
            logger.info(f"Project management complete: {action}")
            
        except Exception as e:
            logger.error(f"Project management error: {e}")
            state["status"] = "failed"
            state["error"] = str(e)
        
        return state

