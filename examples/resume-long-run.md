# Save and resume a long agent run

Use `agent-checkpoint` to snapshot a long-running agent session so you can
pause it, reboot your machine, and resume without starting from scratch.

## What you need

- `agent-checkpoint` installed (`pipx install git+https://github.com/Victorchatter/agent-checkpoint.git`)
- An agent that writes the canonical JSONL checkpoint envelope (Claude Code
  can be wrapped with the `AGENT_CHECKPOINT_INIT` convention)

## Copy-paste commands

```bash
# 1. Start a long task and watch the checkpoint file grow.
agent-checkpoint save --watch -o checkpoint.jsonl -- claude -p "read every file in this repo and write a design doc"

# 2. Let it run for a while, then stop it with Ctrl+C.
# checkpoint.jsonl now contains every turn up to the stop point.

# 3. Later, resume from the checkpoint.
agent-checkpoint resume checkpoint.jsonl -- claude -p "continue the design doc"
```

## Expected output

While watching, you see checkpoint events appended:

```text
checkpoint.jsonl: 12 turns, 4.2 KB
checkpoint.jsonl: 13 turns, 4.5 KB
...
```

After resume, the agent continues from turn 13 instead of re-reading every
file from the beginning. The final output is the same as if the run had never
been interrupted.

## Why this matters

Long agent runs can take minutes or hours. A crash, a reboot, or a deliberate
pause should not waste the progress already made. A local, portable checkpoint
lets you treat an agent run like a resumable process, not a one-shot command.
