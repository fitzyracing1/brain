#!/usr/bin/env python3
"""Brain HTTP API. Stdlib only.

  python3 api.py
  curl http://127.0.0.1:8787/v1/health
  curl -X POST http://127.0.0.1:8787/v1/tick -H 'content-type: application/json' -d '{"input":"what next"}'
  curl -X POST http://127.0.0.1:8787/v1/look -H 'content-type: application/json' -d '{"url":"https://example.com"}'
"""

from __future__ import annotations

import json
import re
import socket
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
HOST = "0.0.0.0"
PORT = 8787
MAX_BODY = 8000
MAX_FETCH = 120_000
TIMEOUT = 8
READ = [
    "memory/rules.md",
    "cortex/layers.md",
    "memory/who.md",
    "cortex/tick.md",
    "skills/index.json",
    "internet/allow.md",
    "agent/STRUCTURE.md",
]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
    return "Do one file-level act for: " + line.strip()


def tick(line: str, extra: str = "") -> dict:
    files = load()
    layer = layer_for(line)
    item = {
        "at": now(),
        "input": line,
        "read": [k for k, v in files.items() if v],
        "layer": layer,
        "act": act_for(line, layer),
        "why": "highest matching layer; rules file was loaded first",
        "internet": extra[:500] if extra else "",
    }
    log = ROOT / "log"
    log.mkdir(exist_ok=True)
    with (log / "ticks.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(item) + "\n")
    return item


def brain_doc() -> dict:
    files = load()
    return {
        "name": "brain",
        "repo": "https://github.com/fitzyracing1/brain",
        "site": "https://fitzyracing1.github.io/brain/",
        "at": now(),
        "files": files,
        "call": {
            "health": "GET /v1/health",
            "brain": "GET /v1/brain",
            "tick": "POST /v1/tick {input}",
            "look": "POST /v1/look {url}",
            "search": "GET /v1/internet?q=",
            "code": "POST /v1/code {input}",
        },
    }


def blocked(host: str) -> bool:
    host = host.lower().strip(".")
    if host in {"localhost", "0.0.0.0"} or host.endswith(".local"):
        return True
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return True
    for info in infos:
        ip = info[4][0]
        if ip.startswith("127.") or ip.startswith("10.") or ip.startswith("192.168."):
            return True
        if ip.startswith("172."):
            parts = ip.split(".")
            if len(parts) > 1 and parts[1].isdigit() and 16 <= int(parts[1]) <= 31:
                return True
        if ip == "::1" or ip.startswith("fe80") or ip.startswith("fc") or ip.startswith("fd"):
            return True
    return False


def fetch_url(url: str) -> dict:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {"ok": False, "error": "only http and https"}
    host = parsed.hostname or ""
    if blocked(host):
        return {"ok": False, "error": "host blocked"}
    req = Request(url, headers={"User-Agent": "fitzyracing1-brain/1"})
    try:
        with urlopen(req, timeout=TIMEOUT) as res:
            raw = res.read(MAX_FETCH)
            text = raw.decode("utf-8", errors="replace")
            text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
            text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            return {"ok": True, "url": url, "status": res.status, "text": text[:4000]}
    except URLError as exc:
        return {"ok": False, "error": str(exc.reason)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def search(q: str) -> dict:
    url = "https://api.duckduckgo.com/?q=" + quote(q) + "&format=json&no_html=1&skip_disambig=1"
    got = fetch_url(url)
    if not got.get("ok"):
        return got
    try:
        data = json.loads(got["text"])
    except json.JSONDecodeError:
        return {"ok": False, "error": "search parse failed"}
    topics = []
    for item in (data.get("RelatedTopics") or [])[:6]:
        if isinstance(item, dict) and item.get("Text"):
            topics.append({"text": item.get("Text"), "url": item.get("FirstURL")})
    return {
        "ok": True,
        "q": q,
        "abstract": data.get("AbstractText") or "",
        "heading": data.get("Heading") or "",
        "url": data.get("AbstractURL") or "",
        "topics": topics,
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("access-control-allow-origin", "*")
        self.send_header("access-control-allow-methods", "GET, POST, OPTIONS")
        self.send_header("access-control-allow-headers", "content-type")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read(self) -> dict:
        n = int(self.headers.get("content-length") or 0)
        if n > MAX_BODY:
            return {"_error": "body too big"}
        raw = self.rfile.read(n) if n else b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return {"_error": "bad json"}
        return data if isinstance(data, dict) else {"_error": "json object required"}

    def do_OPTIONS(self) -> None:
        self._send(200, {"ok": True})

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/v1/health"}:
            self._send(200, {"ok": True, "name": "brain", "at": now()})
            return
        if parsed.path == "/v1/brain":
            self._send(200, brain_doc())
            return
        if parsed.path == "/v1/internet":
            q = (parse_qs(parsed.query).get("q") or [""])[0].strip()
            if not q:
                self._send(400, {"ok": False, "error": "q required"})
                return
            self._send(200, search(q))
            return
        self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        data = self._read()
        if data.get("_error"):
            self._send(400, {"ok": False, "error": data["_error"]})
            return
        if parsed.path == "/v1/tick":
            line = str(data.get("input") or "").strip()
            if not line:
                self._send(400, {"ok": False, "error": "input required"})
                return
            extra = ""
            if data.get("url"):
                looked = fetch_url(str(data["url"]))
                extra = looked.get("text") or looked.get("error") or ""
            self._send(200, tick(line, extra))
            return
        if parsed.path == "/v1/look":
            url = str(data.get("url") or "").strip()
            if not url:
                self._send(400, {"ok": False, "error": "url required"})
                return
            self._send(200, fetch_url(url))
            return
        if parsed.path == "/v1/code":
            line = str(data.get("input") or "").strip()
            if not line:
                self._send(400, {"ok": False, "error": "input required"})
                return
            sys.path.insert(0, str(ROOT / "agent"))
            from coder import plan
            self._send(200, plan(line))
            return
        self._send(404, {"ok": False, "error": "not found"})

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s %s\n" % (now(), fmt % args))


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("brain api on http://127.0.0.1:%d" % PORT)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
