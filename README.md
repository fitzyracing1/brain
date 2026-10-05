# brain

A brain as a public GitHub repo. Memory is markdown. Rules are files. The site is the face. The API is how you call it.

Repo: https://github.com/fitzyracing1/brain
Site: https://fitzyracing1.github.io/brain/
Static call: https://fitzyracing1.github.io/brain/api/v1/brain.json

## Layout

```
memory/who.md       durable facts
memory/rules.md     hard rules
cortex/layers.md    air, eat, win, talk
cortex/tick.md      one cycle
skills/index.json   admit and forbid
internet/allow.md   what the brain may fetch
agent/coder.py      coding agent on the ternary tree
api.py              live HTTP API
docs/index.html     website
```

## Call the live API

```bash
python3 api.py
curl http://127.0.0.1:8787/v1/health
curl http://127.0.0.1:8787/v1/brain
curl -X POST http://127.0.0.1:8787/v1/tick \
  -H 'content-type: application/json' \
  -d '{"input":"what next"}'
curl -X POST http://127.0.0.1:8787/v1/look \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com"}'
curl "http://127.0.0.1:8787/v1/internet?q=cambridge"
curl -X POST http://127.0.0.1:8787/v1/code \
  -H 'content-type: application/json' \
  -d '{"input":"add a helper that echoes a tick"}'
python3 agent/coder.py "add a helper that echoes a tick"
```

The coder plans on a ternary node: left is air, mid is eat, right is win. Symbols live in a ternary search tree. Scratch files land in `agent/scratch/`.

The live process is the one that can append ticks and fetch the public web. GitHub Pages serves the site and the static brain document. It cannot run the tick server.

## Law

- Higher layers inhibit lower ones.
- A rule beats a habit.
- No secrets in this repo.
- Internet looks stay on public http and https.
