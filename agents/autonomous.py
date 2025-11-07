"""
Autonomous Agent

Purpose: Autonomous agent that can commit changes and proceed with work
while you're away. Includes configurable milestones to stop at reasonable points.

Features:
- Automatic git commits when changes are detected
- Task queue processing
- Milestone-based stopping (max commits, time, tasks, etc.)
- Configurable settings for safe autonomous operation

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import os
import subprocess
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class AutonomousAgent:
    """
    Autonomous Agent - Commits changes and proceeds with work autonomously
    
    Operations:
    - Monitor git status and commit changes automatically
    - Process task queue autonomously
    - Stop at configurable milestones
    - Log all activities for review
    """
    
    def __init__(self, 
                 max_commits: int = 10,
                 max_time_hours: float = 8.0,
                 max_tasks: int = 50,
                 commit_interval_seconds: int = 300,  # 5 minutes
                 auto_push: bool = False,
                 branch: str = None,
                 work_dir: str = None):
        """
        Initialize autonomous agent
        
        Args:
            max_commits: Maximum number of commits before stopping
            max_time_hours: Maximum hours to run before stopping
            max_tasks: Maximum number of tasks to process before stopping
            commit_interval_seconds: Minimum seconds between commits
            auto_push: Whether to automatically push commits
            branch: Git branch to work on (default: current branch)
            work_dir: Working directory (default: current directory)
        """
        self.name = "autonomous_agent"
        self.max_commits = max_commits
        self.max_time_hours = max_time_hours
        self.max_tasks = max_tasks
        self.commit_interval_seconds = commit_interval_seconds
        self.auto_push = auto_push
        self.work_dir = work_dir or os.getcwd()
        self.branch = branch
        
        # Tracking
        self.commit_count = 0
        self.task_count = 0
        self.start_time = None
        self.last_commit_time = None
        self.task_queue: List[Dict] = []
        self.activity_log: List[Dict] = []
        
        logger.info(f"Initialized {self.name} with milestones: "
                   f"max_commits={max_commits}, max_time={max_time_hours}h, "
                   f"max_tasks={max_tasks}")
    
    def _run_git_command(self, command: List[str], check: bool = True) -> Tuple[str, str, int]:
        """
        Run a git command and return output
        
        Args:
            command: Git command as list of strings
            check: Whether to raise exception on error
            
        Returns:
            Tuple of (stdout, stderr, returncode)
        """
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                check=check
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(command)} - {e}")
            return e.stdout.strip(), e.stderr.strip(), e.returncode
        except Exception as e:
            logger.error(f"Error running git command: {e}")
            return "", str(e), 1
    
    def _get_current_branch(self) -> Optional[str]:
        """Get current git branch"""
        stdout, _, returncode = self._run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])
        if returncode == 0:
            return stdout
        return None
    
    def _check_git_status(self) -> Dict[str, Any]:
        """
        Check git status and return information about changes
        
        Returns:
            Dictionary with status information
        """
        # Check if there are changes
        stdout, _, returncode = self._run_git_command(['status', '--porcelain'])
        has_changes = bool(stdout.strip())
        
        # Get branch
        branch = self._get_current_branch()
        
        # Count changes
        if has_changes:
            lines = stdout.strip().split('\n')
            modified = sum(1 for line in lines if line.startswith(' M'))
            added = sum(1 for line in lines if line.startswith('A ') or line.startswith('??'))
            deleted = sum(1 for line in lines if line.startswith(' D'))
        else:
            modified = added = deleted = 0
        
        return {
            'has_changes': has_changes,
            'branch': branch,
            'modified': modified,
            'added': added,
            'deleted': deleted,
            'status_output': stdout
        }
    
    def _generate_commit_message(self, status: Dict[str, Any]) -> str:
        """
        Generate a commit message based on changes
        
        Args:
            status: Git status dictionary
            
        Returns:
            Commit message string
        """
        changes = []
        if status['added'] > 0:
            changes.append(f"{status['added']} new file(s)")
        if status['modified'] > 0:
            changes.append(f"{status['modified']} modified file(s)")
        if status['deleted'] > 0:
            changes.append(f"{status['deleted']} deleted file(s)")
        
        change_summary = ", ".join(changes) if changes else "changes"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"Autonomous commit: {change_summary}\n\n"
        message += f"Timestamp: {timestamp}\n"
        message += f"Commit #{self.commit_count + 1} of {self.max_commits}\n"
        message += f"Task #{self.task_count} completed"
        
        return message
    
    def commit_changes(self, message: Optional[str] = None) -> bool:
        """
        Commit current changes if any exist
        
        Args:
            message: Optional commit message (auto-generated if not provided)
            
        Returns:
            True if commit was successful, False otherwise
        """
        # Check if enough time has passed since last commit
        if self.last_commit_time:
            elapsed = time.time() - self.last_commit_time
            if elapsed < self.commit_interval_seconds:
                logger.info(f"Skipping commit - only {elapsed:.1f}s since last commit "
                           f"(minimum: {self.commit_interval_seconds}s)")
                return False
        
        # Check git status
        status = self._check_git_status()
        
        if not status['has_changes']:
            logger.info("No changes to commit")
            return False
        
        # Check milestone: max commits
        if self.commit_count >= self.max_commits:
            logger.warning(f"Milestone reached: max commits ({self.max_commits})")
            return False
        
        # Generate commit message if not provided
        if not message:
            message = self._generate_commit_message(status)
        
        # Stage all changes
        logger.info(f"Staging changes: {status['modified']} modified, "
                   f"{status['added']} added, {status['deleted']} deleted")
        stdout, stderr, returncode = self._run_git_command(['add', '.'])
        if returncode != 0:
            logger.error(f"Failed to stage changes: {stderr}")
            return False
        
        # Commit
        logger.info(f"Committing changes (commit #{self.commit_count + 1})...")
        stdout, stderr, returncode = self._run_git_command(
            ['commit', '-m', message],
            check=False
        )
        
        if returncode == 0:
            self.commit_count += 1
            self.last_commit_time = time.time()
            self.activity_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'commit',
                'commit_number': self.commit_count,
                'message': message,
                'status': status
            })
            logger.info(f"Successfully committed (commit #{self.commit_count})")
            
            # Auto-push if enabled
            if self.auto_push:
                self.push_changes()
            
            return True
        else:
            logger.error(f"Failed to commit: {stderr}")
            return False
    
    def push_changes(self) -> bool:
        """
        Push commits to remote repository
        
        Returns:
            True if push was successful, False otherwise
        """
        branch = self.branch or self._get_current_branch()
        if not branch:
            logger.error("Could not determine branch to push")
            return False
        
        logger.info(f"Pushing to origin/{branch}...")
        stdout, stderr, returncode = self._run_git_command(
            ['push', 'origin', branch],
            check=False
        )
        
        if returncode == 0:
            self.activity_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'push',
                'branch': branch
            })
            logger.info(f"Successfully pushed to origin/{branch}")
            return True
        else:
            logger.error(f"Failed to push: {stderr}")
            return False
    
    def check_milestones(self) -> Dict[str, Any]:
        """
        Check if any milestones have been reached
        
        Returns:
            Dictionary with milestone status
        """
        if not self.start_time:
            return {'reached': False}
        
        elapsed_time = time.time() - self.start_time
        elapsed_hours = elapsed_time / 3600
        
        milestones = {
            'max_commits': self.commit_count >= self.max_commits,
            'max_time': elapsed_hours >= self.max_time_hours,
            'max_tasks': self.task_count >= self.max_tasks,
            'elapsed_hours': elapsed_hours,
            'commit_count': self.commit_count,
            'task_count': self.task_count
        }
        
        milestones['reached'] = any([
            milestones['max_commits'],
            milestones['max_time'],
            milestones['max_tasks']
        ])
        
        return milestones
    
    def add_task(self, task: Dict) -> None:
        """
        Add a task to the queue
        
        Args:
            task: Task dictionary with 'type', 'action', etc.
        """
        self.task_queue.append({
            **task,
            'added_at': datetime.now().isoformat(),
            'status': 'pending'
        })
        logger.info(f"Added task to queue: {task.get('type', 'unknown')} "
                   f"(queue size: {len(self.task_queue)})")
    
    def process_task(self, task: Dict) -> Dict:
        """
        Process a single task
        
        Args:
            task: Task dictionary
            
        Returns:
            Result dictionary
        """
        task_type = task.get('type', 'unknown')
        logger.info(f"Processing task: {task_type} (task #{self.task_count + 1})")
        
        # Mark task as in progress
        task['status'] = 'in_progress'
        task['started_at'] = datetime.now().isoformat()
        
        result = {
            'task': task,
            'success': False,
            'error': None,
            'output': None
        }
        
        try:
            # Here you can integrate with other agents or custom logic
            # For now, this is a placeholder that can be extended
            action = task.get('action', 'process')
            
            if action == 'commit':
                # Force commit
                success = self.commit_changes(task.get('message'))
                result['success'] = success
                result['output'] = f"Commit {'succeeded' if success else 'failed'}"
            
            elif action == 'wait':
                # Wait for specified seconds
                wait_seconds = task.get('seconds', 60)
                logger.info(f"Waiting {wait_seconds} seconds...")
                time.sleep(wait_seconds)
                result['success'] = True
                result['output'] = f"Waited {wait_seconds} seconds"
            
            else:
                # Default: just log the task
                result['success'] = True
                result['output'] = f"Processed task: {task_type}"
            
            task['status'] = 'completed'
            task['completed_at'] = datetime.now().isoformat()
            self.task_count += 1
            
        except Exception as e:
            logger.error(f"Error processing task: {e}")
            task['status'] = 'failed'
            task['error'] = str(e)
            result['error'] = str(e)
        
        self.activity_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'process_task',
            'task': task,
            'result': result
        })
        
        return result
    
    def run(self, tasks: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Run the autonomous agent
        
        Args:
            tasks: Optional list of tasks to process
            
        Returns:
            Summary dictionary with results
        """
        self.start_time = time.time()
        self.start_time_dt = datetime.now()
        
        logger.info(f"Starting autonomous agent run...")
        logger.info(f"Milestones: max_commits={self.max_commits}, "
                   f"max_time={self.max_time_hours}h, max_tasks={self.max_tasks}")
        
        # Add tasks to queue if provided
        if tasks:
            for task in tasks:
                self.add_task(task)
        
        # Main loop
        while True:
            # Check milestones
            milestones = self.check_milestones()
            if milestones['reached']:
                reason = []
                if milestones['max_commits']:
                    reason.append(f"max commits ({self.commit_count}/{self.max_commits})")
                if milestones['max_time']:
                    reason.append(f"max time ({milestones['elapsed_hours']:.2f}h/{self.max_time_hours}h)")
                if milestones['max_tasks']:
                    reason.append(f"max tasks ({self.task_count}/{self.max_tasks})")
                
                logger.info(f"Milestone reached: {', '.join(reason)}. Stopping.")
                break
            
            # Process task if available
            if self.task_queue:
                task = self.task_queue.pop(0)
                self.process_task(task)
            else:
                # No tasks, check for changes and commit if needed
                self.commit_changes()
            
            # Small sleep to avoid tight loop
            time.sleep(10)
        
        # Final commit if there are changes
        self.commit_changes()
        
        # Generate summary
        elapsed_time = time.time() - self.start_time
        summary = {
            'start_time': self.start_time_dt.isoformat(),
            'end_time': datetime.now().isoformat(),
            'elapsed_hours': elapsed_time / 3600,
            'commits_made': self.commit_count,
            'tasks_processed': self.task_count,
            'milestones_reached': milestones,
            'activity_log': self.activity_log
        }
        
        logger.info(f"Autonomous agent run completed:")
        logger.info(f"  - Commits: {self.commit_count}/{self.max_commits}")
        logger.info(f"  - Tasks: {self.task_count}/{self.max_tasks}")
        logger.info(f"  - Time: {elapsed_time/3600:.2f}h/{self.max_time_hours}h")
        
        return summary
    
    def save_log(self, filepath: str = None) -> str:
        """
        Save activity log to file
        
        Args:
            filepath: Optional filepath (default: autonomous_log_YYYYMMDD_HHMMSS.json)
            
        Returns:
            Path to saved log file
        """
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.work_dir, f"autonomous_log_{timestamp}.json")
        
        log_data = {
            'agent': self.name,
            'settings': {
                'max_commits': self.max_commits,
                'max_time_hours': self.max_time_hours,
                'max_tasks': self.max_tasks,
                'commit_interval_seconds': self.commit_interval_seconds,
                'auto_push': self.auto_push
            },
            'activity_log': self.activity_log
        }
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        logger.info(f"Activity log saved to: {filepath}")
        return filepath

