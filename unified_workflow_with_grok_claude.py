#!/usr/bin/env python3
"""
Unified Workflow with Grok and Claude Together
Gematria Hive - Comprehensive workflow using Grok and Claude together

Purpose:
- Use Grok and Claude together for analysis
- Run all system scripts for workflows and tools
- Process bookmarks with both Grok and Claude
- Generate comprehensive reports
- Provide unifying guidance

Author: Gematria Hive Team
Date: January 9, 2025
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

from dotenv import load_dotenv
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('unified_workflow.log')
    ]
)
logger = logging.getLogger(__name__)

# Import our systems
try:
    from agents.bookmark_ingestion import BookmarkIngestionAgent
    from agents.claude_integrator import ClaudeIntegratorAgent
    from agents.twitter_fetcher import TwitterFetcherAgent
    from agents.knowledge_registry import get_registry
    from agents.mcp_tool_registry import get_tool_registry
    from claude_go_get_bookmark_skill import ClaudeGoGetBookmarkSkill
    HAS_AGENTS = True
except ImportError as e:
    HAS_AGENTS = False
    logger.warning(f"Some agents not available: {e}")


@dataclass
class UnifiedAnalysis:
    """Unified analysis result using Grok and Claude together"""
    timestamp: str
    query: str
    grok_analysis: Optional[Dict[str, Any]] = None
    claude_analysis: Optional[Dict[str, Any]] = None
    synthesis: Optional[Dict[str, Any]] = None
    recommendations: List[str] = field(default_factory=list)


class UnifiedWorkflowWithGrokClaude:
    """
    Unified Workflow using Grok and Claude Together
    
    Features:
    - Use Grok and Claude together for analysis
    - Process bookmarks with both systems
    - Run all workflow scripts
    - Generate comprehensive reports
    """
    
    def __init__(self):
        """Initialize unified workflow"""
        self.project_root = Path(__file__).parent
        self.results_path = self.project_root / "data" / "unified_workflow"
        self.results_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize agents
        self.bookmark_agent = BookmarkIngestionAgent() if HAS_AGENTS else None
        self.claude_agent = ClaudeIntegratorAgent() if HAS_AGENTS else None
        self.grok_agent = TwitterFetcherAgent() if HAS_AGENTS else None
        self.knowledge_registry = get_registry() if HAS_AGENTS else None
        self.mcp_registry = get_tool_registry() if HAS_AGENTS else None
        self.bookmark_skill = ClaudeGoGetBookmarkSkill() if HAS_AGENTS else None
        
        logger.info("Initialized Unified Workflow with Grok and Claude")
    
    def analyze_with_grok_and_claude(self, query: str, context: Optional[Dict] = None) -> UnifiedAnalysis:
        """
        Analyze query using both Grok and Claude together
        
        Args:
            query: Query string
            context: Optional context dictionary
            
        Returns:
            UnifiedAnalysis with both Grok and Claude results
        """
        logger.info("=" * 80)
        logger.info("ANALYZING WITH GROK AND CLAUDE TOGETHER")
        logger.info("=" * 80)
        logger.info(f"Query: {query[:100]}...")
        
        analysis = UnifiedAnalysis(
            timestamp=datetime.now().isoformat(),
            query=query
        )
        
        # Grok analysis (via Twitter fetcher agent)
        if self.grok_agent and hasattr(self.grok_agent, 'api_key') and self.grok_agent.api_key:
            try:
                logger.info("🔍 Getting Grok analysis...")
                # Note: Grok agent is primarily for Twitter, but we can use it for general analysis
                # For Twitter/X URLs, use Grok to fetch thread context
                if context and 'url' in context:
                    url = context['url']
                    if 'twitter.com' in url or 'x.com' in url:
                        thread = self.grok_agent.fetch_thread_via_grok(url)
                        analysis.grok_analysis = {
                            'type': 'twitter_thread',
                            'thread': thread,
                            'status': 'success'
                        }
                        logger.info("✅ Grok thread fetched")
                    else:
                        analysis.grok_analysis = {
                            'type': 'general',
                            'status': 'available',
                            'note': 'Grok agent available for Twitter/X thread fetching'
                        }
                else:
                    analysis.grok_analysis = {
                        'type': 'general',
                        'status': 'available',
                        'note': 'Grok agent available for Twitter/X thread fetching'
                    }
            except Exception as e:
                logger.warning(f"⚠️  Grok analysis error: {e}")
                analysis.grok_analysis = {'error': str(e), 'status': 'failed'}
        else:
            logger.warning("⚠️  Grok agent not available (need GROK_API_KEY)")
            analysis.grok_analysis = {
                'error': 'Grok agent not available',
                'status': 'unavailable',
                'note': 'Set GROK_API_KEY in .env file'
            }
        
        # Claude analysis
        if self.claude_agent:
            try:
                logger.info("🔍 Getting Claude analysis...")
                claude_result = self.claude_agent.analyze_with_claude(
                    query=query,
                    context=context or {},
                    apply_first_principles=True
                )
                analysis.claude_analysis = claude_result
                logger.info("✅ Claude analysis complete")
            except Exception as e:
                logger.warning(f"⚠️  Claude analysis error: {e}")
                analysis.claude_analysis = {'error': str(e), 'status': 'failed'}
        else:
            logger.warning("⚠️  Claude agent not available")
            analysis.claude_analysis = {
                'error': 'Claude agent not available',
                'status': 'unavailable',
                'note': 'Set ANTHROPIC_API_KEY in .env file'
            }
        
        # Synthesize results
        if analysis.grok_analysis and analysis.claude_analysis:
            try:
                synthesis = self._synthesize_grok_claude(analysis)
                analysis.synthesis = synthesis
                logger.info("✅ Synthesis complete")
            except Exception as e:
                logger.warning(f"⚠️  Synthesis error: {e}")
                analysis.synthesis = {'error': str(e)}
        
        # Generate recommendations
        analysis.recommendations = self._generate_recommendations(analysis)
        
        return analysis
    
    def _synthesize_grok_claude(self, analysis: UnifiedAnalysis) -> Dict[str, Any]:
        """Synthesize Grok and Claude results"""
        synthesis = {
            'timestamp': datetime.now().isoformat(),
            'grok_available': analysis.grok_analysis and 'error' not in analysis.grok_analysis,
            'claude_available': analysis.claude_analysis and 'error' not in analysis.claude_analysis,
            'insights': [],
            'recommendations': []
        }
        
        # Grok insights
        if analysis.grok_analysis and 'error' not in analysis.grok_analysis:
            if analysis.grok_analysis.get('type') == 'twitter_thread':
                synthesis['insights'].append("Grok provided Twitter/X thread context")
            else:
                synthesis['insights'].append("Grok agent available for Twitter/X thread fetching")
        
        # Claude insights
        if analysis.claude_analysis and 'error' not in analysis.claude_analysis:
            if 'response' in analysis.claude_analysis:
                claude_response = analysis.claude_analysis['response']
                synthesis['claude_response'] = claude_response[:2000]  # First 2000 chars
                synthesis['insights'].append("Claude provided deep analysis with first principles thinking")
        
        # Combined recommendations
        if synthesis['grok_available'] and synthesis['claude_available']:
            synthesis['recommendations'].append("Use Claude for deep analysis and Grok for Twitter/X thread context")
        elif synthesis['claude_available']:
            synthesis['recommendations'].append("Use Claude for analysis (Grok not available)")
        elif synthesis['grok_available']:
            synthesis['recommendations'].append("Use Grok for Twitter/X threads (Claude not available)")
        else:
            synthesis['recommendations'].append("Set up API keys for both Grok and Claude")
        
        return synthesis
    
    def _generate_recommendations(self, analysis: UnifiedAnalysis) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if not analysis.grok_analysis or 'error' in analysis.grok_analysis:
            recommendations.append("Set up GROK_API_KEY for Twitter/X thread fetching")
        
        if not analysis.claude_analysis or 'error' in analysis.claude_analysis:
            recommendations.append("Set up ANTHROPIC_API_KEY for Claude analysis")
        
        if analysis.synthesis and analysis.synthesis.get('grok_available') and analysis.synthesis.get('claude_available'):
            recommendations.append("Both Grok and Claude are available - use together for comprehensive analysis")
        
        return recommendations
    
    def process_bookmarks_with_grok_claude(self, bookmarks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process bookmarks using both Grok and Claude together
        
        Args:
            bookmarks: List of bookmarks to process
            
        Returns:
            Processing results
        """
        logger.info("=" * 80)
        logger.info("PROCESSING BOOKMARKS WITH GROK AND CLAUDE")
        logger.info("=" * 80)
        logger.info(f"Processing {len(bookmarks)} bookmarks...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_bookmarks': len(bookmarks),
            'processed': 0,
            'failed': 0,
            'bookmarks': []
        }
        
        for bookmark in bookmarks:
            url = bookmark.get('url', '')
            title = bookmark.get('title', '')
            description = bookmark.get('description', '')
            
            bookmark_result = {
                'url': url,
                'title': title,
                'grok_analysis': None,
                'claude_analysis': None,
                'synthesis': None,
                'status': 'pending'
            }
            
            try:
                # Detect URL type
                url_type = self.bookmark_agent.detect_url_type(url) if self.bookmark_agent else 'unknown'
                bookmark_result['url_type'] = url_type
                
                # If Twitter/X, use Grok to fetch thread
                if url_type == 'twitter' and self.grok_agent and hasattr(self.grok_agent, 'api_key') and self.grok_agent.api_key:
                    try:
                        logger.info(f"Fetching Twitter thread via Grok: {url}")
                        thread = self.grok_agent.fetch_thread_via_grok(url)
                        bookmark_result['grok_analysis'] = {
                            'type': 'twitter_thread',
                            'thread': thread,
                            'status': 'success'
                        }
                        logger.info("✅ Grok thread fetched")
                    except Exception as e:
                        logger.warning(f"⚠️  Grok thread fetch failed: {e}")
                        bookmark_result['grok_analysis'] = {'error': str(e), 'status': 'failed'}
                
                # Use Claude to analyze bookmark
                if self.claude_agent:
                    try:
                        query = f"Analyze this bookmark: {title}\n\nDescription: {description}"
                        context = {
                            'bookmark': bookmark,
                            'url_type': url_type,
                            'grok_thread': bookmark_result.get('grok_analysis', {}).get('thread')
                        }
                        
                        claude_result = self.claude_agent.analyze_with_claude(
                            query=query,
                            context=context,
                            apply_first_principles=True
                        )
                        bookmark_result['claude_analysis'] = claude_result
                        logger.info("✅ Claude analysis complete")
                    except Exception as e:
                        logger.warning(f"⚠️  Claude analysis failed: {e}")
                        bookmark_result['claude_analysis'] = {'error': str(e), 'status': 'failed'}
                
                # Synthesize results
                if bookmark_result['grok_analysis'] or bookmark_result['claude_analysis']:
                    synthesis = self._synthesize_bookmark_analysis(bookmark_result)
                    bookmark_result['synthesis'] = synthesis
                
                bookmark_result['status'] = 'complete'
                results['processed'] += 1
                
            except Exception as e:
                logger.error(f"❌ Error processing bookmark {url}: {e}")
                bookmark_result['status'] = 'failed'
                bookmark_result['error'] = str(e)
                results['failed'] += 1
            
            results['bookmarks'].append(bookmark_result)
        
        logger.info(f"✅ Processed {results['processed']}/{results['total_bookmarks']} bookmarks")
        
        # Save results
        self._save_bookmark_results(results)
        
        return results
    
    def _synthesize_bookmark_analysis(self, bookmark_result: Dict) -> Dict[str, Any]:
        """Synthesize bookmark analysis results"""
        synthesis = {
            'timestamp': datetime.now().isoformat(),
            'has_grok': bookmark_result.get('grok_analysis') is not None,
            'has_claude': bookmark_result.get('claude_analysis') is not None,
            'insights': []
        }
        
        if bookmark_result.get('grok_analysis'):
            grok_analysis = bookmark_result['grok_analysis']
            if grok_analysis.get('type') == 'twitter_thread':
                synthesis['insights'].append("Grok provided Twitter/X thread context")
        
        if bookmark_result.get('claude_analysis'):
            claude_analysis = bookmark_result['claude_analysis']
            if 'response' in claude_analysis:
                synthesis['claude_insight'] = claude_analysis['response'][:500]  # First 500 chars
                synthesis['insights'].append("Claude provided deep analysis")
        
        return synthesis
    
    def run_all_workflow_scripts(self) -> Dict[str, Any]:
        """Run all workflow scripts (check status only)"""
        logger.info("=" * 80)
        logger.info("CHECKING WORKFLOW SCRIPTS")
        logger.info("=" * 80)
        
        workflow_scripts = [
            ('execute_critical_path.py', 'Critical path execution'),
            ('execute_ingestions.py', 'Ingestion execution'),
            ('ingest_pass1.py', 'Pass 1 ingestion'),
            ('ingest_csv.py', 'CSV ingestion'),
            ('comprehensive_system_analysis.py', 'Comprehensive system analysis')
        ]
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'scripts': [],
            'available': 0,
            'missing': 0
        }
        
        for script_name, description in workflow_scripts:
            script_path = self.project_root / script_name
            script_result = {
                'name': script_name,
                'description': description,
                'exists': script_path.exists(),
                'status': 'available' if script_path.exists() else 'missing'
            }
            
            if script_path.exists():
                results['available'] += 1
            else:
                results['missing'] += 1
            
            results['scripts'].append(script_result)
        
        logger.info(f"✅ Found {results['available']}/{len(workflow_scripts)} workflow scripts")
        
        return results
    
    def _save_bookmark_results(self, results: Dict[str, Any]):
        """Save bookmark processing results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = self.results_path / f"bookmark_processing_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Results saved to: {results_file}")
    
    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive report"""
        logger.info("=" * 80)
        logger.info("GENERATING COMPREHENSIVE REPORT")
        logger.info("=" * 80)
        
        report_parts = []
        
        report_parts.append("# Unified Workflow Report - Grok and Claude Together\n")
        report_parts.append(f"**Generated:** {datetime.now().isoformat()}\n\n")
        
        # System Status
        report_parts.append("## System Status\n\n")
        
        # Grok Status
        grok_available = self.grok_agent and hasattr(self.grok_agent, 'api_key') and self.grok_agent.api_key
        report_parts.append(f"- **Grok Agent:** {'✅ Available' if grok_available else '❌ Not Available (need GROK_API_KEY)'}\n")
        
        # Claude Status
        claude_available = self.claude_agent and hasattr(self.claude_agent, 'claude_client') and self.claude_agent.claude_client
        report_parts.append(f"- **Claude Agent:** {'✅ Available' if claude_available else '❌ Not Available (need ANTHROPIC_API_KEY)'}\n")
        
        # Bookmark Agent Status
        bookmark_available = self.bookmark_agent is not None
        report_parts.append(f"- **Bookmark Agent:** {'✅ Available' if bookmark_available else '❌ Not Available'}\n")
        
        # Knowledge Registry Status
        registry_available = self.knowledge_registry is not None
        report_parts.append(f"- **Knowledge Registry:** {'✅ Available' if registry_available else '❌ Not Available'}\n")
        
        # MCP Tool Registry Status
        mcp_available = self.mcp_registry is not None
        report_parts.append(f"- **MCP Tool Registry:** {'✅ Available' if mcp_available else '❌ Not Available'}\n")
        
        # Recommendations
        report_parts.append("\n## Recommendations\n\n")
        
        if not grok_available:
            report_parts.append("1. Set up GROK_API_KEY in .env file for Twitter/X thread fetching\n")
        
        if not claude_available:
            report_parts.append("2. Set up ANTHROPIC_API_KEY in .env file for Claude analysis\n")
        
        if grok_available and claude_available:
            report_parts.append("3. ✅ Both Grok and Claude are available - use together for comprehensive analysis\n")
        
        report_parts.append("4. Process bookmarks using both Grok and Claude together\n")
        report_parts.append("5. Run workflow scripts to process data\n")
        
        report = "".join(report_parts)
        
        # Save report
        report_file = self.results_path / f"unified_workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved to: {report_file}")
        
        # Also save to project root
        root_report_file = self.project_root / "UNIFIED_WORKFLOW_REPORT.md"
        with open(root_report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report also saved to: {root_report_file}")
        
        return report


def main():
    """Main function"""
    logger.info("=" * 80)
    logger.info("UNIFIED WORKFLOW WITH GROK AND CLAUDE")
    logger.info("=" * 80)
    logger.info("")
    
    workflow = UnifiedWorkflowWithGrokClaude()
    
    # Example query
    query = """
    Analyze the current state of the Gematria Hive system:
    1. Claude skills implementation status
    2. Bookmark processing status
    3. Knowledge base completeness
    4. Workflow script availability
    5. MCP tools registration
    
    Provide insights and recommendations for improvement.
    """
    
    # Analyze with Grok and Claude together
    analysis = workflow.analyze_with_grok_and_claude(query)
    
    # Example bookmarks
    example_bookmarks = [
        {
            'id': 'bookmark-1',
            'url': 'https://example.com/sacred-geometry',
            'title': 'Sacred Geometry Patterns',
            'description': 'Information about sacred geometry patterns and their meanings'
        }
    ]
    
    # Process bookmarks with Grok and Claude
    bookmark_results = workflow.process_bookmarks_with_grok_claude(example_bookmarks)
    
    # Check workflow scripts
    script_results = workflow.run_all_workflow_scripts()
    
    # Generate comprehensive report
    report = workflow.generate_comprehensive_report()
    
    # Print summary
    print("\n" + "=" * 80)
    print("UNIFIED WORKFLOW SUMMARY")
    print("=" * 80)
    print(f"\n✅ Grok Available: {analysis.grok_analysis and 'error' not in analysis.grok_analysis}")
    print(f"✅ Claude Available: {analysis.claude_analysis and 'error' not in analysis.claude_analysis}")
    print(f"📊 Bookmarks Processed: {bookmark_results['processed']}/{bookmark_results['total_bookmarks']}")
    print(f"📜 Workflow Scripts: {script_results['available']}/{len(script_results['scripts'])}")
    print("\n📄 Full report saved to:")
    print(f"   - data/unified_workflow/")
    print(f"   - UNIFIED_WORKFLOW_REPORT.md")
    print("\n" + "=" * 80)
    print("✅ UNIFIED WORKFLOW COMPLETE")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
