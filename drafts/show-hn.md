<!--
VERIFY BEFORE POSTING:
- [x] All ten tools install from PyPI with their distribution names (8 live now, remaining 2 retried every 30 min).
      `pipx install tokenauditor toolcall-linter transcript-to-test localab-circuit-breaker toolcall-cache
       localab-checkpoint transcript-bridge mcp-openai-bridge prompt-portability-linter localab-vcr`
- [x] GitHub topics/descriptions verified live on all 11 repos.
- [x] CI-green claim re-verified 2026-07-29 via `gh run list -R Victorchatter/<repo> --limit 1` on all ten repos
      (all `completed / success`, Python 3.10 + 3.13).
- [ ] Re-run the dogfood example against a current local transcript before quoting numbers publicly —
      the 503-turn / 475,630-token figure is from 2026-07-25. The transcript itself is not shared,
      only the aggregate numbers.
- [ ] Confirm the three named competitors still describe themselves the way this post describes them
      (context-viewer, MCP-Bridge, Sagar Chhatrala's agent-circuit-breaker, Pramod Voola's agent-vcr) —
      READMEs and feature sets drift.
- [ ] HN penalizes posts that read as a portfolio dump. If this doesn't land, the likely failure mode is
      "10 tools" reading as unfocused — have a one-line answer ready for "why not just one tool" in comments.
-->

**Title:** Show HN: LocalLab – 10 local-first CLIs for agent work, sharing one tape format

**URL:** https://github.com/Victorchatter/LocalLab

**Text:**

I kept hitting the same five problems building and running Claude Code / MCP agents: I couldn't see where my token budget went, tool calls silently drifted from their schemas, spend had no hard ceiling, agent transcripts were locked to whichever provider recorded them, and every regression test I wrote by hand went stale the moment the agent's phrasing changed.

None of these are novel problems, and — to be upfront — most of the individual tools I built aren't novel solutions either. `tokenauditor` does roughly what [context-viewer](https://github.com/auditt98/context-viewer) does. `mcp-openai-bridge` does a narrower version of what [MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge) does, which is more mature and in `awesome-mcp-servers`. There's already a PyPI package named `agent-circuit-breaker` (Sagar Chhatrala's, v1.4.8) with near-identical positioning to mine, and one named `agent-vcr` (Pramod Voola's) that already ships a `diff` command mine doesn't have yet.

What I couldn't find is any of these as a *family*: ten small tools, one MIT license each, no telemetry, no accounts, `pipx`-installable, built against a shared JSONL tape envelope. Every prior-art hit I found is a one-off.

**This is now true end to end, and it wasn't a week ago.** One tape from `agent-vcr` is read by `tokenauditor` (which gets an *exact* system+tools prefix from it rather than an inferred one), converted by `transcript-bridge`, and turned into a pytest regression by `transcript-to-test`. Each has a selfcheck asserting it, running in CI on every push. Getting there meant fixing a reader that crashed on every real tape — it had only ever been tested against a hand-built fixture.

Install any tool with `pipx install <name>`:

```bash
pipx install localab-vcr tokenauditor toolcall-linter transcript-to-test \
  localab-circuit-breaker toolcall-cache localab-checkpoint \
  transcript-bridge mcp-openai-bridge prompt-portability-linter
```

The two `localab-*` names are because `agent-circuit-breaker` and `agent-vcr` were already taken on PyPI by unrelated projects; the repos and CLI names stay `agent-circuit-breaker` / `agent-vcr`. The umbrella CLI is `pipx install locallab`.

Repo: https://github.com/Victorchatter/LocalLab

If you try one and it breaks, file an issue — real bug reports are worth more than stars to me right now.

