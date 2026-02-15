#!/usr/bin/env python3
"""
Tests for GM Tools - Tri-Check System

Tests the tri_check_result method which provides narrative guidelines
for the Fate Tri-Check System based on the number of successes (0-3).
"""

import sys
import os
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from gm_tools import GMTools


def capture_output(func, *args, **kwargs):
    """Helper function to capture stdout"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        func(*args, **kwargs)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    
    return output


def test_tri_check_full_success():
    """Test tri_check_result with 3 successes (full success)"""
    tools = GMTools()
    output = capture_output(tools.tri_check_result, 3)
    
    # Check for expected content
    assert "TRI-CHECK OUTCOME" in output
    assert "Full Success (3/3)" in output
    assert "accomplish your goal brilliantly" in output
    assert "exceeds expectations" in output
    print("✓ Test passed: Full Success (3/3)")


def test_tri_check_major_success():
    """Test tri_check_result with 2 successes (major success)"""
    tools = GMTools()
    output = capture_output(tools.tri_check_result, 2)
    
    # Check for expected content
    assert "TRI-CHECK OUTCOME" in output
    assert "Major Success (2/3)" in output
    assert "succeed, but with a small cost" in output
    assert "minor consequence" in output
    print("✓ Test passed: Major Success (2/3)")


def test_tri_check_partial_success():
    """Test tri_check_result with 1 success (partial success)"""
    tools = GMTools()
    output = capture_output(tools.tri_check_result, 1)
    
    # Check for expected content
    assert "TRI-CHECK OUTCOME" in output
    assert "Partial Success (1/3)" in output
    assert "only partly succeed" in output
    assert "major complication" in output
    print("✓ Test passed: Partial Success (1/3)")


def test_tri_check_failure():
    """Test tri_check_result with 0 successes (failure)"""
    tools = GMTools()
    output = capture_output(tools.tri_check_result, 0)
    
    # Check for expected content
    assert "TRI-CHECK OUTCOME" in output
    assert "Failure (0/3)" in output
    assert "do not succeed" in output
    assert "story moves forward" in output
    print("✓ Test passed: Failure (0/3)")


def test_tri_check_boundary_cases():
    """Test tri_check_result with edge cases"""
    tools = GMTools()
    
    # Test with values greater than 3 (should be treated as full success)
    output = capture_output(tools.tri_check_result, 4)
    assert "Full Success (3/3)" in output
    
    output = capture_output(tools.tri_check_result, 10)
    assert "Full Success (3/3)" in output
    
    # Test with negative values (should be treated as failure)
    output = capture_output(tools.tri_check_result, -1)
    assert "Failure (0/3)" in output
    
    print("✓ Test passed: Boundary cases")


def test_tri_check_formatting():
    """Test that output is properly formatted"""
    tools = GMTools()
    output = capture_output(tools.tri_check_result, 2)
    
    # Check for proper formatting elements
    assert "="*70 in output
    assert "\n" in output
    print("✓ Test passed: Output formatting")


def run_all_tests():
    """Run all test cases"""
    print("="*70)
    print("RUNNING GM TOOLS TRI-CHECK TESTS")
    print("="*70)
    print()
    
    test_tri_check_full_success()
    test_tri_check_major_success()
    test_tri_check_partial_success()
    test_tri_check_failure()
    test_tri_check_boundary_cases()
    test_tri_check_formatting()
    
    print()
    print("="*70)
    print("ALL TESTS PASSED")
    print("="*70)


if __name__ == "__main__":
    run_all_tests()
