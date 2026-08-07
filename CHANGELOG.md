# LocalLab umbrella changelog

## Unreleased

### Fixed
- `selfcheck.py` failed unconditionally on POSIX (Linux/macOS): fake tools
  were written as `<name>.py`, but `shutil.which()` only matches the exact
  executable filename on non-Windows, so every tool reported "not
  installed" and `versions`/`doctor` checks always failed. Fake tools are
  now written without an extension (with the executable bit set) on POSIX.
- `locallab pipeline` never created the `{output}` directory it exposes to
  recipe steps, so the bundled example recipes (`record-audit-lint.yaml`,
  `hydrate-replay.yaml`) failed on a real (non-`--dry-run`) run as soon as
  the first step tried to write into `{output}/...`.
- An `assert.jq` expression referencing a missing JSON key crashed
  `locallab pipeline` with a raw `KeyError`/`IndexError` traceback instead
  of the documented `exit code 2` usage error.

### Added
- `AUDIT-2026-08.md`: bug/feature audit covering the umbrella CLI (verified
  against code) and all ten LocalLab tools (audited against their published
  design).

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
