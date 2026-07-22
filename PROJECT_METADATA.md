# LocalLab — GitHub Repo Metadata

Ready-to-paste descriptions, topics, website links, and social-preview one-liners for each LocalLab project repo.

---

## agent-vcr / AgentVCR

**Repository name:** `AgentVCR`

**GitHub Description (short, ≤ 350 chars):**
```
Record and replay AI agent runs locally. Wire-level proxies capture model API + MCP tool traffic to a JSONL tape; replay re-runs the agent with tools stubbed — deterministic, offline, no agent changes.
```

**GitHub Topics:**
```
ai-agents
agent-debugging
record-replay
transcript
mcp
model-context-protocol
local-first
offline-first
observability
python
cli
pipx
mit-license
no-telemetry
regression-testing
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Record agent runs. Replay them offline. No cloud, no changes to your agent.
```

---

## tokenauditor / Tokenauditor

**Repository name:** `Tokenauditor`

**GitHub Description (short, ≤ 350 chars):**
```
Audit recorded agent transcripts to see exactly where token budget went. Per-turn breakdown of system prompt, tool definitions, tool results, and messages — plus waste flags. Offline, no API keys.
```

**GitHub Topics:**
```
token-usage
llm-costs
agent-observability
transcript-analysis
cost-optimization
local-first
offline-first
cli
python
pipx
anthropic
openai
claude-code
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Find out where your agent's token budget actually went.
```

---

## toolcall-linter / toolcall-linter

**Repository name:** `toolcall-linter`

**GitHub Description (short, ≤ 350 chars):**
```
Offline linter that cross-checks agent transcript tool calls against declared schemas. Catches undefined tools, wrong arity, bad types, missing required args, and bad enums — with exact line numbers.
```

**GitHub Topics:**
```
agent-tools
tool-calls
schema-validation
linter
transcript
mcp
json-schema
local-first
offline-first
cli
python
pipx
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Lint your agent's tool calls against their real schemas.
```

---

## transcript-to-test

**Repository name:** `transcript-to-test`

**GitHub Description (short, ≤ 350 chars):**
```
Turn one recorded agent run into a standalone pytest regression test. Extracts tool calls and recorded results, stubs them by exact (tool, canonical args) keys, and asserts on the final answer.
```

**GitHub Topics:**
```
agent-testing
regression-tests
pytest
transcript
record-replay
agent-vcr
mcp
test-generation
local-first
offline-first
cli
python
pipx
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Turn a recorded agent run into a pytest regression test.
```

---

## agent-circuit-breaker

**Repository name:** `agent-circuit-breaker`

**GitHub Description (short, ≤ 350 chars):**
```
Tiny local spend guard for LLM agents. Hard-caps model spend per-run and per-day in USD, with a global kill switch. Returns a clear Budget exhausted error when the cap is hit — never silently degrades.
```

**GitHub Topics:**
```
llm-cost-control
spend-caps
budget-guard
agent-safety
circuit-breaker
openai
anthropic
proxy
local-first
offline-first
cli
python
pipx
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Stop runaway agents before they stop your wallet.
```

---

## toolcall-cache

**Repository name:** `toolcall-cache`

**GitHub Description (short, ≤ 350 chars):**
```
Local, content-addressed cache for MCP tool results. Sits as an MCP proxy between your agent and any MCP server; repeats return the cached result instead of re-running the tool. SQLite-backed, TTL, denylist.
```

**GitHub Topics:**
```
mcp
model-context-protocol
tool-cache
caching
agent-performance
local-first
offline-first
sqlite
proxy
cli
python
pipx
claude-code
cursor
codex
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Cache MCP tool results locally. Fast, safe, no cloud.
```

---

## agent-checkpoint

**Repository name:** `agent-checkpoint`

**GitHub Description (short, ≤ 350 chars):**
```
Save and resume agent conversations via a vendor-neutral JSONL checkpoint. Suspends a long run, reboot, and continue anywhere without re-prompting from scratch. One AGENT_CHECKPOINT_INIT env var.
```

**GitHub Topics:**
```
agent-checkpoint
save-state
resume
agent-orchestration
long-running-tasks
transcript
local-first
offline-first
jsonl
cli
python
pipx
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Pause an agent run. Resume it anywhere, later.
```

---

## transcript-bridge

**Repository name:** `transcript-bridge`

**GitHub Description (short, ≤ 350 chars):**
```
Loss-aware, vendor-neutral transcript format conversion. Convert agent session logs between Claude Code JSONL, OpenAI messages, Codex traces, and a canonical JSONL shape. Reports unrepresentable fields instead of dropping them.
```

**GitHub Topics:**
```
transcript-conversion
interoperability
openai
anthropic
claude-code
codex
jsonl
agent-logs
portability
local-first
offline-first
cli
python
pipx
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Move agent transcripts between providers without losing data.
```

---

## mcp-openai-bridge

**Repository name:** `mcp-openai-bridge`

**GitHub Description (short, ≤ 350 chars):**
```
Give any OpenAI-function-calling agent access to the entire MCP tool ecosystem. Exposes MCP servers as OpenAI-compatible function-calling tools through a local wire-level shim — no rewrites, no hosted backend.
```

**GitHub Topics:**
```
mcp
model-context-protocol
openai
function-calling
openai-tools
agent-interop
bridge
local-first
offline-first
proxy
cli
python
pipx
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Use every MCP tool from any OpenAI-function-calling agent.
```

---

## prompt-portability-linter

**Repository name:** `prompt-portability-linter`

**GitHub Description (short, ≤ 350 chars):**
```
Scan prompts, tool definitions, and agent configs for vendor-locked features — cache_control, computer_use, response_format, responseSchema, slash-commands — and get portable alternatives. Editable rules.yaml, CI-friendly.
```

**GitHub Topics:**
```
prompt-engineering
vendor-lock-in
portability
llm-prompts
linter
anthropic
openai
gemini
codex
rules-yaml
local-first
offline-first
cli
python
pipx
mit-license
no-telemetry
```

**Website:**
```
https://github.com/Victorchatter/LocalLab
```

**Social-preview one-liner:**
```
Catch vendor lock-in before it catches you.
```

---

## LocalLab umbrella

For completeness, the umbrella repo metadata is in README.md and in the main conversation summary.

**Repository name:** `LocalLab`

**GitHub Description:**
```
A local-first laboratory of 10 small, sharp Python tools for building, debugging, and running AI agents. Record, audit, lint, cap spend, cache, checkpoint, bridge, and test — all offline, MIT, no telemetry.
```

**Website:**
```
https://github.com/Victorchatter
```

**Topics:**
```
ai-agents
agent-tools
local-first
offline-first
developer-tools
debugging
observability
mcp
model-context-protocol
agent-testing
token-auditing
cost-control
cli-tools
pipx
python
open-source
mit-license
no-telemetry
ai-observability
local-lab
```