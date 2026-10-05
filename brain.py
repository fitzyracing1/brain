#!/usr/bin/env python3
"""Tick runner. Reads the brain tree and emits one next act."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
READ = [
    "memory/rules.md",
    "cortex/layers.md",
    "memory/who.md",
    "cortex/tick.md",
    "skills/index.json",
]


def load() -> dict[str, str]:
    out = {}
    for rel in READ:
        path = ROOT / rel
        out[rel] = path.read_text(encoding="utf-8") if path.exists() else ""
    return out


def layer_for(line: str) -> str:
    text = line.lower()
    if any(w in text for w in ("down", "unreadable", "auth", "crash", "disk")):
        return "air"
    if any(w in text for w in ("remember", "memory", "commit", "save")):
        return "eat"
    if any(w in text for w in ("status", "report", "tell", "explain")):
        return "talk"
    return "win"


def act_for(line: str, layer: str) -> str:
    if layer == "air":
        return "Check that memory/, cortex/, and skills/index.json are readable before any other act."
    if layer == "eat":
        return "Append the new fact to memory/who.md and commit it. Do not edit old ticks."
    if layer == "talk":
        return "Report the last tick from log/ticks.jsonl, then stop."
    return f"Do one file-level act for: {line.strip()}"


def main() -> int:
    line = " ".join(sys.argv[1:]).strip() or "what should the next act be"
    files = load()
    layer = layer_for(line)
    tick = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "input": line,
        "read": [k for k, v in files.items() if v],
        "layer": layer,
        "act": act_for(line, layer),
        "why": "highest matching layer; rules file was loaded first",
    }
    log = ROOT / "log"
    log.mkdir(exist_ok=True)
    with (log / "ticks.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(tick) + "\n")
    print(json.dumps(tick, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
