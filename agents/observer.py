"""
Observer Agent

Purpose: Monitor system activity, track metrics, log events, and maintain
observational notes about the agent system's behavior and performance.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import logging
import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
from agents.orchestrator import AgentState
from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import create_client, Client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False
    print("Warning: supabase not installed, observer will use file-based storage")

logger = logging.getLogger(__name__)


class ObserverAgent:
    """
    Observer Agent - Monitors and tracks system activity
    
    Operations:
    - Monitor agent executions and performance
    - Track metrics (cost, time, success rates)
    - Log events and observations
    - Maintain observational notes
    - Generate system health reports
    """
    
    def __init__(self, notes_dir: str = None):
        """
        Initialize observer agent
        
        Args:
            notes_dir: Directory for storing observation notes (default: ./notes/observations)
        """
        self.name = "observer_agent"
        self.notes_dir = Path(notes_dir) if notes_dir else Path("./notes/observations")
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        
        # Metrics tracking
        self.metrics = {
            "agent_executions": {},
            "total_cost": 0.0,
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "average_execution_time": 0.0,
            "observations": []
        }
        
        # Supabase for persistent storage
        if HAS_SUPABASE:
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            if supabase_url and supabase_key:
                self.supabase = create_client(supabase_url, supabase_key)
                logger.info("Observer: Supabase connected for persistent storage")
            else:
                self.supabase = None
        else:
            self.supabase = None
        
        logger.info(f"Initialized {self.name} with notes directory: {self.notes_dir}")
    
    def observe(self, event_type: str, data: Dict, agent_name: str = None) -> str:
        """
        Record an observation
        
        Args:
            event_type: Type of event (execution_start, execution_end, error, etc.)
            data: Event data dictionary
            agent_name: Name of agent that triggered the event
            
        Returns:
            Observation ID
        """
        observation = {
            "id": f"obs_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "agent_name": agent_name,
            "data": data
        }
        
        # Add to metrics
        self.metrics["observations"].append(observation)
        
        # Save to file
        self._save_observation(observation)
        
        # Save to Supabase if available
        if self.supabase:
            try:
                self.supabase.table("observations").insert({
                    "observation_id": observation["id"],
                    "timestamp": observation["timestamp"],
                    "event_type": event_type,
                    "agent_name": agent_name,
                    "data": json.dumps(data)
                }).execute()
            except Exception as e:
                logger.error(f"Error saving observation to Supabase: {e}")
        
        logger.debug(f"Observation recorded: {event_type} from {agent_name}")
        return observation["id"]
    
    def _save_observation(self, observation: Dict) -> None:
        """Save observation to file"""
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = self.notes_dir / f"observations_{date_str}.jsonl"
        
        with open(filepath, 'a') as f:
            f.write(json.dumps(observation) + '\n')
    
    def track_execution(self, agent_name: str, state: AgentState, 
                       execution_time: float = None) -> None:
        """
        Track agent execution
        
        Args:
            agent_name: Name of the agent
            state: Agent state after execution
            execution_time: Execution time in seconds
        """
        if agent_name not in self.metrics["agent_executions"]:
            self.metrics["agent_executions"][agent_name] = {
                "count": 0,
                "total_time": 0.0,
                "total_cost": 0.0,
                "successes": 0,
                "failures": 0
            }
        
        metrics = self.metrics["agent_executions"][agent_name]
        metrics["count"] += 1
        self.metrics["total_tasks"] += 1
        
        if execution_time:
            metrics["total_time"] += execution_time
        
        cost = state.get("cost", 0.0)
        metrics["total_cost"] += cost
        self.metrics["total_cost"] += cost
        
        status = state.get("status", "unknown")
        if status == "completed":
            metrics["successes"] += 1
            self.metrics["successful_tasks"] += 1
        elif status == "failed":
            metrics["failures"] += 1
            self.metrics["failed_tasks"] += 1
        
        # Record observation
        self.observe("execution_complete", {
            "agent": agent_name,
            "status": status,
            "cost": cost,
            "execution_time": execution_time,
            "data_count": len(state.get("data", [])),
            "results_count": len(state.get("results", []))
        }, agent_name)
    
    def record_error(self, agent_name: str, error: Exception, context: Dict = None) -> None:
        """
        Record an error observation
        
        Args:
            agent_name: Name of agent that encountered error
            error: Exception object
            context: Additional context dictionary
        """
        self.observe("error", {
            "agent": agent_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        }, agent_name)
        
        logger.warning(f"Error recorded from {agent_name}: {error}")
    
    def record_metric(self, metric_name: str, value: Any, agent_name: str = None) -> None:
        """
        Record a custom metric
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            agent_name: Optional agent name
        """
        self.observe("metric", {
            "metric_name": metric_name,
            "value": value,
            "agent": agent_name
        }, agent_name)
    
    def execute(self, state: AgentState) -> AgentState:
        """
        Execute observer task (monitor other agents)
        
        Args:
            state: Agent state
            
        Returns:
            Updated state with observation data
        """
        task = state.get("task", {})
        task_type = task.get("type", "monitor")
        
        logger.info(f"Observer agent: {task_type}")
        
        if task_type == "monitor":
            # Monitor current system state
            health_report = self.generate_health_report()
            state["results"].append({
                "agent": self.name,
                "action": "monitor",
                "health_report": health_report
            })
        
        elif task_type == "metrics":
            # Return current metrics
            state["results"].append({
                "agent": self.name,
                "action": "metrics",
                "metrics": self.get_metrics_summary()
            })
        
        elif task_type == "notes":
            # Return recent observations
            recent_notes = self.get_recent_observations(hours=24)
            state["results"].append({
                "agent": self.name,
                "action": "notes",
                "observations": recent_notes
            })
        
        return state
    
    def generate_health_report(self) -> Dict[str, Any]:
        """
        Generate system health report
        
        Returns:
            Dictionary with health metrics
        """
        total_executions = sum(
            m["count"] for m in self.metrics["agent_executions"].values()
        )
        
        success_rate = 0.0
        if self.metrics["total_tasks"] > 0:
            success_rate = (self.metrics["successful_tasks"] / 
                          self.metrics["total_tasks"]) * 100
        
        avg_time = 0.0
        if total_executions > 0:
            total_time = sum(
                m["total_time"] for m in self.metrics["agent_executions"].values()
            )
            avg_time = total_time / total_executions
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_tasks": self.metrics["total_tasks"],
            "successful_tasks": self.metrics["successful_tasks"],
            "failed_tasks": self.metrics["failed_tasks"],
            "success_rate": round(success_rate, 2),
            "total_cost": round(self.metrics["total_cost"], 4),
            "average_execution_time": round(avg_time, 2),
            "agent_performance": {
                name: {
                    "executions": m["count"],
                    "success_rate": round(
                        (m["successes"] / m["count"] * 100) if m["count"] > 0 else 0, 2
                    ),
                    "avg_cost": round(
                        m["total_cost"] / m["count"] if m["count"] > 0 else 0, 4
                    ),
                    "avg_time": round(
                        m["total_time"] / m["count"] if m["count"] > 0 else 0, 2
                    )
                }
                for name, m in self.metrics["agent_executions"].items()
            },
            "recent_observations_count": len(self.metrics["observations"][-100:])
        }
        
        return report
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        return {
            "total_cost": self.metrics["total_cost"],
            "total_tasks": self.metrics["total_tasks"],
            "successful_tasks": self.metrics["successful_tasks"],
            "failed_tasks": self.metrics["failed_tasks"],
            "agent_executions": self.metrics["agent_executions"],
            "observations_count": len(self.metrics["observations"])
        }
    
    def get_recent_observations(self, hours: int = 24, limit: int = 100) -> List[Dict]:
        """
        Get recent observations
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of observations to return
            
        Returns:
            List of observation dictionaries
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        recent = [
            obs for obs in self.metrics["observations"]
            if datetime.fromisoformat(obs["timestamp"]) >= cutoff
        ]
        
        return recent[-limit:]
    
    def save_notes(self, filepath: str = None) -> str:
        """
        Save all observations to a file
        
        Args:
            filepath: Optional filepath (default: notes/observations_summary_YYYYMMDD.json)
            
        Returns:
            Path to saved file
        """
        if not filepath:
            date_str = datetime.now().strftime("%Y%m%d")
            filepath = self.notes_dir / f"observations_summary_{date_str}.json"
        
        notes_data = {
            "generated_at": datetime.utcnow().isoformat(),
            "metrics": self.metrics,
            "health_report": self.generate_health_report()
        }
        
        with open(filepath, 'w') as f:
            json.dump(notes_data, f, indent=2)
        
        logger.info(f"Observer notes saved to: {filepath}")
        return str(filepath)

