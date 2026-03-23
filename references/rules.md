# Markdown Math Normalization Rules

Use these rules when deciding whether to apply a manual fix after the bundled script runs.

## Safe conversions

- Convert `\(...\)` to `$...$` when the delimiters are balanced on one line.
- Convert `\[...\]` to a `$$` block when the delimiters are balanced.
- Convert fenced blocks labelled `math` or `latex` to `$$` blocks.
- Reformat `$$ x^2 $$` to:

```md
$$
x^2
$$
```

## Leave unchanged

- Dollar signs used for currency or shell variables outside obvious math contexts.
- Broken LaTeX commands where intent is unclear.
- Mixed prose and math inside one delimiter pair if changing delimiters could alter spacing or punctuation.
- Content inside ordinary fenced code blocks.

## Diagnostic hints

- If source looks correct but preview is wrong, suspect missing KaTeX/MathJax support first.
- GitHub, many static-site generators, and many note apps differ in math support.
- If a viewer only supports `$...$` and `$$...$$`, normalize toward those delimiters.
