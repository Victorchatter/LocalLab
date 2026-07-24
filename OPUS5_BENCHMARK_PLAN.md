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

## Round 1 results (2026-07-24)

Ran a small warm-up task first, direct via `claude -p --model <opus|sonnet>`
in isolated sandboxes (not through agent-vcr yet — that needs its proxy set up;
noted as follow-up below). Task: implement `is_balanced(s)` + a self-test,
run it, confirm it passes. Verified both solutions independently (didn't just
trust the self-report).

| Metric | Opus 5 | Sonnet 5 |
|---|---|---|
| Cost | $0.398 | $0.264 |
| API time | 17.0s | 9.6s |
| Output tokens | 625 | 493 |
| Turns | 3 | 3 |
| Test cases written (asked for 6) | 9 | 6 |
| Correctness | pass | pass |

Both got it right. Opus 5 volunteered more test coverage than asked, at
~50% higher cost and ~77% more API time — for a task this small, that's
the expected "flagship does more work" pattern, not yet a meaningful quality
signal. Posted as `LINKEDIN_POST_OPUS5_RESULTS.md`.

Still open, per the original plan:
- [ ] Wire up agent-vcr/tokenauditor/toolcall-linter properly instead of
      reading `claude -p --output-format json` directly
- [ ] Run an actual Korrin-shaped task and a LocalLab dev task (the harder,
      multi-step cases where a capability gap is more likely to show)
- [ ] Long-horizon/autonomous-run degradation check
