# tick

Input: one line from the keeper.

Steps:

1. Load `memory/rules.md` and `cortex/layers.md`.
2. Load `memory/who.md` and `skills/index.json`.
3. Pick the highest layer the line requires.
4. Write one next act that obeys the rules.
5. Append JSON to `log/ticks.jsonl`.

Output fields: `read`, `layer`, `act`, `why`.
