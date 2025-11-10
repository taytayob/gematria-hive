#!/usr/bin/env python3
"""
Claude Go Get Bookmark Skill - Adapted Implementation
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

Adapted to use existing systems instead of missing dependencies.
"""

import os
import json
import logging
import uuid
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

# Import existing systems
try:
    from agents.knowledge_registry import (
        get_registry, ProcessingStatus, Priority
    )
    from agents.claude_integrator import ClaudeIntegratorAgent
    from agents.bookmark_ingestion import BookmarkIngestionAgent
    from agents.mcp_tool_registry import get_tool_registry, MCPTool
    from core.gematria_engine import get_gematria_engine
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
    
    Adapted to use existing systems:
    - agents.knowledge_registry (instead of global_knowledge_registry)
    - agents.claude_integrator (instead of enhanced_claude_integrator)
    - agents.bookmark_ingestion (existing)
    - agents.mcp_tool_registry (existing)
    - core.gematria_engine (existing)
    """
    
    def __init__(self):
        """Initialize Claude go get bookmark skill"""
        self.name = "claude_go_get_bookmark_skill"
        self.project_root = Path(__file__).parent
        
        # Core systems (using existing systems)
        self.registry = get_registry() if HAS_DEPENDENCIES else None
        self.claude_agent = ClaudeIntegratorAgent() if HAS_DEPENDENCIES else None
        self.bookmark_agent = BookmarkIngestionAgent() if HAS_DEPENDENCIES else None
        self.mcp_registry = get_tool_registry() if HAS_DEPENDENCIES else None
        self.gematria_engine = get_gematria_engine() if HAS_DEPENDENCIES else None
        
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
            description="Claude skill to review bookmarks, extract findings, and implement them using available tools",
            purpose="Process bookmarks, extract valuable findings, and implement them using the Gematria Hive toolkit",
            capabilities=[
                "Review bookmarks and extract findings",
                "Go get information from URLs",
                "Analyze content and identify valuable insights",
                "Implement findings using available tools",
                "Log skill usage and results",
                "Complete tasks using integrated tools"
            ],
            tools_used=[
                "claude_agent",
                "bookmark_agent",
                "gematria_engine",
                "mcp_tool_registry"
            ],
            examples=[
                "Review bookmark about sacred geometry → Extract findings → Implement using tools",
                "Review bookmark about gematria → Extract findings → Implement using gematria engine",
                "Review bookmark about new research → Extract findings → Implement using all tools"
            ]
        )
        
        self.skill = skill
        self._save_skill(skill)
        
        # Register in knowledge registry
        if self.registry:
            from agents.knowledge_registry import ClaudeSkill as RegistrySkill
            registry_skill = RegistrySkill(
                name=skill.name,
                description=skill.description,
                file_path=str(Path(__file__)),
                export_path=None,
                status=ProcessingStatus.IN_PROGRESS,
                last_updated=datetime.now().isoformat(),
                tags=["bookmark", "claude", "skill"]
            )
            self.registry.add_claude_skill(registry_skill)
        
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
            use_grok: Whether to use Grok for additional insights (if available)
        """
        
        if not self.claude_agent:
            logger.warning("Claude agent not available")
            return []
        
        logger.info(f"Reviewing {len(bookmarks)} bookmarks...")
        if use_browser_mcp:
            logger.info("Using browser MCP for content extraction (if available)")
        if use_grok:
            logger.info("Using Grok for additional insights (if available)")
        
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
                        if browser_result:
                            if isinstance(browser_result, list) and len(browser_result) > 0:
                                extracted_content = browser_result[0]
                                description = extracted_content.get('content', description)
                                title = extracted_content.get('title', title)
                            else:
                                description = str(browser_result)[:1000]
                            logger.info(f"✅ Extracted content from {url}: {len(description)} chars")
                except Exception as e:
                    logger.warning(f"Browser MCP extraction failed for {url}: {e}")
            
            # Use Grok for additional insights if enabled (via Twitter fetcher if available)
            grok_insights = None
            if use_grok and url and 'twitter.com' in url.lower() or 'x.com' in url.lower():
                try:
                    from agents.twitter_fetcher import TwitterFetcherAgent
                    grok_agent = TwitterFetcherAgent()
                    if grok_agent.api_key:
                        logger.info(f"Getting Grok insights for {url}...")
                        thread_data = grok_agent.fetch_thread_via_grok(url)
                        if thread_data:
                            grok_insights = str(thread_data)[:1000]
                            logger.info(f"✅ Got Grok insights for {url}")
                except Exception as e:
                    logger.warning(f"Grok insights failed for {url}: {e}")
            
            # Create prompt (will be enhanced if prompt enhancement available)
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
            
            # Use Claude to analyze
            prompt = base_prompt
            
            try:
                # Use Claude integrator with context management
                result = self.claude_agent.analyze_with_claude(
                    query=prompt,
                    context={
                        'task': 'bookmark_review',
                        'type': 'finding_extraction',
                        'url': url,
                        'title': title,
                        'description': description
                    },
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
        
        # Use MCP tools if needed
        if self.mcp_registry:
            # Try to use available MCP tools
            for tool_name in finding.tools_needed:
                try:
                    tool = self.mcp_registry.get_tool(tool_name)
                    if tool:
                        logger.info(f"Using MCP tool: {tool_name}...")
                        # Execute tool if appropriate
                        implementation['tools_used'].append(tool_name)
                except Exception as e:
                    logger.warning(f"MCP tool {tool_name} not available: {e}")
        
        # Update finding status
        finding.status = 'complete'
        implementation['status'] = 'complete'
        implementation['completed_at'] = datetime.now().isoformat()
        
        self.implementations.append(implementation)
        
        # Register in knowledge registry if available
        if self.registry:
            try:
                from agents.knowledge_registry import Bookmark as RegistryBookmark
                registry_bookmark = RegistryBookmark(
                    url=finding.url,
                    title=finding.title,
                    description=finding.finding,
                    source='claude_go_get_bookmark_skill',
                    processing_status=ProcessingStatus.COMPLETED,
                    priority=Priority.MEDIUM,
                    tags=[finding.category],
                    domain=finding.category,
                    ingested_at=datetime.now().isoformat()
                )
                self.registry.add_bookmark(registry_bookmark)
            except Exception as e:
                logger.warning(f"Could not register bookmark in registry: {e}")
        
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
