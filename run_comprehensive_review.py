#!/usr/bin/env python3
"""
Comprehensive System Review - Simplified Runner
Runs comprehensive review with graceful dependency handling
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to load dependencies
try:
    from dotenv import load_dotenv
    load_dotenv()
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False
    logger.warning("dotenv not available, skipping .env loading")

# Import systems with graceful fallback
try:
    from agents.knowledge_registry import KnowledgeRegistry, get_registry
    HAS_KNOWLEDGE_REGISTRY = True
except ImportError as e:
    HAS_KNOWLEDGE_REGISTRY = False
    logger.warning(f"Knowledge registry not available: {e}")

try:
    from agents.claude_integrator import ClaudeIntegratorAgent
    HAS_CLAUDE = True
except ImportError as e:
    HAS_CLAUDE = False
    logger.warning(f"Claude integrator not available: {e}")

try:
    from agents.bookmark_ingestion import BookmarkIngestionAgent
    HAS_BOOKMARK = True
except ImportError as e:
    HAS_BOOKMARK = False
    logger.warning(f"Bookmark ingestion not available: {e}")

try:
    from agents.mcp_tool_registry import MCPToolRegistry, get_tool_registry
    HAS_MCP = True
except ImportError as e:
    HAS_MCP = False
    logger.warning(f"MCP tool registry not available: {e}")


def review_file_system():
    """Review file system structure"""
    logger.info("Reviewing file system...")
    
    project_root = Path(__file__).parent
    results = {
        'project_root': str(project_root),
        'directories': {},
        'files': {},
        'scripts': []
    }
    
    # Check key directories
    key_dirs = ['agents', 'core', 'docs', 'migrations', 'config', 'data']
    for dir_name in key_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            files = list(dir_path.glob('*.py'))
            results['directories'][dir_name] = {
                'exists': True,
                'python_files': len(files)
            }
        else:
            results['directories'][dir_name] = {'exists': False}
    
    # Check key files
    key_files = [
        'app.py',
        'run_agents.py',
        'internal_api.py',
        'kanban_api.py',
        'gematria_calculator.py'
    ]
    for file_name in key_files:
        file_path = project_root / file_name
        results['files'][file_name] = file_path.exists()
    
    # Find all Python scripts
    scripts = list(project_root.glob('*.py'))
    results['scripts'] = [s.name for s in scripts if s.is_file()]
    
    return results


def review_claude_skills():
    """Review Claude skills status"""
    logger.info("Reviewing Claude skills...")
    
    results = {
        'available': False,
        'total_skills': 0,
        'skills': {},
        'errors': []
    }
    
    if HAS_KNOWLEDGE_REGISTRY:
        try:
            registry = get_registry()
            skills = registry.claude_skills
            results['available'] = True
            results['total_skills'] = len(skills)
            results['skills'] = {
                name: {
                    'name': skill.name,
                    'description': skill.description,
                    'status': skill.status.value if hasattr(skill.status, 'value') else str(skill.status),
                    'export_path': skill.export_path
                }
                for name, skill in skills.items()
            }
        except Exception as e:
            results['errors'].append(str(e))
    else:
        results['errors'].append("Knowledge registry not available")
    
    return results


def review_bookmarks():
    """Review bookmarks status"""
    logger.info("Reviewing bookmarks...")
    
    project_root = Path(__file__).parent
    results = {
        'bookmark_agent_available': HAS_BOOKMARK,
        'bookmark_files': [],
        'registered_bookmarks': 0,
        'errors': []
    }
    
    # Find bookmark files
    bookmark_files = list(project_root.glob('**/*bookmark*.json'))
    bookmark_files.extend(list(project_root.glob('**/*bookmark*.md')))
    results['bookmark_files'] = [str(f) for f in bookmark_files]
    
    # Check knowledge registry
    if HAS_KNOWLEDGE_REGISTRY:
        try:
            registry = get_registry()
            bookmarks = registry.bookmarks
            results['registered_bookmarks'] = len(bookmarks)
        except Exception as e:
            results['errors'].append(str(e))
    
    return results


def review_knowledge_base():
    """Review knowledge base status"""
    logger.info("Reviewing knowledge base...")
    
    results = {
        'available': False,
        'summary': {},
        'errors': []
    }
    
    if HAS_KNOWLEDGE_REGISTRY:
        try:
            registry = get_registry()
            summary = registry.get_summary()
            results['available'] = True
            results['summary'] = summary
        except Exception as e:
            results['errors'].append(str(e))
    else:
        results['errors'].append("Knowledge registry not available")
    
    return results


def review_mcp_tools():
    """Review MCP tools status"""
    logger.info("Reviewing MCP tools...")
    
    results = {
        'available': False,
        'total_tools': 0,
        'tools_by_category': {},
        'errors': []
    }
    
    if HAS_MCP:
        try:
            registry = get_tool_registry()
            tools_info = registry.list_all_tools()
            results['available'] = True
            results['total_tools'] = tools_info.get('total_tools', 0)
            results['tools_by_category'] = tools_info.get('tools_by_category', {})
        except Exception as e:
            results['errors'].append(str(e))
    else:
        results['errors'].append("MCP tool registry not available")
    
    return results


def review_environment():
    """Review environment variables"""
    logger.info("Reviewing environment...")
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY',
        'ANTHROPIC_API_KEY'
    ]
    
    results = {
        'required_vars': {},
        'optional_vars': {}
    }
    
    for var in required_vars:
        value = os.getenv(var)
        results['required_vars'][var] = {
            'set': value is not None,
            'has_value': bool(value)
        }
    
    optional_vars = [
        'GROK_API_KEY',
        'PERPLEXITY_API_KEY',
        'OPENAI_API_KEY'
    ]
    
    for var in optional_vars:
        value = os.getenv(var)
        results['optional_vars'][var] = {
            'set': value is not None,
            'has_value': bool(value)
        }
    
    return results


def generate_report():
    """Generate comprehensive report"""
    logger.info("=" * 80)
    logger.info("COMPREHENSIVE SYSTEM REVIEW")
    logger.info("=" * 80)
    
    # Run all reviews
    file_system = review_file_system()
    claude_skills = review_claude_skills()
    bookmarks = review_bookmarks()
    knowledge_base = review_knowledge_base()
    mcp_tools = review_mcp_tools()
    environment = review_environment()
    
    # Build report
    report = {
        'timestamp': datetime.now().isoformat(),
        'review_id': f"REVIEW-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'file_system': file_system,
        'claude_skills': claude_skills,
        'bookmarks': bookmarks,
        'knowledge_base': knowledge_base,
        'mcp_tools': mcp_tools,
        'environment': environment,
        'summary': {
            'claude_skills_available': claude_skills['available'],
            'total_claude_skills': claude_skills['total_skills'],
            'bookmark_agent_available': bookmarks['bookmark_agent_available'],
            'bookmark_files_found': len(bookmarks['bookmark_files']),
            'registered_bookmarks': bookmarks['registered_bookmarks'],
            'knowledge_base_available': knowledge_base['available'],
            'mcp_tools_available': mcp_tools['available'],
            'total_mcp_tools': mcp_tools['total_tools']
        }
    }
    
    # Save report
    storage_path = Path(__file__).parent / "data" / "system_reviews"
    storage_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = storage_path / f"comprehensive_review_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Generate markdown report
    md_file = storage_path / f"comprehensive_review_{timestamp}.md"
    generate_markdown_report(report, md_file)
    
    logger.info(f"Report saved to: {report_file}")
    logger.info(f"Markdown report saved to: {md_file}")
    
    return report


def generate_markdown_report(report: dict, output_file: Path):
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
    lines.append(f"- **Claude Skills Available:** {summary['claude_skills_available']}")
    lines.append(f"- **Total Claude Skills:** {summary['total_claude_skills']}")
    lines.append(f"- **Bookmark Agent Available:** {summary['bookmark_agent_available']}")
    lines.append(f"- **Bookmark Files Found:** {summary['bookmark_files_found']}")
    lines.append(f"- **Registered Bookmarks:** {summary['registered_bookmarks']}")
    lines.append(f"- **Knowledge Base Available:** {summary['knowledge_base_available']}")
    lines.append(f"- **MCP Tools Available:** {summary['mcp_tools_available']}")
    lines.append(f"- **Total MCP Tools:** {summary['total_mcp_tools']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Claude Skills Status")
    lines.append("")
    cs = report['claude_skills']
    if cs['available']:
        lines.append(f"- **Total Skills:** {cs['total_skills']}")
        for name, skill in cs['skills'].items():
            lines.append(f"  - **{skill['name']}:** {skill['status']}")
            lines.append(f"    - Description: {skill['description']}")
    else:
        lines.append("- **Status:** Not available")
        for error in cs['errors']:
            lines.append(f"  - Error: {error}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Bookmarks Status")
    lines.append("")
    bm = report['bookmarks']
    lines.append(f"- **Bookmark Agent Available:** {bm['bookmark_agent_available']}")
    lines.append(f"- **Bookmark Files Found:** {len(bm['bookmark_files'])}")
    if bm['bookmark_files']:
        lines.append("  - Files:")
        for file in bm['bookmark_files']:
            lines.append(f"    - {file}")
    lines.append(f"- **Registered Bookmarks:** {bm['registered_bookmarks']}")
    if bm['errors']:
        lines.append("  - Errors:")
        for error in bm['errors']:
            lines.append(f"    - {error}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Knowledge Base Status")
    lines.append("")
    kb = report['knowledge_base']
    if kb['available']:
        summary = kb['summary']
        lines.append(f"- **Total Domains:** {summary.get('total_domains', 0)}")
        lines.append(f"- **Total Bookmarks:** {summary.get('total_bookmarks', 0)}")
        lines.append(f"- **Total Git Repos:** {summary.get('total_git_repos', 0)}")
        lines.append(f"- **Total Claude Skills:** {summary.get('total_claude_skills', 0)}")
        unprocessed = summary.get('unprocessed', {})
        if any(unprocessed.values()):
            lines.append("  - Unprocessed Items:")
            for item_type, count in unprocessed.items():
                if count > 0:
                    lines.append(f"    - {item_type}: {count}")
    else:
        lines.append("- **Status:** Not available")
        for error in kb['errors']:
            lines.append(f"  - Error: {error}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## MCP Tools Status")
    lines.append("")
    mcp = report['mcp_tools']
    if mcp['available']:
        lines.append(f"- **Total Tools:** {mcp['total_tools']}")
        for category, count in mcp['tools_by_category'].items():
            lines.append(f"  - {category}: {count} tools")
    else:
        lines.append("- **Status:** Not available")
        for error in mcp['errors']:
            lines.append(f"  - Error: {error}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Environment Variables")
    lines.append("")
    env = report['environment']
    lines.append("### Required Variables")
    for var, status in env['required_vars'].items():
        status_icon = "✅" if status['set'] and status['has_value'] else "❌"
        lines.append(f"- {status_icon} **{var}:** {'Set' if status['set'] else 'Not set'}")
    lines.append("")
    lines.append("### Optional Variables")
    for var, status in env['optional_vars'].items():
        status_icon = "✅" if status['set'] and status['has_value'] else "⚠️"
        lines.append(f"- {status_icon} **{var}:** {'Set' if status['set'] else 'Not set'}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## File System")
    lines.append("")
    fs = report['file_system']
    lines.append(f"- **Project Root:** {fs['project_root']}")
    lines.append("")
    lines.append("### Directories")
    for dir_name, dir_info in fs['directories'].items():
        if dir_info.get('exists'):
            lines.append(f"- ✅ **{dir_name}:** {dir_info.get('python_files', 0)} Python files")
        else:
            lines.append(f"- ❌ **{dir_name}:** Not found")
    lines.append("")
    lines.append("### Key Files")
    for file_name, exists in fs['files'].items():
        status_icon = "✅" if exists else "❌"
        lines.append(f"- {status_icon} **{file_name}**")
    lines.append("")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    """Main function"""
    logger.info("Starting comprehensive system review...")
    
    try:
        report = generate_report()
        
        # Print summary
        print("\n" + "=" * 80)
        print("COMPREHENSIVE SYSTEM REVIEW SUMMARY")
        print("=" * 80)
        summary = report['summary']
        print(f"\nClaude Skills: {'✅ Available' if summary['claude_skills_available'] else '❌ Not available'} ({summary['total_claude_skills']} skills)")
        print(f"Bookmark Agent: {'✅ Available' if summary['bookmark_agent_available'] else '❌ Not available'}")
        print(f"Bookmark Files: {summary['bookmark_files_found']} found, {summary['registered_bookmarks']} registered")
        print(f"Knowledge Base: {'✅ Available' if summary['knowledge_base_available'] else '❌ Not available'}")
        print(f"MCP Tools: {'✅ Available' if summary['mcp_tools_available'] else '❌ Not available'} ({summary['total_mcp_tools']} tools)")
        
        print("\n" + "=" * 80)
        print("✅ COMPREHENSIVE REVIEW COMPLETE")
        print("=" * 80)
        
        return report
    except Exception as e:
        logger.error(f"Error during review: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
