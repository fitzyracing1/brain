#!/usr/bin/env python3
"""Coding agent whose plan is the brain's ternary tree.

left  = air   read the tree, stop if it is unreadable
mid   = eat   keep symbols in the ternary search tree
right = win   one code act
talk        report after the walk, never before air

  python3 agent/coder.py "add a helper that echoes a tick"
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ternary import TernarySearchTree, TernaryTree

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "log", "__pycache__"}
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def files() -> list[Path]:
    out = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP for part in path.parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pyc"}:
            continue
        out.append(path)
    return out


def air() -> dict:
    needed = ["memory/rules.md", "cortex/layers.md", "skills/index.json"]
    missing = [rel for rel in needed if not (ROOT / rel).exists()]
    return {"layer": "air", "ok": not missing, "missing": missing, "files": len(files())}


def eat() -> tuple[TernarySearchTree, dict]:
    tree = TernarySearchTree()
    count = 0
    for path in files():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(path.relative_to(ROOT))
        for word in set(WORD.findall(text)):
            key = word.lower()
            prev = tree.get(key) or []
            if rel not in prev:
                prev = prev + [rel]
                tree.insert(key, prev)
                count += 1
    return tree, {"layer": "eat", "symbols": len(tree), "inserts": count}


def win(goal: str, symbols: list[str]) -> dict:
    stem = re.sub(r"[^a-z0-9]+", "_", goal.lower()).strip("_")[:40] or "act"
    rel = "agent/scratch/" + stem + ".py"
    body = (
        '"""Scratch act from the brain coder. One file. Do not treat as merged."""\n\n'
        "GOAL = %r\n"
        "SYMBOLS = %r\n\n"
        "def act():\n"
        "    return {'goal': GOAL, 'symbols': SYMBOLS}\n\n"
        "if __name__ == '__main__':\n"
        "    print(act())\n"
    ) % (goal, symbols[:8])
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return {"layer": "win", "wrote": rel, "symbols": symbols[:8]}


def plan(goal: str) -> dict:
    breath = air()
    plan_tree = TernaryTree()
    plan_tree.insert(goal)
    plan_tree.insert("air")
    plan_tree.insert("eat")
    plan_tree.insert("win")
    if not breath["ok"]:
        return {
            "at": now(),
            "goal": goal,
            "layer": "air",
            "act": "stop: tree unreadable",
            "tree": plan_tree.pretty(),
            "air": breath,
        }
    symbols, fed = eat()
    keys = []
    for word in WORD.findall(goal):
        keys.extend(symbols.starts_with(word.lower()[:4]))
    keys = list(dict.fromkeys(keys))[:12]
    wrote = win(goal, keys)
    return {
        "at": now(),
        "goal": goal,
        "layer": "win",
        "talk": "air then eat then win; talk is this report",
        "map": {"left": "air", "mid": "eat", "right": "win"},
        "tree": plan_tree.pretty(),
        "air": breath,
        "eat": fed,
        "win": wrote,
        "found": keys,
    }


def main() -> int:
    goal = " ".join(sys.argv[1:]).strip() or "index the brain and write one helper"
    item = plan(goal)
    log = ROOT / "log"
    log.mkdir(exist_ok=True)
    with (log / "coder.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({k: v for k, v in item.items() if k != "tree"}) + "\n")
    print(json.dumps(item, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
