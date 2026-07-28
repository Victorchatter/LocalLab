# Turn an agent run into a regression test

Record a successful agent run with `agent-vcr`, generate a pytest regression
test with `transcript-to-test`, then run it in CI so future changes do not
silently break the behavior.

## What you need

- `agent-vcr` installed (`pipx install git+https://github.com/Victorchatter/AgentVCR.git`)
- `transcript-to-test` installed (`pipx install git+https://github.com/Victorchatter/transcript-to-test.git`)
- `pytest` installed (`pipx install pytest` or `pip install pytest`)

## Copy-paste commands

```bash
# 1. Record the run you want to lock in.
agent-vcr record -o tape.jsonl -- claude -p "what is 2 + 2"

# 2. Convert the tape into a standalone pytest regression test.
transcript-to-test tape.jsonl -o test_regression.py

# 3. Run the test locally.
pytest test_regression.py -v

# 4. Add it to CI.
cat > .github/workflows/regression.yml <<'EOF'
name: regression
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv tool install git+https://github.com/Victorchatter/transcript-to-test.git
      - run: uv tool install pytest
      - run: pytest test_regression.py
EOF
```

## Expected output

`transcript-to-test` writes a file like `test_regression.py` that stubs the
tool calls recorded on the tape and asserts the final answer matches:

```text
test_regression.py::test_run PASSED
```

If a later prompt or model change makes the agent produce a different answer,
the test fails with a clear diff.

## Why this matters

Agent outputs are non-deterministic. A small prompt tweak can change tool-call
patterns or final answers. Recording a golden run and turning it into a test
gives you a reproducible baseline: you catch regressions without manually
re-running the agent every time.
