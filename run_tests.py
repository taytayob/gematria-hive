#!/usr/bin/env python3
"""
Run All Tests

Comprehensive test runner for Gematria Hive.
"""

import sys
import os
import unittest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def discover_and_run_tests():
    """Discover and run all tests"""
    # Discover tests
    loader = unittest.TestLoader()
    start_dir = project_root / 'tests'
    suite = loader.discover(str(start_dir), pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = discover_and_run_tests()
    sys.exit(exit_code)

