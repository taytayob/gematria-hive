#!/usr/bin/env python3
"""
Knowledge Registry CLI

Purpose: Command-line interface for managing the knowledge registry
- View Claude skills and tools
- Check processing status
- View domains and foundations
- List git repositories and URLs
- Get prioritization sequences

Usage:
    python registry_cli.py [command] [options]

Commands:
    summary          - Show summary statistics
    skills           - List all Claude skills
    domains          - List all domains with foundations
    bookmarks        - List all bookmarks/URLs
    git              - List all git repositories
    queue            - Show processing queue
    unprocessed      - Show unprocessed items
    priority         - Show prioritization sequence
    export           - Export Claude skills for upload
"""

import sys
import json
from pathlib import Path
from typing import Optional

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.knowledge_registry import (
    get_registry,
    ProcessingStatus,
    Priority,
    DomainCategory
)


def print_summary():
    """Print summary statistics"""
    registry = get_registry()
    summary = registry.get_summary()
    
    print("\n" + "=" * 60)
    print("KNOWLEDGE REGISTRY SUMMARY")
    print("=" * 60)
    print(f"Total Claude Skills: {summary['total_claude_skills']}")
    print(f"Total Domains: {summary['total_domains']}")
    print(f"Total Bookmarks: {summary['total_bookmarks']}")
    print(f"Total Git Repos: {summary['total_git_repos']}")
    print(f"\nProcessing Queue Size: {summary['processing_queue_size']}")
    print("\nUnprocessed Items:")
    print(f"  - Bookmarks: {summary['unprocessed']['bookmarks']}")
    print(f"  - Domains: {summary['unprocessed']['domains']}")
    print(f"  - Git Repos: {summary['unprocessed']['git_repos']}")
    print(f"  - Claude Skills: {summary['unprocessed']['claude_skills']}")
    print("=" * 60 + "\n")


def print_skills():
    """Print all Claude skills"""
    registry = get_registry()
    
    print("\n" + "=" * 60)
    print("CLAUDE SKILLS & TOOLS")
    print("=" * 60)
    
    for name, skill in registry.claude_skills.items():
        print(f"\n📋 {skill.name}")
        print(f"   Description: {skill.description}")
        print(f"   Status: {skill.status.value}")
        if skill.export_path:
            print(f"   Export Path: {skill.export_path}")
        if skill.file_path:
            print(f"   File Path: {skill.file_path}")
        if skill.tags:
            print(f"   Tags: {', '.join(skill.tags)}")
        if skill.last_updated:
            print(f"   Last Updated: {skill.last_updated}")
    
    print("\n" + "=" * 60 + "\n")


def print_domains():
    """Print all domains with foundations"""
    registry = get_registry()
    
    print("\n" + "=" * 60)
    print("DOMAINS & FOUNDATIONS")
    print("=" * 60)
    
    # Group by category
    by_category = {}
    for name, domain in registry.domains.items():
        cat = domain.category.value
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(domain)
    
    for category, domains in sorted(by_category.items()):
        print(f"\n📂 {category.upper()}")
        print("-" * 60)
        
        for domain in sorted(domains, key=lambda d: d.priority.value):
            print(f"\n  🔷 {domain.name}")
            print(f"     Foundation: {domain.foundation}")
            print(f"     Description: {domain.description}")
            print(f"     Status: {domain.processing_status.value}")
            print(f"     Priority: {domain.priority.value}")
            if domain.related_domains:
                print(f"     Related: {', '.join(domain.related_domains)}")
            if domain.libraries:
                print(f"     Libraries: {', '.join(domain.libraries)}")
            if domain.data_sources:
                print(f"     Data Sources: {', '.join(domain.data_sources)}")
    
    print("\n" + "=" * 60 + "\n")


def print_bookmarks():
    """Print all bookmarks/URLs"""
    registry = get_registry()
    
    print("\n" + "=" * 60)
    print("BOOKMARKS & URLs")
    print("=" * 60)
    
    if not registry.bookmarks:
        print("\nNo bookmarks registered yet.")
    else:
        # Group by status
        by_status = {}
        for url, bookmark in registry.bookmarks.items():
            status = bookmark.processing_status.value
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(bookmark)
        
        for status, bookmarks in sorted(by_status.items()):
            print(f"\n📌 {status.upper()}")
            print("-" * 60)
            
            for bookmark in sorted(bookmarks, key=lambda b: b.priority.value):
                print(f"\n  🔗 {bookmark.url}")
                if bookmark.title:
                    print(f"     Title: {bookmark.title}")
                if bookmark.description:
                    print(f"     Description: {bookmark.description[:100]}...")
                print(f"     Priority: {bookmark.priority.value}")
                if bookmark.source:
                    print(f"     Source: {bookmark.source}")
                if bookmark.tags:
                    print(f"     Tags: {', '.join(bookmark.tags)}")
                if bookmark.domain:
                    print(f"     Domain: {bookmark.domain}")
    
    print("\n" + "=" * 60 + "\n")


def print_git_repos():
    """Print all git repositories"""
    registry = get_registry()
    
    print("\n" + "=" * 60)
    print("GIT REPOSITORIES")
    print("=" * 60)
    
    # Group by phase
    by_phase = {}
    for name, repo in registry.git_repos.items():
        phase = repo.integration_phase or "Unassigned"
        if phase not in by_phase:
            by_phase[phase] = []
        by_phase[phase].append(repo)
    
    for phase, repos in sorted(by_phase.items()):
        print(f"\n📦 {phase}")
        print("-" * 60)
        
        for repo in sorted(repos, key=lambda r: r.priority.value):
            print(f"\n  🔷 {repo.name}")
            print(f"     URL: {repo.url}")
            print(f"     Purpose: {repo.purpose}")
            print(f"     Status: {repo.status.value}")
            print(f"     Priority: {repo.priority.value}")
            if repo.branch:
                print(f"     Branch: {repo.branch}")
            if repo.last_synced:
                print(f"     Last Synced: {repo.last_synced}")
            if repo.notes:
                print(f"     Notes: {repo.notes}")
    
    print("\n" + "=" * 60 + "\n")


def print_queue(priority_filter: Optional[str] = None):
    """Print processing queue"""
    registry = get_registry()
    
    priority = None
    if priority_filter:
        try:
            priority = Priority(priority_filter.lower())
        except ValueError:
            print(f"Invalid priority: {priority_filter}")
            return
    
    queue = registry.get_processing_queue(priority)
    
    print("\n" + "=" * 60)
    print("PROCESSING QUEUE")
    if priority:
        print(f"Filter: {priority.value.upper()}")
    print("=" * 60)
    
    if not queue:
        print("\nNo items in processing queue.")
    else:
        # Group by priority
        by_priority = {}
        for item in queue:
            pri = item.priority.value
            if pri not in by_priority:
                by_priority[pri] = []
            by_priority[pri].append(item)
        
        for pri, items in sorted(by_priority.items()):
            print(f"\n🔴 {pri.upper()}")
            print("-" * 60)
            
            for item in items:
                print(f"  • [{item.item_type}] {item.item_id}")
                print(f"    Status: {item.status.value}")
                if item.dependencies:
                    print(f"    Dependencies: {', '.join(item.dependencies)}")
    
    print("\n" + "=" * 60 + "\n")


def print_unprocessed():
    """Print unprocessed items"""
    registry = get_registry()
    unprocessed = registry.get_unprocessed_items()
    
    print("\n" + "=" * 60)
    print("UNPROCESSED ITEMS")
    print("=" * 60)
    
    for item_type, items in unprocessed.items():
        if items:
            print(f"\n📋 {item_type.upper()}")
            print("-" * 60)
            for item in items:
                if item_type == "bookmarks":
                    print(f"  🔗 {item['url']}")
                    if item.get('title'):
                        print(f"     Title: {item['title']}")
                    print(f"     Priority: {item['priority']}")
                    if item.get('source'):
                        print(f"     Source: {item['source']}")
                elif item_type == "domains":
                    print(f"  🔷 {item['name']}")
                    print(f"     Category: {item['category']}")
                    print(f"     Priority: {item['priority']}")
                elif item_type == "git_repos":
                    print(f"  📦 {item['name']}")
                    print(f"     URL: {item['url']}")
                    print(f"     Priority: {item['priority']}")
                    if item.get('phase'):
                        print(f"     Phase: {item['phase']}")
                elif item_type == "claude_skills":
                    print(f"  📋 {item['name']}")
                    print(f"     Description: {item['description']}")
                    if item.get('export_path'):
                        print(f"     Export Path: {item['export_path']}")
        else:
            print(f"\n✅ {item_type.upper()}: All processed!")
    
    print("\n" + "=" * 60 + "\n")


def print_priority_sequence():
    """Print prioritization sequence"""
    registry = get_registry()
    sequence = registry.get_prioritization_sequence()
    
    print("\n" + "=" * 60)
    print("PRIORITIZATION SEQUENCE")
    print("=" * 60)
    
    print("\n🔧 BACKEND SEQUENCE")
    print("-" * 60)
    for i, item in enumerate(sequence["backend"], 1):
        print(f"  {i}. {item}")
    
    print("\n📚 LIBRARIES SEQUENCE")
    print("-" * 60)
    for i, item in enumerate(sequence["libraries"], 1):
        repo = registry.git_repos.get(item)
        if repo:
            phase = repo.integration_phase or "Unassigned"
            print(f"  {i}. {item} ({phase}, {repo.priority.value})")
        else:
            print(f"  {i}. {item}")
    
    print("\n📊 DATA SEQUENCE")
    print("-" * 60)
    if sequence["data"]:
        for i, url in enumerate(sequence["data"][:20], 1):  # Limit to first 20
            bookmark = registry.bookmarks.get(url)
            if bookmark:
                print(f"  {i}. {url} ({bookmark.priority.value})")
            else:
                print(f"  {i}. {url}")
        if len(sequence["data"]) > 20:
            print(f"  ... and {len(sequence['data']) - 20} more")
    else:
        print("  No unprocessed data items")
    
    print("\n" + "=" * 60 + "\n")


def export_claude_skills():
    """Export Claude skills for upload"""
    registry = get_registry()
    output_file = registry.export_claude_skills()
    print(f"\n✅ Exported Claude skills to {output_file}\n")


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        "summary": print_summary,
        "skills": print_skills,
        "domains": print_domains,
        "bookmarks": print_bookmarks,
        "git": print_git_repos,
        "queue": lambda: print_queue(sys.argv[2] if len(sys.argv) > 2 else None),
        "unprocessed": print_unprocessed,
        "priority": print_priority_sequence,
        "export": export_claude_skills
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()

