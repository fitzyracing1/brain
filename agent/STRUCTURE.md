# coder

The coding agent matches the brain by using a ternary tree.

Plan node children:

- left = air. Read the tree. Stop if rules or layers are missing.
- mid = eat. Store symbols in a ternary search tree (lo / eq / hi).
- right = win. Write one scratch file under agent/scratch/.

Talk is the JSON report after the walk. It does not outrank air.

```bash
python3 agent/coder.py "add a helper that echoes a tick"
curl -X POST http://127.0.0.1:8787/v1/code \
  -H 'content-type: application/json' \
  -d '{"input":"add a helper that echoes a tick"}'
```

Scratch files are proposals. They are not merged into memory or cortex.
