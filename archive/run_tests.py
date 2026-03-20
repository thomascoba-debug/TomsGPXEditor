#!/usr/bin/env python3
"""
Test runner for GPX Editor
"""

import sys
import os
import unittest
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from tests.test_framework import run_tests


def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Run GPX Editor tests")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--pattern", "-p",
        default="test_*.py",
        help="Test file pattern (default: test_*.py)"
    )
    parser.add_argument(
        "--module", "-m",
        help="Run specific test module (e.g., test_recent_files)"
    )
    
    args = parser.parse_args()
    
    # Change to tests directory
    tests_dir = Path(__file__).parent / "tests"
    os.chdir(tests_dir)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    
    if args.module:
        # Run specific module
        suite = loader.loadTestsFromName(args.module)
    else:
        # Discover all tests
        start_dir = "."
        pattern = args.pattern
        suite = loader.discover(start_dir, pattern=pattern)
    
    # Configure test runner
    verbosity = 2 if args.verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity, buffer=True)
    
    # Run tests
    print(f"Running tests with pattern: {args.pattern}")
    print("=" * 70)
    
    result = runner.run(suite)
    
    # Print summary
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    # Return exit code
    success = result.wasSuccessful()
    print(f"\n{'SUCCESS' if success else 'FAILURE'}")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
