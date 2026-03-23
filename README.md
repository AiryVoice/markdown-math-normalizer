# markdown-math-normalizer

Codex skill for normalizing Markdown LaTeX math delimiters and display blocks.

## What it does

- Converts `\(...\)` to `$...$`
- Converts `\[...\]` to `$$ ... $$`
- Converts fenced `math` or `latex` blocks into display math blocks
- Expands one-line `$$ formula $$` blocks into multiline display math
- Preserves ordinary code fences and non-math content

## Install

1. Download or clone this repository.
2. Copy it to your Codex skills directory:
   - Windows: `%USERPROFILE%\.codex\skills\markdown-math-normalizer`
   - macOS/Linux: `~/.codex/skills/markdown-math-normalizer`
3. Restart Codex.

## Usage

Mention the skill explicitly, or ask Codex to normalize Markdown math formatting.

Example prompts:

- `Use markdown-math-normalizer to fix this Markdown file.`
- `Normalize the LaTeX math delimiters in this .md document.`
- `Convert \(...\) and \[...\] into Markdown-compatible math blocks.`

## Repository layout

- `SKILL.md`: trigger metadata and workflow
- `scripts/normalize_markdown_math.py`: deterministic normalization script
- `references/rules.md`: manual decision rules
- `agents/openai.yaml`: UI metadata

## Notes

This skill focuses on safe formatting normalization. It does not attempt semantic LaTeX repair for ambiguous or broken formulas.
