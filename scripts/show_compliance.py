#!/usr/bin/env python3
"""
Show Compliance - Display Compliance Reports

Purpose: Display compliance reports in terminal showing planned vs actual execution,
violations, missing items, and suggestions.

Usage:
    python scripts/show_compliance.py [--days DAYS]

Author: Gematria Hive Team
Date: January 6, 2025
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.compliance_auditor import get_compliance_auditor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def print_compliance_report(report):
    """Print compliance report in formatted way"""
    print("\n" + "=" * 70)
    print("Compliance Report")
    print("=" * 70)
    print(f"Period: {report['period_days']} days")
    print(f"Generated at: {report['generated_at']}")
    print(f"Total tasks: {report['total_tasks']}")
    print(f"Average compliance score: {report['average_compliance_score']:.2f}")
    
    # Compliance distribution
    print("\n" + "-" * 70)
    print("Compliance Distribution:")
    print("-" * 70)
    dist = report['compliance_distribution']
    print(f"  Excellent (>=0.9): {dist['excellent']}")
    print(f"  Good (0.7-0.9):    {dist['good']}")
    print(f"  Fair (0.5-0.7):    {dist['fair']}")
    print(f"  Poor (<0.5):       {dist['poor']}")
    
    # Violations
    print("\n" + "-" * 70)
    print("Violations:")
    print("-" * 70)
    violations = report['violations']
    print(f"Total violations: {violations['total']}")
    print("\nViolations by type:")
    for vtype, count in violations['by_type'].items():
        print(f"  {vtype}: {count}")
    
    # Violation details
    if violations['details']:
        print("\nViolation details:")
        for vtype, vlist in violations['details'].items():
            print(f"\n  {vtype}:")
            for i, violation in enumerate(vlist[:5], 1):  # Show first 5
                print(f"    {i}. {violation.get('message', 'No message')}")
            if len(vlist) > 5:
                print(f"    ... and {len(vlist) - 5} more")
    
    # Patterns
    if report['patterns']:
        print("\n" + "-" * 70)
        print("Patterns Detected:")
        print("-" * 70)
        for pattern in report['patterns'][:10]:  # Show first 10
            print(f"  {pattern.get('type', 'unknown')}: {pattern.get('description', 'No description')}")
    
    # Suggestions
    if report['suggestions']:
        print("\n" + "-" * 70)
        print("Suggestions:")
        print("-" * 70)
        for i, suggestion in enumerate(report['suggestions'], 1):
            print(f"  {i}. {suggestion}")
    
    print("\n" + "=" * 70)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Show compliance reports")
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to include in report (default: 7)"
    )
    
    args = parser.parse_args()
    
    print("Initializing Compliance Auditor...")
    
    try:
        compliance_auditor = get_compliance_auditor()
    except Exception as e:
        logger.error(f"Error initializing compliance auditor: {e}")
        print(f"Error: {e}")
        return 1
    
    # Generate and display report
    report = compliance_auditor.generate_compliance_report(days=args.days)
    print_compliance_report(report)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

