# 10 Tools. 63 Commits. 3 Days.

July 20–22: I shipped **10 DevTools for AI agent workflows** — all to their own repos, all under 2K lines each.

## Why these tools?

Working with local AI agents, I kept running into the same friction points:

**💰 Cost creep**: Long agent loops meant runaway API bills. No way to catch a bug before it costs $200.

**🔁 Repeated work**: Agents re-read the same files, re-grep the same patterns, re-fetch the same data. No cache layer existed that worked across Claude Code, Codex, Cursor.

**🧪 No regression tests**: You fix an agent run by hand, it works — then a tool changes silently. How do you know the fix still holds?

**🔀 Format friction**: Converting agent transcripts between Claude Code, OpenAI, and tape formats meant hand-translation or fragile scripts.

**🎯 Vendor lock-in creep**: Prompts and configs accumulate vendor-specific syntax. No linter caught it before deployment.

**🔌 Interop gaps**: MCP tools work in Claude/Cursor/Codex, but OpenAI's function-calling runs a separate ecosystem. No bridge.

---

## The tools

### Spend control
**agent-circuit-breaker** — Local proxy with hard per-run and per-day USD caps. Stops infinite loops before your bill does. Kill switch for emergencies.

### Caching & observation
**toolcall-cache** — Content-addressed MCP tool result cache. Deterministic tools (reads, GETs, greps) return cached results. Saves tokens, latency, and money on repeated calls.

**tokenauditor** — Audit where every token in a session went. Which tool calls burned budget? Which prompts? Which model?

**agent-vcr** — Record agent runs to tape, replay them identically. Deterministic and debuggable.

**agent-checkpoint** — Save and restore agent state mid-run. Pause/resume workflows without replaying.

### Testing & quality
**transcript-to-test** — One CLI: feed it a successful agent run, get back a `pytest`-compatible test. Regressions = test fails. No framework, no ceremony.

**toolcall-linter** — Lint tool-calling patterns in agent code. Catch common mistakes before they cost.

**prompt-portability-linter** — Scan prompts and configs for vendor-locked syntax. Flag OpenAI-isms when targeting Anthropic, Claude Code shortcuts in a production prompt.

### Bridging
**transcript-bridge** — Convert between Claude Code JSONL, OpenAI message lists, and agent-vcr tape format. One canonical format in the middle.

**mcp-openai-bridge** — Expose MCP tools as OpenAI function-calling. Run OpenAI agents against your Claude MCP ecosystem.

---

## The numbers

- **63 commits** — real work, not scaffolding.
- **~10,030 lines** across 10 tools — largest is 1,942 lines (agent-vcr).
- **Zero external dependencies** — stdlib + aiohttp + sqlalchemy (minimal set).
- **Every tool is CLI-first** — `pipx install .` and go.
- **Self-checks included** — each ships its own deterministic test.

---

## What's next?

These are v0.1.0s: core loop works, APIs stable. They'll sit at the intersection of my own workflows and the broader AI infra problem. If you hit the same friction points (spend control, caching, regression testing, transcript conversion), grab one.

All 10 are on GitHub: github.com/Victorchatter/LocalLab

---

**Tech stack**: Python 3.10+, aiohttp, SQLite. Built on Windows, tested in CI. No GPU, no containers, no cloud dependencies.
