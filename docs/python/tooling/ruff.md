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
