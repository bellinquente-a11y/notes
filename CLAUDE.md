# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo is a personal knowledge base. The user asks Claude to explain topics; Claude responds with a detailed explanation in the terminal and simultaneously writes a concise `.md` file capturing the key points.

## Workflow

I will ask you to explain a topic by starting the query with the uppercase string `EXPLAIN`. When asked to explain a topic:
1. **Respond in the terminal** with a thorough explanation — more depth than the file, including intuition and context.
2. **Review folder structure** to understand whether a change in an existing file is needed vs. the creation of a new file or folder.
3. **Write an `.md` file** in the appropriate directory. The file should be more succinct than the terminal explanation but still informative: prefer bullet points and short code examples over prose.
4. **Update `README.md`** in the relevant subdirectory and the root `README.md` if a new directory is created.
5. **Update other .md files** with appropriate links, only if needed. The aim is to maintain conceptual links between different topics.

## File organisation

```
notes/
├── python/     — Python language, tooling, type system
├── git/        — Git workflows and commands
└── misc/       — Diagrams, tools, and everything else
```

Each subdirectory has a `README.md` table with three columns: **file**, **type** (`note` or `ref`), **one-line description**.

- `note` — narrative explanation of a concept (the "why" and "how")
- `ref` — command/syntax quick-reference meant for lookup

When adding a new file, add a row to the subdirectory `README.md`. When adding a new directory, add a row to the root `README.md`.

## Cross-linking

Link related files using relative markdown links. Prefer linking on the first meaningful mention of a topic (e.g. if `mypy.md` mentions Poetry, link it). Don't link every occurrence — once per file is enough.

## Note style

- Lead with what the thing is and why it matters, then how to use it.
- Short code examples are preferred over long ones.
- Use bullet points for lists of facts; use prose only for conceptual explanations.
- No multi-paragraph docstrings or wall-of-text sections.
