# brain

A brain as a GitHub repo. Memory is markdown. Rules are files. A tick reads the tree and writes one next act.

This is not a model weight file. It is the part of a mind that can live in git: what it remembers, what it will not do, and how it decides the next small move.

## Layout

```
memory/who.md       durable facts the brain is allowed to keep
memory/rules.md     hard rules, higher than habits
cortex/layers.md    priority stack: air, eat, win, talk
cortex/tick.md      one cycle: read, rank, act, log
skills/index.json   names of skills this brain may call
brain.py            local tick runner
log/ticks.jsonl     append-only tick log (created at runtime)
```

## Run

```bash
python3 brain.py "what should the next act be"
```

The runner prints one JSON object: the files it read, the winning layer, and one next act. It appends the same object to `log/ticks.jsonl`.

## Law

- Higher layers inhibit lower ones.
- A rule in `memory/rules.md` beats a habit in `memory/who.md`.
- Secrets never enter this repo.
- Every tick is a commit candidate. The brain does not rewrite history.
