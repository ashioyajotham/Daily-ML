"""
Python source code linter implementation that checks for:
1. Unused imports
2. Unused variables
3. Duplicate dictionary keys

The linter uses Python's AST (Abstract Syntax Tree) to analyze source code
and identify potential issues without executing the code.
"""

import ast
from typing import Any
from collections import defaultdict

class LintError:
    """Represents a linting error with its location and description."""
    def __init__(self, rule_name: str, message: str, line_number: int) -> None:
        """
        Args:
            rule_name: Identifier for the rule that was violated
            message: Description of the error
            line_number: Line number where the error occurred
        """
        self.rule_name = rule_name
        self.message = message
        self.line_number = line_number

class BaseLintRule(ast.NodeVisitor):
    """Base class for all linting rules using the visitor pattern."""
    def __init__(self, rule_name: str) -> None:
        """
        Args:
            rule_name: Identifier for this rule
        """
        super().__init__()
        self.errors: list[LintError] = []
        self.rule_name = rule_name

class UnusedImportsRule(BaseLintRule):
    """Detects imports that are never used in the code.
    
    Tracks both direct imports (import x) and from imports (from x import y).
    Handles aliased imports (import x as y) correctly.
    """
    
    def __init__(self, rule_name: str) -> None:
        """Initialize with empty import tracking."""
        super().__init__(rule_name)
        self.reset()

    def reset(self):
        """Reset the rule's state for a new check."""
        self.imports = {}  # Maps imported name -> line number
        self.used_names = set()  # Set of names actually used
        self.errors = []

    def visit_Import(self, node: ast.Import) -> None:
        """Record direct imports like 'import x' or 'import x as y'."""
        for alias in node.names:
            name = alias.asname or alias.name
            self.imports[name] = node.lineno

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Record from-imports like 'from module import x'."""
        for alias in node.names:
            name = alias.asname or alias.name
            if name != '*':
                self.imports[name] = node.lineno

    def visit_Name(self, node: ast.Name) -> None:
        """Track when a name is used in the code."""
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def check(self, tree: ast.AST) -> list[LintError]:
        """Check for unused imports in the AST."""
        self.reset()
        self.visit(tree)
        for name, line in self.imports.items():
            if name not in self.used_names:
                self.errors.append(
                    LintError(
                        rule_name=self.rule_name,
                        message=f'Import "{name}" is unused',
                        line_number=line
                    )
                )
        return self.errors

class UnusedVariablesRule(BaseLintRule):
    """Detects variables that are defined but never used.
    
    Handles multiple scopes (global, function, comprehension),
    ignores names starting with underscore, and tracks variable usage
    across nested scopes.
    """
    
    def __init__(self, rule_name: str) -> None:
        """Initialize with global scope."""
        super().__init__(rule_name)
        self.reset()

    def reset(self):
        """Reset the rule's state for a new check."""
        self.scopes = [{}]
        self.used_names = [set()]
        self.in_function = False
        self.errors = []

    def push_scope(self):
        """Create a new scope for variables (e.g., entering a function)."""
        self.scopes.append({})
        self.used_names.append(set())

    def pop_scope(self):
        """Exit current scope and check for unused variables."""
        if len(self.scopes) > 1:  # Don't pop global scope
            scope = self.scopes.pop()
            used = self.used_names.pop()
            self.check_scope(scope, used)

    def check_scope(self, scope, used):
        """Check for unused variables in a single scope."""
        for name, (line, is_param) in scope.items():
            if name not in used and not name.startswith('_'):
                self.errors.append(
                    LintError(
                        rule_name=self.rule_name,
                        message=f'Variable "{name}" is unused',
                        line_number=line
                    )
                )

    def add_definition(self, name: str, lineno: int, is_param: bool = False):
        """Add a variable definition to the current scope."""
        if not name.startswith('_'):
            self.scopes[-1][name] = (lineno, is_param)

    def mark_used(self, name: str):
        """Mark a variable as used in the current scope."""
        for used in reversed(self.used_names):
            used.add(name)

    def visit_Name(self, node: ast.Name) -> None:
        """Track variable definitions and usages."""
        if isinstance(node.ctx, ast.Store):
            self.add_definition(node.id, node.lineno)
        elif isinstance(node.ctx, ast.Load):
            self.mark_used(node.id)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Handle function definitions and their arguments."""
        self.push_scope()
        for arg in node.args.args:
            self.add_definition(arg.arg, node.lineno, True)
        self.generic_visit(node)
        self.pop_scope()

    def visit_ListComp(self, node: ast.ListComp) -> None:
        """Handle list comprehensions."""
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()

    def visit_SetComp(self, node: ast.SetComp) -> None:
        """Handle set comprehensions."""
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()

    def visit_DictComp(self, node: ast.DictComp) -> None:
        """Handle dictionary comprehensions."""
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        """Handle generator expressions."""
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()

    def check(self, tree: ast.AST) -> list[LintError]:
        """Check for unused variables in the AST."""
        self.reset()
        self.visit(tree)
        # Only process non-global scopes
        while len(self.scopes) > 1:
            self.pop_scope()
        return self.errors

class DuplicateDictKeysRule(BaseLintRule):
    """Detects duplicate keys in dictionary literals.
    
    Handles nested dictionaries and reports line numbers of all duplicates.
    Only checks literal keys (not computed keys).
    """
    
    def visit_Dict(self, node: ast.Dict) -> None:
        """Process a dictionary literal node and check for duplicates."""
        seen = defaultdict(list)
        for key, value in zip(node.keys, node.values):
            if isinstance(key, ast.Constant):
                metadata = {"lineno": key.lineno, "key": key.value}
                seen[key.value].append(metadata)

            if isinstance(value, ast.Dict):
                self.visit(value)

        for key, metadata in seen.items():
            if len(metadata) > 1:
                lines = ", ".join(str(line["lineno"]) for line in metadata)
                self.errors.append(
                    LintError(
                        rule_name=self.rule_name,
                        message=f'Key "{key}" has been repeated on lines {lines}',
                        line_number=metadata[0]["lineno"],
                    )
                )

    def check(self, tree: ast.AST) -> list[LintError]:
        """Check for duplicate dictionary keys in the AST."""
        self.errors = []  # Reset errors before checking
        self.visit(tree)
        return self.errors

class Linter:
    """Main linter class that coordinates all lint rules.
    
    Applies all rules to given source code and collects their results.
    Returns errors sorted by line number.
    """
    
    def __init__(self) -> None:
        """Initialize with default set of rules."""
        self.rules = [
            UnusedImportsRule(rule_name="unused_import"),
            UnusedVariablesRule(rule_name="unused_variable"),
            DuplicateDictKeysRule(rule_name="duplicate_dict_keys"),
        ]

    def lint(self, source_code: str) -> list[LintError]:
        """
        Lint the given source code using all rules.
        
        Args:
            source_code: Python source code to check
            
        Returns:
            List of LintError objects sorted by line number
        """
        tree = ast.parse(source_code)
        errors: list[LintError] = []

        for rule in self.rules:
            errors.extend(rule.check(tree))

        return sorted(errors, key=lambda e: e.line_number)
