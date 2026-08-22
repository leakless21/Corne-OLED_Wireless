#!/usr/bin/env python3
"""
Static validation test suite for ZMK build configuration and West manifest.
Enforces multi-keyboard targets, pinned dependency revisions, and CI integrity.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_YAML_PATH = REPO_ROOT / "build.yaml"
WEST_YML_PATH = REPO_ROOT / "config" / "west.yml"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "build.yml"

EXPECTED_ARTIFACTS = {
    "corne-left",
    "corne-right",
    "sofle-left",
    "sofle-right",
    "settings-reset",
}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def validate_build_yaml() -> None:
    if not BUILD_YAML_PATH.exists():
        fail(f"build.yaml not found at {BUILD_YAML_PATH}")

    content = BUILD_YAML_PATH.read_text(encoding="utf-8")

    # Check that all expected artifacts are defined
    found_artifacts = set(re.findall(r"artifact-name:\s*([\w-]+)", content))
    missing = EXPECTED_ARTIFACTS - found_artifacts
    if missing:
        fail(f"build.yaml is missing expected artifact targets: {missing}")

    # Check nice_nano board definitions
    boards = re.findall(r"board:\s*([^\n]+)", content)
    for b in boards:
        b_clean = b.strip().strip('"').strip("'")
        if b_clean != "nice_nano@2.0.0//zmk":
            fail(f"build.yaml contains non-canonical board target '{b_clean}', expected 'nice_nano@2.0.0//zmk'")

    # Verify central targets have studio snippet & cmake args
    if "shield: corne_left nice_oled" not in content:
        fail("build.yaml missing 'corne_left nice_oled' shield definition")
    if "shield: sofle_left nice_oled" not in content:
        fail("build.yaml missing 'sofle_left nice_oled' shield definition")

    print(f"PASS: build.yaml validated ({len(found_artifacts)} targets: {', '.join(sorted(found_artifacts))}).")


def validate_west_manifest() -> None:
    if not WEST_YML_PATH.exists():
        fail(f"config/west.yml not found at {WEST_YML_PATH}")

    content = WEST_YML_PATH.read_text(encoding="utf-8")

    # Check for unpinned/moving revisions (e.g. revision: main or revision: master)
    for match in re.finditer(r"revision:\s*(\S+)", content):
        rev = match.group(1).strip('"').strip("'")
        if rev in ("main", "master", "develop", "HEAD"):
            fail(f"config/west.yml has unpinned floating revision '{rev}'. All projects must be pinned to explicit immutable SHAs.")

    # Check required projects
    required_projects = ["zmk", "zmk-nice-oled", "zmk-helpers"]
    for proj in required_projects:
        if f"name: {proj}" not in content:
            fail(f"config/west.yml is missing required project '{proj}'")

    print(f"PASS: config/west.yml validated (single canonical manifest with immutable pinned revisions).")


def validate_workflow_integrity() -> None:
    if not WORKFLOW_PATH.exists():
        fail(f".github/workflows/build.yml not found at {WORKFLOW_PATH}")

    content = WORKFLOW_PATH.read_text(encoding="utf-8")

    # Must run validation steps before build
    required_validators = [
        "scripts/check_corne_keymap.py",
        "scripts/check_sofle_keymap.py",
        "scripts/check_host_protocol.py",
        "scripts/check_build_config.py",
    ]
    for v in required_validators:
        if v not in content:
            fail(f".github/workflows/build.yml must execute validator '{v}'")

    # Must watch hosts/ path rather than dotfiles/
    if "dotfiles/**" in content:
        fail(".github/workflows/build.yml still references obsolete path 'dotfiles/**'")
    if "hosts/**" not in content:
        fail(".github/workflows/build.yml must include 'hosts/**' in trigger paths")

    print("PASS: .github/workflows/build.yml validated (all validation steps & updated host paths present).")


def main() -> None:
    print("=" * 70)
    print("RUNNING BUILD CONFIG & MANIFEST VALIDATION")
    print("=" * 70)

    validate_build_yaml()
    validate_west_manifest()
    validate_workflow_integrity()

    print("=" * 70)
    print("ALL BUILD CONFIG & MANIFEST VALIDATION CHECKS PASSED.")
    print("=" * 70)


if __name__ == "__main__":
    main()
