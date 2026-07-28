<!--
VERIFY BEFORE POSTING / MERGING:
- [ ] This is a PROPOSED replacement for the opening of README.md — it does not edit README.md. Paste
      manually after reading it once more with the current README open side by side.
- [ ] The current README opens with "10 small, sharp, local-first Python tools" and a philosophy/who's-it-for
      section but never names competitors or explains why a *family* is the differentiator instead of any
      single tool. This version leads with that, per LOCALLAB-ROADMAP.md Part 0.
- [ ] Re-check the "0 stars" framing isn't stale by the time this ships — if the launch posts land first,
      this line may need to change from "publicly, for the first time" to something else.
- [ ] Confirm the three named competitors (context-viewer, MCP-Bridge, the taken PyPI names) haven't shipped
      something that closes the family-vs-one-off gap since 2026-07-25 — that gap is the whole hook.
- [ ] Keep the existing badges block and everything after "## Who this is for" as-is; this only replaces
      the title block through "Why this exists."
- [ ] Added a CI badge below — confirm the workflow badge URL pattern matches what's actually configured
      per-repo (this draft assumes each repo's Actions workflow is named `ci`, since that's what
      `gh run list` showed for all ten on 2026-07-25 — `completed / success`, Python 3.10 + 3.13, all green).
      A badge on the umbrella README pointing at ten separate per-repo workflows needs ten separate badge
      URLs or a rollup — pick one before merging, don't ship a broken badge.
-->

<div align="center">

# 🧪 LocalLab

### Ten local-first Python CLIs for AI agent work, sharing one tape format.

[![10 tools](https://img.shields.io/badge/tools-10%20shipped-2EA44F.svg)](#-the-tools)
[![CI](https://img.shields.io/badge/CI-10%2F10%20green-2EA44F.svg)](#-the-tools)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Local-first](https://img.shields.io/badge/local--first-offline%20ready-2EA44F.svg)](#philosophy)
[![No telemetry](https://img.shields.io/badge/telemetry-none-4B0082.svg)](#trust-model)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](#contributing)

</div>

---

**LocalLab** is ten small Python CLIs for building, debugging, and running AI agents — recording runs, auditing token spend, linting tool calls, capping cost, caching tool results, checkpointing state, converting transcripts between providers, and turning runs into regression tests. Each tool lives in its own repo, does one job, runs fully on your machine, and installs with `pipx`. No accounts, no API keys of our own, no phone home.

## Why this exists, and why not just one tool

Most of these problems already have a solution somewhere. `tokenauditor` does roughly what [context-viewer](https://github.com/auditt98/context-viewer) does. `mcp-openai-bridge` is a narrower version of the more mature [MCP-Bridge](https://github.com/SecretiveShell/MCP-Bridge). There's an unrelated, already-published `agent-circuit-breaker` on PyPI with near-identical positioning to ours, and an `agent-vcr` that ships a `diff` command ours doesn't have yet. If you're evaluating any single tool in this repo against its category, assume a competitor exists and go look — most of the time you'll find one.

What doesn't exist, as far as we've found, is the *set*: ten tools built against one JSONL tape envelope. One tape recorded by `agent-vcr` is read by `tokenauditor` — which gets an *exact* system+tools prefix from it instead of an inferred one — converted by `transcript-bridge`, and turned into a pytest regression by `transcript-to-test`. Each of those has a selfcheck asserting it, running in CI on every push, so the claim can't quietly stop being true. MIT, no telemetry, no hosted backend, `pipx`-installable, and — unlike most of the one-off prior art above — all ten with green CI (Python 3.10 and 3.13, a real `pip install -e .` + `selfcheck.py` run per push, not a badge nobody wired up). A coherent family rather than ten repos that happen to share an author. That's the part we're actually claiming, and it's the reason this exists as a "lab" instead of shipping the strongest tool alone.

## What this is for

The agent ecosystem is moving fast, and the tooling around it is mostly either hosted SaaS that wants your API keys, or heavy frameworks that do everything and own your workflow. This fills the gap in between: small, sharp, local-first tools you can read end-to-end, run offline, and own completely — with a shared tape format so using more than one of them costs less than using them separately.

