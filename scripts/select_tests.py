
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TESTS = ROOT / "tests"


def git_changed_files():
    """Find changed files compared with the previous commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def imports_in(path):
    """Extract local Python imports from a source file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return set()

    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split(".")[0])

    return found


def module_name(path):
    return path.stem


def main():
    if not SRC.exists() or not TESTS.exists():
        print(" ".join(str(p.relative_to(ROOT)) for p in sorted(TESTS.glob("test_*.py"))))
        return

    changed = git_changed_files()
    all_tests = sorted(TESTS.glob("test_*.py"))

    # When Git cannot identify the diff, run every test.
    if changed is None:
        print(" ".join(str(p.relative_to(ROOT)) for p in all_tests))
        return

    changed_sources = {
        (ROOT / name).resolve()
        for name in changed
        if name.startswith("src/") and name.endswith(".py")
    }

    # Changes outside src can affect the whole project.
    if not changed_sources:
        print(" ".join(str(p.relative_to(ROOT)) for p in all_tests))
        return

    source_files = sorted(SRC.glob("*.py"))
    imports = {p.resolve(): imports_in(p) for p in source_files}
    impact = set(changed_sources)

    # If module A imports module B, a change to B can affect A.
    changed = True
    while changed:
        changed = False
        impacted_names = {module_name(p) for p in impact}
        for path, dependencies in imports.items():
            if path not in impact and dependencies & impacted_names:
                impact.add(path)
                changed = True

    impacted_names = {module_name(p) for p in impact}
    selected = []

    for test in all_tests:
        test_imports = imports_in(test)
        if test_imports & impacted_names:
            selected.append(test)

    # Never silently skip tests if no match is found.
    if not selected:
        selected = all_tests

    print(" ".join(str(p.relative_to(ROOT)) for p in selected))


if __name__ == "__main__":
    main()
