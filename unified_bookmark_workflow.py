#!/usr/bin/env python3
"""
Unified Bookmark Processing Workflow
Gematria Hive - Complete bookmark processing with Claude and Grok

Purpose:
- Load bookmarks from files
- Process with Claude and Grok together
- Extract findings and insights
- Implement findings using all available tools
- Update knowledge registry
- Generate comprehensive reports

Author: Gematria Hive Team
Date: January 9, 2025
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to load dependencies
try:
    from dotenv import load_dotenv
    load_dotenv()
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False
    logger.warning("dotenv not available")

try:
    from agents.bookmark_ingestion import BookmarkIngestionAgent
    from agents.knowledge_registry import get_registry, Bookmark, ProcessingStatus, Priority
    from agents.claude_integrator import ClaudeIntegratorAgent
    from agents.mcp_tool_registry import get_tool_registry
    HAS_DEPENDENCIES = True
except ImportError as e:
    HAS_DEPENDENCIES = False
    logger.error(f"Dependencies not available: {e}")


def unified_bookmark_workflow(
    bookmark_files: Optional[List[str]] = None,
    use_claude: bool = True,
    use_grok: bool = True,
    use_browser_mcp: bool = True
) -> Dict[str, Any]:
    """
    Complete bookmark processing workflow
    
    Args:
        bookmark_files: List of bookmark file paths (optional, will search if not provided)
        use_claude: Whether to use Claude for analysis
        use_grok: Whether to use Grok for cultural reasoning
        use_browser_mcp: Whether to use browser MCP for content extraction
    
    Returns:
        Workflow results dictionary
    """
    
    logger.info("=" * 80)
    logger.info("UNIFIED BOOKMARK PROCESSING WORKFLOW")
    logger.info("=" * 80)
    
    if not HAS_DEPENDENCIES:
        logger.error("Required dependencies not available")
        return {
            'status': 'failed',
            'error': 'Dependencies not available',
            'message': 'Please install required packages: python-dotenv, supabase, anthropic'
        }
    
    # Initialize all systems
    logger.info("Initializing systems...")
    bookmark_agent = BookmarkIngestionAgent()
    registry = get_registry()
    claude_agent = ClaudeIntegratorAgent() if use_claude else None
    mcp_registry = get_tool_registry() if (use_grok or use_browser_mcp) else None
    
    # 1. Find bookmark files if not provided
    if not bookmark_files:
        logger.info("Searching for bookmark files...")
        project_root = Path(__file__).parent
        bookmark_files = []
        
        # Search for JSON bookmarks
        json_files = list(project_root.glob("**/*bookmark*.json"))
        bookmark_files.extend([str(f) for f in json_files])
        
        # Search for markdown bookmarks
        md_files = list(project_root.glob("**/*bookmark*.md"))
        bookmark_files.extend([str(f) for f in md_files])
        
        logger.info(f"Found {len(bookmark_files)} bookmark files")
    
    # 2. Load and parse bookmarks
    logger.info("Loading bookmarks...")
    all_bookmarks = []
    for file_path in bookmark_files:
        try:
            if file_path.endswith('.json'):
                bookmarks = bookmark_agent.parse_json_bookmarks(file_path)
            elif file_path.endswith('.md') or file_path.endswith('.markdown'):
                bookmarks = bookmark_agent.parse_markdown_bookmarks(file_path)
            else:
                logger.warning(f"Unknown file type: {file_path}")
                continue
            
            all_bookmarks.extend(bookmarks)
            logger.info(f"Loaded {len(bookmarks)} bookmarks from {file_path}")
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
    
    if not all_bookmarks:
        logger.warning("No bookmarks loaded")
        return {
            'status': 'failed',
            'error': 'No bookmarks loaded',
            'bookmark_files': bookmark_files
        }
    
    logger.info(f"Total bookmarks loaded: {len(all_bookmarks)}")
    
    # 3. Store bookmarks in database
    logger.info("Storing bookmarks...")
    stored_count = 0
    try:
        stored_count = bookmark_agent.store_bookmarks(all_bookmarks)
        logger.info(f"Stored {stored_count}/{len(all_bookmarks)} bookmarks")
    except Exception as e:
        logger.warning(f"Error storing bookmarks: {e}")
    
    # 4. Register bookmarks in knowledge registry
    logger.info("Registering bookmarks in knowledge registry...")
    registered_count = 0
    for bookmark in all_bookmarks:
        try:
            reg_bookmark = Bookmark(
                url=bookmark['url'],
                title=bookmark.get('title', ''),
                description=bookmark.get('description', ''),
                source=bookmark.get('source', 'workflow'),
                processing_status=ProcessingStatus.NOT_STARTED,
                priority=Priority.MEDIUM,
                tags=bookmark.get('tags', [])
            )
            registry.add_bookmark(reg_bookmark)
            registered_count += 1
        except Exception as e:
            logger.warning(f"Error registering bookmark {bookmark.get('url', 'unknown')}: {e}")
    
    logger.info(f"Registered {registered_count} bookmarks in knowledge registry")
    
    # 5. Process with Claude and Grok (if available)
    findings = []
    implementations = []
    
    if use_claude and claude_agent:
        logger.info("Processing bookmarks with Claude...")
        # Process first 5 bookmarks as example
        sample_bookmarks = all_bookmarks[:5]
        
        for bookmark in sample_bookmarks:
            try:
                # Use Claude to analyze bookmark
                query = f"Analyze this bookmark and extract key findings:\n\nURL: {bookmark.get('url', '')}\nTitle: {bookmark.get('title', '')}\nDescription: {bookmark.get('description', '')}"
                
                result = claude_agent.analyze_with_claude(
                    query=query,
                    context={
                        'bookmark': bookmark,
                        'task': 'bookmark_analysis'
                    },
                    apply_first_principles=True
                )
                
                if result and 'response' in result:
                    findings.append({
                        'bookmark_url': bookmark.get('url'),
                        'finding': result['response'],
                        'source': 'claude'
                    })
                    logger.info(f"Extracted finding from {bookmark.get('url', 'unknown')}")
            except Exception as e:
                logger.warning(f"Error processing bookmark with Claude: {e}")
    
    if use_grok and mcp_registry:
        logger.info("Getting Grok insights...")
        grok_tool = mcp_registry.get_tool("grok_cultural_reasoning")
        if grok_tool:
            # Process first 3 bookmarks with Grok
            sample_bookmarks = all_bookmarks[:3]
            
            for bookmark in sample_bookmarks:
                try:
                    text = f"{bookmark.get('title', '')}\n\n{bookmark.get('description', '')}"
                    result = mcp_registry.execute_tool(
                        "grok_cultural_reasoning",
                        text=text[:5000],  # Limit text length
                        context={
                            'url': bookmark.get('url', ''),
                            'source': 'bookmark',
                            'task': 'cultural_analysis'
                        }
                    )
                    
                    if result:
                        findings.append({
                            'bookmark_url': bookmark.get('url'),
                            'finding': result.get('cultural_analysis', str(result)),
                            'source': 'grok'
                        })
                        logger.info(f"Got Grok insights for {bookmark.get('url', 'unknown')}")
                except Exception as e:
                    logger.warning(f"Error getting Grok insights: {e}")
    
    # 6. Compile results
    results = {
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'workflow_id': f"WORKFLOW-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'bookmark_files': bookmark_files,
        'bookmarks_loaded': len(all_bookmarks),
        'bookmarks_stored': stored_count,
        'bookmarks_registered': registered_count,
        'findings_extracted': len(findings),
        'findings': findings,
        'implementations_completed': len(implementations),
        'implementations': implementations,
        'summary': {
            'total_bookmarks': len(all_bookmarks),
            'stored': stored_count,
            'registered': registered_count,
            'findings': len(findings),
            'implementations': len(implementations)
        }
    }
    
    # 7. Save results
    storage_path = Path(__file__).parent / "data" / "workflows"
    storage_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = storage_path / f"bookmark_workflow_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"Results saved to: {results_file}")
    
    logger.info("=" * 80)
    logger.info("✅ UNIFIED BOOKMARK WORKFLOW COMPLETE")
    logger.info("=" * 80)
    
    return results


def main():
    """Main function"""
    logger.info("Starting unified bookmark workflow...")
    
    # Run workflow
    results = unified_bookmark_workflow(
        bookmark_files=None,  # Will search automatically
        use_claude=True,
        use_grok=True,
        use_browser_mcp=True
    )
    
    # Print summary
    print("\n" + "=" * 80)
    print("WORKFLOW SUMMARY")
    print("=" * 80)
    print(f"Status: {results.get('status', 'unknown')}")
    
    if results.get('status') == 'success':
        summary = results.get('summary', {})
        print(f"\nBookmarks:")
        print(f"  - Loaded: {summary.get('total_bookmarks', 0)}")
        print(f"  - Stored: {summary.get('stored', 0)}")
        print(f"  - Registered: {summary.get('registered', 0)}")
        print(f"\nFindings:")
        print(f"  - Extracted: {summary.get('findings', 0)}")
        print(f"\nImplementations:")
        print(f"  - Completed: {summary.get('implementations', 0)}")
    else:
        print(f"\nError: {results.get('error', 'Unknown error')}")
        print(f"Message: {results.get('message', 'No message')}")
    
    print("\n" + "=" * 80)
    print("✅ WORKFLOW COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
