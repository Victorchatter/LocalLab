<!--
VERIFY BEFORE POSTING:
- [x] All ten tools install from PyPI with their distribution names (8 live now, remaining 2 retried every 30 min).
      `pipx install tokenauditor toolcall-linter transcript-to-test localab-circuit-breaker toolcall-cache
       localab-checkpoint transcript-bridge mcp-openai-bridge prompt-portability-linter localab-vcr`
- [x] GitHub topics/descriptions verified live on all 11 repos.
- [x] CI-green claim re-verified 2026-07-29 via `gh run list -R Victorchatter/<repo> --limit 1` on all ten repos.
- [ ] Re-verify the 475,630-token / ~106x figure against a current local transcript before tweets 3 goes out.
- [ ] Confirm you're comfortable naming competitors directly in tweet 2.
- [ ] Thread numbering breaks if you edit tweets after posting — reread as a whole once before sending.
-->

**1/**
Built 10 local-first CLIs for debugging/auditing AI agent sessions.

No accounts. No telemetry. MIT. Install with pipx.

The individual tools aren't all new ideas. What's new (as far as I can find) is shipping them as one family that shares a tape format.

🧵

**2/**
Being upfront about prior art because I actually checked:

• tokenauditor overlaps with context-viewer
• mcp-openai-bridge is a narrower MCP-Bridge
• PyPI already had agent-circuit-breaker and agent-vcr, so ours install as localab-*

The family is the claim, not each tool alone.

**3/**
The number that made me finish this:

Ran tokenauditor on my own 503-turn Claude Code session. One Read tool result = ~475,630 tokens. Every user message in the whole session combined = ~4,473.

One tool call, ~106x my entire side of the conversation.

**4/**
That's why the shared tape matters.

One JSONL envelope every tool reads/writes, instead of ten tools each inventing their own format.

Record → audit → lint → test → cache → cap spend. Same tape.

**5/**
The tools:

agent-vcr • tokenauditor • toolcall-linter • transcript-to-test
agent-circuit-breaker • toolcall-cache • agent-checkpoint
transcript-bridge • mcp-openai-bridge • prompt-portability-linter

Each does one job. Each runs offline. Each pipx-installable.

**6/**
Install the whole lab:

```bash
pipx install localab-vcr tokenauditor toolcall-linter transcript-to-test \
  localab-circuit-breaker toolcall-cache localab-checkpoint \
  transcript-bridge mcp-openai-bridge prompt-portability-linter
```

Or grab the umbrella: `pipx install locallab`

**7/**
Built this because I needed it. If you run local AI agents and you've ever stared at a JSONL file wondering where the money went, try one and tell me what breaks.

Repo: github.com/Victorchatter/LocalLab
