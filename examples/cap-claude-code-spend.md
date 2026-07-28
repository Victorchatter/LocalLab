# Cap Claude Code spend with agent-circuit-breaker

Hard-cap a single Claude Code run at $5 so a runaway loop or oversized context
window cannot surprise you with a large bill.

## What you need

- `agent-circuit-breaker` installed (`pipx install git+https://github.com/Victorchatter/agent-circuit-breaker.git`)
- `claude` CLI installed and authenticated with your own API key

## Copy-paste commands

```bash
# 1. Start the breaker proxy with a $5 per-run cap.
agent-circuit-breaker \
  --run-budget 5.00 \
  --daily-budget 20.00 \
  --port 8080 \
  --anthropic-base-url https://api.anthropic.com

# 2. In another terminal, point Claude Code at the proxy.
export ANTHROPIC_BASE_URL=http://127.0.0.1:8080/anthropic
claude -p "refactor the entire codebase using the most expensive model"
```

## Expected output

While the run is under budget you see normal Claude Code output. Once the
proxied spend reaches $5.00 the breaker returns an error like:

```text
429 Budget exhausted: run cap 5.00 reached
```

Claude Code surfaces the error and stops making further model calls. Your
actual Anthropic bill is capped at $5 for that run.

## Why this matters

Agentic tools can issue dozens or hundreds of model calls in a single session.
A coding assistant with a long context window and an expensive model can burn
through a budget before you notice. A local, hard spend cap keeps the worst
case predictable and does not require trusting a hosted dashboard.
