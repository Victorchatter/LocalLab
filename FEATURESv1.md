# LocalLab — Feature Execution Prompts v1

This document contains self-contained implementation prompts for the next wave of LocalLab features. Each section is one tier; each tier's prompt can be copied into a fresh Claude Code session (after `@PROMPT.md`) and executed end-to-end.

> Philosophy guardrails (apply to every prompt): local-first, no telemetry, no accounts, no hosted backend, MIT license, CLI-first, `pipx install`-able, stdlib-first, each tool does one job.

---

## Tier 1 — Quick Wins: CI polish, format sniffing, cost visibility, cache observability

### Prompt

Implement the following six features across the LocalLab tool family. Work in the existing per-tool repos under `C:\Users\Victor\dev\tools\`. Do not create new umbrella-level code. Each feature must ship with updated README, `pyproject.toml` bump to `0.2.0`, `selfcheck.py` updates, and a CHANGELOG entry.

**1. `agent-vcr diff` — loss-aware tape comparison**
- Add `agent-vcr diff <tape-a> <tape-b> [--format text|json]`.
- Normalize both tapes to canonical turns.
- Compare: model outputs per turn, tool-call hashes, tool results hashes, turn count, timing.
- Report divergent turn indices, the nature of the divergence, and a final `identical|different` verdict.
- In JSON mode, emit a machine-readable diff object with arrays of `only_in_a`, `only_in_b`, `changed`.
- Exit code: `0` identical, `1` different, `2` usage error.
- Add a `selfcheck.py` case that records the same prompt twice and asserts `diff` returns identical, then mutates one tape and asserts different.

**2. Auto-detect transcript format in `transcript-to-test`**
- Remove the need for explicit `--format` in `transcript-to-test <file>`.
- Sniff order of preference: agent-vcr tape (look for `event`/`seq`/`kind` fields), Claude Code JSONL (look for `timestamp`/`message`/`type`), OpenAI messages (top-level JSON array with `role`/`content`), Codex rollout JSONL (look for Codex-specific fields).
- On ambiguity, print a clear message and require explicit `--format`.
- Add a `detect.py` module and unit tests for each format.
- Update README quick-start to remove `--format` examples.

**3. SARIF and CI JSON output for `toolcall-linter` and `prompt-portability-linter`**
- Add `--format sarif` to both tools.
- SARIF must include `runs[0].results` with `ruleId`, `message.text`, `locations[0].physicalLocation` mapped to the transcript/prompt file and line number when available.
- Keep existing `text|json` output unchanged.
- Add `--format json` to `prompt-portability-linter` if not already present.
- Add GitHub Action example in README showing how to fail a PR on blocker findings.
- Update `selfcheck.py` to validate SARIF schema against the SARIF 2.1.0 JSON schema (download once, cache locally, or include a minimal subset).

**4. Portability score + fix hints in `prompt-portability-linter`**
- Add `prompt-portability-linter --prompt prompt.md --score` which prints a `0-100` portability score and a breakdown by provider.
- Score formula: start at 100, subtract weighted points per blocker (e.g., `-10` per Anthropic-only feature, `-8` OpenAI-only, etc.) and warnings (`-3`). Document the weights in README.
- Add `--suggest-fixes` which emits a Markdown patch report: for each finding, show the original line and a concrete portable rewrite.
- For example, `cache_control` → `"replace with explicit context window management or strip when moving to OpenAI"`; `response_format: { type: "json_schema" }` → `"add a JSON schema constraint in system prompt or use provider-native structured output wrapper"`.
- Do not auto-rewrite the file. Output to stdout or `--output fixes.md`.

**5. Cost reporting in `tokenauditor` using `agent-circuit-breaker` pricing data**
- Add `tokenauditor <file> --cost` which estimates USD spend per turn and total.
- Embed or vendor a `prices.json` (reuse the one from `agent-circuit-breaker`, but keep `tokenauditor` self-contained; copy the file into the repo under `tokenauditor/data/prices.json`).
- Detect model from transcript fields (`model`, `model_id`, etc.). If unknown, use a heuristic and warn.
- Use provider-reported token counts when present; otherwise fall back to tiktoken/heuristic counts.
- Output columns: turn, input tokens, output tokens, cache tokens, cost (input/output/cache), cumulative cost.
- Add `--cost-json` for machine output.
- Update `selfcheck.py` to assert a known tape costs a known amount within 1 %.

**6. `toolcall-cache stats --watch`**
- Add `toolcall-cache stats --watch [seconds]` (default 2) which polls the SQLite store and prints a live updating table.
- Columns: total entries, hits, misses, hit rate %, entries expiring in 5 min, top 5 cached tools by hit count.
- Use ANSI escape sequences to clear screen between updates. Add `--no-clear` for CI/logging.
- Press `Ctrl+C` to exit cleanly.
- Add `selfcheck.py` test that runs the proxy, makes two identical calls, then verifies `stats` reports `hits >= 1`.

**Cross-cutting requirements for Tier 1**
- Every new CLI flag must have a usage example in the tool README.
- Every tool must pass its existing `selfcheck.py` plus new self-checks.
- Commit message convention: `feat(<tool>): <short description>`.
- Do not add heavy dependencies. SARIF can be generated with stdlib `json`; no `sarif` SDK.

---

## Tier 2 — Core Extensions: Granular budgets, fuzzy cache, checkpoint merge, schema inference, format packs, test templates

### Prompt

Implement the following seven features across the LocalLab tool family. Work in the existing per-tool repos. Bump each touched tool to `0.3.0`. Each feature ships with README updates, `selfcheck.py` extensions, and CHANGELOG entry.

**1. Per-tool and per-model budgets in `agent-circuit-breaker`**
- Extend SQLite schema: add `model` and `tool_name` columns to the spend log table.
- New CLI flags:
  - `--model-budget MODEL=USD` (repeatable)
  - `--tool-budget TOOL=USD` (repeatable)
  - `--budget-config budgets.yaml` for YAML-based multi-budget config
- Evaluate budgets in this order: kill switch → per-tool → per-model → per-run → per-day.
- When a granular budget trips, return a `429 Budget exhausted: <model/tool> cap <USD> reached` so the agent can react.
- Add `agent-circuit-breaker budgets` subcommand to list active budgets and current spend per model/tool/run/day.
- Update `prices.json` loader to support per-model lookups.
- Add `selfcheck.py` tests that trip each budget type independently.

**2. Semantic/fuzzy cache in `toolcall-cache`**
- Add `--fuzzy` mode to `toolcall-cache start`.
- Normalize args before hashing: strip whitespace, lower-case string values, ignore specified keys via `--fuzzy-ignore-keys key1,key2`.
- On cache miss, search the last N entries (configurable, default 100) for the same tool and compute a similarity score. Use Levenshtein distance on the canonical JSON string of args (stdlib-only; implement a small Levenshtein function; no external package). If score >= `--fuzzy-threshold` (default 0.85), return the cached result with a warning header in the MCP response `_meta.locallab_fuzzy_match: true`.
- Add `toolcall-cache fuzzy-test <tool> <args-a> <args-b>` to preview whether two arg sets would fuzzy-match.
- Ensure deterministic cache remains the default; fuzzy is opt-in.

**3. Checkpoint diff and merge in `agent-checkpoint`**
- Add `agent-checkpoint diff <checkpoint-a.jsonl> <checkpoint-b.jsonl>`:
  - Compare turn counts, roles, message content (scrubbing timestamps), tool calls, and results.
  - Output: summary + per-turn diff. JSON mode via `--format json`.
  - Exit codes: `0` identical, `1` different, `2` usage error.
- Add `agent-checkpoint merge <checkpoint-a.jsonl> <checkpoint-b.jsonl> -o merged.jsonl`:
  - Append turns from B that are not present in A, based on `(role, content_hash, tool_calls_hash)`.
  - Preserve `_meta.source` tags for provenance.
  - Detect and warn on conflicting tool result hashes for the same turn.
- Add round-trip `selfcheck.py` tests.

**4. Schema inference from tape in `toolcall-linter`**
- Add `toolcall-linter infer <transcript> -o tools.json [--pretty]`.
- For each tool observed in the transcript, build a JSON Schema:
  - Collect all arg objects for that tool.
  - Union required keys (key is required if present in every object).
  - Infer types: `string`, `integer`, `number`, `boolean`, `array`, `object`.
  - Infer enums for strings when <= 10 unique values.
  - Add `description` placeholders and `_meta.inferred_from: N calls`.
- Validate the inferred schema against the original tape using existing linter logic (no errors should occur if the schema is sound).
- Update README with a use case: "I have a tape but no `tools.json`".

**5. Provider format packs: Gemini, LangSmith, Langfuse, Ollama in `transcript-bridge`**
- Add reader/writer modules:
  - `formats/gemini.py`: Gemini `contents` list with `role`/`parts`.
  - `formats/langsmith.py`: LangSmith run traces (LLM + tool run spans).
  - `formats/langfuse.py`: Langfuse observation trace format.
  - `formats/ollama.py`: Ollama `/api/chat` request/response format.
- Follow the existing `reader → canonical → writer → loss report` contract.
- Each format must report loss honestly and support `--strict`.
- Add `transcript-bridge formats` listing with descriptions.
- Add one self-check round-trip per new format using synthetic data.

**6. Variable/assertion templates for `transcript-to-test`**
- Add `--assert-template` presets:
  - `exact`: current behavior (default).
  - `contains`: `--assert contains` already exists; map to `contains` template.
  - `regex`: map existing `--assert regex`.
  - `json-path`: new. `--assert-template json-path --assert-value '$.status' --assert-pattern 'success'` asserts the final answer parses as JSON and `status == success`.
  - `no-error`: new. Asserts the replay completes without exceptions; ignores final answer.
  - `structured-match`: new. Treat the final answer as JSON and assert a subset of keys match a provided schema/value snapshot.
- Preserve backward compatibility of existing CLI.
- Generated tests must remain standalone and stdlib-only.
- Add template examples to README.

**7. Auto-cost warnings in `tokenauditor`**
- Combine with feature #5 from Tier 1: when `--cost` is used, also flag turns whose cost exceeds `--cost-threshold USD` (default 0.10).
- Warnings: `EXPENSIVE_TURN`, `EXPENSIVE_TOOL` (when a tool result dominates token cost).
- Add `--cost-json` output that includes `warnings` array.

**Cross-cutting requirements for Tier 2**
- Any new storage migration in `agent-circuit-breaker` or `toolcall-cache` must auto-migrate existing SQLite files on first open.
- All fuzzy/semantic behavior must be deterministic and reproducible.
- Keep each tool under ~2.5 KLOC if possible; if a feature forces growth, split it into a new module.
- Prefer stdlib. If an external dep is unavoidable (e.g., `mcp` SDK is already required), document it.

---

## Tier 3 — Ecosystem Integrations: Umbrella CLI, cross-tool pipelines, unified state, tape-aware cache, multi-server bridge

### Prompt

Implement the following six features. The first umbrella-level package is allowed here. Each touched tool gets bumped to `0.4.0`; new umbrella package starts at `0.1.0`.

**1. `locallab` umbrella CLI package in the LocalLab repo**
- Create `locallab/` package inside the umbrella repo (`C:\Users\Victor\dev\tools\LocalLabs\`).
- Commands:
  - `locallab install-all`: install all 10 tools via `pipx install git+https://github.com/Victorchatter/<repo>.git`. Print progress and final versions.
  - `locallab update`: run `pipx upgrade` for each installed LocalLab tool.
  - `locallab versions`: print installed versions of each tool (or `not installed`).
  - `locallab doctor`: smoke-test each installed tool with a tiny deterministic command (e.g., `--help`, `formats`, `rules`) and report pass/fail.
  - `locallab pipeline <recipe.yaml>`: see feature #2.
- Store per-tool repo mapping in `locallab/data/tools.json`.
- Use `subprocess` to invoke `pipx`. Do not shell out unsafely; validate tool names against the mapping.
- Add `pyproject.toml`, README section, and `selfcheck.py` that tests `locallab versions` and `doctor` without requiring network (mock or use `--help`).

**2. Cross-tool pipeline recipes**
- Add `locallab pipeline <recipe.yaml>` command.
- Recipe YAML schema:
  ```yaml
  name: record-audit-lint
  steps:
    - run: agent-vcr record -o tape.jsonl -- {agent_cmd}
    - run: tokenauditor tape.jsonl --cost --json -o audit.json
    - run: toolcall-linter tape.jsonl --tools tools.json --format sarif -o lint.sarif
    - run: transcript-to-test tape.jsonl -o test_regression.py
    - assert:
        file: audit.json
        jq: '.total_cost <= 2.00'
    - assert:
        file: lint.sarif
        jq: '.runs[0].results | length == 0'
  ```
- Support `{input}`, `{output}`, `{timestamp}` placeholders.
- Support `--dry-run` to print commands without executing.
- Support `env:` map per step and global `env:` map.
- Exit code propagates first failing step.
- Add example recipes in `locallab/recipes/`.

**3. `agent-vcr record --test <test.py>` one-shot**
- Add `agent-vcr record -o tape.jsonl --test tests/test_run.py -- <agent-cmd>`.
- After successful recording, invoke `transcript-to-test` internally (as a Python function, not subprocess) to generate `tests/test_run.py` from the tape.
- Use the same defaults as `transcript-to-test` CLI, but allow `--assert`, `--framework`, `--scrub` passthrough via `agent-vcr` CLI.
- If `transcript-to-test` is not installed, print a helpful install hint and still save the tape.
- Add `selfcheck.py` case.

**4. Unified SQLite state directory**
- In `agent-circuit-breaker` and `toolcall-cache`, add `--state-dir ~/.locallab` default with fallback to existing per-tool defaults.
- The directory structure:
  ```
  ~/.locallab/
    agent-circuit-breaker/state.db
    toolcall-cache/cache.db
  ```
- Keep `--state` / `--db` as explicit overrides for backward compatibility.
- On first run, create the directory if it does not exist.
- Print the active state path at startup in verbose mode.
- Update READMEs and `selfcheck.py` to use temp dirs but verify `--state-dir` is honored.

**5. Tape-aware cache hydration in `toolcall-cache`**
- Add `toolcall-cache hydrate --tape tape.jsonl [--dry-run]`.
- Parse the tape and pre-populate the cache with every `tools/call` result observed.
- Skip entries where the result contains an error or is marked non-cacheable.
- Use the same hash key policy as live proxy mode.
- This lets `agent-vcr` partial replays avoid live MCP calls.
- Add `selfcheck.py` case.

**6. Multi-server aggregation in `mcp-openai-bridge`**
- Extend CLI to accept multiple servers:
  - `--stdio "cmd1" --stdio "cmd2"`
  - `--http <url1> --http <url2>`
- Namespace tool names: `server_id__tool_name`. Default `server_id` to `stdio-N` or `http-N` if not provided.
- Add `--server-id <name>` that pairs with the next `--stdio`/`--http`.
- `GET /v1/tools` returns the union.
- `POST /v1/execute` routes by the prefix before `__`.
- Update README with multi-server example.
- Add `selfcheck.py` case launching two stdio servers.

**Cross-cutting requirements for Tier 3**
- The umbrella CLI must not duplicate logic from individual tools; orchestrate only.
- All new paths must respect the existing trust model: no telemetry, no accounts, local state.
- Document which commands require network (`install-all`, `update`) and which do not (`doctor`, `versions`, `pipeline` when using local recipes).

---

## Tier 4 — Community & Discoverability: GitHub Actions, pre-commit hooks, cookbook, benchmarks, doctor

### Prompt

Implement the following five features. These are primarily packaging, documentation, and CI assets. They do not change core tool behavior but dramatically improve adoption.

**1. GitHub Action for `toolcall-linter`**
- Add `action.yml` to `toolcall-linter` repo root.
- Inputs:
  - `transcript`: path to transcript(s), glob supported.
  - `tools`: path to tools.json or MCP source.
  - `format`: `text|json|sarif` (default `sarif`).
  - `fail-on-blockers`: boolean.
- Outputs:
  - `findings-count`: number of findings.
  - `report-path`: path to generated report.
- Example workflow in README.
- Add a self-check workflow in `.github/workflows/selfcheck.yml` that runs the action on sample data.

**2. Pre-commit hooks for `toolcall-linter` and `prompt-portability-linter`**
- Add `.pre-commit-hooks.yaml` to each repo root.
- Hook IDs: `toolcall-linter`, `prompt-portability-linter`.
- Args support `--tools`, `--prompt`, `--rules`, `--format`, `--warn-only`.
- Include example `.pre-commit-config.yaml` snippet in README.
- Test locally with `pre-commit try-repo` in `selfcheck.py` if `pre-commit` is installed; skip otherwise.

**3. GitHub Action for `prompt-portability-linter`**
- Add `action.yml` to `prompt-portability-linter` repo root.
- Inputs: `prompts`, `tools`, `config`, `rules`, `format`, `warn-only`, `fail-on-blockers`.
- Outputs: `score` (0–100), `findings-count`, `report-path`.
- Add example workflow and `.github/workflows/selfcheck.yml`.

**4. Cookbook / examples directory in the umbrella repo**
- Create `examples/` directory in `LocalLabs` umbrella repo.
- Add at least five runnable recipes:
  - `cap-claude-code-spend.md`: run Claude Code through `agent-circuit-breaker` with a $5 cap.
  - `cache-filesystem-mcp.md`: run an MCP filesystem server through `toolcall-cache`.
  - `regression-test-from-tape.md`: record with `agent-vcr`, generate test with `transcript-to-test`, run in CI.
  - `portability-check-before-migration.md`: lint prompts with `prompt-portability-linter`.
  - `resume-long-run.md`: save and resume a run with `agent-checkpoint`.
- Each recipe includes copy-paste commands, expected output, and a short explanation of why it matters.

**5. Benchmark harness and published results**
- For each tool that already has a `benchmarks/` directory, add a `README.md` inside `benchmarks/` summarizing the latest numbers.
- Add a GitHub workflow (where missing) that runs benchmarks on `ubuntu-latest` and commits results to `benchmarks/results/` only on release tags (do not spam main).
- Standardize benchmark output format:
  ```json
  {
    "tool": "toolcall-cache",
    "version": "0.4.0",
    "date": "2026-08-01",
    "results": [
      {"name": "cache_hit_latency", "unit": "ms", "value": 0.8}
    ]
  }
  ```
- Link the latest results from the main README.

**Cross-cutting requirements for Tier 4**
- All CI assets must be MIT-licensed and require no secrets.
- Actions should fail gracefully when inputs are missing, with clear error messages.
- Cookbook examples must be tested manually or via `selfcheck.py` at least once before publishing.

---

## Suggested release order

1. **Ship Tier 1 as "LocalLab 0.2 — CI Ready"** — SARIF, sniffing, cost, cache watch.
2. **Ship Tier 2 as "LocalLab 0.3 — Deeper Control"** — budgets, fuzzy cache, checkpoints, format packs.
3. **Ship Tier 3 as "LocalLab 0.4 — One Lab"** — umbrella CLI, pipelines, unified state.
4. **Ship Tier 4 as "LocalLab 0.5 — Community"** — actions, hooks, cookbook, benchmarks.

Each tier should be announced with its own post cycle (see `POSTSv1.md`).
