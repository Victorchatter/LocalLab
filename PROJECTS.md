# LocalLab — Project Index

A family of small, sharp, **local-first** open-source tools for AI agentic work and agents themselves. One repo per project; this file is the map.

**Umbrella repo:** [Victorchatter/LocalLab](https://github.com/Victorchatter/LocalLab)  
**License:** MIT (per project and umbrella)  
**Stack:** Python · pipx-installable · no hosted backend · no telemetry

---

## At a glance

Click any project name to open its repository home page.

### Debug & observability

| # | Project | What it does | Install |
|---|---------|--------------|---------|
| 1 | [agent-vcr](https://github.com/Victorchatter/AgentVCR) | Record/replay agent runs with tool outputs stubbed | `pipx install git+https://github.com/Victorchatter/AgentVCR.git` |
| 2 | [tokenauditor](https://github.com/Victorchatter/Tokenauditor) | Per-turn token breakdown + waste flags from any transcript | `pipx install git+https://github.com/Victorchatter/Tokenauditor.git` |
| 3 | [toolcall-linter](https://github.com/Victorchatter/toolcall-linter) | Lint agent tool calls against declared schemas | `pipx install git+https://github.com/Victorchatter/toolcall-linter.git` |
| 4 | [transcript-to-test](https://github.com/Victorchatter/transcript-to-test) | Turn a recorded run into a pytest regression test | `pipx install git+https://github.com/Victorchatter/transcript-to-test.git` |

### Runtime & orchestration

| # | Project | What it does | Install |
|---|---------|--------------|---------|
| 5 | [agent-circuit-breaker](https://github.com/Victorchatter/agent-circuit-breaker) | Hard-cap model spend per-run/per-day + kill switch | `pipx install git+https://github.com/Victorchatter/agent-circuit-breaker.git` |
| 6 | [toolcall-cache](https://github.com/Victorchatter/toolcall-cache) | Content-addressed cache for MCP tool results | `pipx install git+https://github.com/Victorchatter/toolcall-cache.git` |
| 7 | [agent-checkpoint](https://github.com/Victorchatter/agent-checkpoint) | Save/resume an agent run via a canonical JSONL tape | `pipx install git+https://github.com/Victorchatter/agent-checkpoint.git` |

### Interop & portability

| # | Project | What it does | Install |
|---|---------|--------------|---------|
| 8 | [transcript-bridge](https://github.com/Victorchatter/transcript-bridge) | Convert agent transcripts between provider formats | `pipx install git+https://github.com/Victorchatter/transcript-bridge.git` |
| 9 | [mcp-openai-bridge](https://github.com/Victorchatter/mcp-openai-bridge) | Expose MCP servers as OpenAI function-calling tools | `pipx install git+https://github.com/Victorchatter/mcp-openai-bridge.git` |
| 10 | [prompt-portability-linter](https://github.com/Victorchatter/prompt-portability-linter) | Flag vendor-locked features in your prompts | `pipx install git+https://github.com/Victorchatter/prompt-portability-linter.git` |

---

## The projects

### Debugging & observability

#### 1. [agent-vcr](https://github.com/Victorchatter/AgentVCR) ✅
Record/replay an AI agent run with tool outputs stubbed. Two wire-level proxies (model API: OpenAI + Anthropic streaming; tools: MCP stdio + HTTP) capture a run to a JSONL tape; replay re-runs the agent with tools stubbed so you reproduce bugs offline, no side effects, no tool re-execution.
- **Local:** `C:\Users\Victor\agent-vcr`
- **Install:** `pipx install git+https://github.com/Victorchatter/AgentVCR.git`
- **CLI:** `agent-vcr record -- claude -p "fix the bug"`
- **Spec:** `agent-vcr/docs/superpowers/specs/2026-07-20-agent-vcr-design.md`

#### 2. [tokenauditor](https://github.com/Victorchatter/Tokenauditor) ✅
A read-only CLI that parses an agent session transcript (Claude Code JSONL, OpenAI messages) and reports a per-turn token breakdown — system prompt vs tool defs vs tool results vs messages — plus waste flags. Tells you where the budget actually went.
- **Local:** `C:\Users\Victor\tokenauditor`
- **Install:** `pipx install git+https://github.com/Victorchatter/Tokenauditor.git`
- **CLI:** `tokenauditor session.jsonl`

#### 3. [toolcall-linter](https://github.com/Victorchatter/toolcall-linter) ✅
Cross-checks an agent transcript's tool calls against declared tool schemas; flags undefined-tool calls, wrong arity, wrong types, missing required args, bad enums — the #1 silent agent failure mode, caught at lint time.
- **Local:** `C:\Users\Victor\toolcall-linter`
- **Install:** `pipx install git+https://github.com/Victorchatter/toolcall-linter.git`
- **CLI:** `toolcall-linter session.jsonl --tools tools.json`

#### 4. [transcript-to-test](https://github.com/Victorchatter/transcript-to-test) ✅
Turn one recorded successful agent run into a standalone pytest regression test: extracts tool calls + recorded results, stubs them, re-runs the agent, asserts on the final answer. Reads agent-vcr tapes directly.
- **Local:** `C:\Users\Victor\transcript-to-test`
- **Install:** `pipx install git+https://github.com/Victorchatter/transcript-to-test.git`
- **CLI:** `transcript-to-test tape.jsonl --out test_auth.py`

---

### Runtime & orchestration

#### 5. [agent-circuit-breaker](https://github.com/Victorchatter/agent-circuit-breaker) ✅
A tiny local proxy that hard-caps model spend per-run and per-day (USD), with a global kill switch. Sits between any agent and any model API; refuses with a clear error when the cap is hit — never silently degrades. SQLite state, bundled editable `prices.json`.
- **Local:** `C:\Users\Victor\agent-circuit-breaker`
- **Install:** `pipx install git+https://github.com/Victorchatter/agent-circuit-breaker.git`
- **CLI:** `agent-circuit-breaker --run-budget 2.00 --daily-budget 20.00`

#### 6. [toolcall-cache](https://github.com/Victorchatter/toolcall-cache) ✅
A local, content-addressed cache for MCP tool results. Sits as an MCP proxy between the agent and any MCP server; returns the cached result for a repeated `(server, tool, args)` call instead of re-running the tool. One SQLite store, denylist + opt-in allowlist policy, TTL.
- **Local:** `C:\Users\Victor\toolcall-cache`
- **Install:** `pipx install git+https://github.com/Victorchatter/toolcall-cache.git`
- **CLI:** `toolcall-cache --config cache-config.yaml`

#### 7. [agent-checkpoint](https://github.com/Victorchatter/agent-checkpoint) ✅
Framework-agnostic "save agent state now, resume later" via a single JSONL snapshot + an `AGENT_CHECKPOINT_INIT` env convention any agent can adopt. Suspend a long run, reboot, continue without re-prompting from scratch.
- **Local:** `C:\Users\Victor\agent-checkpoint`
- **Install:** `pipx install git+https://github.com/Victorchatter/agent-checkpoint.git`
- **CLI:** `agent-checkpoint save` / `agent-checkpoint resume checkpoint.jsonl`

---

### Interop & portability

#### 8. [transcript-bridge](https://github.com/Victorchatter/transcript-bridge) ✅
Convert agent session logs between formats — Claude Code JSONL ↔ OpenAI messages ↔ Codex traces ↔ canonical JSONL. Reports loss (fields with no native home) instead of silently dropping them. `--strict` fails on any loss.
- **Local:** `C:\Users\Victor\transcript-bridge`
- **Install:** `pipx install git+https://github.com/Victorchatter/transcript-bridge.git`
- **CLI:** `transcript-bridge session.jsonl --from claude --to openai`

#### 9. [mcp-openai-bridge](https://github.com/Victorchatter/mcp-openai-bridge) ✅
Expose any MCP server's tools as OpenAI function-calling JSON-Schema tools, and execute the calls back against the MCP server. Lets OpenAI-function-calling agents use the whole Claude-first MCP ecosystem.
- **Local:** `C:\Users\Victor\mcp-openai-bridge`
- **Install:** `pipx install git+https://github.com/Victorchatter/mcp-openai-bridge.git`
- **CLI:** `mcp2openai --config mcp-servers.json`

#### 10. [prompt-portability-linter](https://github.com/Victorchatter/prompt-portability-linter) ✅
Scans a system prompt (+ tool defs / agent config) for vendor-locked features — `cache_control`, `computer_use`, OpenAI `response_format` strict, Gemini `responseSchema`, Codex slash-commands — and tells you what to change to run the same prompt on another provider. Editable `rules.yaml`.
- **Local:** `C:\Users\Victor\prompt-portability-linter`
- **Install:** `pipx install git+https://github.com/Victorchatter/prompt-portability-linter.git`
- **CLI:** `prompt-portability-linter prompt.md --rules rules.yaml`

---

## How they fit together

Several projects share **one JSONL event envelope** — a *tape* — so a recording from one is consumable by another:

```
agent-vcr           records the run       →  tape
toolcall-cache      caches tool results   →  (subset of the same shape)
agent-checkpoint    save/resume           →  canonical tape
transcript-to-test  tape → regression test →  reads the tape
transcript-bridge   converts between provider transcripts and the canonical shape
```

Each tool is **standalone** — install one, use it alone. But built in roughly the order above, later tools reuse earlier ones' formats rather than forking them.

## Working on a project

Every project repo contains a `PROMPT.md` that seeds a fresh Claude Code session with the full design direction and constraints. To start one:

```bash
git clone https://github.com/Victorchatter/<project>.git
cd <project>
claude          # then send: @PROMPT.md
```

## Contributing

Issues and PRs are welcome on any project repo. Please keep the umbrella philosophy: **local-first, small, MIT, no telemetry.**

Good first contributions:

- New transcript-format parsers for `tokenauditor` / `transcript-bridge`
- New vendor-lock rules for `prompt-portability-linter`'s `rules.yaml`
- New cacheability denylist entries for `toolcall-cache`
- Self-checks and edge-case reports from real agent runs