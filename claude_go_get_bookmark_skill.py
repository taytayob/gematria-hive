#!/usr/bin/env python3
"""
Claude Go Get Bookmark Skill
Gematria Hive - Claude skill to go get and implement findings from bookmarks

Purpose:
- New Claude "go get" skill for bookmark processing
- Review bookmarks and extract findings
- Implement findings using all our tools
- Log new skill
- Use on tasks
- Complete using all tools

Author: Gematria Hive Team
Date: January 9, 2025
"""

import os
import json
import logging
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
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
    from global_resource_tracking_and_workflow_system import (
        get_resource_tracking_system, ResourceType, ItemStatus
    )
    from prompt_enhancement_and_writer_system import (
        get_prompt_enhancement_system, PromptEnhancementType, ContentType
    )
    from agents.mcp_tool_registry import MCPToolRegistry, get_tool_registry, MCPTool
    from core.gematria_engine import get_gematria_engine
    from core.sacred_geometry_engine import get_sacred_geometry_engine
    from core.domain_expansion_engine import get_domain_expansion_engine
    from comprehensive_html_reporting_and_indexing_system import ComprehensiveHTMLReportingAndIndexingSystem
    HAS_DEPENDENCIES = True
except ImportError as e:
    HAS_DEPENDENCIES = False
    logger.warning(f"Some dependencies not available: {e}")


@dataclass
class BookmarkFinding:
    """Bookmark finding"""
    finding_id: str
    bookmark_id: str
    url: str
    title: str
    finding: str
    category: str
    implementation_notes: str = ""
    tools_needed: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, implementing, complete
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ClaudeSkill:
    """Claude skill definition"""
    skill_id: str
    name: str
    description: str
    purpose: str
    capabilities: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class ClaudeGoGetBookmarkSkill:
    """
    Claude Go Get Bookmark Skill
    
    Features:
    - Review bookmarks and extract findings
    - Go get information from bookmarks
    - Implement findings using all tools
    - Log skill usage
    - Complete tasks using all tools
    """
    
    def __init__(self):
        """Initialize Claude go get bookmark skill"""
        self.name = "claude_go_get_bookmark_skill"
        self.project_root = Path(__file__).parent
        
        # Core systems
        self.registry = get_global_registry() if HAS_DEPENDENCIES else None
        self.claude_agent = ClaudeIntegratorAgent() if HAS_DEPENDENCIES else None
        self.enhanced_claude = EnhancedClaudeIntegrator() if HAS_DEPENDENCIES else None
        self.bookmark_agent = BookmarkIngestionAgent() if HAS_DEPENDENCIES else None
        self.mcp_registry = get_tool_registry() if HAS_DEPENDENCIES else None
        self.gematria_engine = get_gematria_engine() if HAS_DEPENDENCIES else None
        self.sacred_geometry_engine = get_sacred_geometry_engine() if HAS_DEPENDENCIES else None
        self.domain_expansion_engine = get_domain_expansion_engine() if HAS_DEPENDENCIES else None
        self.html_system = ComprehensiveHTMLReportingAndIndexingSystem() if HAS_DEPENDENCIES else None
        self.resource_tracking = get_resource_tracking_system() if HAS_DEPENDENCIES else None
        self.prompt_enhancement = get_prompt_enhancement_system() if HAS_DEPENDENCIES else None
        
        # Skill state
        self.skill: Optional[ClaudeSkill] = None
        self.findings: Dict[str, BookmarkFinding] = {}
        self.implementations: List[Dict[str, Any]] = []
        
        # Storage
        self.storage_path = self.project_root / "data" / "claude_skills"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized {self.name}")
    
    def create_skill(self) -> ClaudeSkill:
        """Create Claude go get bookmark skill"""
        
        skill_id = f"SKILL-{uuid.uuid4().hex[:8]}"
        
        skill = ClaudeSkill(
            skill_id=skill_id,
            name="Go Get Bookmark Findings",
            description="Claude skill to review bookmarks, extract findings, and implement them using all available tools",
            purpose="Process bookmarks, extract valuable findings, and implement them using the full Gematria Hive toolkit",
            capabilities=[
                "Review bookmarks and extract findings",
                "Go get information from URLs",
                "Analyze content and identify valuable insights",
                "Implement findings using all available tools",
                "Log skill usage and results",
                "Complete tasks using integrated tools"
            ],
            tools_used=[
                "claude_agent",
                "bookmark_agent",
                "gematria_engine",
                "sacred_geometry_engine",
                "domain_expansion_engine",
                "html_reporting_system",
                "mcp_tool_registry"
            ],
            examples=[
                "Review bookmark about sacred geometry → Extract findings → Implement using sacred geometry engine",
                "Review bookmark about gematria → Extract findings → Implement using gematria engine",
                "Review bookmark about new research → Extract findings → Implement using all tools"
            ]
        )
        
        self.skill = skill
        self._save_skill(skill)
        logger.info(f"Created Claude skill: {skill_id} ({skill.name})")
        return skill
    
    def _save_skill(self, skill: ClaudeSkill):
        """Save skill to file"""
        skill_file = self.storage_path / f"{skill.skill_id}.json"
        with open(skill_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(skill), f, indent=2, default=str)
        
        # Also save to master skills list
        master_skills_file = self.storage_path / "master_skills.json"
        master_skills = []
        if master_skills_file.exists():
            try:
                with open(master_skills_file, 'r', encoding='utf-8') as f:
                    master_skills = json.load(f)
            except:
                master_skills = []
        
        master_skills.append(asdict(skill))
        
        with open(master_skills_file, 'w', encoding='utf-8') as f:
            json.dump(master_skills, f, indent=2, default=str)
    
    def review_bookmarks(self, bookmarks: List[Dict[str, Any]], 
                        use_browser_mcp: bool = True,
                        use_grok: bool = True) -> List[BookmarkFinding]:
        """
        Review bookmarks and extract findings
        
        Args:
            bookmarks: List of bookmarks to review
            use_browser_mcp: Whether to use browser MCP to extract content
            use_grok: Whether to use Grok for additional insights
        """
        
        if not self.claude_agent:
            logger.warning("Claude agent not available")
            return []
        
        logger.info(f"Reviewing {len(bookmarks)} bookmarks...")
        if use_browser_mcp:
            logger.info("Using browser MCP for content extraction")
        if use_grok:
            logger.info("Using Grok for additional insights")
        
        findings = []
        
        for bookmark in bookmarks:
            url = bookmark.get('url', '')
            title = bookmark.get('title', '')
            description = bookmark.get('description', '')
            
            # Use browser MCP to extract content if enabled
            if use_browser_mcp and self.mcp_registry and url:
                try:
                    # Try to use browser agent through MCP if available
                    browser_tool = self.mcp_registry.get_tool("browser_scrape")
                    if browser_tool:
                        logger.info(f"Extracting content from {url} using browser MCP...")
                        browser_result = self.mcp_registry.execute_tool(
                            "browser_scrape",
                            url=url,
                            max_depth=1
                        )
                        if browser_result and isinstance(browser_result, list) and len(browser_result) > 0:
                            extracted_content = browser_result[0]
                            description = extracted_content.get('content', description)
                            title = extracted_content.get('title', title)
                            logger.info(f"✅ Extracted content from {url}: {len(description)} chars")
                except Exception as e:
                    logger.warning(f"Browser MCP extraction failed for {url}: {e}")
            
            # Use Grok for additional insights if enabled
            grok_insights = None
            if use_grok and self.mcp_registry and url:
                try:
                    grok_tool = self.mcp_registry.get_tool("grok_cultural_reasoning")
                    if grok_tool:
                        logger.info(f"Getting Grok insights for {url}...")
                        grok_result = self.mcp_registry.execute_tool(
                            "grok_cultural_reasoning",
                            text=f"{title}\n\n{description}",
                            context={'url': url, 'source': 'bookmark'}
                        )
                        if grok_result and 'cultural_analysis' in grok_result:
                            grok_insights = grok_result['cultural_analysis']
                            logger.info(f"✅ Got Grok insights for {url}")
                except Exception as e:
                    logger.warning(f"Grok insights failed for {url}: {e}")
            
            # Create prompt (will be enhanced)
            grok_section = ""
            if grok_insights:
                grok_section = f"""
## Grok Cultural Reasoning Insights
{grok_insights[:1000]}  # Limit to first 1000 chars
"""
            
            base_prompt = f"""# Bookmark Review and Finding Extraction

## Bookmark Information
- **URL:** {url}
- **Title:** {title}
- **Description:** {description}
{grok_section}

## Your Task

Review this bookmark and extract valuable findings that can be implemented using our Gematria Hive tools.

### What to Extract

1. **Key Findings:** What valuable information or insights does this bookmark contain?
   - Be specific and actionable
   - Identify patterns, connections, or insights
   - Note any mathematical, geometric, or esoteric significance

2. **Category:** What category does this belong to?
   - Options: gematria, sacred_geometry, numerology, research, tool, theorem, proof, pattern, frequency, color, language, historical, equation, plank, absolute_value, plotting
   - Choose the most relevant category

3. **Implementation Notes:** How can we implement this using our tools?
   - Be specific about what to implement
   - Describe the approach
   - Note any calculations, patterns, or analyses needed

4. **Tools Needed:** Which tools would be useful?
   - Options: gematria_engine, sacred_geometry_engine, domain_expansion_engine, html_reporting_system, bookmark_agent, mcp_tool_registry
   - List all relevant tools

### Our Available Tools

- **Gematria Engine:** Gematria calculations (English, Hebrew, Greek, etc.)
- **Sacred Geometry Engine:** Sacred geometry patterns (Vesica Piscis, Flower of Life, Metatron's Cube, etc.)
- **Domain Expansion Engine:** Domain expansion and pattern stacking across all domains
- **HTML Reporting System:** Generate comprehensive HTML reports
- **MCP Tool Registry:** Access to all tools via MCP protocol
- **Bookmark Agent:** Process and analyze bookmarks
- **And more...**

### Output Format

Provide your response in this exact format:

**FINDING:**
[Clear, detailed description of the finding - 2-4 sentences]

**CATEGORY:**
[One of: gematria, sacred_geometry, numerology, research, tool, theorem, proof, pattern, frequency, color, language, historical, equation, plank, absolute_value, plotting]

**IMPLEMENTATION_NOTES:**
[Detailed implementation notes - 3-5 sentences describing how to implement]

**TOOLS_NEEDED:**
[Comma-separated list of tools: gematria_engine, sacred_geometry_engine, domain_expansion_engine, html_reporting_system, bookmark_agent, mcp_tool_registry]

Begin your review now.
"""
            
            # Enhance prompt if available
            if self.prompt_enhancement:
                try:
                    enhanced_prompt_obj = self.prompt_enhancement.enhance_prompt(
                        prompt=base_prompt,
                        enhancement_type=PromptEnhancementType.OPTIMIZATION,
                        context={
                            'url': url,
                            'title': title,
                            'description': description,
                            'task': 'bookmark_review'
                        }
                    )
                    prompt = enhanced_prompt_obj.enhanced_prompt
                    logger.info(f"Enhanced prompt: {enhanced_prompt_obj.prompt_id} (score: {enhanced_prompt_obj.score_before:.2f} → {enhanced_prompt_obj.score_after:.2f})")
                except Exception as e:
                    logger.warning(f"Error enhancing prompt: {e}, using original")
                    prompt = base_prompt
            else:
                prompt = base_prompt
            
            try:
                # Use enhanced Claude integrator with context management for better results
                if self.enhanced_claude:
                    result = self.enhanced_claude.analyze_with_context_management(
                        query=prompt,
                        context={
                            'task': 'bookmark_review',
                            'type': 'finding_extraction',
                            'url': url,
                            'title': title,
                            'description': description
                        },
                        persona='Bookmark Analyst',
                        max_context_size=8000
                    )
                else:
                    # Fallback to regular Claude agent
                    result = self.claude_agent.analyze_with_claude(
                        query=prompt,
                        context={'task': 'bookmark_review', 'type': 'finding_extraction'},
                        persona='Bookmark Analyst',
                        apply_first_principles=True
                    )
                
                if result and 'response' in result:
                    response_text = result['response']
                    
                    # Extract structured data from response
                    finding_id = f"FINDING-{uuid.uuid4().hex[:8]}"
                    
                    # Parse structured response
                    finding_text = self._extract_section(response_text, 'FINDING:')
                    category = self._extract_section(response_text, 'CATEGORY:') or self._extract_category(response_text)
                    implementation_notes = self._extract_section(response_text, 'IMPLEMENTATION_NOTES:') or self._extract_implementation_notes(response_text)
                    tools_needed_str = self._extract_section(response_text, 'TOOLS_NEEDED:') or ''
                    tools_needed = [t.strip() for t in tools_needed_str.split(',') if t.strip()] or self._extract_tools_needed(response_text)
                    
                    finding = BookmarkFinding(
                        finding_id=finding_id,
                        bookmark_id=bookmark.get('id', ''),
                        url=url,
                        title=title,
                        finding=finding_text or response_text[:1000],  # Use extracted finding or first 1000 chars
                        category=category.strip().lower() if category else 'general',
                        implementation_notes=implementation_notes or response_text[:500],
                        tools_needed=tools_needed
                    )
                    
                    self.findings[finding_id] = finding
                    findings.append(finding)
                    
                    logger.info(f"Extracted finding: {finding_id} from {title}")
            except Exception as e:
                logger.error(f"Error reviewing bookmark {url}: {e}")
                continue
        
        logger.info(f"✅ Extracted {len(findings)} findings from {len(bookmarks)} bookmarks")
        return findings
    
    def _extract_category(self, text: str) -> str:
        """Extract category from text"""
        categories = ['gematria', 'sacred_geometry', 'numerology', 'research', 'tool', 'theorem', 'proof']
        text_lower = text.lower()
        
        for category in categories:
            if category in text_lower:
                return category
        
        return 'general'
    
    def _extract_implementation_notes(self, text: str) -> str:
        """Extract implementation notes from text"""
        # Look for implementation section
        if "implementation" in text.lower() or "implement" in text.lower():
            lines = text.split('\n')
            implementation_lines = []
            in_implementation = False
            
            for line in lines:
                if "implementation" in line.lower() or "implement" in line.lower():
                    in_implementation = True
                if in_implementation:
                    implementation_lines.append(line)
                    if len(implementation_lines) > 10:
                        break
            
            return '\n'.join(implementation_lines)
        
        return text[:500]  # First 500 chars
    
    def _extract_section(self, text: str, section_header: str) -> Optional[str]:
        """Extract a specific section from structured response"""
        if section_header not in text:
            return None
        
        # Find the section
        start_idx = text.find(section_header)
        if start_idx == -1:
            return None
        
        # Find the content after the header
        content_start = start_idx + len(section_header)
        
        # Find the next section or end of text
        next_section_headers = ['FINDING:', 'CATEGORY:', 'IMPLEMENTATION_NOTES:', 'TOOLS_NEEDED:']
        next_section_idx = len(text)
        
        for header in next_section_headers:
            if header != section_header:
                idx = text.find(header, content_start)
                if idx != -1 and idx < next_section_idx:
                    next_section_idx = idx
        
        # Extract content
        content = text[content_start:next_section_idx].strip()
        
        # Clean up (remove markdown formatting, extra whitespace)
        content = content.replace('**', '').replace('*', '').strip()
        
        return content if content else None
    
    def _extract_tools_needed(self, text: str) -> List[str]:
        """Extract tools needed from text"""
        tools = []
        text_lower = text.lower()
        
        tool_keywords = {
            'gematria_engine': ['gematria', 'gematria engine'],
            'sacred_geometry_engine': ['sacred geometry', 'geometry engine', 'sacred_geometry'],
            'domain_expansion_engine': ['domain expansion', 'domain engine', 'domain_expansion'],
            'html_reporting_system': ['html', 'report', 'reporting', 'html_reporting'],
            'bookmark_agent': ['bookmark', 'bookmark agent'],
            'mcp_tool_registry': ['mcp', 'tool registry', 'mcp_tool']
        }
        
        for tool, keywords in tool_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                if tool not in tools:
                    tools.append(tool)
        
        return tools
    
    def implement_finding(self, finding: BookmarkFinding) -> Dict[str, Any]:
        """Implement finding using all available tools"""
        
        logger.info(f"Implementing finding: {finding.finding_id} ({finding.title})")
        
        implementation = {
            'finding_id': finding.finding_id,
            'title': finding.title,
            'category': finding.category,
            'tools_used': [],
            'results': {},
            'status': 'implementing',
            'created_at': datetime.now().isoformat()
        }
        
        # Use tools as needed
        if 'gematria_engine' in finding.tools_needed and self.gematria_engine:
            logger.info("Using gematria engine...")
            # Example: calculate gematria for title
            if finding.title:
                try:
                    gematria_result = self.gematria_engine.calculate_gematria(finding.title, "english")
                    implementation['results']['gematria'] = gematria_result
                    implementation['tools_used'].append('gematria_engine')
                except Exception as e:
                    logger.error(f"Gematria engine error: {e}")
        
        if 'sacred_geometry_engine' in finding.tools_needed and self.sacred_geometry_engine:
            logger.info("Using sacred geometry engine...")
            # Example: generate sacred geometry pattern
            try:
                pattern = self.sacred_geometry_engine.generate_metatrons_cube()
                implementation['results']['sacred_geometry'] = {'pattern': 'metatrons_cube', 'generated': True}
                implementation['tools_used'].append('sacred_geometry_engine')
            except Exception as e:
                logger.error(f"Sacred geometry engine error: {e}")
        
        if 'domain_expansion_engine' in finding.tools_needed and self.domain_expansion_engine:
            logger.info("Using domain expansion engine...")
            # Example: expand domain
            try:
                expansion = self.domain_expansion_engine.expand_domain(finding.category, [])
                implementation['results']['domain_expansion'] = {'expanded': True}
                implementation['tools_used'].append('domain_expansion_engine')
            except Exception as e:
                logger.error(f"Domain expansion engine error: {e}")
        
        if 'html_reporting_system' in finding.tools_needed and self.html_system:
            logger.info("Using HTML reporting system...")
            # Generate HTML report for finding
            try:
                report = self.html_system.html_generator.generate_html_report(
                    title=f"Finding: {finding.title}",
                    content={
                        'finding': finding.finding,
                        'category': finding.category,
                        'implementation_notes': finding.implementation_notes,
                        'tools_needed': finding.tools_needed
                    },
                    category=finding.category,
                    perspectives=['mathematical', 'geometric', 'esoteric'],
                    domains=[finding.category]
                )
                
                # Save HTML
                html_file = self.html_system.storage_path / f"{report.report_id}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(report.html_content)
                
                implementation['results']['html_report'] = str(html_file)
                implementation['tools_used'].append('html_reporting_system')
            except Exception as e:
                logger.error(f"HTML reporting system error: {e}")
        
        # Update finding status
        finding.status = 'complete'
        implementation['status'] = 'complete'
        implementation['completed_at'] = datetime.now().isoformat()
        
        self.implementations.append(implementation)
        
        # Register resources and HTML replies with resource tracking system
        if self.resource_tracking:
            # Register HTML report if generated
            if 'html_report' in implementation['results']:
                html_path = implementation['results']['html_report']
                html_reply = self.resource_tracking.register_html_reply(
                    html_path=html_path,
                    title=f"Finding: {finding.title}",
                    category=finding.category,
                    status=ItemStatus.COMPLETE,
                    related_resources=[finding.finding_id],
                    kanban_task_id=None  # Can be linked to kanban if needed
                )
                implementation['html_reply_id'] = html_reply.reply_id
            
            # Create workflow item
            workflow_item = self.resource_tracking.create_workflow_item(
                title=f"Implement Finding: {finding.title}",
                description=finding.finding,
                category=finding.category,
                status=ItemStatus.COMPLETE,
                resource_ids=[finding.finding_id],
                html_reply_id=implementation.get('html_reply_id'),
                tools_used=implementation['tools_used'],
                agents_used=['claude_go_get_bookmark_skill']
            )
            implementation['workflow_item_id'] = workflow_item.item_id
        
        # Log to registry
        if self.registry:
            self.registry.add_finding(
                title=f"Implemented Finding: {finding.title}",
                description=finding.finding,
                category=finding.category,
                rank=FindingRank.HIGH,
                confidence=0.9,
                source='claude_go_get_bookmark_skill'
            )
        
        logger.info(f"✅ Implemented finding: {finding.finding_id}")
        return implementation
    
    def process_bookmarks_with_skill(self, bookmarks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process bookmarks using the go get skill"""
        
        logger.info("=" * 80)
        logger.info("Processing Bookmarks with Claude Go Get Skill")
        logger.info("=" * 80)
        
        # Create skill if not exists
        if not self.skill:
            self.skill = self.create_skill()
        
        # Review bookmarks
        findings = self.review_bookmarks(bookmarks)
        
        # Implement findings
        implementations = []
        for finding in findings:
            implementation = self.implement_finding(finding)
            implementations.append(implementation)
        
        # Compile results
        results = {
            'timestamp': datetime.now().isoformat(),
            'skill_id': self.skill.skill_id,
            'skill_name': self.skill.name,
            'total_bookmarks': len(bookmarks),
            'total_findings': len(findings),
            'total_implementations': len(implementations),
            'findings': [asdict(f) for f in findings],
            'implementations': implementations
        }
        
        # Save results
        self._save_results(results)
        
        logger.info("=" * 80)
        logger.info("✅ Bookmark Processing with Claude Go Get Skill Complete")
        logger.info("=" * 80)
        
        return results
    
    def _save_results(self, results: Dict[str, Any]):
        """Save results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = self.storage_path / f"bookmark_processing_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Results saved to: {results_file}")
    
    def _sync_with_dewey(self) -> List[Dict[str, Any]]:
        """Sync bookmarks with Dewey Chrome extension"""
        try:
            # Try to load from Dewey export directory
            dewey_path = self.project_root / "DeweyExport"
            if not dewey_path.exists():
                logger.warning("DeweyExport directory not found")
                return []
            
            bookmarks = []
            # Look for JSON files in Dewey export
            for json_file in dewey_path.rglob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Handle different Dewey export formats
                        if isinstance(data, list):
                            bookmarks.extend(data)
                        elif isinstance(data, dict):
                            if 'bookmarks' in data:
                                bookmarks.extend(data['bookmarks'])
                            else:
                                bookmarks.append(data)
                except Exception as e:
                    logger.warning(f"Error loading {json_file}: {e}")
            
            return bookmarks
        except Exception as e:
            logger.error(f"Error syncing with Dewey: {e}")
            return []


def main():
    """Main function"""
    
    logger.info("=" * 80)
    logger.info("Claude Go Get Bookmark Skill")
    logger.info("=" * 80)
    
    skill = ClaudeGoGetBookmarkSkill()
    
    # Create skill
    skill_obj = skill.create_skill()
    
    # Example bookmarks (would come from actual bookmark processing)
    example_bookmarks = [
        {
            'id': 'bookmark-1',
            'url': 'https://example.com/sacred-geometry',
            'title': 'Sacred Geometry Patterns',
            'description': 'Information about sacred geometry patterns and their meanings'
        },
        {
            'id': 'bookmark-2',
            'url': 'https://example.com/gematria',
            'title': 'Gematria Calculations',
            'description': 'Gematria calculation methods and examples'
        }
    ]
    
    # Process bookmarks
    results = skill.process_bookmarks_with_skill(example_bookmarks)
    
    # Print summary
    print("\n" + "=" * 80)
    print("SKILL SUMMARY")
    print("=" * 80)
    print(f"Skill ID: {results['skill_id']}")
    print(f"Skill Name: {results['skill_name']}")
    print(f"Total Bookmarks: {results['total_bookmarks']}")
    print(f"Total Findings: {results['total_findings']}")
    print(f"Total Implementations: {results['total_implementations']}")
    
    print("\n" + "=" * 80)
    print("✅ CLAUDE GO GET BOOKMARK SKILL COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
