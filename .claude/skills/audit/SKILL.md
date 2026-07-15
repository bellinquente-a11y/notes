---
name: audit
description: Check notes for staleness — verify version-sensitive claims and code snippets against current library/tool versions, report findings, and fix after approval. Use when the user asks to audit notes or check for outdated content.
argument-hint: "[path or topic — default: least recently touched notes]"
---

Audit knowledge-base notes for content that has gone stale since it was written.

## Scope

- If the user gives a path or topic, audit those notes.
- Otherwise pick the least recently modified notes: `git log -1 --format=%ci -- <file>` per file, audit the ~10 oldest.

## Steps

1. **Read the notes in scope** and extract every claim that can rot:
   - version statements ("current major version is X", "Python 3.x+")
   - deprecated/renamed APIs, CLI flags, config keys
   - "recommended/idiomatic way to do X" claims
   - external URLs
2. **Verify each claim** against current reality:
   - WebSearch/WebFetch official changelogs, release notes, and docs
   - run self-contained code snippets with `python3` (or the repo's environment) where practical — skip snippets that need external services or heavy setup
   - check the installed version (`pip show`, `mkdocs --version`, etc.) when the repo itself uses the tool
3. **Report findings** as a table: file:line, the claim, current reality, proposed fix. Separate confirmed-stale from unverifiable. If nothing is stale, say so and stop.
4. **Wait for approval** before editing anything.
5. **After approval**: apply fixes following the note style in CLAUDE.md, run `mkdocs build --strict`, and commit without prompting.

Keep fixes minimal — update the stale fact, don't rewrite the note. If a note is so outdated it needs rewriting, flag that as a finding rather than doing it silently.
