#!/usr/bin/env python3
"""
Configure Standards - Interactive CLI Tool

Purpose: Interactive CLI tool for configuring standards, templates, and compliance rules.

Usage:
    python scripts/configure_standards.py

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.standards_manager import get_standards_manager
from agents.template_manager import get_template_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def print_menu():
    """Print main menu"""
    print("\n" + "=" * 70)
    print("Standards Configuration Tool")
    print("=" * 70)
    print("1. View System Standards")
    print("2. View Agent Standards")
    print("3. Update System Standards")
    print("4. Update Agent Standards")
    print("5. View Templates")
    print("6. Create/Update Template")
    print("7. View Compliance Rules")
    print("8. Exit")
    print("=" * 70)


def view_system_standards(standards_manager):
    """View system standards"""
    print("\n" + "=" * 70)
    print("System Standards")
    print("=" * 70)
    standards = standards_manager.get_system_standards()
    print(json.dumps(standards, indent=2))


def view_agent_standards(standards_manager):
    """View agent standards"""
    print("\n" + "=" * 70)
    print("Agent Standards")
    print("=" * 70)
    agent_name = input("Enter agent name (or 'all' for all agents): ").strip()
    
    if agent_name == "all":
        agent_standards = standards_manager.agent_standards
        for name, std in agent_standards.items():
            print(f"\n{name}:")
            print(json.dumps(std, indent=2))
    else:
        std = standards_manager.get_agent_standards(agent_name)
        if std:
            print(json.dumps(std, indent=2))
        else:
            print(f"No standards found for agent: {agent_name}")


def update_system_standards(standards_manager):
    """Update system standards"""
    print("\n" + "=" * 70)
    print("Update System Standards")
    print("=" * 70)
    print("Current system standards:")
    current = standards_manager.get_system_standards()
    print(json.dumps(current, indent=2))
    
    print("\nEnter updates as JSON (or 'cancel' to cancel):")
    updates_str = input().strip()
    
    if updates_str.lower() == "cancel":
        print("Cancelled")
        return
    
    try:
        updates = json.loads(updates_str)
        standards_manager.update_system_standards(updates)
        print("System standards updated successfully")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")


def update_agent_standards(standards_manager):
    """Update agent standards"""
    print("\n" + "=" * 70)
    print("Update Agent Standards")
    print("=" * 70)
    agent_name = input("Enter agent name: ").strip()
    
    current = standards_manager.get_agent_standards(agent_name)
    if current:
        print(f"Current standards for {agent_name}:")
        print(json.dumps(current, indent=2))
    else:
        print(f"No existing standards for {agent_name}")
        current = {}
    
    print("\nEnter updates as JSON (or 'cancel' to cancel):")
    updates_str = input().strip()
    
    if updates_str.lower() == "cancel":
        print("Cancelled")
        return
    
    try:
        updates = json.loads(updates_str)
        new_standards = {**current, **updates}
        standards_manager.save_agent_standards(agent_name, new_standards)
        print(f"Agent standards for {agent_name} updated successfully")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")


def view_templates(template_manager):
    """View templates"""
    print("\n" + "=" * 70)
    print("Templates")
    print("=" * 70)
    print("1. SOP Templates")
    print("2. Prompt Templates")
    print("3. Execution Templates")
    choice = input("Select option: ").strip()
    
    if choice == "1":
        print("\nSOP Templates:")
        print(json.dumps(template_manager.sop_templates, indent=2))
    elif choice == "2":
        print("\nPrompt Templates:")
        print(json.dumps(template_manager.prompt_templates, indent=2))
    elif choice == "3":
        print("\nExecution Templates:")
        print(json.dumps(template_manager.execution_templates, indent=2))
    else:
        print("Invalid option")


def view_compliance_rules(standards_manager):
    """View compliance rules"""
    print("\n" + "=" * 70)
    print("Compliance Rules")
    print("=" * 70)
    rules = standards_manager.get_compliance_rules()
    print(json.dumps(rules, indent=2))


def main():
    """Main function"""
    print("Initializing Standards Configuration Tool...")
    
    try:
        standards_manager = get_standards_manager()
        template_manager = get_template_manager()
    except Exception as e:
        logger.error(f"Error initializing managers: {e}")
        print(f"Error: {e}")
        return 1
    
    while True:
        print_menu()
        choice = input("Select option: ").strip()
        
        if choice == "1":
            view_system_standards(standards_manager)
        elif choice == "2":
            view_agent_standards(standards_manager)
        elif choice == "3":
            update_system_standards(standards_manager)
        elif choice == "4":
            update_agent_standards(standards_manager)
        elif choice == "5":
            view_templates(template_manager)
        elif choice == "6":
            print("Template creation/update not yet implemented")
        elif choice == "7":
            view_compliance_rules(standards_manager)
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid option")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

