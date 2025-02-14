"""
Test suite for the Python source code linter.
Tests various linting rules including:
- Unused imports
- Unused variables
- Duplicate dictionary keys

Each test case is designed to verify specific linting scenarios.
"""

from solution import Linter

def test_linter():
    """Run a series of test cases through the linter and display results."""
    
    # Test cases with expected violations
    test_cases = [
        # Test 1: Basic unused imports and variables
        """
# Test 1: Basic unused imports and variables
import os  # unused
import sys
from math import pi, sqrt  # sqrt unused

def func(unused_param):
    x = 10
    y = 20  # unused
    return x
""",
        # Test 2: Duplicate dictionary keys
        """
# Test 2: Duplicate dictionary keys
data = {
    "a": 1,
    "b": 2,
    "a": 3,  # duplicate
    "c": {
        "x": 1,
        "x": 2  # duplicate nested
    }
}
""",
        # Test 3: Complex scoping and shadowing
        """
# Test 3: Scope handling
x = 10  # unused global
def outer(a):  # unused param
    y = 20  # unused
    def inner(b):
        z = 30
        return z
    return inner

result = outer(5)
""",
        # Test 4: Comprehensions and generator expressions
        """
# Test 4: Comprehensions
squares = [x*x for x in range(10)]  # x is used
data = {
    k: v  # k is used, v is used
    for k, v in [('a', 1), ('a', 2)]  # duplicate key
}
"""
    ]

    linter = Linter()
    
    for i, source in enumerate(test_cases, 1):
        print(f"\nTest Case {i}")
        print("=" * 50)
        print("Source Code:")
        print("-" * 40)
        print(source.strip())
        print("-" * 40)
        
        errors = linter.lint(source)
        if errors:
            print("\nLinting Errors:")
            # Group errors by rule type
            by_rule = {}
            for error in errors:
                by_rule.setdefault(error.rule_name, []).append(error)
            
            for rule_name, rule_errors in by_rule.items():
                print(f"\n{rule_name.replace('_', ' ').title()}:")
                for error in rule_errors:
                    print(f"  Line {error.line_number}: {error.message}")
        else:
            print("\nNo linting errors found!")
        print("\n" + "="*50)

if __name__ == "__main__":
    test_linter()
