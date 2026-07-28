"""Self-check for the locallab umbrella CLI.

Tests `locallab versions` and `locallab doctor` offline by creating fake
installed tools on a temporary PATH and pointing the CLI at them.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _run_locallab(args: list[str], env: dict[str, str]) -> tuple[int, str, str]:
    cmd = [sys.executable, "-m", "locallab.cli", *args]
    result = subprocess.run(
        cmd,
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def _write_fake_tool(bindir: Path, name: str, version: str) -> None:
    """Create a fake CLI tool as a Python script on PATH.

    On Windows the file must have a .py extension to be executable from PATH
    via PATHEXT; shutil.which('agent-vcr') will find agent-vcr.py. On Unix the
    same works when the file is executable, and the .py extension is harmless.
    """
    script = bindir / f"{name}.py"
    content = (
        "#!/usr/bin/env python3\n"
        "import sys\n"
        f"name = {name!r}\n"
        f"version = {version!r}\n"
        "if len(sys.argv) > 1 and sys.argv[1] == '--version':\n"
        "    print(f'{name} {version}')\n"
        "elif len(sys.argv) > 1 and sys.argv[1] == '--help':\n"
        "    print(f'usage: {name} [--version] [--help]')\n"
    )
    script.write_text(content, encoding="utf-8")
    if os.name != "nt":
        os.chmod(script, 0o755)


def _write_fake_tool_subcommand(bindir: Path, name: str, subcommand: str, version: str) -> None:
    script = bindir / f"{name}.py"
    content = (
        "#!/usr/bin/env python3\n"
        "import sys\n"
        f"name = {name!r}\n"
        f"subcommand = {subcommand!r}\n"
        f"version = {version!r}\n"
        "if len(sys.argv) > 1 and sys.argv[1] == subcommand:\n"
        "    print(f'{name} {subcommand} ok')\n"
        "elif len(sys.argv) > 1 and sys.argv[1] == '--version':\n"
        "    print(f'{name} {version}')\n"
        "elif len(sys.argv) > 1 and sys.argv[1] == '--help':\n"
        "    print(f'usage: {name} [{subcommand}] [--version] [--help]')\n"
    )
    script.write_text(content, encoding="utf-8")
    if os.name != "nt":
        os.chmod(script, 0o755)


def check_versions() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        bindir = Path(tmp) / "bin"
        bindir.mkdir()

        _write_fake_tool(bindir, "agent-vcr", "0.4.0")
        _write_fake_tool(bindir, "tokenauditor", "0.4.0")
        _write_fake_tool(bindir, "toolcall-linter", "0.4.0")
        _write_fake_tool(bindir, "transcript-to-test", "0.4.0")
        _write_fake_tool(bindir, "agent-circuit-breaker", "0.4.0")
        _write_fake_tool(bindir, "toolcall-cache", "0.4.0")
        _write_fake_tool(bindir, "agent-checkpoint", "0.4.0")
        _write_fake_tool_subcommand(bindir, "transcript-bridge", "formats", "0.4.0")
        _write_fake_tool(bindir, "mcp-openai-bridge", "0.4.0")
        _write_fake_tool_subcommand(bindir, "prompt-portability-linter", "rules", "0.4.0")

        env = dict(os.environ)
        env["PATH"] = str(bindir) + os.pathsep + env.get("PATH", "")
        # Point PYTHONPATH at the local package so `python -m locallab.cli` works.
        env["PYTHONPATH"] = str(ROOT)

        rc, out, err = _run_locallab(["versions"], env)
        assert rc == 0, f"versions failed: {err}\n{out}"
        assert "0.4.0" in out, f"expected version in output:\n{out}"
        assert "not installed" not in out, f"all tools should appear installed:\n{out}"


def check_doctor() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        bindir = Path(tmp) / "bin"
        bindir.mkdir()

        _write_fake_tool(bindir, "agent-vcr", "0.4.0")
        _write_fake_tool(bindir, "tokenauditor", "0.4.0")
        _write_fake_tool(bindir, "toolcall-linter", "0.4.0")
        _write_fake_tool(bindir, "transcript-to-test", "0.4.0")
        _write_fake_tool(bindir, "agent-circuit-breaker", "0.4.0")
        _write_fake_tool(bindir, "toolcall-cache", "0.4.0")
        _write_fake_tool(bindir, "agent-checkpoint", "0.4.0")
        _write_fake_tool_subcommand(bindir, "transcript-bridge", "formats", "0.4.0")
        _write_fake_tool(bindir, "mcp-openai-bridge", "0.4.0")
        _write_fake_tool_subcommand(bindir, "prompt-portability-linter", "rules", "0.4.0")

        env = dict(os.environ)
        env["PATH"] = str(bindir) + os.pathsep + env.get("PATH", "")
        env["PYTHONPATH"] = str(ROOT)

        rc, out, err = _run_locallab(["doctor"], env)
        assert rc == 0, f"doctor failed: {err}\n{out}"
        assert "PASS" in out, f"expected PASS in doctor output:\n{out}"
        assert "All tools healthy." in out, f"expected healthy summary:\n{out}"


def check_pipeline_dry_run() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        recipe_dir = Path(tmp)
        recipe = recipe_dir / "demo.yaml"
        recipe.write_text(
            "name: demo\n"
            "steps:\n"
            '  - run: "echo hello {timestamp}"\n'
            "  - assert:\n"
            '      file: "{output}/x.json"\n'
            "      jq: '.ok == true'\n",
            encoding="utf-8",
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT)

        rc, out, err = _run_locallab(["pipeline", str(recipe), "--dry-run"], env)
        assert rc == 0, f"pipeline dry-run failed: {err}\n{out}"
        assert "hello" in out, f"expected expanded command in dry-run output:\n{out}"
        assert "step" in out, f"expected step markers in dry-run output:\n{out}"


def check_pipeline_assertion() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        recipe_dir = Path(tmp)
        data = recipe_dir / "data.json"
        data.write_text('{"total_cost": 1.50}\n', encoding="utf-8")
        recipe = recipe_dir / "assert.yaml"
        recipe.write_text(
            "name: assert-demo\n"
            "steps:\n"
            "  - assert:\n"
            "      file: data.json\n"
            "      jq: '.total_cost <= 2.00'\n"
            "  - assert:\n"
            "      file: data.json\n"
            "      jq: '.total_cost > 5.00'\n",
            encoding="utf-8",
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT)

        rc, out, err = _run_locallab(["pipeline", str(recipe)], env)
        assert rc == 1, f"expected failing assertion to return 1, got {rc}:\n{out}\n{err}"
        assert "ASSERTION FAILED" in err, f"expected ASSERTION FAILED:\n{err}"


REQUIRED_RECIPE_SECTIONS = [
    "# ",
    "## What you need",
    "## Copy-paste commands",
    "## Expected output",
    "## Why this matters",
]

RECIPE_FILES = [
    "cap-claude-code-spend.md",
    "cache-filesystem-mcp.md",
    "regression-test-from-tape.md",
    "portability-check-before-migration.md",
    "resume-long-run.md",
]


def check_cookbook() -> None:
    examples_dir = ROOT / "examples"
    assert examples_dir.is_dir(), f"examples/ directory not found at {examples_dir}"
    for name in RECIPE_FILES:
        path = examples_dir / name
        assert path.exists(), f"missing recipe: {path}"
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_RECIPE_SECTIONS:
            assert section in text, f"{path} missing required section marker: {section}"
        # Every recipe must contain at least one bash fenced block.
        assert "```bash" in text, f"{path} missing a bash code block"
    print("cookbook OK")


def main() -> int:
    check_versions()
    check_doctor()
    check_pipeline_dry_run()
    check_pipeline_assertion()
    check_cookbook()
    print("locallab selfcheck OK")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(f"selfcheck FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
