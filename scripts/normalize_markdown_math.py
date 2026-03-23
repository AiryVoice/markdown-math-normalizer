#!/usr/bin/env python3
"""Normalize common AI-generated Markdown math issues."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

MATH_FENCE_RE = re.compile(
    r"(^|\n)```(?:math|latex)\s*\n(.*?)(?:\n)?```(?=\n|$)",
    re.DOTALL | re.IGNORECASE,
)
INLINE_PAREN_RE = re.compile(r"\\\((.+?)\\\)")
BLOCK_BRACKET_RE = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)
INLINE_DOUBLE_DOLLAR_LINE_RE = re.compile(r"(?m)^([ \t]*)\$\$\s*(.+?)\s*\$\$([ \t]*)$")


def convert_math_fences(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        prefix = match.group(1)
        body = match.group(2).strip("\n")
        return f"{prefix}$$\n{body}\n$$"

    return MATH_FENCE_RE.sub(repl, text)


def convert_inline_paren(text: str) -> str:
    return INLINE_PAREN_RE.sub(lambda m: f"${m.group(1).strip()}$", text)


def convert_block_bracket(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        body = match.group(1).strip("\n")
        return f"$$\n{body}\n$$"

    return BLOCK_BRACKET_RE.sub(repl, text)


def expand_single_line_display_blocks(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        indent = match.group(1)
        body = match.group(2).strip()
        trailing = match.group(3)
        suffix = trailing if trailing else ""
        return f"{indent}$$\n{indent}{body}\n{indent}$${suffix}"

    return INLINE_DOUBLE_DOLLAR_LINE_RE.sub(repl, text)


def split_by_fences(text: str) -> list[tuple[bool, str]]:
    segments: list[tuple[bool, str]] = []
    lines = text.splitlines(keepends=True)
    current: list[str] = []
    in_fence = False

    for line in lines:
        if line.lstrip().startswith("```"):
            current.append(line)
            if in_fence:
                segments.append((True, "".join(current)))
                current = []
                in_fence = False
            else:
                if len(current) > 1:
                    before = "".join(current[:-1])
                    if before:
                        segments.append((False, before))
                    current = [current[-1]]
                in_fence = True
            continue
        current.append(line)

    if current:
        segments.append((in_fence, "".join(current)))
    return segments


def normalize_text(text: str) -> str:
    # Convert explicit math fences before generic fence splitting so they are not protected.
    text = convert_math_fences(text)
    parts = split_by_fences(text)
    normalized: list[str] = []

    for is_fence, part in parts:
        if is_fence:
            normalized.append(part)
            continue
        part = convert_block_bracket(part)
        part = convert_inline_paren(part)
        part = expand_single_line_display_blocks(part)
        normalized.append(part)

    return "".join(normalized)


def process_file(path: Path, check_only: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    normalized = normalize_text(original)
    changed = normalized != original

    if check_only:
        if changed:
            diff = difflib.unified_diff(
                original.splitlines(),
                normalized.splitlines(),
                fromfile=str(path),
                tofile=f"{path} (normalized)",
                lineterm="",
            )
            sys.stdout.write("\n".join(diff) + "\n")
        return changed

    if changed:
        path.write_text(normalized, encoding="utf-8", newline="")
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize Markdown math delimiters.")
    parser.add_argument("paths", nargs="+", help="Markdown files to normalize")
    parser.add_argument("--check", action="store_true", help="Show diff without modifying files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    changed_any = False

    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            print(f"Missing file: {path}", file=sys.stderr)
            return 2
        if path.suffix.lower() != ".md":
            print(f"Skip non-Markdown file: {path}", file=sys.stderr)
            continue
        changed = process_file(path, check_only=args.check)
        changed_any = changed_any or changed
        status = "would change" if args.check and changed else "changed" if changed else "unchanged"
        print(f"{path}: {status}")

    return 1 if args.check and changed_any else 0


if __name__ == "__main__":
    raise SystemExit(main())
