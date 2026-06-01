import ast
import sys
from pathlib import Path

_STDLIB_ROOTS: frozenset[str] = frozenset(sys.stdlib_module_names)


class ImportCollector(ast.NodeVisitor):
    def __init__(self) -> None:
        self.detected: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.detected.add(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self.detected.add(node.module)
            for alias in node.names:
                if alias.name != "*":
                    self.detected.add(f"{node.module}.{alias.name}")


def analyze_file(filepath: str) -> list[str]:
    try:
        content = Path(filepath).read_text(encoding="utf-8")
        tree = ast.parse(content, filename=filepath)
        collector = ImportCollector()
        collector.visit(tree)
        return sorted(collector.detected)
    except Exception:
        return []


def analyze_stdlib_only(filepath: str) -> list[str]:
    return [m for m in analyze_file(filepath) if m.split(".")[0] in _STDLIB_ROOTS]


def analyze_third_party(filepath: str) -> list[str]:
    return [m for m in analyze_file(filepath) if m.split(".")[0] not in _STDLIB_ROOTS]
