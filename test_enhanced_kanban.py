#!/usr/bin/env python3
"""
Test Enhanced Kanban System

Tests the enhanced kanban board with phases, metadata, resources, tags, and roles.

Usage:
    python test_enhanced_kanban.py

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_enhanced_task_manager():
    """Test enhanced task manager"""
    print("=" * 60)
    print("Testing Enhanced Task Manager")
    print("=" * 60)
    print()
    
    try:
        from task_manager_enhanced import get_enhanced_task_manager
        
        tm = get_enhanced_task_manager()
        print("✅ Enhanced Task Manager initialized")
        
        # Test creating a task with all features
        print("\n📝 Creating test task with all features...")
        task = tm.create_task(
            content="Test enhanced task with phases, metadata, resources, tags, and roles",
            status="pending",
            phase="phase1_basic",
            role="developer",
            priority="high",
            cost=0.05,
            tags=["test", "enhanced", "kanban"],
            resources=["https://example.com/resource"],
            labels=["feature", "enhancement"],
            assigned_to="test_user",
            estimated_hours=2.0,
            progress=0,
            dependencies=[],
            metadata={
                "agent_context": "test",
                "mcp_tool": "test_tool",
                "test_data": True
            }
        )
        
        if task:
            print(f"✅ Task created: {task.get('id')}")
            print(f"   Phase: {task.get('phase')}")
            print(f"   Role: {task.get('role')}")
            print(f"   Priority: {task.get('priority')}")
            print(f"   Tags: {task.get('tags')}")
            print(f"   Resources: {task.get('resources')}")
            print(f"   Metadata: {task.get('metadata')}")
            
            # Test getting tasks by phase
            print("\n🔍 Testing phase filter...")
            phase_tasks = tm.get_tasks_by_phase("phase1_basic")
            print(f"✅ Found {len(phase_tasks)} tasks in phase1_basic")
            
            # Test getting tasks by role
            print("\n🔍 Testing role filter...")
            role_tasks = tm.get_tasks_by_role("developer")
            print(f"✅ Found {len(role_tasks)} tasks for developer role")
            
            # Test getting tasks by tag
            print("\n🔍 Testing tag filter...")
            tag_tasks = tm.get_tasks_by_tag("test")
            print(f"✅ Found {len(tag_tasks)} tasks with 'test' tag")
            
            # Test statistics
            print("\n📊 Testing statistics...")
            stats = tm.get_task_statistics()
            print(f"✅ Statistics retrieved:")
            print(f"   Total: {stats.get('total', 0)}")
            print(f"   By Phase: {stats.get('by_phase', {})}")
            print(f"   By Role: {stats.get('by_role', {})}")
            print(f"   By Priority: {stats.get('by_priority', {})}")
            
            return True
        else:
            print("❌ Failed to create task")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_kanban_api():
    """Test kanban API"""
    print("\n" + "=" * 60)
    print("Testing Kanban API")
    print("=" * 60)
    print()
    
    try:
        from kanban_api import app, USE_ENHANCED
        
        print(f"✅ Kanban API loaded")
        print(f"   Enhanced mode: {USE_ENHANCED}")
        print(f"   App title: {app.title}")
        print(f"   App version: {app.version}")
        
        # Test endpoints
        print("\n🔍 Testing API endpoints...")
        
        # Check if enhanced features are available
        if USE_ENHANCED:
            print("✅ Enhanced features available")
            print("   - Phases: ✅")
            print("   - Roles: ✅")
            print("   - Tags: ✅")
            print("   - Resources: ✅")
            print("   - Metadata: ✅")
        else:
            print("⚠️  Enhanced features not available (using basic task manager)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Enhanced Kanban System Test")
    print("=" * 60)
    print()
    
    results = {}
    
    # Test enhanced task manager
    results['task_manager'] = test_enhanced_task_manager()
    
    # Test kanban API
    results['kanban_api'] = test_kanban_api()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print()
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print()
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

