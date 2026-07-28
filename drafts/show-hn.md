<!--
VERIFY BEFORE POSTING:
- [ ] Run `pipx install git+https://github.com/Victorchatter/Tokenauditor.git` on a clean machine/venv and confirm it works (repo is public but nothing is on PyPI yet).
- [ ] Re-run the dogfood example against the live file path before pasting output publicly —
      C:\Users\Victor\.claude\projects\C--Users-Victor\5b965cfd-fb0d-483c-a800-b220d0edb27d.jsonl
      (503-turn session, tiktoken mode; verified 2026-07-25). The transcript itself is not shared,
      only the aggregate numbers.
- [ ] Confirm all three named competitors still describe themselves the way this post describes them
      (context-viewer, MCP-Bridge, Sagar Chhatrala's agent-circuit-breaker, Pramod Voola's agent-vcr) —
      READMEs and feature sets drift.
- [ ] Double check GitHub topics/description are live on all 11 repos before this goes up — a Show HN
      that gets clicked into an undecorated repo wastes the traffic.
- [ ] HN penalizes posts that read as a portfolio dump. If this doesn't land, the likely failure mode is
      "10 tools" reading as unfocused — have a one-line answer ready for "why not just one tool" in comments.
- [ ] CI-green claim verified 2026-07-25 via `gh run list -R Victorchatter/<repo> --limit 1` on all ten repos
      (all `completed / success`) — re-check right before posting in case a later commit broke a run.
-->

**Title:** Show HN: LocalLab – 10 local-first CLIs for agent work, sharing one tape format

**URL:** https://github.com/Victorchatter/LocalLab

**Text:**

I kept hitting the same five problems building and running Claude Code / MCP agents: I couldn't see where my token budget went, tool calls silently drifted from their schemas, spend had no hard ceiling, agent transcripts were locked to whichever provider recorded them, and every regression test I wrote by hand went stale the moment the agent's phrasing changed.

None of these are novel problems, and — to be upfront — most of the individual tools I built aren't novel solutions either. `tokenauditor` does roughly what [context-viewer](https://github.com/auditt98/context-viewer) does. `mcp-openai-bridge` does a narrower version of what [MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge) does, which is more mature and in `awesome-mcp-servers`. There's already a PyPI package named `agent-circuit-breaker` (Sagar Chhatrala's, v1.4.8) with near-identical positioning to mine, and one named `agent-vcr` (Pramod Voola's) that already ships a `diff` command mine doesn't have yet.

What I couldn't find is any of these as a *family*: ten small tools, one MIT license each, no telemetry, no accounts, `pipx`-installable, built against a shared JSONL tape envelope. Every prior-art hit I found is a one-off.

**This is now true end to end, and it wasn't a week ago.** One tape from `agent-vcr` is read by `tokenauditor` (which gets an *exact* system+tools prefix from it rather than an inferred one), converted by `transcript-bridge`, and turned into a pytest regression by `transcript-to-test`. Each has a selfcheck asserting it, running in CI on every push. Getting there meant fixing a reader that crashed on every real tape — it had only ever been tested against a hand-built fixture.

