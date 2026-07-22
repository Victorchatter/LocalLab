> **Note:** this umbrella repo is being renamed from `OpenSourceProjects` to **`LocalLab`** to better describe what it holds. Old links will redirect automatically once the rename is complete.

# LocalLab — Project Index

A family of small, sharp, **local-first** open-source tools for AI agentic work and agents themselves. One repo per project; this file is the map.

**Umbrella repo:** <https://github.com/Victorchatter/LocalLab> (was `OpenSourceProjects`)  
**License:** MIT (per project and umbrella)  
**Stack:** Python · pipx-installable · no hosted backend · no telemetry

---

## Status legend

| Mark | Meaning |
|------|---------|
| ✅ Built | Code + `selfcheck.py` + README + LICENSE, pushed to its own repo |
| 🚧 In progress | Scaffolded / partially implemented |
| 📋 Planned | `PROMPT.md` written, not yet built |

---

## At a glance

| # | Project | Category | What it does | Status | Install |
|---|---------|----------|--------------|:------:|---------|
| 1 | [agent-vcr](https://github.com/Victorchatter/AgentVCR) | Debug | Record/replay agent runs with tool outputs stubbed | ✅ | `pipx install git+https://github.com/Victorchatter/AgentVCR.git` |
| 2 | [tokenauditor](https://github.com/Victorchatter/Tokenauditor) | Observability | Per-turn token breakdown + waste flags from any transcript | ✅ | `pipx install git+https://github.com/Victorchatter/Tokenauditor.git` |
| 3 | [toolcall-linter](https://github.com/Victorchatter/toolcall-linter) | Debug | Lint agent tool calls against declared schemas | ✅ | `pipx install git+https://github.com/Victorchatter/toolcall-linter.git` |
| 4 | [agent-circuit-breaker](https://github.com/Victorchatter/agent-circuit-breaker) | Runtime | Hard-cap model spend per-run/per-day + kill switch | ✅ | `pipx install git+https://github.com/Victorchatter/agent-circuit-breaker.git` |
| 5 | toolcall-cache | Runtime | Content-addressed cache for MCP tool results | ✅ | _repo coming soon — `origin` needs fixing before push_ |
| 6 | [agent-checkpoint](https://github.com/Victorchatter/agent-checkpoint) | Runtime | Save/resume an agent run via a canonical JSONL tape | 🚧 | _scaffold + format done; selfcheck + README pending_ |
| 7 | transcript-bridge | Interop | Convert agent transcripts between provider formats | 📋 | seed at `transcript-bridge/PROMPT.md` |
| 8 | mcp-openai-bridge | Interop | Expose MCP servers as OpenAI function-calling tools | 📋 | seed at `mcp-openai-bridge/PROMPT.md` |
| 9 | prompt-portability-linter | Interop | Flag vendor-locked features in your prompts | 📋 | seed at `prompt-portability-linter/PROMPT.md` |
| 10 | transcript-to-test | Debug | Turn a recorded run into a pytest regression test | 📋 | seed at `transcript-to-test/PROMPT.md` |

---

## The projects

### Debugging & observability

#### 1. agent-vcr ✅
Record/replay an AI agent run with tool outputs stubbed. Two wire-level proxies (model API: OpenAI + Anthropic streaming; tools: MCP stdio + HTTP) capture a run to a JSONL tape; replay re-runs the agent with tools stubbed so you reproduce bugs offline, no side effects, no tool re-execution.
- **Repo:** <https://github.com/Victorchatter/AgentVCR>
- **Local:** `C:\Users\Victor\agent-vcr`
- **Install:** `pipx install git+https://github.com/Victorchatter/AgentVCR.git`
- **Spec:** `agent-vcr/docs/superpowers/specs/2026-07-20-agent-vcr-design.md`

#### 2. tokenauditor ✅
A read-only CLI that parses an agent session transcript (Claude Code JSONL, OpenAI messages) and reports a per-turn token breakdown — system prompt vs tool defs vs tool results vs messages — plus waste flags. Tells you where the budget actually went.
- **Repo:** <https://github.com/Victorchatter/Tokenauditor>
- **Local:** `C:\Users\Victor\tokenauditor`
- **Install:** `pipx install git+https://github.com/Victorchatter/Tokenauditor.git`

#### 3. toolcall-linter ✅
Cross-checks an agent transcript's tool calls against declared tool schemas; flags undefined-tool calls, wrong arity, wrong types, missing required args, bad enums — the #1 silent agent failure mode, caught at lint time.
- **Repo:** <https://github.com/Victorchatter/toolcall-linter>
- **Local:** `C:\Users\Victor\toolcall-linter`
- **Install:** `pipx install git+https://github.com/Victorchatter/toolcall-linter.git`

#### 4. transcript-to-test 📋
Turn one recorded successful agent run into a standalone pytest regression test: extracts tool calls + recorded results, stubs them, re-runs the agent, asserts on the final answer. Reads agent-vcr tapes directly.
- **Local:** `C:\Users\Victor\transcript-to-test`
- **Seed:** `transcript-to-test/PROMPT.md`
- **Repo:** _TBD_

---

### Runtime & orchestration

#### 5. agent-circuit-breaker ✅
A tiny local proxy that hard-caps model spend per-run and per-day (USD), with a global kill switch. Sits between any agent and any model API; refuses with a clear error when the cap is hit — never silently degrades. SQLite state, bundled editable `prices.json`.
- **Repo:** <https://github.com/Victorchatter/agent-circuit-breaker>
- **Local:** `C:\Users\Victor\agent-circuit-breaker`
- **Install:** `pipx install git+https://github.com/Victorchatter/agent-circuit-breaker.git`

#### 6. toolcall-cache ✅
A local, content-addressed cache for MCP tool results. Sits as an MCP proxy between the agent and any MCP server; returns the cached result for a repeated `(server, tool, args)` call instead of re-running the tool. One SQLite store, denylist + opt-in allowlist policy, TTL.
- **Repo:** _TBD_ — `origin` currently misconfigured (points at agent-circuit-breaker's repo); fix before push.
- **Local:** `C:\Users\Victor\toolcall-cache`
- **Seed:** `toolcall-cache/PROMPT.md`

#### 7. agent-checkpoint 🚧
Framework-agnostic "save agent state now, resume later" via a single JSONL snapshot + an `AGENT_CHECKPOINT_INIT` env convention any agent can adopt. Suspend a long run, reboot, continue without re-prompting from scratch.
- **Repo:** <https://github.com/Victorchatter/agent-checkpoint>
- **Local:** `C:\Users\Victor\agent-checkpoint`
- **Seed:** `agent-checkpoint/PROMPT.md`
- **Status:** package scaffold + canonical checkpoint format done; selfcheck + README pending.

---

### Interop & portability

#### 8. transcript-bridge 📋
Convert agent session logs between formats — Claude Code JSONL ↔ OpenAI messages ↔ Codex traces ↔ canonical JSONL. Reports loss (fields with no native home) instead of silently dropping them. `--strict` fails on any loss.
- **Local:** `C:\Users\Victor\transcript-bridge`
- **Seed:** `transcript-bridge/PROMPT.md`
- **Repo:** _TBD_

#### 9. mcp-openai-bridge 📋
Expose any MCP server's tools as OpenAI function-calling JSON-Schema tools, and execute the calls back against the MCP server. Lets OpenAI-function-calling agents use the whole Claude-first MCP ecosystem. v1 ships `mcp2openai`.
- **Local:** `C:\Users\Victor\mcp-openai-bridge`
- **Seed:** `mcp-openai-bridge/PROMPT.md`
- **Repo:** _TBD_

#### 10. prompt-portability-linter 📋
Scans a system prompt (+ tool defs / agent config) for vendor-locked features — `cache_control`, `computer_use`, OpenAI `response_format` strict, Gemini `responseSchema`, Codex slash-commands — and tells you what to change to run the same prompt on another provider. Editable `rules.yaml`.
- **Local:** `C:\Users\Victor\prompt-portability-linter`
- **Seed:** `prompt-portability-linter/PROMPT.md`
- **Repo:** _TBD_

---

## How they fit together

The four "tape" projects share **one JSONL event envelope** so a recording from one is consumable by another:

```
agent-vcr           records the run       →  tape
toolcall-cache      caches tool results   →  (subset of the same shape)
agent-checkpoint    save/resume           →  canonical tape
transcript-to-test  tape → regression test →  reads the tape
transcript-bridge   converts between provider transcripts and the canonical shape
```

Each project is **standalone** — install one, use it alone. But built in roughly the order above, later projects reuse earlier ones' formats rather than forking them.

## Working on a project

Every project folder contains a `PROMPT.md` that seeds a fresh Claude Code session with the full design direction and constraints. To start one:

```bash
cd /c/Users/Victor/<project>
claude          # then send: @PROMPT.md
```

## Roadmap

- ✅ agent-vcr, tokenauditor, toolcall-linter, agent-circuit-breaker, toolcall-cache
- 🚧 agent-checkpoint (finish selfcheck + README → ship)
- 📋 transcript-bridge, mcp-openai-bridge, prompt-portability-linter, transcript-to-test (build from `PROMPT.md`)
- 🔧 Fix `toolcall-cache` git `origin` (currently points at agent-circuit-breaker's repo)

## Contributing

Issues and PRs are welcome on any project repo. Please keep the umbrella philosophy: **local-first, small, MIT, no telemetry.**

Good first contributions:

- New transcript-format parsers for `tokenauditor` / `transcript-bridge`
- New vendor-lock rules for `prompt-portability-linter`'s `rules.yaml`
- New cacheability denylist entries for `toolcall-cache`
- Self-checks and edge-case reports from real agent runs