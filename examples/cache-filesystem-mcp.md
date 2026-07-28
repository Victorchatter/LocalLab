# Cache an MCP filesystem server with toolcall-cache

Wrap the official MCP filesystem server with `toolcall-cache` so repeated
`read_file` or `list_directory` calls are served from a local SQLite cache
instead of hitting the filesystem every time.

## What you need

- `toolcall-cache` installed (`pipx install git+https://github.com/Victorchatter/toolcall-cache.git`)
- Node.js / npx available

## Copy-paste commands

```bash
# 1. Create a small demo directory to explore.
mkdir -p /tmp/demo
echo "hello world" > /tmp/demo/greeting.txt

# 2. Start the cache proxy in front of the filesystem MCP server.
toolcall-cache start \
  --transport stdio \
  --upstream "npx -y @modelcontextprotocol/server-filesystem /tmp/demo" \
  --allowlist read_file,list_directory \
  --ttl 3600
```

In another terminal, send two identical MCP requests through the proxy (the
exact client command depends on your MCP client). The first call reaches the
filesystem; the second is served from cache:

```bash
# First call: ~milliseconds, filesystem read.
# Second call: sub-millisecond, SQLite cache hit.
```

You can also inspect the cache directly:

```bash
toolcall-cache stats
```

## Expected output

`toolcall-cache stats` shows something like:

```text
entries: 2
hits:    1
misses:  1
hit rate: 50%
```

The first call is a miss, the second is a hit. Both return the same file
content.

## Why this matters

Agent runs often re-read the same files many times: source files, dependency
manifests, documentation. A local cache eliminates redundant filesystem or
network MCP calls, makes replays deterministic, and keeps the agent fast even
when the upstream server is slow or temporarily unavailable.
