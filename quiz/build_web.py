#!/usr/bin/env python3
"""Compile quiz/banks/**/*.yaml into docs/quiz/data.json for the web quiz app.

Bank format: one YAML file per note, mirroring the docs/ tree. See quiz/README.md.

Card identity: the app keys scheduling state on "<bank path>#<question id>", so
renaming a question id or moving a bank file creates a NEW card and orphans the
old one's history. Editing question text in place is safe.
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
BANKS_DIR = ROOT / "banks"
OUT_FILE = ROOT.parent / "docs" / "quiz" / "data.json"


def load_bank(path: Path) -> dict:
    rel = path.relative_to(BANKS_DIR).as_posix()
    try:
        bank = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        sys.exit(f"{rel}: YAML parse error\n{e}")
    for key in ("note", "tier", "questions"):
        if key not in bank:
            sys.exit(f"{rel}: missing top-level key '{key}'")
    if bank["tier"] not in ("core", "detail"):
        sys.exit(f"{rel}: tier must be core|detail, got {bank['tier']!r}")
    seen = set()
    for q in bank["questions"]:
        qid = q.get("id")
        if not qid or qid in seen:
            sys.exit(f"{rel}: missing or duplicate question id {qid!r}")
        seen.add(qid)
        if q.get("type") not in ("mcq", "recall"):
            sys.exit(f"{rel}:{qid}: type must be mcq|recall")
        if q["type"] == "mcq" and not (3 <= len(q.get("options", [])) <= 5):
            sys.exit(f"{rel}:{qid}: mcq needs 3-5 options (first = correct)")
        if q["type"] == "recall" and not q.get("answer"):
            sys.exit(f"{rel}:{qid}: recall needs an answer")
        if not q.get("q"):
            sys.exit(f"{rel}:{qid}: missing question text 'q'")
    return bank


def export_question(q: dict) -> dict:
    out = {"id": q["id"], "type": q["type"], "q": str(q["q"])}
    if q["type"] == "mcq":
        out["options"] = [str(o) for o in q["options"]]
        if q.get("explain"):
            out["explain"] = str(q["explain"])
    else:
        out["answer"] = str(q["answer"])
    return out


def main() -> None:
    bank_paths = sorted(BANKS_DIR.rglob("*.yaml"))
    if not bank_paths:
        sys.exit(f"no banks found under {BANKS_DIR}")

    banks = []
    n_questions = 0
    for path in bank_paths:
        rel = path.relative_to(BANKS_DIR).as_posix()
        bank = load_bank(path)
        banks.append(
            {
                "path": rel.removesuffix(".yaml"),
                "note": bank["note"],
                "tier": bank["tier"],
                "area": rel.split("/")[0],
                "questions": [export_question(q) for q in bank["questions"]],
            }
        )
        n_questions += len(bank["questions"])

    data = {"generated": datetime.date.today().isoformat(), "banks": banks}
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {OUT_FILE.relative_to(ROOT.parent)}: {n_questions} questions from {len(bank_paths)} banks")


if __name__ == "__main__":
    main()
