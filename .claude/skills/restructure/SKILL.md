---
name: restructure
description: Survey the knowledge base for oversized files and folders, propose a reorganisation, and execute it after approval. Use when the user starts a query with RESTRUCTURE or asks to reorganise the notes.
disable-model-invocation: true
---

Reorganise the knowledge base. This skill has two phases: a proposal (always stops for approval) and execution (only after explicit approval).

## Phase 1 — Survey and propose

1. **Survey cheaply**: read only the `README.md` files in each directory and run `wc -l` on every `.md` file. Do **not** open individual note files unless their line count exceeds ~200 and you need their section headings (`grep '^## '`) to propose a sensible split.
2. **Identify problems**: flag any file >200 lines and any folder with >10 files (excluding `README.md`).
3. **Propose a new structure** that resolves the problems:
   - Group topics by logical criteria (language feature area, tool category) — never by arbitrary criteria like alphabetical order or file size alone.
   - Only introduce a subfolder when it will contain at least 3 files; keep new folders minimal.
   - Files >200 lines *may* be split into two focused files — propose each split with a one-line rationale, and explicitly list oversized files you recommend leaving intact (e.g. coherent single-topic refs) with a reason.
4. **Output both the old and proposed structures as directory-tree diagrams** (tree-style ASCII). Annotate files with line counts and folders with file counts. Unchanged subtrees may be collapsed to one annotated line.
5. **Do not move, rename, or create anything yet.** End the turn awaiting explicit approval.
6. **Ask for clarification** if a grouping decision is genuinely ambiguous (a file that belongs equally well in two places) — fold the question into the proposal.

## Phase 2 — Execute (after approval only)

7. Use `git mv` for moves so history is preserved. For splits, keep a short pointer or link in the source file to the extracted note.
8. **Update all README files**: rows for new files/folders, remove rows for moved ones, fix changed paths. New folders get their own `README.md` table.
9. **Update all cross-file links** in every `.md` file — both inbound links to moved files and outbound links inside them (relative depth changes).
10. **Sort all README table rows alphabetically** by filename within each directory.
11. **Verify** with `mkdocs build --strict` (must exit 0), then **commit** without prompting.
