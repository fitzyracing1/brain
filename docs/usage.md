# Usage

## HTTP API (`api.py`, port 8787)

| Method | Path | Body / query |
|---|---|---|
| GET | `/v1/health` (also `/`) | |
| GET | `/v1/brain` | |
| POST | `/v1/tick` | `{"input": "what next"}` |
| POST | `/v1/look` | `{"url": "https://example.com"}` (public http/https only, per `internet/allow.md`) |
| GET | `/v1/internet?q=...` | search |
| POST | `/v1/code` | `{"input": "add a helper that echoes a tick"}` |

## Coding agent

```bash
python3 agent/coder.py "add a helper that echoes a tick"
```

It plans on a ternary node (left = air, mid = eat, right = win) and keeps symbols in a ternary search tree. Scratch files go to `agent/scratch/`.
