"""LocalLab umbrella CLI."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

from . import __version__, load_tools
from . import pipeline as pipeline_mod


def _tool_command(tool_name: str, extra: list[str]) -> list[str]:
    """Return the argv list for invoking an installed tool.

    Use the full resolved path so the subprocess call works on Windows even
    when the executable relies on PATHEXT. Script files (.py, .bat, .cmd) need
    an interpreter wrapper on Windows.
    """
    resolved = shutil.which(tool_name)
    if not resolved:
        return [sys.executable, "-m", tool_name.replace("-", "_"), *extra]

    lower = resolved.lower()
    if os.name == "nt":
        if lower.endswith(".py") or lower.endswith(".pyw"):
            return [sys.executable, resolved, *extra]
        if lower.endswith(".bat") or lower.endswith(".cmd"):
            return ["cmd", "/c", resolved, *extra]
    return [resolved, *extra]


def _run_tool(tool_name: str, extra: list[str]) -> tuple[int, str, str]:
    cmd = _tool_command(tool_name, extra)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return -1, "", f"{tool_name}: command not found"
    except subprocess.TimeoutExpired:
        return -2, "", f"{tool_name}: timed out"


def _pipx_run(args: list[str], *, check: bool = False) -> subprocess.CompletedProcess:
    cmd = ["pipx", *args]
    try:
        return subprocess.run(cmd, check=check, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError("pipx not found on PATH. Install pipx first.") from exc


def cmd_install_all(args: argparse.Namespace) -> int:
    tools = load_tools()
    print("Installing all LocalLab tools via pipx...")
    failures = []
    for name, meta in tools.items():
        repo = meta["repo"]
        url = f"git+https://github.com/Victorchatter/{repo}.git"
        print(f"\n[{name}] pipx install {url}")
        result = _pipx_run(["install", url])
        if result.returncode != 0:
            print(f"  failed: {result.stderr.strip()}", file=sys.stderr)
            failures.append(name)
        else:
            print(f"  installed")
    print("\nInstall summary:")
    for name, meta in tools.items():
        pkg = meta["package"]
        if name in failures:
            print(f"  {name}: FAILED")
            continue
        ver_rc, ver_out, ver_err = _run_tool(name, ["--version"])
        if ver_rc == 0:
            version = (ver_out + ver_err).strip().splitlines()[0]
        else:
            version = "unknown"
        print(f"  {name} ({pkg}): {version}")
    if failures:
        print(f"\n{len(failures)} install(s) failed.", file=sys.stderr)
        return 1
    print("\nAll LocalLab tools installed.")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    tools = load_tools()
    print("Upgrading all LocalLab tools via pipx...")
    failures = []
    for name, meta in tools.items():
        pkg = meta["package"]
        print(f"\n[{name}] pipx upgrade {pkg}")
        result = _pipx_run(["upgrade", pkg])
        if result.returncode != 0:
            # A common "success" case is "not installed" which still exits nonzero.
            msg = result.stderr.strip() or result.stdout.strip()
            if "not installed" in msg.lower():
                print(f"  skipped: {pkg} not installed")
                continue
            print(f"  failed: {msg}", file=sys.stderr)
            failures.append(name)
        else:
            print(f"  upgraded")
    if failures:
        print(f"\n{len(failures)} upgrade(s) failed.", file=sys.stderr)
        return 1
    print("\nAll LocalLab tools upgraded.")
    return 0


def cmd_versions(args: argparse.Namespace) -> int:
    tools = load_tools()
    widths = {"name": max(len(n) for n in tools), "status": 12}
    print(f"{'tool':<{widths['name']}}  {'version':<{widths['status']}}")
    print("-" * (widths["name"] + widths["status"] + 2))
    for name in tools:
        rc, out, err = _run_tool(name, ["--version"])
        text = (out + err).strip()
        if rc != 0 or not text:
            print(f"{name:<{widths['name']}}  not installed")
            continue
        first = text.splitlines()[0]
        # Extract a version-like token if present.
        m = _version_from_text(first)
        version = m if m else first
        print(f"{name:<{widths['name']}}  {version:<{widths['status']}}")
    return 0


def _version_from_text(text: str) -> str:
    """Look for a version token such as 'agent-vcr 0.4.0' or just '0.4.0'."""
    for token in text.split():
        if re.match(r"^\d+\.\d+\.\d+([a-z0-9.+-]*)?$", token, re.IGNORECASE):
            return token
    return ""


def cmd_doctor(args: argparse.Namespace) -> int:
    tools = load_tools()
    failures = []
    print("LocalLab doctor")
    print("-" * 40)
    for name, meta in tools.items():
        smoke = list(meta.get("smoke") or ["--help"])
        rc, out, err = _run_tool(name, smoke)
        status = "PASS" if rc == 0 else "FAIL"
        print(f"  {name} {' '.join(smoke)} ... {status}")
        if rc != 0:
            failures.append(name)
            detail = (err or out).strip().splitlines()[0] if (err or out) else ""
            if detail:
                print(f"    {detail}")
    print("-" * 40)
    if failures:
        print(f"Failures: {', '.join(failures)}", file=sys.stderr)
        return 1
    print("All tools healthy.")
    return 0


def cmd_pipeline(args: argparse.Namespace) -> int:
    return pipeline_mod.run(args.recipe, dry_run=args.dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="locallab",
        description="Umbrella CLI for the LocalLab family of local-first agent tools.",
    )
    parser.add_argument(
        "--version", action="version", version=f"locallab {__version__}"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser(
        "install-all",
        help="install all 10 LocalLab tools via pipx (requires network)",
    ).set_defaults(func=cmd_install_all)

    sub.add_parser(
        "update",
        help="upgrade all installed LocalLab tools via pipx (requires network)",
    ).set_defaults(func=cmd_update)

    sub.add_parser(
        "versions",
        help="print installed versions of each tool (offline; uses --version)",
    ).set_defaults(func=cmd_versions)

    sub.add_parser(
        "doctor",
        help="smoke-test each installed tool with a deterministic command (offline)",
    ).set_defaults(func=cmd_doctor)

    pipe = sub.add_parser(
        "pipeline",
        help="run a cross-tool pipeline recipe YAML (offline when recipes are local)",
    )
    pipe.add_argument("recipe", help="path to recipe YAML")
    pipe.add_argument(
        "--dry-run",
        action="store_true",
        help="print resolved commands without executing",
    )
    pipe.set_defaults(func=cmd_pipeline)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
