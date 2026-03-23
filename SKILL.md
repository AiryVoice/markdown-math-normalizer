---
name: markdown-math-normalizer
description: Normalize and validate Markdown files that contain LaTeX math. Use by default whenever Codex generates, rewrites, expands, translates, or edits `.md` content that includes formulas, equations, theorem notation, derivations, scientific notation, or any inline or block math. Also use when formulas render incorrectly, delimiters are mixed, math is wrapped in code fences, `\\(...\\)` or `\\[...\\]` should be converted, or Markdown math needs consistency before previewing, publishing, or further editing.
---

# Markdown Math Normalizer

Normalize Markdown math conservatively. Prefer fixes that improve renderer compatibility without rewriting prose or changing mathematical meaning.

## Workflow

1. Identify the target `.md` files and inspect whether the problem is delimiter-related, code-fence-related, or renderer-related.
2. Read [references/rules.md](C:/Users/Administrator/.codex/skills/markdown-math-normalizer/references/rules.md) when deciding whether a transformation is safe.
3. Run `scripts/normalize_markdown_math.py` in `--check` mode first when multiple files are involved.
4. Run the script without `--check` to apply deterministic fixes.
5. Review the diff for ambiguous cases the script intentionally leaves untouched.
6. If rendering is still broken, explain whether the remaining issue is likely due to the Markdown renderer lacking KaTeX/MathJax support rather than malformed source.

## Script

Use the bundled script for repeatable cleanup:

```powershell
python C:\Users\Administrator\.codex\skills\markdown-math-normalizer\scripts\normalize_markdown_math.py --check path\to\file.md
python C:\Users\Administrator\.codex\skills\markdown-math-normalizer\scripts\normalize_markdown_math.py path\to\file.md
python C:\Users\Administrator\.codex\skills\markdown-math-normalizer\scripts\normalize_markdown_math.py docs\a.md docs\b.md
```

The script performs these safe transformations:

- Convert fenced `math` or `latex` blocks into `$$ ... $$`
- Convert `\(...\)` into `$...$`
- Convert `\[...\]` into `$$ ... $$`
- Normalize one-line `$$ formula $$` blocks into a multi-line block
- Preserve ordinary code fences and non-math content

## Manual Rules

Apply manual edits only after the script if the file still has problems.

- Keep inline math as `$...$`
- Keep display math as a standalone `$$` block on its own lines
- Do not place formulas inside regular code fences unless the user explicitly wants source examples
- Do not guess missing braces, missing command names, or mathematically ambiguous content
- Prefer reporting unsupported renderer issues over inventing LaTeX repairs

## Limits

This skill does not attempt semantic LaTeX repair. It will not infer intended formulas from broken fragments such as unmatched `{`, missing `\frac` arguments, or prose that accidentally contains dollar signs.
