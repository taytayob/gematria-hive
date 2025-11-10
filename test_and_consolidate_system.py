#!/usr/bin/env python3
"""
Test and Consolidate System
Gematria Hive - Test all systems and provide consolidated report

This script tests all available systems and generates a comprehensive report
without requiring all dependencies to be installed.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Setup basic logging
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Test results
TEST_RESULTS = {
    'timestamp': datetime.now().isoformat(),
    'systems': {},
    'errors': {},
    'warnings': {},
    'recommendations': []
}

def test_import(module_name: str, description: str) -> Dict[str, Any]:
    """Test if a module can be imported"""
    result = {
        'status': 'unknown',
        'message': '',
        'details': {}
    }
    
    try:
        module = __import__(module_name, fromlist=[''])
        result['status'] = 'success'
        result['message'] = f'{description} imported successfully'
        result['details'] = {
            'module': module_name,
            'has_module': True
        }
        logger.info(f"✅ {description}")
    except ImportError as e:
        result['status'] = 'error'
        result['message'] = f'{description} import failed: {str(e)}'
        result['details'] = {
            'module': module_name,
            'error': str(e)
        }
        logger.warning(f"⚠️ {description}: {str(e)}")
    except Exception as e:
        result['status'] = 'error'
        result['message'] = f'{description} error: {str(e)}'
        result['details'] = {
            'module': module_name,
            'error': str(e)
        }
        logger.error(f"❌ {description}: {str(e)}")
    
    return result

def test_file_exists(file_path: str, description: str) -> Dict[str, Any]:
    """Test if a file exists"""
    result = {
        'status': 'unknown',
        'message': '',
        'details': {}
    }
    
    path = Path(file_path)
    if path.exists():
        result['status'] = 'success'
        result['message'] = f'{description} exists'
        result['details'] = {
            'path': str(path),
            'size': path.stat().st_size,
            'exists': True
        }
        logger.info(f"✅ {description}")
    else:
        result['status'] = 'error'
        result['message'] = f'{description} not found'
        result['details'] = {
            'path': str(path),
            'exists': False
        }
        logger.warning(f"⚠️ {description} not found")
    
    return result

def test_env_var(var_name: str, description: str) -> Dict[str, Any]:
    """Test if an environment variable is set"""
    result = {
        'status': 'unknown',
        'message': '',
        'details': {}
    }
    
    value = os.getenv(var_name)
    if value:
        result['status'] = 'success'
        result['message'] = f'{description} is configured'
        result['details'] = {
            'var': var_name,
            'configured': True,
            'length': len(value)
        }
        logger.info(f"✅ {description}")
    else:
        result['status'] = 'warning'
        result['message'] = f'{description} not configured'
        result['details'] = {
            'var': var_name,
            'configured': False
        }
        logger.warning(f"⚠️ {description} not configured")
    
    return result

def main():
    """Main test function"""
    
    print("=" * 80)
    print("GEMATRIA HIVE - SYSTEM TEST AND CONSOLIDATION")
    print("=" * 80)
    print()
    
    # Test core systems
    print("Testing Core Systems...")
    print("-" * 80)
    
    # Test imports
    TEST_RESULTS['systems']['knowledge_registry'] = test_import(
        'agents.knowledge_registry', 'Knowledge Registry'
    )
    
    TEST_RESULTS['systems']['bookmark_ingestion'] = test_import(
        'agents.bookmark_ingestion', 'Bookmark Ingestion Agent'
    )
    
    TEST_RESULTS['systems']['claude_integrator'] = test_import(
        'agents.claude_integrator', 'Claude Integrator Agent'
    )
    
    TEST_RESULTS['systems']['twitter_fetcher'] = test_import(
        'agents.twitter_fetcher', 'Grok/Twitter Agent'
    )
    
    TEST_RESULTS['systems']['mcp_tool_registry'] = test_import(
        'agents.mcp_tool_registry', 'MCP Tool Registry'
    )
    
    TEST_RESULTS['systems']['gematria_engine'] = test_import(
        'core.gematria_engine', 'Gematria Engine'
    )
    
    TEST_RESULTS['systems']['sacred_geometry_engine'] = test_import(
        'core.sacred_geometry_engine', 'Sacred Geometry Engine'
    )
    
    TEST_RESULTS['systems']['domain_expansion_engine'] = test_import(
        'core.domain_expansion_engine', 'Domain Expansion Engine'
    )
    
    print()
    
    # Test missing files
    print("Testing Missing Files...")
    print("-" * 80)
    
    missing_files = [
        ('agents/enhanced_claude_integrator.py', 'Enhanced Claude Integrator'),
        ('global_knowledge_registry_and_report_card.py', 'Global Knowledge Registry'),
        ('global_resource_tracking_and_workflow_system.py', 'Resource Tracking System'),
        ('prompt_enhancement_and_writer_system.py', 'Prompt Enhancement System'),
        ('comprehensive_html_reporting_and_indexing_system.py', 'HTML Reporting System'),
        ('claude_go_get_bookmark_skill.py', 'Claude Go Get Bookmark Skill'),
    ]
    
    for file_path, description in missing_files:
        result = test_file_exists(file_path, description)
        if result['status'] == 'error':
            TEST_RESULTS['errors'][file_path] = result['message']
            TEST_RESULTS['recommendations'].append(f"Create {file_path}")
    
    print()
    
    # Test environment variables
    print("Testing Environment Variables...")
    print("-" * 80)
    
    env_vars = [
        ('ANTHROPIC_API_KEY', 'Claude API Key'),
        ('GROK_API_KEY', 'Grok API Key'),
        ('SUPABASE_URL', 'Supabase URL'),
        ('SUPABASE_KEY', 'Supabase Key'),
    ]
    
    for var_name, description in env_vars:
        result = test_env_var(var_name, description)
        if result['status'] == 'warning':
            TEST_RESULTS['warnings'][var_name] = result['message']
            TEST_RESULTS['recommendations'].append(f"Set {var_name} in .env")
    
    print()
    
    # Test knowledge registry if available
    if TEST_RESULTS['systems']['knowledge_registry']['status'] == 'success':
        print("Testing Knowledge Registry...")
        print("-" * 80)
        
        try:
            from agents.knowledge_registry import get_registry
            registry = get_registry()
            
            summary = registry.get_summary()
            TEST_RESULTS['knowledge_registry_summary'] = summary
            
            print(f"✅ Total Claude Skills: {summary.get('total_claude_skills', 0)}")
            print(f"✅ Total Domains: {summary.get('total_domains', 0)}")
            print(f"✅ Total Bookmarks: {summary.get('total_bookmarks', 0)}")
            print(f"✅ Total Git Repos: {summary.get('total_git_repos', 0)}")
            print(f"✅ Unprocessed Items: {summary.get('unprocessed', {})}")
            
        except Exception as e:
            logger.error(f"Error testing knowledge registry: {e}")
            TEST_RESULTS['errors']['knowledge_registry_test'] = str(e)
    
    print()
    
    # Generate report
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    success_count = sum(1 for s in TEST_RESULTS['systems'].values() if s['status'] == 'success')
    error_count = sum(1 for s in TEST_RESULTS['systems'].values() if s['status'] == 'error')
    warning_count = len(TEST_RESULTS['warnings'])
    
    print(f"\n✅ Successful: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"⚠️ Warnings: {warning_count}")
    
    if TEST_RESULTS['recommendations']:
        print(f"\n📋 Recommendations ({len(TEST_RESULTS['recommendations'])}):")
        for i, rec in enumerate(TEST_RESULTS['recommendations'], 1):
            print(f"  {i}. {rec}")
    
    # Save results
    results_file = Path('data/system_test_results.json')
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(TEST_RESULTS, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to: {results_file}")
    print()
    
    return TEST_RESULTS

if __name__ == "__main__":
    main()
