import ast
from typing import Any

class UnusedImportsRule(BaseLintRule):
    def __init__(self, rule_name: str) -> None:
        super().__init__(rule_name)
        self.imports = {}  # name -> line_number
        self.used_names = set()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.asname or alias.name
            self.imports[name] = node.lineno

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            name = alias.asname or alias.name
            if name != '*':
                self.imports[name] = node.lineno

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def check(self, tree: ast.AST) -> list[LintError]:
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
    def __init__(self, rule_name: str) -> None:
        super().__init__(rule_name)
        self.scopes = [{}]  # Stack of scopes
        self.used_names = [set()]  # Stack of used names per scope

    def push_scope(self):
        self.scopes.append({})
        self.used_names.append(set())

    def pop_scope(self):
        scope = self.scopes.pop()
        used = self.used_names.pop()
        for name, (line, _) in scope.items():
            if name not in used and not name.startswith('_'):
                self.errors.append(
                    LintError(
                        rule_name=self.rule_name,
                        message=f'Variable "{name}" is unused',
                        line_number=line
                    )
                )

    def add_definition(self, name: str, lineno: int, is_param: bool = False):
        if not name.startswith('_'):
            self.scopes[-1][name] = (lineno, is_param)

    def mark_used(self, name: str):
        for used in reversed(self.used_names):
            used.add(name)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Store):
            self.add_definition(node.id, node.lineno)
        elif isinstance(node.ctx, ast.Load):
            self.mark_used(node.id)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.push_scope()
        for arg in node.args.args:
            self.add_definition(arg.arg, node.lineno, True)
        self.generic_visit(node)
        self.pop_scope()

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()

    def visit_SetComp(self, node: ast.SetComp) -> None:
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()

    def visit_DictComp(self, node: ast.DictComp) -> None:
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()

    def check(self, tree: ast.AST) -> list[LintError]:
        self.visit(tree)
        while len(self.scopes) > 0:
            self.pop_scope()
        return self.errors
