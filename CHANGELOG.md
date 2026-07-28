# LocalLab umbrella changelog

## 0.2.0 — 2026-07-28

### Added
- New `examples/` cookbook directory with five runnable recipes:
  - cap Claude Code spend through `agent-circuit-breaker`
  - cache an MCP filesystem server with `toolcall-cache`
  - turn an `agent-vcr` tape into a regression test with `transcript-to-test`
  - lint prompts with `prompt-portability-linter` before provider migration
  - save and resume a long run with `agent-checkpoint`
- README sections linking the cookbook and published benchmark results.
- `selfcheck.py` validates that every cookbook recipe has the required
  structure and code blocks.

## 0.1.0 — 2026-07-28

### Added
- New `locallab` umbrella CLI package (`pipx install git+https://github.com/Victorchatter/LocalLab.git`).
- `locallab install-all`: install all 10 LocalLab tools via `pipx`.
- `locallab update`: run `pipx upgrade` for every LocalLab tool.
- `locallab versions`: print installed versions (offline).
- `locallab doctor`: deterministic smoke-test for every installed tool.
- `locallab pipeline <recipe.yaml>`: cross-tool recipe runner with placeholders, per-step and global `env`, `--dry-run`, and `jq`-like assertions.
- `locallab/data/tools.json`: mapping of tool names to repos, packages, and smoke commands.
- Example recipes in `locallab/recipes/`.
- `selfcheck.py` covering `versions`, `doctor`, and `pipeline` (fully offline).
