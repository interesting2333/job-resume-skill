#!/usr/bin/env python3
"""Create a compact inventory of a software project for resume-oriented analysis."""

from __future__ import annotations

import argparse
import os
from collections import Counter
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "out",
    ".next",
    ".nuxt",
    ".venv",
    "venv",
    "env",
    "coverage",
}

IMPORTANT_NAMES = {
    "readme.md",
    "readme.txt",
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "go.mod",
    "go.sum",
    "pyproject.toml",
    "requirements.txt",
    "poetry.lock",
    "cargo.toml",
    "dockerfile",
    "docker-compose.yml",
    "compose.yml",
    "makefile",
    ".github/workflows",
}

LANG_BY_EXT = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript/React",
    ".ts": "TypeScript",
    ".tsx": "TypeScript/React",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".cs": "C#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".sql": "SQL",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".md": "Markdown",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".toml": "TOML",
    ".xml": "XML",
}


def should_ignore_dir(name: str) -> bool:
    return name.lower() in IGNORE_DIRS


def is_important(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix().lower()
    return path.name.lower() in IMPORTANT_NAMES or rel in IMPORTANT_NAMES or rel.startswith(".github/workflows/")


def walk_project(root: Path, max_files: int) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    important: list[Path] = []

    for current, dirs, filenames in os.walk(root):
        dirs[:] = [d for d in dirs if not should_ignore_dir(d)]
        current_path = Path(current)
        for filename in filenames:
            path = current_path / filename
            files.append(path)
            if is_important(path, root):
                important.append(path)
            if len(files) >= max_files:
                return files, important

    return files, important


def top_dirs(files: list[Path], root: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in files:
        rel = path.relative_to(root)
        top = rel.parts[0] if len(rel.parts) > 1 else "."
        counts[top] += 1
    return counts


def render(root: Path, files: list[Path], important: list[Path]) -> str:
    ext_counts = Counter(path.suffix.lower() or "[no extension]" for path in files)
    lang_counts = Counter(LANG_BY_EXT.get(path.suffix.lower(), "Other") for path in files)
    dirs = top_dirs(files, root)

    lines: list[str] = []
    lines.append(f"# Project Inventory: {root}")
    lines.append("")
    lines.append(f"- Scanned files: {len(files)}")
    lines.append("")

    lines.append("## Likely Languages")
    for language, count in lang_counts.most_common(12):
        lines.append(f"- {language}: {count}")
    lines.append("")

    lines.append("## File Extensions")
    for ext, count in ext_counts.most_common(15):
        lines.append(f"- {ext}: {count}")
    lines.append("")

    lines.append("## Top Directories")
    for directory, count in dirs.most_common(20):
        lines.append(f"- {directory}: {count}")
    lines.append("")

    lines.append("## Important Files")
    if important:
        for path in sorted(important, key=lambda p: p.relative_to(root).as_posix().lower())[:80]:
            lines.append(f"- {path.relative_to(root).as_posix()}")
    else:
        lines.append("- No common manifest or README files found.")
    lines.append("")

    lines.append("## Suggested Next Reads")
    suggestions = sorted(important, key=lambda p: p.relative_to(root).as_posix().lower())[:12]
    if suggestions:
        for path in suggestions:
            lines.append(f"- {path.relative_to(root).as_posix()}")
    else:
        for path in sorted(files, key=lambda p: p.relative_to(root).as_posix().lower())[:12]:
            lines.append(f"- {path.relative_to(root).as_posix()}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a project directory for key-point extraction.")
    parser.add_argument("path", help="Project directory")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"Path not found: {root}")
        return 2
    if not root.is_dir():
        print(f"Path is not a directory: {root}")
        return 2

    files, important = walk_project(root, args.max_files)
    print(render(root, files, important))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
