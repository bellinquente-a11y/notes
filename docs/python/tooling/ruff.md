---
tags:
  - config
---

# Ruff

Ruff is a fast Python linter and formatter written in Rust. It replaces tools like `flake8`, `isort`, and `black` in a single tool.

## Installation

```bash
poetry add --group dev ruff
```

## Usage

```bash
poetry run ruff check src    # lint
poetry run ruff format src   # format
```

## Rule selection

Ruff only lints with `E` (pycodestyle) and `F` (Pyflakes) by default — the same narrow surface flake8 always covered: unused imports, undefined names, whitespace. That catches almost no real bugs. A CI step running bare `ruff check .` looks like a lint gate but is close to a no-op unless `[tool.ruff.lint]` opts into more rule categories:

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "RET"]
```

| Prefix | Source | Catches |
|--------|--------|---------|
| `E`, `F` | pycodestyle, Pyflakes | style + unused/undefined names (defaults) |
| `I` | isort | import ordering — diff hygiene, fully autofixable |
| `B` | flake8-bugbear | real bug patterns: mutable default args, closures over loop variables, swallowed exceptions |
| `UP` | pyupgrade | modernises syntax for the declared `target-version` (e.g. `Optional[int]` → `int \| None`) |
| `SIM` | flake8-simplify | convoluted-but-working code (redundant `if`/`else`, boolean comparisons) |
| `RET` | flake8-return | inconsistent/unneeded control flow around `return` |

!!! note "select is an allow-list, not a bug scanner by default"
    Each prefix is an opt-in category equivalent to what used to be a separate flake8 plugin — the tool is inert until you choose categories. `B` (bugbear) has the highest signal for catching real bugs; `E`/`F` alone is mostly style.

- Use `ignore` to disable specific rules within a selected category, and `extend-select` (instead of `select`) to add categories on top of a shared/inherited base config.
- Adopting `I`, `UP`, `SIM`, `RET` on an existing codebase: run `ruff check --fix .` first — most of these are autofixable. `B` findings are mostly manual triage since they flag design issues.
- Pin `target-version` (e.g. `target-version = "py312"`) so `UP` only suggests syntax your minimum supported Python actually has.

## Ignoring rules

Three scopes, from broadest to narrowest — pick the narrowest one that fits so the rest of the codebase stays covered:

```toml
[tool.ruff.lint]
ignore = ["E501"]  # project-wide: rule is never useful here (e.g. line length, formatter already wraps)

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]     # per-file/glob: assert is fine in tests, not in src
"__init__.py" = ["F401"]  # re-exports are the point of an __init__
```

```python
x = eval(user_input)  # noqa: S307
```

- Project-wide `ignore`: the rule is systematically wrong for this codebase, not just this line — e.g. `D203` conflicting with another docstring rule, or a formatter-owned concern like `E501`.
- `per-file-ignores`: the rule is right in general but a whole file/glob is a known exception — test files, migrations, generated code, `__init__.py` re-exports.
- Inline `# noqa: CODE`: a single line is a deliberate, justified exception. Always include the code (bare `# noqa` silences everything on the line, hiding future violations too).
- Prefer fixing the flagged code over ignoring when the rule is `B` (bugbear) — those are usually real bugs, not style preferences.
- `ruff check --add-noqa` inserts `# noqa` comments for all current violations — useful for a one-time baseline when adopting a new rule on a large existing codebase, but audit the diff rather than accepting it blindly.
