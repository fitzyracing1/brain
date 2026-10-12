# Architecture

| Path | Role |
|---|---|
| `memory/who.md`, `memory/rules.md` | durable facts and hard rules |
| `cortex/layers.md`, `cortex/tick.md` | the air / eat / win / talk layers and one cycle |
| `skills/index.json` | admitted and forbidden skills |
| `internet/allow.md` | what the brain may fetch |
| `brain.py` | tick runner |
| `api.py` | live HTTP API (`ThreadingHTTPServer`) |
| `agent/coder.py`, `agent/ternary.py`, `agent/STRUCTURE.md` | coding agent on ternary plan nodes and a ternary search tree |
| `BRAIN.md` | brain description |
| `docs/` | website and static API documents |

Laws (README): higher layers inhibit lower ones, a rule beats a habit, the repo holds no secrets, and internet looks stay on public http and https.
