"""
Standards Manager - Hierarchical Parameter Standards Management

Purpose: Manages hierarchical parameter standards (system-level and agent-level),
validates template compliance, and tracks parameter variations. Integrates with
hive mind for collective standards.

Author: Gematria Hive Team
Date: January 6, 2025
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class StandardsManager:
    """
    Standards Manager - Manages hierarchical parameter standards
    
    Operations:
    - Manages system-level and agent-level standards
    - Validates template compliance
    - Tracks parameter variations
    - Integrates with hive mind for collective standards
    """
    
    def __init__(self, config_dir: str = None):
        """
        Initialize standards manager
        
        Args:
            config_dir: Directory containing standards config files
        """
        self.config_dir = Path(config_dir) if config_dir else Path("./config/standards")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Load standards
        self.system_standards = self._load_system_standards()
        self.agent_standards = self._load_agent_standards()
        self.compliance_rules = self._load_compliance_rules()
        
        logger.info(f"Standards Manager initialized with {len(self.agent_standards)} agent standards")
    
    def _load_system_standards(self) -> Dict:
        """Load system-level standards"""
        system_standards_path = self.config_dir / "system_standards.json"
        
        if system_standards_path.exists():
            try:
                with open(system_standards_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading system standards: {e}")
        
        # Default system standards
        return {
            "system_level": {
                "enforce_template_checks": True,
                "require_compliance_audit": True,
                "mandatory_tools": ["observer", "cost_manager"],
                "default_template": "standard",
                "meta_cognitive_enabled": True,
                "multi_perspective_learning": True,
                "geometric_visualization": True,
                "truth_seeking_mode": True
            },
            "hive_mind": {
                "collective_intelligence": True,
                "knowledge_sharing": True,
                "tribal_knowledge": True,
                "multi_timeline": True
            },
            "meta_cognitive": {
                "track_known_knowns": True,
                "track_known_unknowns": True,
                "detect_unknown_unknowns": True,
                "anomaly_detection": True,
                "fibonacci_patterns": True
            }
        }
    
    def _load_agent_standards(self) -> Dict:
        """Load agent-level standards"""
        agent_standards_dir = self.config_dir / "agent_standards"
        agent_standards_dir.mkdir(parents=True, exist_ok=True)
        
        standards = {}
        
        # Load individual agent standards files
        for agent_file in agent_standards_dir.glob("*.json"):
            try:
                agent_name = agent_file.stem
                with open(agent_file, 'r') as f:
                    standards[agent_name] = json.load(f)
            except Exception as e:
                logger.error(f"Error loading agent standards from {agent_file}: {e}")
        
        return standards
    
    def _load_compliance_rules(self) -> Dict:
        """Load compliance rules"""
        compliance_rules_path = self.config_dir / "compliance_rules.json"
        
        if compliance_rules_path.exists():
            try:
                with open(compliance_rules_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading compliance rules: {e}")
        
        # Default compliance rules
        return {
            "enforcement_mode": "guidance",
            "track_planned_vs_actual": True,
            "log_missing_tools": True,
            "log_missing_agents": True,
            "log_missing_parameters": True,
            "generate_compliance_reports": True,
            "create_feedback_loop": True
        }
    
    def get_system_standards(self) -> Dict:
        """Get system-level standards"""
        return self.system_standards
    
    def get_agent_standards(self, agent_name: str) -> Optional[Dict]:
        """Get agent-specific standards"""
        return self.agent_standards.get(agent_name)
    
    def get_compliance_rules(self) -> Dict:
        """Get compliance rules"""
        return self.compliance_rules
    
    def validate_task(self, task: Dict, agent_name: str = None) -> Dict:
        """
        Validate task against standards
        
        Args:
            task: Task dictionary
            agent_name: Optional agent name for agent-specific validation
            
        Returns:
            Validation result with compliance status
        """
        validation_result = {
            "valid": True,
            "warnings": [],
            "suggestions": [],
            "compliance": {}
        }
        
        # Validate against system standards
        system_validation = self._validate_system_standards(task)
        validation_result["compliance"]["system"] = system_validation
        
        if not system_validation.get("compliant", True):
            validation_result["warnings"].extend(system_validation.get("warnings", []))
        
        # Validate against agent standards if agent specified
        if agent_name:
            agent_validation = self._validate_agent_standards(task, agent_name)
            validation_result["compliance"]["agent"] = agent_validation
            
            if not agent_validation.get("compliant", True):
                validation_result["warnings"].extend(agent_validation.get("warnings", []))
        
        # Add suggestions based on standards
        validation_result["suggestions"] = self._generate_suggestions(task, agent_name)
        
        # Determine overall validity (guidance mode - never block)
        validation_result["valid"] = True  # Always allow execution in guidance mode
        
        return validation_result
    
    def _validate_system_standards(self, task: Dict) -> Dict:
        """Validate against system-level standards"""
        result = {
            "compliant": True,
            "warnings": [],
            "checks": {}
        }
        
        system_level = self.system_standards.get("system_level", {})
        
        # Check template requirements
        if system_level.get("enforce_template_checks", False):
            if "template" not in task:
                result["warnings"].append("No template specified - consider using a template")
                result["checks"]["template"] = False
            else:
                result["checks"]["template"] = True
        
        # Check meta-cognitive awareness
        if system_level.get("meta_cognitive_enabled", False):
            if "meta_cognitive" not in task.get("context", {}):
                result["warnings"].append("Meta-cognitive awareness not specified - consider enabling")
                result["checks"]["meta_cognitive"] = False
            else:
                result["checks"]["meta_cognitive"] = True
        
        # Check multi-perspective learning
        if system_level.get("multi_perspective_learning", False):
            if "multi_perspective" not in task.get("context", {}):
                result["warnings"].append("Multi-perspective learning not specified - consider enabling")
                result["checks"]["multi_perspective"] = False
            else:
                result["checks"]["multi_perspective"] = True
        
        # Overall compliance (guidance mode - warnings don't block)
        result["compliant"] = True
        
        return result
    
    def _validate_agent_standards(self, task: Dict, agent_name: str) -> Dict:
        """Validate against agent-specific standards"""
        result = {
            "compliant": True,
            "warnings": [],
            "checks": {}
        }
        
        agent_std = self.get_agent_standards(agent_name)
        if not agent_std:
            return result
        
        # Check required tools
        required_tools = agent_std.get("required_tools", [])
        task_tools = task.get("tools", [])
        
        missing_tools = [tool for tool in required_tools if tool not in task_tools]
        if missing_tools:
            result["warnings"].append(f"Suggested tools not specified: {missing_tools}")
            result["checks"]["required_tools"] = False
        else:
            result["checks"]["required_tools"] = True
        
        # Check template variations
        template_variations = agent_std.get("template_variations", [])
        task_template = task.get("template")
        
        if task_template and task_template not in template_variations:
            result["warnings"].append(f"Template '{task_template}' not in suggested variations: {template_variations}")
        
        # Overall compliance (guidance mode)
        result["compliant"] = True
        
        return result
    
    def _generate_suggestions(self, task: Dict, agent_name: str = None) -> List[str]:
        """Generate suggestions based on standards"""
        suggestions = []
        
        system_level = self.system_standards.get("system_level", {})
        
        # Suggest meta-cognitive awareness
        if system_level.get("meta_cognitive_enabled", False):
            if "meta_cognitive" not in task.get("context", {}):
                suggestions.append("Consider enabling meta-cognitive awareness for better anomaly detection")
        
        # Suggest multi-perspective learning
        if system_level.get("multi_perspective_learning", False):
            if "multi_perspective" not in task.get("context", {}):
                suggestions.append("Consider enabling multi-perspective learning for richer understanding")
        
        # Suggest geometric analysis
        if system_level.get("geometric_visualization", False):
            if "geometric_analysis" not in task.get("context", {}):
                suggestions.append("Consider enabling geometric analysis for perspective shifts")
        
        # Agent-specific suggestions
        if agent_name:
            agent_std = self.get_agent_standards(agent_name)
            if agent_std:
                if agent_std.get("show_work", False):
                    suggestions.append(f"Consider enabling 'show_work' for {agent_name} to document reasoning")
                if agent_std.get("multi_perspective", False):
                    suggestions.append(f"Consider enabling multi-perspective analysis for {agent_name}")
        
        return suggestions
    
    def save_agent_standards(self, agent_name: str, standards: Dict):
        """Save agent-specific standards"""
        agent_standards_dir = self.config_dir / "agent_standards"
        agent_standards_dir.mkdir(parents=True, exist_ok=True)
        
        agent_file = agent_standards_dir / f"{agent_name}.json"
        
        try:
            with open(agent_file, 'w') as f:
                json.dump(standards, f, indent=2)
            
            # Reload agent standards
            self.agent_standards[agent_name] = standards
            logger.info(f"Saved standards for agent: {agent_name}")
        except Exception as e:
            logger.error(f"Error saving agent standards: {e}")
    
    def update_system_standards(self, updates: Dict):
        """Update system-level standards"""
        self.system_standards.update(updates)
        
        system_standards_path = self.config_dir / "system_standards.json"
        
        try:
            with open(system_standards_path, 'w') as f:
                json.dump(self.system_standards, f, indent=2)
            logger.info("Updated system standards")
        except Exception as e:
            logger.error(f"Error updating system standards: {e}")


# Singleton instance
_standards_manager = None

def get_standards_manager() -> StandardsManager:
    """Get or create standards manager singleton"""
    global _standards_manager
    if _standards_manager is None:
        _standards_manager = StandardsManager()
    return _standards_manager

