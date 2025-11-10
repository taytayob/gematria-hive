#!/usr/bin/env python3
"""
Comprehensive System Review and Consolidation
Gematria Hive - Complete system review using Claude and Grok together

Purpose:
- Review all open editors and documents
- Check Claude skills, bookmarks, and knowledge base status
- Run all system scripts and workflows
- Use Grok and Claude together for analysis
- Generate unified comprehensive report

Author: Gematria Hive Team
Date: January 9, 2025
"""

import os
import json
import logging
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict

from dotenv import load_dotenv
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our systems
try:
    from global_knowledge_registry_and_report_card import (
        get_global_registry, FindingRank, RuleType, RuleCategory
    )
    from agents.claude_integrator import ClaudeIntegratorAgent
    from agents.enhanced_claude_integrator import EnhancedClaudeIntegrator
    from agents.bookmark_ingestion import BookmarkIngestionAgent
    from agents.knowledge_registry import KnowledgeRegistry, get_registry
    from agents.mcp_tool_registry import MCPToolRegistry, get_tool_registry
    from global_resource_tracking_and_workflow_system import (
        get_resource_tracking_system, ResourceType, ItemStatus
    )
    from prompt_enhancement_and_writer_system import (
        get_prompt_enhancement_system, PromptEnhancementType, ContentType
    )
    from core.gematria_engine import get_gematria_engine
    from core.sacred_geometry_engine import get_sacred_geometry_engine
    from core.domain_expansion_engine import get_domain_expansion_engine
    from comprehensive_html_reporting_and_indexing_system import ComprehensiveHTMLReportingAndIndexingSystem
    HAS_DEPENDENCIES = True
except ImportError as e:
    HAS_DEPENDENCIES = False
    logger.warning(f"Some dependencies not available: {e}")


@dataclass
class SystemComponent:
    """System component status"""
    name: str
    status: str  # working, failed, partial, not_tested
    description: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    last_tested: Optional[str] = None


@dataclass
class ScriptResult:
    """Script execution result"""
    script_name: str
    status: str  # success, failed, skipped
    output: str = ""
    errors: List[str] = field(default_factory=list)
    execution_time: float = 0.0


class ComprehensiveSystemReview:
    """
    Comprehensive System Review and Consolidation
    
    Features:
    - Review all system components
    - Check Claude skills and bookmarks
    - Review knowledge base
    - Run all scripts and workflows
    - Use Grok and Claude together
    - Generate unified report
    """
    
    def __init__(self):
        """Initialize comprehensive system review"""
        self.name = "comprehensive_system_review"
        self.project_root = Path(__file__).parent
        
        # Core systems
        self.registry = get_global_registry() if HAS_DEPENDENCIES else None
        self.claude_agent = ClaudeIntegratorAgent() if HAS_DEPENDENCIES else None
        self.enhanced_claude = EnhancedClaudeIntegrator() if HAS_DEPENDENCIES else None
        self.bookmark_agent = BookmarkIngestionAgent() if HAS_DEPENDENCIES else None
        self.knowledge_registry = get_registry() if HAS_DEPENDENCIES else None
        self.mcp_registry = get_tool_registry() if HAS_DEPENDENCIES else None
        self.gematria_engine = get_gematria_engine() if HAS_DEPENDENCIES else None
        self.sacred_geometry_engine = get_sacred_geometry_engine() if HAS_DEPENDENCIES else None
        self.domain_expansion_engine = get_domain_expansion_engine() if HAS_DEPENDENCIES else None
        self.html_system = ComprehensiveHTMLReportingAndIndexingSystem() if HAS_DEPENDENCIES else None
        self.resource_tracking = get_resource_tracking_system() if HAS_DEPENDENCIES else None
        self.prompt_enhancement = get_prompt_enhancement_system() if HAS_DEPENDENCIES else None
        
        # Review state
        self.components: Dict[str, SystemComponent] = {}
        self.script_results: List[ScriptResult] = []
        self.findings: List[Dict[str, Any]] = []
        self.claude_skills_status: Dict[str, Any] = {}
        self.bookmarks_status: Dict[str, Any] = {}
        self.knowledge_base_status: Dict[str, Any] = {}
        
        # Storage
        self.storage_path = self.project_root / "data" / "system_reviews"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized {self.name}")
    
    def review_all_components(self) -> Dict[str, SystemComponent]:
        """Review all system components"""
        
        logger.info("=" * 80)
        logger.info("Reviewing All System Components")
        logger.info("=" * 80)
        
        components = {}
        
        # 1. Claude Skills
        logger.info("Reviewing Claude Skills...")
        claude_skills = self._review_claude_skills()
        components['claude_skills'] = claude_skills
        
        # 2. Bookmark Processing
        logger.info("Reviewing Bookmark Processing...")
        bookmarks = self._review_bookmark_processing()
        components['bookmarks'] = bookmarks
        
        # 3. Knowledge Base
        logger.info("Reviewing Knowledge Base...")
        knowledge_base = self._review_knowledge_base()
        components['knowledge_base'] = knowledge_base
        
        # 4. MCP Tools
        logger.info("Reviewing MCP Tools...")
        mcp_tools = self._review_mcp_tools()
        components['mcp_tools'] = mcp_tools
        
        # 5. Core Engines
        logger.info("Reviewing Core Engines...")
        core_engines = self._review_core_engines()
        components['core_engines'] = core_engines
        
        # 6. Agents
        logger.info("Reviewing Agents...")
        agents = self._review_agents()
        components['agents'] = agents
        
        # 7. Workflows
        logger.info("Reviewing Workflows...")
        workflows = self._review_workflows()
        components['workflows'] = workflows
        
        # 8. Integrations
        logger.info("Reviewing Integrations...")
        integrations = self._review_integrations()
        components['integrations'] = integrations
        
        self.components = components
        logger.info(f"✅ Reviewed {len(components)} component categories")
        return components
    
    def _review_claude_skills(self) -> SystemComponent:
        """Review Claude skills status"""
        status = "working"
        errors = []
        warnings = []
        notes = []
        
        try:
            if self.knowledge_registry:
                skills = self.knowledge_registry.claude_skills
                self.claude_skills_status = {
                    'total_skills': len(skills),
                    'skills': {name: {
                        'name': skill.name,
                        'description': skill.description,
                        'status': skill.status.value,
                        'export_path': skill.export_path
                    } for name, skill in skills.items()}
                }
                
                # Check for unprocessed skills
                unprocessed = [s for s in skills.values() if s.status.value == 'not_started']
                if unprocessed:
                    warnings.append(f"{len(unprocessed)} unprocessed Claude skills")
                    notes.append(f"Unprocessed skills: {[s.name for s in unprocessed]}")
                
                notes.append(f"Total Claude skills: {len(skills)}")
            else:
                errors.append("Knowledge registry not available")
                status = "failed"
        except Exception as e:
            errors.append(f"Error reviewing Claude skills: {e}")
            status = "failed"
        
        return SystemComponent(
            name="Claude Skills",
            status=status,
            description="Claude skills and tools registry",
            errors=errors,
            warnings=warnings,
            notes=notes,
            last_tested=datetime.now().isoformat()
        )
    
    def _review_bookmark_processing(self) -> SystemComponent:
        """Review bookmark processing status"""
        status = "working"
        errors = []
        warnings = []
        notes = []
        
        try:
            if self.bookmark_agent:
                # Check bookmark agent
                notes.append("Bookmark ingestion agent available")
                
                # Check for bookmark files
                bookmark_files = list(self.project_root.glob("**/*bookmark*.json"))
                bookmark_files.extend(list(self.project_root.glob("**/*bookmark*.md")))
                
                if bookmark_files:
                    notes.append(f"Found {len(bookmark_files)} bookmark files")
                    self.bookmarks_status = {
                        'bookmark_files': [str(f) for f in bookmark_files],
                        'total_files': len(bookmark_files)
                    }
                else:
                    warnings.append("No bookmark files found")
                
                # Check knowledge registry for bookmarks
                if self.knowledge_registry:
                    bookmarks = self.knowledge_registry.bookmarks
                    self.bookmarks_status['registered_bookmarks'] = len(bookmarks)
                    notes.append(f"Registered bookmarks: {len(bookmarks)}")
                    
                    unprocessed = [b for b in bookmarks.values() if b.processing_status.value == 'not_started']
                    if unprocessed:
                        warnings.append(f"{len(unprocessed)} unprocessed bookmarks")
            else:
                errors.append("Bookmark agent not available")
                status = "partial"
        except Exception as e:
            errors.append(f"Error reviewing bookmarks: {e}")
            status = "failed"
        
        return SystemComponent(
            name="Bookmark Processing",
            status=status,
            description="Bookmark ingestion and processing",
            errors=errors,
            warnings=warnings,
            notes=notes,
            last_tested=datetime.now().isoformat()
        )
    
    def _review_knowledge_base(self) -> SystemComponent:
        """Review knowledge base status"""
        status = "working"
        errors = []
        warnings = []
        notes = []
        
        try:
            if self.knowledge_registry:
                summary = self.knowledge_registry.get_summary()
                self.knowledge_base_status = summary
                
                notes.append(f"Total domains: {summary['total_domains']}")
                notes.append(f"Total bookmarks: {summary['total_bookmarks']}")
                notes.append(f"Total git repos: {summary['total_git_repos']}")
                notes.append(f"Total Claude skills: {summary['total_claude_skills']}")
                
                unprocessed = summary['unprocessed']
                if any(unprocessed.values()):
                    warnings.append(f"Unprocessed items: {unprocessed}")
                
                # Check processing queue
                queue = self.knowledge_registry.get_processing_queue()
                if queue:
                    notes.append(f"Processing queue: {len(queue)} items")
                    warnings.append(f"{len(queue)} items in processing queue")
            else:
                errors.append("Knowledge registry not available")
                status = "failed"
        except Exception as e:
            errors.append(f"Error reviewing knowledge base: {e}")
            status = "failed"
        
        return SystemComponent(
            name="Knowledge Base",
            status=status,
            description="Knowledge registry and processing status",
            errors=errors,
            warnings=warnings,
            notes=notes,
            last_tested=datetime.now().isoformat()
        )
    
    def _review_mcp_tools(self) -> SystemComponent:
        """Review MCP tools status"""
        status = "working"
        errors = []
        warnings = []
        notes = []
        
        try:
            if self.mcp_registry:
                tools_info = self.mcp_registry.list_all_tools()
                notes.append(f"Total MCP tools: {tools_info['total_tools']}")
                
                for category, count in tools_info['tools_by_category'].items():
                    notes.append(f"  - {category}: {count} tools")
                
                if tools_info['total_tools'] == 0:
                    warnings.append("No MCP tools registered")
            else:
                errors.append("MCP tool registry not available")
                status = "failed"
        except Exception as e:
            errors.append(f"Error reviewing MCP tools: {e}")
            status = "failed"
        
        return SystemComponent(
            name="MCP Tools",
            status=status,
            description="MCP tool registry and availability",
            errors=errors,
            warnings=warnings,
            notes=notes,
            last_tested=datetime.now().isoformat()
        )
    
    def _review_core_engines(self) -> SystemComponent:
        """Review core engines status"""
        status = "working"
        errors = []
        warnings = []
        notes = []
        
        engines = {
            'gematria': self.gematria_engine,
            'sacred_geometry': self.sacred_geometry_engine,
            'domain_expansion': self.domain_expansion_engine
        }
        
        for name, engine in engines.items():
            if engine:
                notes.append(f"{name} engine: available")
            else:
                warnings.append(f"{name} engine: not available")
        
        return SystemComponent(
            name="Core Engines",
            status=status,
            description="Core calculation and analysis engines",
            errors=errors,
            warnings=warnings,
            notes=notes,
            last_tested=datetime.now().isoformat()
        )
    
    def _review_agents(self) -> SystemComponent:
        """Review agents status"""
        status = "working"
        errors = []
        warnings = []
        notes = []
        
        agents = {
            'claude_integrator': self.claude_agent,
            'enhanced_claude': self.enhanced_claude,
            'bookmark_ingestion': self.bookmark_agent
        }
        
        for name, agent in agents.items():
            if agent:
                notes.append(f"{name} agent: available")
            else:
                warnings.append(f"{name} agent: not available")
        
        return SystemComponent(
            name="Agents",
            status=status,
            description="Agent system status",
            errors=errors,
            warnings=warnings,
            notes=notes,
            last_tested=datetime.now().isoformat()
        )
    
    def _review_workflows(self) -> SystemComponent:
        """Review workflows status"""
        status = "working"
        errors = []
        warnings = []
        notes = []
        
        # Check for workflow scripts
        workflow_scripts = [
            'run_agents.py',
            'run_ingestion_pipeline.py',
            'execute_critical_path.py',
            'run_autonomous.py'
        ]
        
        for script in workflow_scripts:
            script_path = self.project_root / script
            if script_path.exists():
                notes.append(f"{script}: exists")
            else:
                warnings.append(f"{script}: not found")
        
        return SystemComponent(
            name="Workflows",
            status=status,
            description="Workflow scripts and execution",
            errors=errors,
            warnings=warnings,
            notes=notes,
            last_tested=datetime.now().isoformat()
        )
    
    def _review_integrations(self) -> SystemComponent:
        """Review integrations status"""
        status = "working"
        errors = []
        warnings = []
        notes = []
        
        # Check environment variables
        required_env_vars = [
            'SUPABASE_URL',
            'SUPABASE_KEY',
            'ANTHROPIC_API_KEY'
        ]
        
        for var in required_env_vars:
            if os.getenv(var):
                notes.append(f"{var}: set")
            else:
                warnings.append(f"{var}: not set")
        
        return SystemComponent(
            name="Integrations",
            status=status,
            description="External integrations and API keys",
            errors=errors,
            warnings=warnings,
            notes=notes,
            last_tested=datetime.now().isoformat()
        )
    
    def run_system_scripts(self) -> List[ScriptResult]:
        """Run all system scripts and capture results"""
        
        logger.info("=" * 80)
        logger.info("Running System Scripts")
        logger.info("=" * 80)
        
        scripts_to_run = [
            ('registry_cli.py', ['summary']),
            ('run_agents.py', ['--skip-verify']),
        ]
        
        results = []
        
        for script_name, args in scripts_to_run:
            script_path = self.project_root / script_name
            if not script_path.exists():
                results.append(ScriptResult(
                    script_name=script_name,
                    status="skipped",
                    output=f"Script not found: {script_path}"
                ))
                continue
            
            logger.info(f"Running {script_name}...")
            start_time = datetime.now()
            
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)] + args,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(self.project_root)
                )
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                if result.returncode == 0:
                    results.append(ScriptResult(
                        script_name=script_name,
                        status="success",
                        output=result.stdout,
                        execution_time=execution_time
                    ))
                    logger.info(f"✅ {script_name} completed successfully")
                else:
                    results.append(ScriptResult(
                        script_name=script_name,
                        status="failed",
                        output=result.stdout,
                        errors=[result.stderr] if result.stderr else [],
                        execution_time=execution_time
                    ))
                    logger.warning(f"⚠️ {script_name} failed")
            except subprocess.TimeoutExpired:
                results.append(ScriptResult(
                    script_name=script_name,
                    status="failed",
                    errors=["Script timeout"],
                    execution_time=60.0
                ))
                logger.error(f"❌ {script_name} timed out")
            except Exception as e:
                results.append(ScriptResult(
                    script_name=script_name,
                    status="failed",
                    errors=[str(e)]
                ))
                logger.error(f"❌ {script_name} error: {e}")
        
        self.script_results = results
        logger.info(f"✅ Ran {len(results)} scripts")
        return results
    
    def analyze_with_claude_and_grok(self) -> Dict[str, Any]:
        """Analyze system status using Claude and Grok together"""
        
        logger.info("=" * 80)
        logger.info("Analyzing with Claude and Grok")
        logger.info("=" * 80)
        
        # Build comprehensive prompt
        prompt = self._build_analysis_prompt()
        
        # Use Claude for analysis
        claude_analysis = None
        if self.claude_agent:
            try:
                logger.info("Using Claude for analysis...")
                claude_analysis = self.claude_agent.analyze_with_claude(
                    query=prompt,
                    context={
                        'components': {name: asdict(comp) for name, comp in self.components.items()},
                        'script_results': [asdict(r) for r in self.script_results],
                        'claude_skills': self.claude_skills_status,
                        'bookmarks': self.bookmarks_status,
                        'knowledge_base': self.knowledge_base_status
                    },
                    apply_first_principles=True
                )
                logger.info("✅ Claude analysis complete")
            except Exception as e:
                logger.error(f"Claude analysis error: {e}")
        
        # Use Grok for additional insights (via MCP if available)
        grok_analysis = None
        if self.mcp_registry:
            try:
                grok_tool = self.mcp_registry.get_tool("grok_cultural_reasoning")
                if grok_tool:
                    logger.info("Using Grok for cultural reasoning insights...")
                    grok_analysis = self.mcp_registry.execute_tool(
                        "grok_cultural_reasoning",
                        text=prompt[:5000],  # Limit text length
                        context={'task': 'system_review', 'source': 'comprehensive_review'}
                    )
                    logger.info("✅ Grok analysis complete")
            except Exception as e:
                logger.warning(f"Grok analysis not available: {e}")
        
        return {
            'claude_analysis': claude_analysis,
            'grok_analysis': grok_analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    def _build_analysis_prompt(self) -> str:
        """Build comprehensive analysis prompt"""
        
        prompt_parts = []
        prompt_parts.append("# Comprehensive System Review Analysis")
        prompt_parts.append("")
        prompt_parts.append("## System Components Status")
        prompt_parts.append("")
        
        for name, component in self.components.items():
            prompt_parts.append(f"### {component.name}")
            prompt_parts.append(f"- Status: {component.status}")
            prompt_parts.append(f"- Description: {component.description}")
            if component.errors:
                prompt_parts.append(f"- Errors: {component.errors}")
            if component.warnings:
                prompt_parts.append(f"- Warnings: {component.warnings}")
            if component.notes:
                prompt_parts.append(f"- Notes: {component.notes}")
            prompt_parts.append("")
        
        prompt_parts.append("## Script Execution Results")
        prompt_parts.append("")
        for result in self.script_results:
            prompt_parts.append(f"### {result.script_name}")
            prompt_parts.append(f"- Status: {result.status}")
            if result.errors:
                prompt_parts.append(f"- Errors: {result.errors}")
            prompt_parts.append("")
        
        prompt_parts.append("## Analysis Request")
        prompt_parts.append("")
        prompt_parts.append("Please provide:")
        prompt_parts.append("1. Overall system health assessment")
        prompt_parts.append("2. Critical issues that need immediate attention")
        prompt_parts.append("3. Recommendations for improvements")
        prompt_parts.append("4. Priority action items")
        prompt_parts.append("5. Unifying guidance for next steps")
        
        return "\n".join(prompt_parts)
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive unified report"""
        
        logger.info("=" * 80)
        logger.info("Generating Comprehensive Report")
        logger.info("=" * 80)
        
        # Analyze with Claude and Grok
        analysis = self.analyze_with_claude_and_grok()
        
        # Build report
        report = {
            'timestamp': datetime.now().isoformat(),
            'review_id': f"REVIEW-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'summary': {
                'total_components': len(self.components),
                'working_components': sum(1 for c in self.components.values() if c.status == 'working'),
                'failed_components': sum(1 for c in self.components.values() if c.status == 'failed'),
                'partial_components': sum(1 for c in self.components.values() if c.status == 'partial'),
                'total_scripts_run': len(self.script_results),
                'successful_scripts': sum(1 for r in self.script_results if r.status == 'success'),
                'failed_scripts': sum(1 for r in self.script_results if r.status == 'failed')
            },
            'components': {name: asdict(comp) for name, comp in self.components.items()},
            'script_results': [asdict(r) for r in self.script_results],
            'claude_skills_status': self.claude_skills_status,
            'bookmarks_status': self.bookmarks_status,
            'knowledge_base_status': self.knowledge_base_status,
            'analysis': analysis,
            'findings': self.findings,
            'recommendations': self._generate_recommendations(),
            'action_items': self._generate_action_items()
        }
        
        # Save report
        self._save_report(report)
        
        logger.info("✅ Comprehensive report generated")
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on review"""
        recommendations = []
        
        # Check for failed components
        failed = [name for name, comp in self.components.items() if comp.status == 'failed']
        if failed:
            recommendations.append(f"Fix failed components: {', '.join(failed)}")
        
        # Check for warnings
        warnings = []
        for name, comp in self.components.items():
            if comp.warnings:
                warnings.append(f"{name}: {len(comp.warnings)} warnings")
        if warnings:
            recommendations.append(f"Address warnings in: {', '.join(warnings)}")
        
        # Check for unprocessed items
        if self.knowledge_base_status:
            unprocessed = self.knowledge_base_status.get('unprocessed', {})
            if any(unprocessed.values()):
                recommendations.append(f"Process unprocessed items: {unprocessed}")
        
        # Check for missing integrations
        integrations = self.components.get('integrations')
        if integrations and integrations.warnings:
            recommendations.append("Set up missing environment variables")
        
        return recommendations
    
    def _generate_action_items(self) -> List[Dict[str, Any]]:
        """Generate prioritized action items"""
        action_items = []
        
        # Critical: Failed components
        for name, comp in self.components.items():
            if comp.status == 'failed':
                action_items.append({
                    'priority': 'critical',
                    'component': name,
                    'action': f"Fix {comp.name}",
                    'description': comp.description,
                    'errors': comp.errors
                })
        
        # High: Warnings
        for name, comp in self.components.items():
            if comp.warnings:
                action_items.append({
                    'priority': 'high',
                    'component': name,
                    'action': f"Address warnings in {comp.name}",
                    'warnings': comp.warnings
                })
        
        # Medium: Unprocessed items
        if self.knowledge_base_status:
            unprocessed = self.knowledge_base_status.get('unprocessed', {})
            for item_type, count in unprocessed.items():
                if count > 0:
                    action_items.append({
                        'priority': 'medium',
                        'component': 'knowledge_base',
                        'action': f"Process {count} unprocessed {item_type}",
                        'count': count
                    })
        
        return action_items
    
    def _save_report(self, report: Dict[str, Any]):
        """Save comprehensive report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.storage_path / f"comprehensive_review_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Also generate markdown report
        md_file = self.storage_path / f"comprehensive_review_{timestamp}.md"
        self._generate_markdown_report(report, md_file)
        
        logger.info(f"Report saved to: {report_file}")
        logger.info(f"Markdown report saved to: {md_file}")
    
    def _generate_markdown_report(self, report: Dict[str, Any], output_file: Path):
        """Generate markdown report"""
        lines = []
        lines.append("# Comprehensive System Review Report")
        lines.append("")
        lines.append(f"**Generated:** {report['timestamp']}")
        lines.append(f"**Review ID:** {report['review_id']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Executive Summary")
        lines.append("")
        summary = report['summary']
        lines.append(f"- **Total Components:** {summary['total_components']}")
        lines.append(f"- **Working Components:** {summary['working_components']}")
        lines.append(f"- **Failed Components:** {summary['failed_components']}")
        lines.append(f"- **Partial Components:** {summary['partial_components']}")
        lines.append(f"- **Scripts Run:** {summary['total_scripts_run']}")
        lines.append(f"- **Successful Scripts:** {summary['successful_scripts']}")
        lines.append(f"- **Failed Scripts:** {summary['failed_scripts']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Component Status")
        lines.append("")
        for name, comp in report['components'].items():
            lines.append(f"### {comp['name']}")
            lines.append(f"- **Status:** {comp['status']}")
            lines.append(f"- **Description:** {comp['description']}")
            if comp['errors']:
                lines.append(f"- **Errors:** {len(comp['errors'])}")
                for error in comp['errors']:
                    lines.append(f"  - {error}")
            if comp['warnings']:
                lines.append(f"- **Warnings:** {len(comp['warnings'])}")
                for warning in comp['warnings']:
                    lines.append(f"  - {warning}")
            if comp['notes']:
                lines.append(f"- **Notes:**")
                for note in comp['notes']:
                    lines.append(f"  - {note}")
            lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Recommendations")
        lines.append("")
        for rec in report['recommendations']:
            lines.append(f"- {rec}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Action Items")
        lines.append("")
        for item in report['action_items']:
            lines.append(f"### {item['priority'].upper()}: {item['action']}")
            lines.append(f"- **Component:** {item['component']}")
            if 'description' in item:
                lines.append(f"- **Description:** {item['description']}")
            lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Claude Skills Status")
        lines.append("")
        if report['claude_skills_status']:
            lines.append(f"- **Total Skills:** {report['claude_skills_status'].get('total_skills', 0)}")
            for name, skill in report['claude_skills_status'].get('skills', {}).items():
                lines.append(f"  - {skill['name']}: {skill['status']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Bookmarks Status")
        lines.append("")
        if report['bookmarks_status']:
            lines.append(f"- **Total Files:** {report['bookmarks_status'].get('total_files', 0)}")
            lines.append(f"- **Registered Bookmarks:** {report['bookmarks_status'].get('registered_bookmarks', 0)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Knowledge Base Status")
        lines.append("")
        if report['knowledge_base_status']:
            kb = report['knowledge_base_status']
            lines.append(f"- **Total Domains:** {kb.get('total_domains', 0)}")
            lines.append(f"- **Total Bookmarks:** {kb.get('total_bookmarks', 0)}")
            lines.append(f"- **Total Git Repos:** {kb.get('total_git_repos', 0)}")
            lines.append(f"- **Total Claude Skills:** {kb.get('total_claude_skills', 0)}")
        lines.append("")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def run_comprehensive_review(self) -> Dict[str, Any]:
        """Run complete comprehensive review"""
        
        logger.info("=" * 80)
        logger.info("COMPREHENSIVE SYSTEM REVIEW")
        logger.info("=" * 80)
        
        # 1. Review all components
        components = self.review_all_components()
        
        # 2. Run system scripts
        script_results = self.run_system_scripts()
        
        # 3. Generate comprehensive report
        report = self.generate_comprehensive_report()
        
        logger.info("=" * 80)
        logger.info("✅ COMPREHENSIVE SYSTEM REVIEW COMPLETE")
        logger.info("=" * 80)
        
        return report


def main():
    """Main function"""
    
    logger.info("=" * 80)
    logger.info("Comprehensive System Review")
    logger.info("=" * 80)
    
    review = ComprehensiveSystemReview()
    report = review.run_comprehensive_review()
    
    # Print summary
    print("\n" + "=" * 80)
    print("REVIEW SUMMARY")
    print("=" * 80)
    summary = report['summary']
    print(f"Total Components: {summary['total_components']}")
    print(f"Working: {summary['working_components']}")
    print(f"Failed: {summary['failed_components']}")
    print(f"Partial: {summary['partial_components']}")
    print(f"\nScripts Run: {summary['total_scripts_run']}")
    print(f"Successful: {summary['successful_scripts']}")
    print(f"Failed: {summary['failed_scripts']}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    for rec in report['recommendations']:
        print(f"- {rec}")
    
    print("\n" + "=" * 80)
    print("ACTION ITEMS")
    print("=" * 80)
    for item in report['action_items']:
        print(f"[{item['priority'].upper()}] {item['action']}")
    
    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE REVIEW COMPLETE")
    print("=" * 80)
    print(f"\nReport saved to: {review.storage_path}")


if __name__ == "__main__":
    main()
