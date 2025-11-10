#!/usr/bin/env python3
"""
Comprehensive System Review and Consolidation
Gematria Hive - Complete system review using Claude and Grok together

Purpose:
- Review all open editors and documents
- Test all systems, workflows, and tools
- Use Grok and Claude together for analysis
- Identify what failed and what completed
- Show current status of Claude skills, bookmarks, and knowledge base
- Provide unifying guidance and code

Author: Gematria Hive Team
Date: January 9, 2025
"""

import os
import json
import logging
import sys
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

from dotenv import load_dotenv
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import all systems
SYSTEMS = {}
ERRORS = {}
WARNINGS = {}

try:
    from agents.knowledge_registry import KnowledgeRegistry, get_registry
    SYSTEMS['knowledge_registry'] = get_registry()
    logger.info("✅ Knowledge Registry loaded")
except Exception as e:
    ERRORS['knowledge_registry'] = str(e)
    logger.error(f"❌ Knowledge Registry failed: {e}")

try:
    from agents.bookmark_ingestion import BookmarkIngestionAgent
    SYSTEMS['bookmark_agent'] = BookmarkIngestionAgent()
    logger.info("✅ Bookmark Ingestion Agent loaded")
except Exception as e:
    ERRORS['bookmark_agent'] = str(e)
    logger.error(f"❌ Bookmark Ingestion Agent failed: {e}")

try:
    from agents.claude_integrator import ClaudeIntegratorAgent
    SYSTEMS['claude_agent'] = ClaudeIntegratorAgent()
    logger.info("✅ Claude Integrator Agent loaded")
except Exception as e:
    ERRORS['claude_agent'] = str(e)
    logger.error(f"❌ Claude Integrator Agent failed: {e}")

try:
    from agents.mcp_tool_registry import MCPToolRegistry, get_tool_registry
    SYSTEMS['mcp_registry'] = get_tool_registry()
    logger.info("✅ MCP Tool Registry loaded")
except Exception as e:
    ERRORS['mcp_registry'] = str(e)
    logger.error(f"❌ MCP Tool Registry failed: {e}")

try:
    from agents.twitter_fetcher import TwitterFetcherAgent
    SYSTEMS['grok_agent'] = TwitterFetcherAgent()
    logger.info("✅ Grok/Twitter Agent loaded")
except Exception as e:
    ERRORS['grok_agent'] = str(e)
    logger.error(f"❌ Grok/Twitter Agent failed: {e}")

try:
    from core.gematria_engine import get_gematria_engine
    SYSTEMS['gematria_engine'] = get_gematria_engine()
    logger.info("✅ Gematria Engine loaded")
except Exception as e:
    ERRORS['gematria_engine'] = str(e)
    logger.error(f"❌ Gematria Engine failed: {e}")

try:
    from core.sacred_geometry_engine import get_sacred_geometry_engine
    SYSTEMS['sacred_geometry_engine'] = get_sacred_geometry_engine()
    logger.info("✅ Sacred Geometry Engine loaded")
except Exception as e:
    ERRORS['sacred_geometry_engine'] = str(e)
    logger.error(f"❌ Sacred Geometry Engine failed: {e}")

try:
    from core.domain_expansion_engine import get_domain_expansion_engine
    SYSTEMS['domain_expansion_engine'] = get_domain_expansion_engine()
    logger.info("✅ Domain Expansion Engine loaded")
except Exception as e:
    ERRORS['domain_expansion_engine'] = str(e)
    logger.error(f"❌ Domain Expansion Engine failed: {e}")

# Try to load enhanced Claude integrator
try:
    from agents.enhanced_claude_integrator import EnhancedClaudeIntegrator
    SYSTEMS['enhanced_claude'] = EnhancedClaudeIntegrator()
    logger.info("✅ Enhanced Claude Integrator loaded")
except Exception as e:
    WARNINGS['enhanced_claude'] = str(e)
    logger.warning(f"⚠️ Enhanced Claude Integrator not available: {e}")

# Try to load global systems
try:
    from global_knowledge_registry_and_report_card import get_global_registry
    SYSTEMS['global_registry'] = get_global_registry()
    logger.info("✅ Global Knowledge Registry loaded")
except Exception as e:
    WARNINGS['global_registry'] = str(e)
    logger.warning(f"⚠️ Global Knowledge Registry not available: {e}")

try:
    from global_resource_tracking_and_workflow_system import get_resource_tracking_system
    SYSTEMS['resource_tracking'] = get_resource_tracking_system()
    logger.info("✅ Resource Tracking System loaded")
except Exception as e:
    WARNINGS['resource_tracking'] = str(e)
    logger.warning(f"⚠️ Resource Tracking System not available: {e}")

try:
    from prompt_enhancement_and_writer_system import get_prompt_enhancement_system
    SYSTEMS['prompt_enhancement'] = get_prompt_enhancement_system()
    logger.info("✅ Prompt Enhancement System loaded")
except Exception as e:
    WARNINGS['prompt_enhancement'] = str(e)
    logger.warning(f"⚠️ Prompt Enhancement System not available: {e}")

try:
    from comprehensive_html_reporting_and_indexing_system import ComprehensiveHTMLReportingAndIndexingSystem
    SYSTEMS['html_system'] = ComprehensiveHTMLReportingAndIndexingSystem()
    logger.info("✅ HTML Reporting System loaded")
except Exception as e:
    WARNINGS['html_system'] = str(e)
    logger.warning(f"⚠️ HTML Reporting System not available: {e}")


@dataclass
class SystemStatus:
    """System status information"""
    name: str
    status: str  # 'operational', 'warning', 'error', 'not_loaded'
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewResults:
    """Comprehensive review results"""
    timestamp: str
    systems_tested: List[SystemStatus]
    claude_skills_status: Dict[str, Any]
    bookmarks_status: Dict[str, Any]
    knowledge_base_status: Dict[str, Any]
    grok_analysis: Optional[Dict[str, Any]] = None
    claude_analysis: Optional[Dict[str, Any]] = None
    unified_guidance: str = ""
    code_recommendations: List[str] = field(default_factory=list)
    errors: Dict[str, str] = field(default_factory=dict)
    warnings: Dict[str, str] = field(default_factory=dict)


class ComprehensiveSystemReviewer:
    """
    Comprehensive System Reviewer
    
    Reviews all systems, tests functionality, uses Claude and Grok together,
    and provides unified guidance.
    """
    
    def __init__(self):
        """Initialize comprehensive system reviewer"""
        self.project_root = Path(__file__).parent
        self.results: Optional[ReviewResults] = None
        
        logger.info("=" * 80)
        logger.info("Comprehensive System Review Initialized")
        logger.info("=" * 80)
    
    def test_system(self, name: str, system: Any) -> SystemStatus:
        """Test a system and return status"""
        try:
            if system is None:
                return SystemStatus(
                    name=name,
                    status='not_loaded',
                    message=f"{name} is not loaded",
                    details={}
                )
            
            # Basic functionality test
            if hasattr(system, 'name'):
                details = {'name': system.name}
            else:
                details = {}
            
            # Test specific methods if available
            if name == 'knowledge_registry':
                summary = system.get_summary()
                details['summary'] = summary
                return SystemStatus(
                    name=name,
                    status='operational',
                    message=f"{name} is operational",
                    details=details
                )
            
            elif name == 'mcp_registry':
                tools = system.list_all_tools()
                details['tools'] = tools
                return SystemStatus(
                    name=name,
                    status='operational',
                    message=f"{name} is operational with {tools.get('total_tools', 0)} tools",
                    details=details
                )
            
            elif name == 'claude_agent':
                has_client = system.claude_client is not None
                details['has_client'] = has_client
                if has_client:
                    return SystemStatus(
                        name=name,
                        status='operational',
                        message=f"{name} is operational with Claude API",
                        details=details
                    )
                else:
                    return SystemStatus(
                        name=name,
                        status='warning',
                        message=f"{name} loaded but Claude API not configured",
                        details=details
                    )
            
            elif name == 'grok_agent':
                has_api = system.api_key is not None
                details['has_api'] = has_api
                if has_api:
                    return SystemStatus(
                        name=name,
                        status='operational',
                        message=f"{name} is operational with Grok API",
                        details=details
                    )
                else:
                    return SystemStatus(
                        name=name,
                        status='warning',
                        message=f"{name} loaded but Grok API not configured",
                        details=details
                    )
            
            else:
                return SystemStatus(
                    name=name,
                    status='operational',
                    message=f"{name} is loaded",
                    details=details
                )
        
        except Exception as e:
            return SystemStatus(
                name=name,
                status='error',
                message=f"{name} test failed: {str(e)}",
                details={'error': str(e), 'traceback': traceback.format_exc()}
            )
    
    def get_claude_skills_status(self) -> Dict[str, Any]:
        """Get Claude skills status"""
        status = {
            'total_skills': 0,
            'skills': [],
            'unprocessed': 0,
            'processing': 0,
            'completed': 0
        }
        
        if 'knowledge_registry' in SYSTEMS:
            registry = SYSTEMS['knowledge_registry']
            skills = registry.claude_skills
            
            status['total_skills'] = len(skills)
            
            for name, skill in skills.items():
                skill_info = {
                    'name': skill.name,
                    'description': skill.description,
                    'status': skill.status.value,
                    'export_path': skill.export_path,
                    'tags': skill.tags
                }
                status['skills'].append(skill_info)
                
                if skill.status.value == 'not_started':
                    status['unprocessed'] += 1
                elif skill.status.value == 'in_progress':
                    status['processing'] += 1
                elif skill.status.value == 'completed':
                    status['completed'] += 1
        
        return status
    
    def get_bookmarks_status(self) -> Dict[str, Any]:
        """Get bookmarks status"""
        status = {
            'total_bookmarks': 0,
            'unprocessed': 0,
            'processing': 0,
            'completed': 0,
            'failed': 0,
            'by_source': {}
        }
        
        if 'knowledge_registry' in SYSTEMS:
            registry = SYSTEMS['knowledge_registry']
            bookmarks = registry.bookmarks
            
            status['total_bookmarks'] = len(bookmarks)
            
            for url, bookmark in bookmarks.items():
                status_key = bookmark.processing_status.value
                if status_key == 'not_started':
                    status['unprocessed'] += 1
                elif status_key == 'in_progress':
                    status['processing'] += 1
                elif status_key == 'completed':
                    status['completed'] += 1
                elif status_key == 'failed':
                    status['failed'] += 1
                
                source = bookmark.source or 'unknown'
                if source not in status['by_source']:
                    status['by_source'][source] = 0
                status['by_source'][source] += 1
        
        return status
    
    def get_knowledge_base_status(self) -> Dict[str, Any]:
        """Get knowledge base status"""
        status = {
            'domains': {},
            'git_repos': {},
            'processing_queue': []
        }
        
        if 'knowledge_registry' in SYSTEMS:
            registry = SYSTEMS['knowledge_registry']
            
            # Domains
            for name, domain in registry.domains.items():
                status['domains'][name] = {
                    'category': domain.category.value,
                    'processing_status': domain.processing_status.value,
                    'priority': domain.priority.value,
                    'foundation': domain.foundation
                }
            
            # Git repos
            for name, repo in registry.git_repos.items():
                status['git_repos'][name] = {
                    'url': repo.url,
                    'status': repo.status.value,
                    'priority': repo.priority.value,
                    'integration_phase': repo.integration_phase
                }
            
            # Processing queue
            queue = registry.get_processing_queue()
            status['processing_queue'] = [
                {
                    'item_id': item.item_id,
                    'item_type': item.item_type,
                    'priority': item.priority.value,
                    'status': item.status.value
                }
                for item in queue[:20]  # First 20 items
            ]
        
        return status
    
    def analyze_with_grok(self, query: str) -> Optional[Dict[str, Any]]:
        """Analyze using Grok API"""
        if 'grok_agent' not in SYSTEMS:
            return None
        
        grok_agent = SYSTEMS['grok_agent']
        if not grok_agent.api_key:
            return None
        
        try:
            # Use Grok for cultural reasoning and insights
            # Note: This is a placeholder - actual Grok integration would go here
            logger.info("Analyzing with Grok...")
            
            # For now, return a structured response
            return {
                'query': query,
                'analysis': 'Grok analysis would go here',
                'insights': [],
                'status': 'placeholder'
            }
        except Exception as e:
            logger.error(f"Grok analysis error: {e}")
            return None
    
    def analyze_with_claude(self, query: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Analyze using Claude API"""
        if 'claude_agent' not in SYSTEMS:
            return None
        
        claude_agent = SYSTEMS['claude_agent']
        if not claude_agent.claude_client:
            return None
        
        try:
            logger.info("Analyzing with Claude...")
            
            # Build comprehensive context
            full_context = context or {}
            full_context.update({
                'systems_status': {name: sys.name if hasattr(sys, 'name') else str(type(sys)) 
                                 for name, sys in SYSTEMS.items()},
                'errors': ERRORS,
                'warnings': WARNINGS
            })
            
            result = claude_agent.analyze_with_claude(
                query=query,
                context=full_context,
                persona='System Architect',
                apply_first_principles=True
            )
            
            return result
        except Exception as e:
            logger.error(f"Claude analysis error: {e}")
            return None
    
    def generate_unified_guidance(self, results: ReviewResults) -> str:
        """Generate unified guidance based on review results"""
        
        guidance_parts = []
        
        guidance_parts.append("# Unified System Guidance\n")
        guidance_parts.append(f"**Generated:** {results.timestamp}\n")
        guidance_parts.append("\n## System Status Summary\n")
        
        # Count statuses
        operational = sum(1 for s in results.systems_tested if s.status == 'operational')
        warnings = sum(1 for s in results.systems_tested if s.status == 'warning')
        errors = sum(1 for s in results.systems_tested if s.status == 'error')
        not_loaded = sum(1 for s in results.systems_tested if s.status == 'not_loaded')
        
        guidance_parts.append(f"- ✅ **Operational:** {operational}")
        guidance_parts.append(f"- ⚠️ **Warnings:** {warnings}")
        guidance_parts.append(f"- ❌ **Errors:** {errors}")
        guidance_parts.append(f"- ⚪ **Not Loaded:** {not_loaded}\n")
        
        # Claude Skills Status
        guidance_parts.append("\n## Claude Skills Status\n")
        cs_status = results.claude_skills_status
        guidance_parts.append(f"- **Total Skills:** {cs_status.get('total_skills', 0)}")
        guidance_parts.append(f"- **Completed:** {cs_status.get('completed', 0)}")
        guidance_parts.append(f"- **In Progress:** {cs_status.get('processing', 0)}")
        guidance_parts.append(f"- **Unprocessed:** {cs_status.get('unprocessed', 0)}\n")
        
        # Bookmarks Status
        guidance_parts.append("\n## Bookmarks Status\n")
        bm_status = results.bookmarks_status
        guidance_parts.append(f"- **Total Bookmarks:** {bm_status.get('total_bookmarks', 0)}")
        guidance_parts.append(f"- **Completed:** {bm_status.get('completed', 0)}")
        guidance_parts.append(f"- **In Progress:** {bm_status.get('processing', 0)}")
        guidance_parts.append(f"- **Unprocessed:** {bm_status.get('unprocessed', 0)}")
        guidance_parts.append(f"- **Failed:** {bm_status.get('failed', 0)}\n")
        
        # Knowledge Base Status
        guidance_parts.append("\n## Knowledge Base Status\n")
        kb_status = results.knowledge_base_status
        guidance_parts.append(f"- **Domains:** {len(kb_status.get('domains', {}))}")
        guidance_parts.append(f"- **Git Repos:** {len(kb_status.get('git_repos', {}))}")
        guidance_parts.append(f"- **Queue Items:** {len(kb_status.get('processing_queue', []))}\n")
        
        # Critical Issues
        if results.errors:
            guidance_parts.append("\n## Critical Issues\n")
            for name, error in results.errors.items():
                guidance_parts.append(f"- ❌ **{name}:** {error}\n")
        
        # Warnings
        if results.warnings:
            guidance_parts.append("\n## Warnings\n")
            for name, warning in results.warnings.items():
                guidance_parts.append(f"- ⚠️ **{name}:** {warning}\n")
        
        # Recommendations
        guidance_parts.append("\n## Recommendations\n")
        
        # Check for missing API keys
        if 'claude_agent' in SYSTEMS and not SYSTEMS['claude_agent'].claude_client:
            guidance_parts.append("1. **Configure Claude API:** Set `ANTHROPIC_API_KEY` in `.env`")
        
        if 'grok_agent' in SYSTEMS and not SYSTEMS['grok_agent'].api_key:
            guidance_parts.append("2. **Configure Grok API:** Set `GROK_API_KEY` in `.env`")
        
        # Check for unprocessed items
        if cs_status.get('unprocessed', 0) > 0:
            guidance_parts.append(f"3. **Process Claude Skills:** {cs_status.get('unprocessed', 0)} skills need processing")
        
        if bm_status.get('unprocessed', 0) > 0:
            guidance_parts.append(f"4. **Process Bookmarks:** {bm_status.get('unprocessed', 0)} bookmarks need processing")
        
        # Add code recommendations
        if results.code_recommendations:
            guidance_parts.append("\n## Code Recommendations\n")
            for i, rec in enumerate(results.code_recommendations, 1):
                guidance_parts.append(f"{i}. {rec}\n")
        
        return "\n".join(guidance_parts)
    
    def run_comprehensive_review(self) -> ReviewResults:
        """Run comprehensive system review"""
        
        logger.info("=" * 80)
        logger.info("Starting Comprehensive System Review")
        logger.info("=" * 80)
        
        # Test all systems
        systems_tested = []
        for name, system in SYSTEMS.items():
            logger.info(f"Testing {name}...")
            status = self.test_system(name, system)
            systems_tested.append(status)
            logger.info(f"  {status.status.upper()}: {status.message}")
        
        # Get status information
        logger.info("Gathering status information...")
        claude_skills_status = self.get_claude_skills_status()
        bookmarks_status = self.get_bookmarks_status()
        knowledge_base_status = self.get_knowledge_base_status()
        
        # Analyze with Claude and Grok
        logger.info("Analyzing with Claude and Grok...")
        
        analysis_query = f"""
        Review the Gematria Hive system status:
        - Systems tested: {len(systems_tested)}
        - Claude skills: {claude_skills_status.get('total_skills', 0)} total, {claude_skills_status.get('unprocessed', 0)} unprocessed
        - Bookmarks: {bookmarks_status.get('total_bookmarks', 0)} total, {bookmarks_status.get('unprocessed', 0)} unprocessed
        - Knowledge base: {len(knowledge_base_status.get('domains', {}))} domains, {len(knowledge_base_status.get('git_repos', {}))} repos
        
        Provide guidance on:
        1. What's working well
        2. What needs attention
        3. Priority actions
        4. Code improvements needed
        """
        
        grok_analysis = self.analyze_with_grok(analysis_query)
        claude_analysis = self.analyze_with_claude(analysis_query, {
            'claude_skills_status': claude_skills_status,
            'bookmarks_status': bookmarks_status,
            'knowledge_base_status': knowledge_base_status
        })
        
        # Create results
        results = ReviewResults(
            timestamp=datetime.now().isoformat(),
            systems_tested=systems_tested,
            claude_skills_status=claude_skills_status,
            bookmarks_status=bookmarks_status,
            knowledge_base_status=knowledge_base_status,
            grok_analysis=grok_analysis,
            claude_analysis=claude_analysis,
            errors=ERRORS,
            warnings=WARNINGS
        )
        
        # Generate unified guidance
        results.unified_guidance = self.generate_unified_guidance(results)
        
        # Generate code recommendations
        code_recommendations = []
        
        # Check for missing integrations
        if 'enhanced_claude' not in SYSTEMS:
            code_recommendations.append("Implement Enhanced Claude Integrator for better context management")
        
        if 'global_registry' not in SYSTEMS:
            code_recommendations.append("Implement Global Knowledge Registry for unified knowledge tracking")
        
        if 'resource_tracking' not in SYSTEMS:
            code_recommendations.append("Implement Resource Tracking System for workflow management")
        
        # Check for unprocessed items
        if claude_skills_status.get('unprocessed', 0) > 0:
            code_recommendations.append(f"Process {claude_skills_status.get('unprocessed', 0)} unprocessed Claude skills")
        
        if bookmarks_status.get('unprocessed', 0) > 0:
            code_recommendations.append(f"Process {bookmarks_status.get('unprocessed', 0)} unprocessed bookmarks")
        
        results.code_recommendations = code_recommendations
        
        self.results = results
        
        logger.info("=" * 80)
        logger.info("Comprehensive System Review Complete")
        logger.info("=" * 80)
        
        return results
    
    def save_results(self, results: ReviewResults):
        """Save review results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_dir = self.project_root / "data" / "system_reviews"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        json_file = results_dir / f"comprehensive_review_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(results), f, indent=2, default=str)
        
        # Save markdown report
        md_file = results_dir / f"comprehensive_review_{timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive System Review\n\n")
            f.write(f"**Generated:** {results.timestamp}\n\n")
            f.write("---\n\n")
            f.write(results.unified_guidance)
            f.write("\n\n---\n\n")
            
            if results.claude_analysis:
                f.write("## Claude Analysis\n\n")
                if 'response' in results.claude_analysis:
                    f.write(results.claude_analysis['response'])
                f.write("\n\n")
            
            if results.grok_analysis:
                f.write("## Grok Analysis\n\n")
                f.write(json.dumps(results.grok_analysis, indent=2))
                f.write("\n\n")
        
        logger.info(f"Results saved to:")
        logger.info(f"  - JSON: {json_file}")
        logger.info(f"  - Markdown: {md_file}")
        
        return json_file, md_file
    
    def print_summary(self, results: ReviewResults):
        """Print summary to console"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE SYSTEM REVIEW SUMMARY")
        print("=" * 80)
        print(f"\nGenerated: {results.timestamp}\n")
        
        print("SYSTEM STATUS:")
        for status in results.systems_tested:
            icon = "✅" if status.status == 'operational' else "⚠️" if status.status == 'warning' else "❌"
            print(f"  {icon} {status.name}: {status.message}")
        
        print(f"\nCLAUDE SKILLS:")
        cs = results.claude_skills_status
        print(f"  Total: {cs.get('total_skills', 0)}")
        print(f"  Completed: {cs.get('completed', 0)}")
        print(f"  In Progress: {cs.get('processing', 0)}")
        print(f"  Unprocessed: {cs.get('unprocessed', 0)}")
        
        print(f"\nBOOKMARKS:")
        bm = results.bookmarks_status
        print(f"  Total: {bm.get('total_bookmarks', 0)}")
        print(f"  Completed: {bm.get('completed', 0)}")
        print(f"  In Progress: {bm.get('processing', 0)}")
        print(f"  Unprocessed: {bm.get('unprocessed', 0)}")
        print(f"  Failed: {bm.get('failed', 0)}")
        
        print(f"\nKNOWLEDGE BASE:")
        kb = results.knowledge_base_status
        print(f"  Domains: {len(kb.get('domains', {}))}")
        print(f"  Git Repos: {len(kb.get('git_repos', {}))}")
        print(f"  Queue Items: {len(kb.get('processing_queue', []))}")
        
        if results.errors:
            print(f"\nERRORS ({len(results.errors)}):")
            for name, error in results.errors.items():
                print(f"  ❌ {name}: {error}")
        
        if results.warnings:
            print(f"\nWARNINGS ({len(results.warnings)}):")
            for name, warning in results.warnings.items():
                print(f"  ⚠️ {name}: {warning}")
        
        if results.code_recommendations:
            print(f"\nCODE RECOMMENDATIONS:")
            for i, rec in enumerate(results.code_recommendations, 1):
                print(f"  {i}. {rec}")
        
        print("\n" + "=" * 80)


def main():
    """Main function"""
    
    print("=" * 80)
    print("COMPREHENSIVE SYSTEM REVIEW")
    print("Gematria Hive - Complete System Analysis")
    print("=" * 80)
    print()
    
    reviewer = ComprehensiveSystemReviewer()
    
    # Run comprehensive review
    results = reviewer.run_comprehensive_review()
    
    # Print summary
    reviewer.print_summary(results)
    
    # Save results
    json_file, md_file = reviewer.save_results(results)
    
    print(f"\n✅ Review complete!")
    print(f"📄 Full report: {md_file}")
    print(f"📊 Data file: {json_file}")
    print()
    
    return results


if __name__ == "__main__":
    main()
