> **Note:** this umbrella repo is being renamed from `OpenSourceProjects` to **`LocalLab`** to better describe what it holds. Old links will redirect automatically once the rename is complete.

<div align="center">

# 🧪 LocalLab

### A local-first laboratory for building, debugging, and running AI agents.

[![10 tools](https://img.shields.io/badge/tools-10%20and%20growing-2EA44F.svg)](#-the-tools)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Local-first](https://img.shields.io/badge/local--first-offline%20ready-2EA44F.svg)](#philosophy)
[![No telemetry](https://img.shields.io/badge/telemetry-none-4B0082.svg)](#trust-model)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](#contributing)

</div>

---

**`LocalLab`** is the umbrella home for a family of small, sharp, **local-first** Python tools for agentic work. Each tool lives in its own repo, does one job, runs fully on your machine, and installs with `pipx`. No accounts, no API keys in our code, no phone home.

Think of it as a **laboratory you own**: record agent runs, audit token spend, lint tool calls, cap costs, cache tool results, checkpoint state, and convert transcripts between providers — all offline, all under your control.

## ✨ Why this exists

The agent ecosystem is moving fast, but the tooling around it is mostly either:

- **Hosted SaaS that wants your API keys**, or
- **Heavy frameworks that do everything and own your workflow**.

There is a gap in the middle for **small, sharp, local-first tools** you can read end-to-end, run offline, and own completely. LocalLab fills that gap.

## 🎯 Who this is for

- **Agent builders** who want visibility into what their agents are actually doing.
- **Developers shipping agent features** who need regression tests for non-deterministic runs.
- **Teams watching model spend** who want hard spend caps and token forensics.
- **MCP ecosystem users** who want OpenAI-compatible bridges and local caching.
- **Anyone** who believes their agent session data should stay on their machine.

## 📦 The tools

| # | Project | Category | What it does | Status | Install |
|---|---------|----------|--------------|:------:|---------|
| 1 | [agent-vcr](https://github.com/Victorchatter/AgentVCR) | Debug | Record/replay agent runs with tool outputs stubbed | ✅ | `pipx install git+https://github.com/Victorchatter/AgentVCR.git` |
| 2 | [tokenauditor](https://github.com/Victorchatter/Tokenauditor) | Observability | Per-turn token breakdown + waste flags from any transcript | ✅ | `pipx install git+https://github.com/Victorchatter/Tokenauditor.git` |
| 3 | [toolcall-linter](https://github.com/Victorchatter/toolcall-linter) | Debug | Lint agent tool calls against declared schemas | ✅ | `pipx install git+https://github.com/Victorchatter/toolcall-linter.git` |
| 4 | [agent-circuit-breaker](https://github.com/Victorchatter/agent-circuit-breaker) | Runtime | Hard-cap model spend per-run/per-day + kill switch | ✅ | `pipx install git+https://github.com/Victorchatter/agent-circuit-breaker.git` |
| 5 | toolcall-cache | Runtime | Content-addressed cache for MCP tool results | ✅ | _repo coming soon — see [PROJECTS.md](PROJECTS.md)_ |
| 6 | [agent-checkpoint](https://github.com/Victorchatter/agent-checkpoint) | Runtime | Save/resume an agent run via a canonical JSONL tape | 🚧 | _see [PROJECTS.md](PROJECTS.md)_ |
| 7 | transcript-bridge | Interop | Convert agent transcripts between provider formats | 📋 | _see [PROJECTS.md](PROJECTS.md)_ |
| 8 | mcp-openai-bridge | Interop | Expose MCP servers as OpenAI function-calling tools | 📋 | _see [PROJECTS.md](PROJECTS.md)_ |
| 9 | prompt-portability-linter | Interop | Flag vendor-locked features in your prompts | 📋 | _see [PROJECTS.md](PROJECTS.md)_ |
| 10 | transcript-to-test | Debug | Turn a recorded run into a pytest regression test | 📋 | _see [PROJECTS.md](PROJECTS.md)_ |

**Status:** ✅ built & shipped · 🚧 in progress · 📋 planned

See **[PROJECTS.md](PROJECTS.md)** for the full map: repo links, local paths, install commands, specs, and seeds.

## 🚀 Quick start

Record a run, audit it, and lint its tool calls in three commands:

```bash
# 1. Record an agent run to a JSONL tape
agent-vcr record -- claude -p "refactor the auth module"

# 2. See exactly where your tokens went
tokenauditor tape.jsonl

# 3. Verify every tool call matches the declared schemas
toolcall-linter tape.jsonl --tools tools.json
```

## 🔗 How they fit together

Four projects share **one JSONL event envelope** — a *tape* — so a recording from one is consumable by another without coupling:

```mermaid
flowchart LR
    Run["Agent run"] --> VCR["agent-vcr<br/>records the run"]
    VCR --> Tape[("JSONL tape")]
    Cache["toolcall-cache<br/>caches tool results"] --> Tape
    Tape --> Check["agent-checkpoint<br/>save / resume"]
    Tape --> T2T["transcript-to-test<br/>tape → regression test"]
    Bridge["transcript-bridge<br/>converts provider ↔ canonical"] <--> Tape
    style Tape fill:#2EA44F,color:#fff,stroke:#1a6b33
```

Each project is **standalone** — install one, use it alone. Built in roughly the order above, later projects reuse earlier formats rather than forking them.

## 📥 Install

Install the shipped tools individually:

```bash
pipx install git+https://github.com/Victorchatter/AgentVCR.git
pipx install git+https://github.com/Victorchatter/Tokenauditor.git
pipx install git+https://github.com/Victorchatter/toolcall-linter.git
pipx install git+https://github.com/Victorchatter/agent-circuit-breaker.git
```

Or install everything at once:

```bash
pipx install git+https://github.com/Victorchatter/AgentVCR.git \
         git+https://github.com/Victorchatter/Tokenauditor.git \
         git+https://github.com/Victorchatter/toolcall-linter.git \
         git+https://github.com/Victorchatter/agent-circuit-breaker.git
```

Then run by name:

```bash
agent-vcr record -- claude -p "fix the bug"
tokenauditor ~/.claude/projects/*/session.jsonl
toolcall-linter session.jsonl --tools tools.json
agent-circuit-breaker --run-budget 2.00 --daily-budget 20.00
```

See each project's README for full usage.

## 🛡️ Trust model

- **No telemetry.** The tools never send usage data anywhere.
- **No accounts.** No signup, no cloud dashboard, no auth provider.
- **No hosted backend.** Everything runs on your machine.
- **Your keys stay with you.** The tools sit at wire-level boundaries; your API keys go only to the providers you choose.
- **MIT licensed.** Every project and this umbrella are MIT-licensed.

## 🧱 Build a project yourself

Each project folder contains a `PROMPT.md` — a self-contained seed with the full design direction, constraints, and scope. To bootstrap one with a fresh Claude Code session:

```bash
cd /path/to/<project>
claude            # then send:  @PROMPT.md
```

The prompt drives the full `design → spec → plan → implement` flow and stops at the spec-approval gate so you stay in control.

## 🤝 Contributing

This is a solo-founded family of tools, but issues and PRs are welcome on any of the project repos. Good first contributions:

- New transcript-format parsers for `tokenauditor` / `transcript-bridge`
- New vendor-lock rules for `prompt-portability-linter`'s `rules.yaml`
- New cacheability denylist entries for `toolcall-cache`
- Self-checks and edge-case reports from real agent runs

Please keep the philosophy: **local-first, small, MIT, no telemetry.**

## 📄 License

[MIT](LICENSE) — every project in the family and this umbrella.

---

<div align="center">

**[→ Full project index: PROJECTS.md](PROJECTS.md)**

Built by [Victor](https://github.com/Victorchatter) · 2026

</div>