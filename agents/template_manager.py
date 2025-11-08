"""
Template Manager - SOP and Prompt Template Management

Purpose: Manages SOP templates, prompt templates, execution templates with variations,
enables template switching at runtime, tracks template usage and compliance, and
auto-generates SOPs from execution patterns.

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


class TemplateManager:
    """
    Template Manager - Manages SOP and prompt templates
    
    Operations:
    - Manages SOP templates, prompt templates, execution templates
    - Supports template variations
    - Enables template switching at runtime
    - Tracks template usage and compliance
    - Auto-generates SOPs from execution patterns
    - Documents proofs and decision flows
    """
    
    def __init__(self, config_dir: str = None):
        """
        Initialize template manager
        
        Args:
            config_dir: Directory containing template config files
        """
        self.config_dir = Path(config_dir) if config_dir else Path("./config/standards/templates")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Load templates
        self.sop_templates = self._load_sop_templates()
        self.prompt_templates = self._load_prompt_templates()
        self.execution_templates = self._load_execution_templates()
        
        # Template usage tracking
        self.template_usage = {}
        
        logger.info(f"Template Manager initialized with {len(self.sop_templates)} SOP templates")
    
    def _load_sop_templates(self) -> Dict:
        """Load SOP templates"""
        sop_templates_path = self.config_dir / "sop_templates.json"
        
        if sop_templates_path.exists():
            try:
                with open(sop_templates_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading SOP templates: {e}")
        
        # Default SOP templates
        return {
            "api_key_setup": {
                "variations": {
                    "browser_required": {
                        "description": "Requires browser agent for web scraping",
                        "required_tools": ["browser"],
                        "prompt_template": "Use browser agent to navigate to {url} and extract API key setup information...",
                        "compliance_checks": ["browser_executed", "pages_scraped"],
                        "expert_board": ["web_scraping_expert", "api_security_expert"],
                        "show_work": True,
                        "multi_perspective": True,
                        "geometric_analysis": True
                    },
                    "api_only": {
                        "description": "Uses API only, no browser",
                        "required_tools": ["api_client"],
                        "prompt_template": "Use API to retrieve {resource} and extract API key information...",
                        "compliance_checks": ["api_called", "data_retrieved"],
                        "expert_board": ["api_expert", "security_expert"],
                        "show_work": True,
                        "multi_perspective": True
                    }
                },
                "auto_generated": True,
                "version": "1.0",
                "proof_documentation": True,
                "decision_flow": True
            }
        }
    
    def _load_prompt_templates(self) -> Dict:
        """Load prompt templates"""
        prompt_templates_path = self.config_dir / "prompt_templates.json"
        
        if prompt_templates_path.exists():
            try:
                with open(prompt_templates_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading prompt templates: {e}")
        
        # Default prompt templates
        return {
            "system_prompt": {
                "default": "Pursue truth with falsifiability. Unify gematria/esoteric with math—log leaps, measure costs.",
                "variations": {
                    "truth_seeking": "Seek eternal truth through exploration. Remain open to hidden truths while maintaining scientific rigor.",
                    "geometric": "Understand data through geometric forms (2D→3D→4D→5D). Recognize sacred geometry patterns.",
                    "multi_perspective": "Analyze from multiple perspectives (windshield, side windows, rearview). Merge insights for richer understanding."
                }
            },
            "mcp_prompt": {
                "default": "Triangulate data, segment phases, update master DB. Route tasks to appropriate agents.",
                "variations": {
                    "hive_mind": "Coordinate with hive mind collective intelligence. Share tribal knowledge. Learn from all perspectives.",
                    "meta_cognitive": "Track known knowns, known unknowns, and unknown unknowns. Detect anomalies.",
                    "geometric": "Apply geometric analysis. Recognize fibonacci/quantum patterns. Enable perspective shifts."
                }
            },
            "task_prompt": {
                "default": "Filter cosine >0.7; measure costs; flag for phase2 if score <0.5.",
                "variations": {
                    "comprehensive": "Execute with full documentation. Show work. Enable multi-perspective analysis. Document all reasoning.",
                    "geometric": "Apply geometric analysis. Recognize patterns. Enable perspective shifts.",
                    "expert_board": "Assemble expert board. Gather multiple perspectives. Document all reasoning."
                }
            }
        }
    
    def _load_execution_templates(self) -> Dict:
        """Load execution templates"""
        execution_templates_path = self.config_dir / "execution_templates.json"
        
        if execution_templates_path.exists():
            try:
                with open(execution_templates_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading execution templates: {e}")
        
        # Default execution templates
        return {
            "standard": {
                "description": "Standard execution template",
                "steps": ["pre_execution", "execution", "post_execution"],
                "compliance_checks": ["basic"]
            },
            "multi_perspective": {
                "description": "Multi-perspective execution template",
                "steps": ["pre_execution", "multi_perspective_setup", "parallel_execution", "perspective_merge", "post_execution"],
                "compliance_checks": ["multi_perspective", "perspective_merge"]
            },
            "geometric": {
                "description": "Geometric analysis execution template",
                "steps": ["pre_execution", "geometric_setup", "execution", "geometric_analysis", "post_execution"],
                "compliance_checks": ["geometric", "pattern_recognition"]
            },
            "expert_board": {
                "description": "Expert board execution template",
                "steps": ["pre_execution", "expert_board_assembly", "parallel_analysis", "expert_merge", "post_execution"],
                "compliance_checks": ["expert_board", "expert_analysis"]
            }
        }
    
    def get_sop_template(self, template_name: str, variation: str = None) -> Optional[Dict]:
        """
        Get SOP template
        
        Args:
            template_name: Name of SOP template
            variation: Optional variation name
            
        Returns:
            Template dictionary or None
        """
        template = self.sop_templates.get(template_name)
        if not template:
            return None
        
        if variation:
            variations = template.get("variations", {})
            return variations.get(variation)
        
        return template
    
    def get_prompt_template(self, template_name: str, variation: str = None) -> Optional[str]:
        """
        Get prompt template
        
        Args:
            template_name: Name of prompt template
            variation: Optional variation name
            
        Returns:
            Prompt string or None
        """
        template = self.prompt_templates.get(template_name)
        if not template:
            return None
        
        if variation:
            variations = template.get("variations", {})
            return variations.get(variation)
        
        return template.get("default")
    
    def get_execution_template(self, template_name: str) -> Optional[Dict]:
        """
        Get execution template
        
        Args:
            template_name: Name of execution template
            
        Returns:
            Template dictionary or None
        """
        return self.execution_templates.get(template_name)
    
    def switch_template(self, task: Dict, new_template: str, variation: str = None) -> Dict:
        """
        Switch template for a task
        
        Args:
            task: Task dictionary
            new_template: New template name
            variation: Optional variation name
            
        Returns:
            Updated task dictionary
        """
        # Get new template
        template = self.get_sop_template(new_template, variation)
        if not template:
            logger.warning(f"Template {new_template} not found")
            return task
        
        # Update task with template information
        task["template"] = new_template
        if variation:
            task["template_variation"] = variation
        
        # Apply template properties
        if "required_tools" in template:
            task["tools"] = template["required_tools"]
        
        if "prompt_template" in template:
            task["prompt"] = template["prompt_template"]
        
        if "compliance_checks" in template:
            task["compliance_checks"] = template["compliance_checks"]
        
        # Track template usage
        self._track_template_usage(new_template, variation)
        
        logger.info(f"Switched task to template: {new_template} (variation: {variation})")
        
        return task
    
    def _track_template_usage(self, template_name: str, variation: str = None):
        """Track template usage"""
        key = f"{template_name}:{variation}" if variation else template_name
        
        if key not in self.template_usage:
            self.template_usage[key] = {
                "count": 0,
                "first_used": datetime.utcnow().isoformat(),
                "last_used": None
            }
        
        self.template_usage[key]["count"] += 1
        self.template_usage[key]["last_used"] = datetime.utcnow().isoformat()
    
    def auto_generate_sop(self, execution_pattern: Dict) -> Dict:
        """
        Auto-generate SOP from execution pattern
        
        Args:
            execution_pattern: Execution pattern dictionary
            
        Returns:
            Generated SOP template
        """
        sop = {
            "name": execution_pattern.get("name", f"auto_generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            "description": execution_pattern.get("description", "Auto-generated SOP"),
            "variations": {
                "default": {
                    "description": "Default variation",
                    "required_tools": execution_pattern.get("tools", []),
                    "prompt_template": execution_pattern.get("prompt", ""),
                    "compliance_checks": execution_pattern.get("compliance_checks", []),
                    "show_work": True,
                    "multi_perspective": execution_pattern.get("multi_perspective", False),
                    "geometric_analysis": execution_pattern.get("geometric_analysis", False)
                }
            },
            "auto_generated": True,
            "version": "1.0",
            "generated_at": datetime.utcnow().isoformat(),
            "proof_documentation": True,
            "decision_flow": True
        }
        
        # Save auto-generated SOP
        self.sop_templates[sop["name"]] = sop
        self._save_sop_templates()
        
        logger.info(f"Auto-generated SOP: {sop['name']}")
        
        return sop
    
    def _save_sop_templates(self):
        """Save SOP templates to file"""
        sop_templates_path = self.config_dir / "sop_templates.json"
        
        try:
            with open(sop_templates_path, 'w') as f:
                json.dump(self.sop_templates, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving SOP templates: {e}")
    
    def get_template_usage_stats(self) -> Dict:
        """Get template usage statistics"""
        return {
            "total_templates": len(self.sop_templates),
            "usage_stats": self.template_usage,
            "most_used": max(self.template_usage.items(), key=lambda x: x[1]["count"])[0] if self.template_usage else None
        }


# Singleton instance
_template_manager = None

def get_template_manager() -> TemplateManager:
    """Get or create template manager singleton"""
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager()
    return _template_manager

