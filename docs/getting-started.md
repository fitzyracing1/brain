# Getting started

```bash
git clone https://github.com/fitzyracing1/brain && cd brain
python3 brain.py "what should the next act be"   # one tick: reads the brain tree, emits one next act
python3 api.py                                   # HTTP API on port 8787
curl http://127.0.0.1:8787/v1/health
```

Note: `api.py` binds `HOST = "0.0.0.0"`, so it listens on all interfaces, not only localhost. GitHub Pages serves only the static site, not the live API.
