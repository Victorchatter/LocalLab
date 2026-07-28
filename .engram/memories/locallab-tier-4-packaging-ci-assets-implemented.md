---
id: "68b822b7"
type: context
tags: ["locallab", "tier-4", "github-actions", "pre-commit", "cookbook", "benchmarks", "ci"]
created: "2026-07-28T16:27:54.029Z"
source: manual
---
# LocalLab Tier 4 packaging/CI assets implemented

Implemented the Tier 4 "Community & Discoverability" features across the LocalLab family:

1. **GitHub Actions** for `toolcall-linter` and `prompt-portability-linter`.
   - Composite actions at repo root (`action.yml`).
   - Self-contained: install from the checked-out repo, no marketplace publishing or secrets.
   - Inputs/outputs per the Tier 4 spec.
   - `prompt-portability-linter` action runs a second JSON pass internally so it can always expose `score` and `findings-count`, even when the requested report format is SARIF/text.

2. **Pre-commit hooks** for both linters via `.pre-commit-hooks.yaml`.
   - Hook IDs: `toolcall-linter`, `prompt-portability-linter`.
   - Users override `args` for `--tools`, `--prompt`, `--rules`, `--format`, `--warn-only`.
   - `selfcheck.py` tests the hook with `pre-commit try-repo` when `pre-commit` is installed, skipping otherwise.

3. **Cookbook** in the `LocalLabs` umbrella repo under `examples/`.
   - Five runnable recipes: cap Claude Code spend, cache filesystem MCP, regression test from tape, portability check before migration, resume long run.
   - Each recipe has "What you need", "Copy-paste commands", "Expected output", "Why this matters".
   - Umbrella `selfcheck.py` validates recipe structure and bash code blocks.

4. **Benchmark harness publishing** for the four tools with existing `benchmarks/` directories.
   - Standardized JSON format with `tool`, `version`, `date`, `results[{name,unit,value}]`.
   - Each benchmark script writes `benchmarks/results.json` (latest) and `benchmarks/results/<date>-<tag>.json` when `BENCHMARK_TAG` is set.
   - Added `benchmarks/README.md` and `.github/workflows/benchmarks.yml` triggered only on `v*.*.*` tags; results are auto-committed by GitHub Actions.

**Version bumps applied:**
- `toolcall-linter`: 0.3.0 → 0.4.0
- `prompt-portability-linter`: 0.2.0 → 0.3.0
- `locallab` umbrella: 0.1.0 → 0.2.0

The benchmarked tools kept their current versions (their benchmark scripts read version from `pyproject.toml`).

**Why:** These assets dramatically lower adoption friction — CI integration, pre-commit guardrails, runnable examples, and published performance numbers — without changing any core tool behavior.

**How to apply:** When adding a new LocalLab tool, follow the same pattern: composite `action.yml`, `.pre-commit-hooks.yaml`, example data in `examples/`, and a `benchmarks/README.md` + tag-triggered workflow if the tool has performance-critical paths.

[[locallab-is-the-umbrella-repo-not-a-shippable-tool]]
