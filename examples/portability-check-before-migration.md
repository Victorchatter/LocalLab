# Check prompt portability before migrating providers

Run `prompt-portability-linter` on your system prompt and tool definitions
before moving a Claude-built agent to OpenAI, Gemini, or another provider.

## What you need

- `prompt-portability-linter` installed (`pipx install git+https://github.com/Victorchatter/prompt-portability-linter.git`)

## Copy-paste commands

```bash
# 1. Save the prompt and tool definitions you plan to migrate.
cat > system.md <<'EOF'
You are a helpful coding assistant.

Use cache_control breakpoints to keep the long instructions warm.
When you call a function, set response_format to json_schema and strict: true.
EOF

# 2. Lint for vendor-locked features.
prompt-portability-linter \
  --prompt system.md \
  --tools tools.json \
  --score \
  --format json \
  -o portability.json

# 3. Inspect the score.
cat portability.json | python -m json.tool
```

## Expected output

```text
anthropic
  system.md:line 3  anthropic-cache-control
    Anthropic prompt cache breakpoints (cache_control) are not portable.
    Suggestion: Remove cache_control blocks; manage context size in app code.

openai
  system.md:line 5  openai-response-format
    OpenAI structured-output response_format is not portable.
    Suggestion: Request plain text or JSON and validate the schema yourself.

2 portability blockers found.
Portability score: 70/100
```

A score below 100 tells you exactly which constructs to remove or wrap before
the migration.

## Why this matters

Provider-specific features (`cache_control`, `response_format`,
`responseSchema`, `/compact`) are easy to add and hard to remove later. Catching
them before you switch providers turns a potential rewrite into a small
editing task.
