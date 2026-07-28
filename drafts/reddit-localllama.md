<!--
VERIFY BEFORE POSTING:
- [ ] r/LocalLLaMA's mods are strict about self-promo cadence — check the sub's current self-promo rules
      (some require a flair, some require an account-age/karma minimum) before posting.
- [ ] Re-verify the dogfood numbers (475,630 tokens / ~106x / 503 turns, plus the 2.78x offline-heuristic
      undercount on tool_results) against the live transcript file before quoting them:
      C:\Users\Victor\.claude\projects\C--Users-Victor\5b965cfd-fb0d-483c-a800-b220d0edb27d.jsonl
      (verified 2026-07-25 — this audience is the most likely to actually reproduce it, so it needs to hold up).
- [ ] This audience will ask "does this work with Ollama / local models, not just Claude/OpenAI?" — the
      honest answer today is: tokenauditor and transcript-bridge parse Claude Code JSONL, OpenAI messages
      JSON, and Codex traces, NOT raw Ollama/llama.cpp logs. Don't imply otherwise; say it plainly if asked.
- [ ] Confirm the "no telemetry" and "no accounts" claims are still true for all 10 repos before posting —
      this is the exact claim this audience will test first.
- [ ] CI-green claim verified 2026-07-25 via `gh run list -R Victorchatter/<repo> --limit 1` on all ten repos
      (all `completed / success`, Python 3.10 + 3.13) — re-check right before posting.
- [ ] Consider flair: "Resources" or "Tutorial | Guide" depending on subreddit convention that week.
-->

**Title:** I built 10 offline CLI tools for debugging/auditing AI agent sessions — no accounts, no telemetry, MIT

**Body:**

Posting here specifically because this crowd tends to actually care about the "local" part and not just tolerate it.

I run a lot of Claude Code and MCP-based agent sessions, and got tired of three things: not knowing where my token budget actually went until the bill showed up, tool calls silently drifting from their declared schemas, and every agent transcript being locked to whatever tool recorded it. So over the last few weeks I built ten small Python CLIs, each doing one job, each running entirely on-machine:

- `tokenauditor` — parses a Claude Code / OpenAI / Codex transcript and shows a per-turn token breakdown plus waste flags (heavy tool result, context growth, repeat calls). Reads a `tiktoken` BPE table on first run unless you pass `--offline`, in which case it falls back to a documented `~4 chars/token` heuristic and labels every number so you know which one you're looking at.
- `agent-vcr` — records an agent run to a JSONL tape (model traffic + tool calls) and replays it with tools stubbed, so you can reproduce a bug without re-running anything live.
- `toolcall-linter` — checks recorded tool calls against declared JSON schemas.
- `agent-circuit-breaker` — a local proxy that hard-caps spend per-run/per-day and refuses (doesn't silently degrade) when you hit the cap.
- `toolcall-cache` — content-addressed local cache for MCP tool results.
- `transcript-bridge` / `mcp-openai-bridge` / `prompt-portability-linter` — interop tools for moving transcripts and prompts between providers without silently losing fields.
- `agent-checkpoint`, `transcript-to-test` — save/resume a run, turn a recorded run into a pytest regression.

None of these run a model themselves and none of them need an API key of their own — they operate on transcripts and traffic your existing agent already produces, entirely offline. `--offline` on tokenauditor guarantees zero network calls, not just "no calls unless something's missing."

I want to be straight about prior art, because I looked and some of it exists: `tokenauditor` overlaps with [context-viewer](https://github.com/auditt98/context-viewer) (web UI instead of CLI, otherwise similar job), and `mcp-openai-bridge` is a narrower version of the more mature [MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge). What's actually new here, as far as I've found, is the set rather than any single tool: one coherent, MIT, no-telemetry family built against a shared JSONL tape envelope, instead of ten unrelated repos.

**This is now true end to end, and it wasn't a week ago.** One tape from `agent-vcr` is read by `tokenauditor` (which gets an *exact* system+tools prefix from it rather than an inferred one), converted by `transcript-bridge`, and turned into a pytest regression by `transcript-to-test`. Each has a selfcheck asserting it, running in CI on every push. Getting there meant fixing a reader that crashed on every real tape — it had only ever been tested against a hand-built fixture.

