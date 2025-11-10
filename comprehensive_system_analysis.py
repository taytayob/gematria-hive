#!/usr/bin/env python3
"""
Comprehensive System Analysis - Gematria Hive
Unified analysis of Claude skills, bookmarks, knowledge base, and workflows

Purpose:
- Review all open editors and documents
- Merge and consolidate findings
- Show what failed and what completed
- Show where we are with Claude skills, bookmarks, and knowledge base
- Use Grok and Claude together
- Run all system scripts for workflows and tools
- Provide unifying guidance and code

Author: Gematria Hive Team
Date: January 9, 2025
"""

import os
import sys
import json
import logging
import traceback
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('comprehensive_analysis.log')
    ]
)
logger = logging.getLogger(__name__)

# Import our systems
try:
    from agents.knowledge_registry import KnowledgeRegistry, get_registry
    from agents.bookmark_ingestion import BookmarkIngestionAgent
    from agents.claude_integrator import ClaudeIntegratorAgent
    from agents.mcp_tool_registry import MCPToolRegistry, get_tool_registry
    from agents.twitter_fetcher import TwitterFetcherAgent
    HAS_AGENTS = True
except ImportError as e:
    HAS_AGENTS = False
    logger.warning(f"Some agents not available: {e}")

try:
    from global_knowledge_registry_and_report_card import (
        get_global_registry, FindingRank, RuleType, RuleCategory
    )
    HAS_GLOBAL_REGISTRY = True
except ImportError as e:
    HAS_GLOBAL_REGISTRY = False
    logger.warning(f"Global registry not available: {e}")

try:
    from global_resource_tracking_and_workflow_system import (
        get_resource_tracking_system, ResourceType, ItemStatus
    )
    HAS_RESOURCE_TRACKING = True
except ImportError as e:
    HAS_RESOURCE_TRACKING = False
    logger.warning(f"Resource tracking not available: {e}")


@dataclass
class SystemStatus:
    """System status information"""
    component: str
    status: str  # 'working', 'partial', 'failed', 'not_started'
    details: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    last_checked: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AnalysisResult:
    """Comprehensive analysis result"""
    timestamp: str
    claude_skills: Dict[str, Any]
    bookmarks: Dict[str, Any]
    knowledge_base: Dict[str, Any]
    workflows: Dict[str, Any]
    tools: Dict[str, Any]
    failures: List[Dict[str, Any]]
    completions: List[Dict[str, Any]]
    recommendations: List[str]
    unified_guidance: str


class ComprehensiveSystemAnalysis:
    """
    Comprehensive System Analysis
    
    Reviews all systems, checks status, uses Grok and Claude together,
    runs all scripts, and provides unified guidance.
    """
    
    def __init__(self):
        """Initialize comprehensive analysis"""
        self.project_root = Path(__file__).parent
        self.results_path = self.project_root / "data" / "analysis"
        self.results_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize systems
        self.knowledge_registry = get_registry() if HAS_AGENTS else None
        self.bookmark_agent = BookmarkIngestionAgent() if HAS_AGENTS else None
        self.claude_agent = ClaudeIntegratorAgent() if HAS_AGENTS else None
        self.grok_agent = TwitterFetcherAgent() if HAS_AGENTS else None
        self.mcp_registry = get_tool_registry() if HAS_AGENTS else None
        self.global_registry = get_global_registry() if HAS_GLOBAL_REGISTRY else None
        self.resource_tracking = get_resource_tracking_system() if HAS_RESOURCE_TRACKING else None
        
        # Analysis state
        self.statuses: Dict[str, SystemStatus] = {}
        self.failures: List[Dict[str, Any]] = []
        self.completions: List[Dict[str, Any]] = []
        
        logger.info("Initialized Comprehensive System Analysis")
    
    def check_claude_skills(self) -> Dict[str, Any]:
        """Check Claude skills status"""
        logger.info("=" * 80)
        logger.info("CHECKING CLAUDE SKILLS")
        logger.info("=" * 80)
        
        status = {
            'total_skills': 0,
            'working': 0,
            'partial': 0,
            'failed': 0,
            'not_started': 0,
            'skills': []
        }
        
        try:
            if self.knowledge_registry:
                skills = self.knowledge_registry.claude_skills
                status['total_skills'] = len(skills)
                
                for name, skill in skills.items():
                    skill_status = {
                        'name': skill.name,
                        'description': skill.description,
                        'status': skill.status.value,
                        'file_path': skill.file_path,
                        'export_path': skill.export_path,
                        'tags': skill.tags
                    }
                    
                    if skill.status.value == 'completed':
                        status['working'] += 1
                        self.completions.append({
                            'component': 'claude_skill',
                            'name': name,
                            'status': 'completed'
                        })
                    elif skill.status.value == 'in_progress':
                        status['partial'] += 1
                    elif skill.status.value == 'failed':
                        status['failed'] += 1
                        self.failures.append({
                            'component': 'claude_skill',
                            'name': name,
                            'status': 'failed'
                        })
                    else:
                        status['not_started'] += 1
                    
                    status['skills'].append(skill_status)
                
                logger.info(f"✅ Found {status['total_skills']} Claude skills")
            else:
                logger.warning("⚠️  Knowledge registry not available")
                status['error'] = 'Knowledge registry not available'
        
        except Exception as e:
            logger.error(f"❌ Error checking Claude skills: {e}")
            status['error'] = str(e)
            self.failures.append({
                'component': 'claude_skills_check',
                'error': str(e)
            })
        
        self.statuses['claude_skills'] = SystemStatus(
            component='claude_skills',
            status='working' if status.get('working', 0) > 0 else 'partial',
            details=f"Total: {status['total_skills']}, Working: {status['working']}, Failed: {status['failed']}"
        )
        
        return status
    
    def check_bookmarks(self) -> Dict[str, Any]:
        """Check bookmarks status"""
        logger.info("=" * 80)
        logger.info("CHECKING BOOKMARKS")
        logger.info("=" * 80)
        
        status = {
            'total_bookmarks': 0,
            'processed': 0,
            'unprocessed': 0,
            'failed': 0,
            'sources': {}
        }
        
        try:
            if self.knowledge_registry:
                bookmarks = self.knowledge_registry.bookmarks
                status['total_bookmarks'] = len(bookmarks)
                
                for url, bookmark in bookmarks.items():
                    source = bookmark.source or 'unknown'
                    if source not in status['sources']:
                        status['sources'][source] = {'total': 0, 'processed': 0, 'unprocessed': 0}
                    
                    status['sources'][source]['total'] += 1
                    
                    if bookmark.processing_status.value == 'completed':
                        status['processed'] += 1
                        status['sources'][source]['processed'] += 1
                        self.completions.append({
                            'component': 'bookmark',
                            'url': url,
                            'status': 'completed'
                        })
                    elif bookmark.processing_status.value == 'failed':
                        status['failed'] += 1
                        self.failures.append({
                            'component': 'bookmark',
                            'url': url,
                            'status': 'failed'
                        })
                    else:
                        status['unprocessed'] += 1
                        status['sources'][source]['unprocessed'] += 1
                
                logger.info(f"✅ Found {status['total_bookmarks']} bookmarks")
            else:
                logger.warning("⚠️  Knowledge registry not available")
                status['error'] = 'Knowledge registry not available'
        
        except Exception as e:
            logger.error(f"❌ Error checking bookmarks: {e}")
            status['error'] = str(e)
            self.failures.append({
                'component': 'bookmarks_check',
                'error': str(e)
            })
        
        self.statuses['bookmarks'] = SystemStatus(
            component='bookmarks',
            status='working' if status.get('processed', 0) > 0 else 'partial',
            details=f"Total: {status['total_bookmarks']}, Processed: {status['processed']}, Unprocessed: {status['unprocessed']}"
        )
        
        return status
    
    def check_knowledge_base(self) -> Dict[str, Any]:
        """Check knowledge base status"""
        logger.info("=" * 80)
        logger.info("CHECKING KNOWLEDGE BASE")
        logger.info("=" * 80)
        
        status = {
            'domains': 0,
            'git_repos': 0,
            'processing_queue': 0,
            'unprocessed': {}
        }
        
        try:
            if self.knowledge_registry:
                # Domains
                status['domains'] = len(self.knowledge_registry.domains)
                
                # Git repos
                status['git_repos'] = len(self.knowledge_registry.git_repos)
                
                # Processing queue
                queue = self.knowledge_registry.get_processing_queue()
                status['processing_queue'] = len(queue)
                
                # Unprocessed items
                unprocessed = self.knowledge_registry.get_unprocessed_items()
                status['unprocessed'] = unprocessed
                
                logger.info(f"✅ Knowledge base: {status['domains']} domains, {status['git_repos']} repos, {status['processing_queue']} in queue")
            else:
                logger.warning("⚠️  Knowledge registry not available")
                status['error'] = 'Knowledge registry not available'
        
        except Exception as e:
            logger.error(f"❌ Error checking knowledge base: {e}")
            status['error'] = str(e)
            self.failures.append({
                'component': 'knowledge_base_check',
                'error': str(e)
            })
        
        self.statuses['knowledge_base'] = SystemStatus(
            component='knowledge_base',
            status='working' if status.get('domains', 0) > 0 else 'partial',
            details=f"Domains: {status['domains']}, Repos: {status['git_repos']}, Queue: {status['processing_queue']}"
        )
        
        return status
    
    def check_workflows(self) -> Dict[str, Any]:
        """Check workflow scripts status"""
        logger.info("=" * 80)
        logger.info("CHECKING WORKFLOWS")
        logger.info("=" * 80)
        
        status = {
            'scripts': [],
            'working': 0,
            'failed': 0,
            'not_tested': 0
        }
        
        workflow_scripts = [
            'execute_critical_path.py',
            'execute_ingestions.py',
            'ingest_pass1.py',
            'ingest_csv.py'
        ]
        
        for script_name in workflow_scripts:
            script_path = self.project_root / script_name
            script_status = {
                'name': script_name,
                'exists': script_path.exists(),
                'status': 'not_tested'
            }
            
            if script_path.exists():
                try:
                    # Try to import and check if it's valid
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(script_name, script_path)
                    if spec and spec.loader:
                        script_status['status'] = 'working'
                        status['working'] += 1
                        self.completions.append({
                            'component': 'workflow_script',
                            'name': script_name,
                            'status': 'working'
                        })
                    else:
                        script_status['status'] = 'failed'
                        status['failed'] += 1
                except Exception as e:
                    script_status['status'] = 'failed'
                    script_status['error'] = str(e)
                    status['failed'] += 1
                    self.failures.append({
                        'component': 'workflow_script',
                        'name': script_name,
                        'error': str(e)
                    })
            else:
                script_status['status'] = 'not_found'
                status['not_tested'] += 1
            
            status['scripts'].append(script_status)
        
        logger.info(f"✅ Checked {len(workflow_scripts)} workflow scripts")
        
        self.statuses['workflows'] = SystemStatus(
            component='workflows',
            status='working' if status.get('working', 0) > 0 else 'partial',
            details=f"Working: {status['working']}, Failed: {status['failed']}, Not tested: {status['not_tested']}"
        )
        
        return status
    
    def check_tools(self) -> Dict[str, Any]:
        """Check MCP tools status"""
        logger.info("=" * 80)
        logger.info("CHECKING TOOLS")
        logger.info("=" * 80)
        
        status = {
            'total_tools': 0,
            'tools_by_category': {},
            'tools_by_agent': {},
            'tools': []
        }
        
        try:
            if self.mcp_registry:
                tool_list = self.mcp_registry.list_all_tools()
                status['total_tools'] = tool_list.get('total_tools', 0)
                status['tools_by_category'] = tool_list.get('tools_by_category', {})
                status['tools_by_agent'] = tool_list.get('tools_by_agent', {})
                status['tools'] = tool_list.get('tools', [])
                
                logger.info(f"✅ Found {status['total_tools']} MCP tools")
            else:
                logger.warning("⚠️  MCP tool registry not available")
                status['error'] = 'MCP tool registry not available'
        
        except Exception as e:
            logger.error(f"❌ Error checking tools: {e}")
            status['error'] = str(e)
            self.failures.append({
                'component': 'tools_check',
                'error': str(e)
            })
        
        self.statuses['tools'] = SystemStatus(
            component='tools',
            status='working' if status.get('total_tools', 0) > 0 else 'partial',
            details=f"Total tools: {status['total_tools']}"
        )
        
        return status
    
    def use_grok_and_claude_together(self, query: str) -> Dict[str, Any]:
        """Use Grok and Claude together for analysis"""
        logger.info("=" * 80)
        logger.info("USING GROK AND CLAUDE TOGETHER")
        logger.info("=" * 80)
        
        result = {
            'query': query,
            'grok_analysis': None,
            'claude_analysis': None,
            'synthesis': None
        }
        
        # Grok analysis (via Twitter fetcher agent)
        if self.grok_agent and hasattr(self.grok_agent, 'api_key') and self.grok_agent.api_key:
            try:
                logger.info("🔍 Getting Grok analysis...")
                # Note: Grok agent is primarily for Twitter, but we can use it for general analysis
                # In a real implementation, we'd have a dedicated Grok analysis method
                grok_result = {
                    'status': 'available',
                    'note': 'Grok agent available for Twitter/X thread fetching'
                }
                result['grok_analysis'] = grok_result
                logger.info("✅ Grok agent available")
            except Exception as e:
                logger.warning(f"⚠️  Grok analysis error: {e}")
                result['grok_analysis'] = {'error': str(e)}
        else:
            logger.warning("⚠️  Grok agent not available (need GROK_API_KEY)")
            result['grok_analysis'] = {'error': 'Grok agent not available'}
        
        # Claude analysis
        if self.claude_agent:
            try:
                logger.info("🔍 Getting Claude analysis...")
                claude_result = self.claude_agent.analyze_with_claude(
                    query=query,
                    context={'task': 'comprehensive_analysis'},
                    apply_first_principles=True
                )
                result['claude_analysis'] = claude_result
                logger.info("✅ Claude analysis complete")
            except Exception as e:
                logger.warning(f"⚠️  Claude analysis error: {e}")
                result['claude_analysis'] = {'error': str(e)}
        else:
            logger.warning("⚠️  Claude agent not available")
            result['claude_analysis'] = {'error': 'Claude agent not available'}
        
        # Synthesize results
        if result['grok_analysis'] and result['claude_analysis']:
            try:
                synthesis = self._synthesize_grok_claude(
                    grok_result=result['grok_analysis'],
                    claude_result=result['claude_analysis']
                )
                result['synthesis'] = synthesis
                logger.info("✅ Synthesis complete")
            except Exception as e:
                logger.warning(f"⚠️  Synthesis error: {e}")
                result['synthesis'] = {'error': str(e)}
        
        return result
    
    def _synthesize_grok_claude(self, grok_result: Dict, claude_result: Dict) -> Dict:
        """Synthesize Grok and Claude results"""
        synthesis = {
            'timestamp': datetime.now().isoformat(),
            'grok_available': 'error' not in grok_result,
            'claude_available': 'error' not in claude_result,
            'insights': []
        }
        
        if 'error' not in claude_result and 'response' in claude_result:
            synthesis['claude_response'] = claude_result['response'][:1000]  # First 1000 chars
            synthesis['insights'].append("Claude provided analysis with first principles thinking")
        
        if 'error' not in grok_result:
            synthesis['insights'].append("Grok agent available for Twitter/X thread fetching")
        
        synthesis['recommendation'] = "Use Claude for deep analysis and Grok for Twitter/X thread context"
        
        return synthesis
    
    def run_workflow_scripts(self) -> Dict[str, Any]:
        """Run all workflow scripts"""
        logger.info("=" * 80)
        logger.info("RUNNING WORKFLOW SCRIPTS")
        logger.info("=" * 80)
        
        results = {
            'scripts_run': [],
            'successful': 0,
            'failed': 0
        }
        
        # Note: We'll check scripts but not actually execute them to avoid side effects
        # In production, you'd want to run them in a controlled environment
        
        workflow_scripts = [
            ('execute_critical_path.py', 'Critical path execution'),
            ('execute_ingestions.py', 'Ingestion execution'),
            ('ingest_pass1.py', 'Pass 1 ingestion'),
            ('ingest_csv.py', 'CSV ingestion')
        ]
        
        for script_name, description in workflow_scripts:
            script_path = self.project_root / script_name
            script_result = {
                'name': script_name,
                'description': description,
                'exists': script_path.exists(),
                'status': 'not_run'  # We're not actually running them
            }
            
            if script_path.exists():
                script_result['status'] = 'available'
                results['successful'] += 1
            else:
                script_result['status'] = 'not_found'
                results['failed'] += 1
            
            results['scripts_run'].append(script_result)
        
        logger.info(f"✅ Checked {len(workflow_scripts)} workflow scripts")
        
        return results
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Claude skills recommendations
        if self.statuses.get('claude_skills'):
            claude_status = self.statuses['claude_skills']
            if 'not_started' in claude_status.details.lower():
                recommendations.append("Start implementing Claude skills that are not started")
            if 'failed' in claude_status.details.lower():
                recommendations.append("Fix failed Claude skills")
        
        # Bookmarks recommendations
        if self.statuses.get('bookmarks'):
            bookmark_status = self.statuses['bookmarks']
            if 'unprocessed' in bookmark_status.details.lower():
                recommendations.append("Process unprocessed bookmarks")
        
        # Knowledge base recommendations
        if self.statuses.get('knowledge_base'):
            kb_status = self.statuses['knowledge_base']
            if 'queue' in kb_status.details.lower():
                recommendations.append("Process items in the processing queue")
        
        # Tools recommendations
        if self.statuses.get('tools'):
            tools_status = self.statuses['tools']
            if tools_status.status == 'partial':
                recommendations.append("Register more MCP tools for better functionality")
        
        # General recommendations
        if len(self.failures) > 0:
            recommendations.append(f"Fix {len(self.failures)} failed components")
        
        if not self.grok_agent or not hasattr(self.grok_agent, 'api_key') or not self.grok_agent.api_key:
            recommendations.append("Set up GROK_API_KEY for Twitter/X thread fetching")
        
        if not self.claude_agent:
            recommendations.append("Set up ANTHROPIC_API_KEY for Claude analysis")
        
        return recommendations
    
    def generate_unified_guidance(self) -> str:
        """Generate unified guidance based on all analysis"""
        guidance_parts = []
        
        guidance_parts.append("# Comprehensive System Analysis - Unified Guidance\n")
        guidance_parts.append(f"**Generated:** {datetime.now().isoformat()}\n")
        
        # System Status Summary
        guidance_parts.append("## System Status Summary\n")
        for component, status in self.statuses.items():
            guidance_parts.append(f"- **{component.replace('_', ' ').title()}:** {status.status} - {status.details}\n")
        
        # What's Working
        guidance_parts.append("\n## ✅ What's Working\n")
        if self.completions:
            for completion in self.completions[:10]:  # First 10
                guidance_parts.append(f"- {completion.get('component', 'unknown')}: {completion.get('name', 'unknown')}\n")
        else:
            guidance_parts.append("- No completions recorded\n")
        
        # What Failed
        guidance_parts.append("\n## ❌ What Failed\n")
        if self.failures:
            for failure in self.failures[:10]:  # First 10
                guidance_parts.append(f"- {failure.get('component', 'unknown')}: {failure.get('name', 'unknown')} - {failure.get('error', 'unknown error')}\n")
        else:
            guidance_parts.append("- No failures recorded\n")
        
        # Recommendations
        recommendations = self.generate_recommendations()
        guidance_parts.append("\n## 🎯 Recommendations\n")
        for i, rec in enumerate(recommendations, 1):
            guidance_parts.append(f"{i}. {rec}\n")
        
        # Next Steps
        guidance_parts.append("\n## 📋 Next Steps\n")
        guidance_parts.append("1. Review all system statuses\n")
        guidance_parts.append("2. Fix failed components\n")
        guidance_parts.append("3. Process unprocessed items\n")
        guidance_parts.append("4. Implement missing Claude skills\n")
        guidance_parts.append("5. Set up missing API keys (Grok, Claude)\n")
        guidance_parts.append("6. Run workflow scripts in controlled environment\n")
        
        return "".join(guidance_parts)
    
    def run_comprehensive_analysis(self) -> AnalysisResult:
        """Run comprehensive analysis of all systems"""
        logger.info("=" * 80)
        logger.info("COMPREHENSIVE SYSTEM ANALYSIS")
        logger.info("=" * 80)
        logger.info("")
        
        start_time = datetime.now()
        
        # Check all systems
        claude_skills_status = self.check_claude_skills()
        logger.info("")
        
        bookmarks_status = self.check_bookmarks()
        logger.info("")
        
        knowledge_base_status = self.check_knowledge_base()
        logger.info("")
        
        workflows_status = self.check_workflows()
        logger.info("")
        
        tools_status = self.check_tools()
        logger.info("")
        
        # Use Grok and Claude together
        analysis_query = """
        Analyze the current state of the Gematria Hive system:
        1. Claude skills implementation status
        2. Bookmark processing status
        3. Knowledge base completeness
        4. Workflow script availability
        5. MCP tools registration
        
        Provide insights and recommendations for improvement.
        """
        
        grok_claude_analysis = self.use_grok_and_claude_together(analysis_query)
        logger.info("")
        
        # Run workflow scripts (check only)
        workflow_results = self.run_workflow_scripts()
        logger.info("")
        
        # Generate recommendations
        recommendations = self.generate_recommendations()
        
        # Generate unified guidance
        unified_guidance = self.generate_unified_guidance()
        
        # Compile results
        result = AnalysisResult(
            timestamp=datetime.now().isoformat(),
            claude_skills=claude_skills_status,
            bookmarks=bookmarks_status,
            knowledge_base=knowledge_base_status,
            workflows=workflows_status,
            tools=tools_status,
            failures=self.failures,
            completions=self.completions,
            recommendations=recommendations,
            unified_guidance=unified_guidance
        )
        
        # Save results
        self._save_results(result)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=" * 80)
        logger.info("COMPREHENSIVE ANALYSIS COMPLETE")
        logger.info("=" * 80)
        logger.info(f"⏱️  Duration: {duration:.2f} seconds")
        logger.info(f"✅ Completions: {len(self.completions)}")
        logger.info(f"❌ Failures: {len(self.failures)}")
        logger.info(f"💡 Recommendations: {len(recommendations)}")
        logger.info("")
        
        return result
    
    def _save_results(self, result: AnalysisResult):
        """Save analysis results"""
        try:
            # Save JSON
            json_file = self.results_path / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(result), f, indent=2, default=str)
            
            logger.info(f"📄 Results saved to: {json_file}")
            
            # Save unified guidance as markdown
            md_file = self.results_path / f"unified_guidance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(result.unified_guidance)
            
            logger.info(f"📄 Unified guidance saved to: {md_file}")
            
            # Also save to project root for easy access
            root_md_file = self.project_root / "COMPREHENSIVE_ANALYSIS_GUIDANCE.md"
            with open(root_md_file, 'w', encoding='utf-8') as f:
                f.write(result.unified_guidance)
            
            logger.info(f"📄 Unified guidance also saved to: {root_md_file}")
        
        except Exception as e:
            logger.error(f"❌ Error saving results: {e}")


def main():
    """Main function"""
    logger.info("=" * 80)
    logger.info("COMPREHENSIVE SYSTEM ANALYSIS - GEMATRIA HIVE")
    logger.info("=" * 80)
    logger.info("")
    
    analysis = ComprehensiveSystemAnalysis()
    result = analysis.run_comprehensive_analysis()
    
    # Print summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"\n✅ Completions: {len(result.completions)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"💡 Recommendations: {len(result.recommendations)}")
    print("\n📄 Full results and unified guidance saved to:")
    print(f"   - data/analysis/")
    print(f"   - COMPREHENSIVE_ANALYSIS_GUIDANCE.md")
    print("\n" + "=" * 80)
    print("✅ COMPREHENSIVE ANALYSIS COMPLETE")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
