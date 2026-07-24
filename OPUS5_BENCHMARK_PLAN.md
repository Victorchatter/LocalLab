# Opus 5 benchmark — plan for tomorrow's follow-up post

Posted the announcement on 2026-07-24. Follow-up post: publish results.

## What to test
Run Opus 5 head-to-head against the models currently in use (Sonnet 5 baseline,
+ whatever else is in rotation) on real agentic tasks — not synthetic benchmarks.

## How (using LocalLab tools)
1. `agent-vcr` — record the same task run once per model to a JSONL tape.
2. `tokenauditor` — per-turn token breakdown for each tape (cost/waste comparison).
3. `toolcall-linter` — check tool-call correctness/schema adherence per model.
4. `transcript-bridge` — normalize tapes if formats differ, for apples-to-apples diffing.

## Candidate tasks to run
- [ ] A real Korrin pipeline task (outreach sourcing/follow-up logic) — agentic, multi-step
- [ ] A LocalLab dev task (bug fix or small feature in one of the 10 tools)
- [ ] One long-horizon / autonomous-run task to check degradation over turns

## Metrics to report
- Token cost per completed task (tokenauditor)
- Tool-call error rate (toolcall-linter flags)
- Task success / correctness (manual judgment)
- Subjective: reasoning quality, instruction-following, agentic reliability

## Post angle for tomorrow
Numbers, not vibes. Show the tape-derived breakdown, name what got better/worse
vs. the previous model, keep it short like today's post.
