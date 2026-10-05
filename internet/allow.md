# internet

The brain may look at the public web. It may not look at private networks.

Allowed:
- http and https only
- public hosts
- DuckDuckGo instant-answer search at GET /v1/internet?q=

Blocked:
- localhost, link-local, and private ranges
- file:, javascript:, and raw IP tricks into those ranges
- bodies over the fetch cap

A look returns text, not a rendered page. The tick may attach that text. It does not store the page unless the keeper commits it.
