<!--
VERIFY BEFORE POSTING:
- [ ] Re-verify the 475,630-token / ~106x figure and the 2.78x offline-heuristic undercount against the
      live transcript before tweets 3 and 7 go out —
      C:\Users\Victor\.claude\projects\C--Users-Victor\5b965cfd-fb0d-483c-a800-b220d0edb27d.jsonl
      (503-turn session; verified 2026-07-25).
- [ ] Confirm the repo URL resolves and the umbrella README's install block still matches what's in
      tweet 6 before posting (this is the most likely thing to have drifted since drafting).
- [ ] Twitter thread numbering breaks if you edit tweets after posting — draft is written to survive
      minor reordering but reread it as a whole thread once, not tweet-by-tweet, before sending.
- [ ] tweet 2 names three competitors by project/maintainer name — confirm you're comfortable with that
      level of directness before it's public and permanent.
- [ ] CI-green claim (tweet 6) verified 2026-07-25 via `gh run list -R Victorchatter/<repo> --limit 1` on
      all ten repos (all `completed / success`, Python 3.10 + 3.13) — re-check right before posting.
-->

**1/**
Built 10 local-first CLIs for debugging/auditing AI agent sessions. No accounts, no telemetry, MIT, install with pipx.

The individual tools aren't all new ideas. What's new (as far as I can find) is shipping them as one family that shares a tape format.

🧵

**2/**
Being upfront about prior art because I actually checked:
- tokenauditor overlaps with context-viewer (auditt98)
- mcp-openai-bridge is a narrower MCP-Bridge (SecretiveShell)
- there's already a PyPI `agent-circuit-breaker` with near-identical positioning
- there's already an `agent-vcr` that ships `diff`, which mine doesn't yet

**3/**
The number that made me actually finish this: ran tokenauditor on my own 503-turn Claude Code session. One `Read` tool result = ~475,630 tokens. Every user message in the whole session combined = ~4,473.

One tool call, ~106x my entire side of the conversation.

**4/**
That's the pitch for the family: one JSONL tape envelope every tool is built against, instead of ten tools that each invent their own.

**This is now true end to end, and it wasn't a week ago.** One tape from `agent-vcr` is read by `tokenauditor` (which gets an *exact* system+tools prefix from it rather than an inferred one), converted by `transcript-bridge`, and turned into a pytest regression by `transcript-to-test`. Each has a selfcheck asserting it, running in CI on every push. Getting there meant fixing a reader that crashed on every real tape — it had only ever been tested against a hand-built fixture.

