#!/usr/bin/env python3
"""
Generated Artifacts & Freshness Validator.

Ensures:
1. All generated artifacts (e.g. docs/host-protocol.md) are strictly fresh and in sync with protocol/semantic-v1.yaml.
2. Undeclared Signal Detection: Scans firmware keymaps and host configs to ensure no undeclared F13-F24 signals or aliases exist.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Set

# Robust path configuration for local and package execution
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    from generate_protocol_files import generate_host_protocol_table
    from lib.keymap_parser import parse_keymap_file
    from lib.protocol import ProtocolManifest, load_protocol
    from lib.validation import assert_in, assert_true, fail, load_json, load_yaml
except ImportError:
    from scripts.generate_protocol_files import generate_host_protocol_table
    from scripts.lib.keymap_parser import parse_keymap_file
    from scripts.lib.protocol import ProtocolManifest, load_protocol
    from scripts.lib.validation import assert_in, assert_true, fail, load_json, load_yaml
DOCS_HOST_PROTOCOL_PATH = REPO_ROOT / "docs" / "host-protocol.md"
CORNE_KEYMAP_PATH = REPO_ROOT / "config" / "corne.keymap"
SOFLE_KEYMAP_PATH = REPO_ROOT / "config" / "sofle.keymap"
KARABINER_PATH = REPO_ROOT / "hosts" / "macos" / "karabiner.json"
GLAZEWM_PATH = REPO_ROOT / "hosts" / "windows" / "glazewm.yaml"
AHK_PATH = REPO_ROOT / "hosts" / "windows" / "keyboard.ahk"


def test_documentation_freshness(manifest: ProtocolManifest) -> None:
    """Verify that docs/host-protocol.md contains the exact generated protocol table."""
    content = DOCS_HOST_PROTOCOL_PATH.read_text(encoding="utf-8")
    expected_table = generate_host_protocol_table(manifest)
    if expected_table not in content:
        fail(
            "docs/host-protocol.md table is stale! "
            "Run 'uv run scripts/generate_protocol_files.py' to synchronize with protocol/semantic-v1.yaml"
        )
    print("PASS: docs/host-protocol.md is up to date with protocol/semantic-v1.yaml.")


def test_undeclared_firmware_signals(manifest: ProtocolManifest) -> None:
    """Scan firmware keymaps for any F13-F24 signals not declared in protocol."""
    declared_zmk_signals = manifest.all_zmk_signals()

    # Pattern matching any F13-F24 keycodes in ZMK DTS
    fkey_pattern = re.compile(r"&kp\s+(?:[A-Z_]+\()*F(?:1[3-9]|2[0-4])\)*")

    for path, name in [(CORNE_KEYMAP_PATH, "Corne"), (SOFLE_KEYMAP_PATH, "Sofle")]:
        cfg = parse_keymap_file(path, layout=name.lower())
        for l_name, layer in cfg.layers.items():
            for b in layer.bindings:
                for match in fkey_pattern.findall(b):
                    assert_in(
                        match,
                        declared_zmk_signals,
                        f"{name} layer '{l_name}' emits undeclared protocol signal '{match}'",
                    )

    print("PASS: No undeclared protocol signals found in Corne or Sofle firmware keymaps.")


def test_undeclared_host_aliases(manifest: ProtocolManifest) -> None:
    """Verify that host configurations do not bind undeclared F13-F24 keys or aliases."""
    declared_keys = {a.signal.key.lower() for a in manifest.actions.values()}

    # Check GlazeWM keybindings
    glazewm_data = load_yaml(GLAZEWM_PATH)
    fkey_token_pattern = re.compile(r"\bf(?:1[3-9]|2[0-4])\b", re.IGNORECASE)

    all_glaze_bindings = []
    for entry in glazewm_data.get("keybindings", []):
        all_glaze_bindings.extend(entry.get("bindings", []))
    for mode in glazewm_data.get("binding_modes", []):
        for entry in mode.get("keybindings", []):
            all_glaze_bindings.extend(entry.get("bindings", []))

    for b in all_glaze_bindings:
        for match in fkey_token_pattern.findall(b):
            assert_in(
                match.lower(),
                declared_keys,
                f"GlazeWM contains undeclared F-key binding '{b}' ({match})",
            )

    print("PASS: No undeclared protocol signals found in host configurations.")


def main() -> None:
    print("=" * 70)
    print("RUNNING GENERATED ARTIFACT & PROTOCOL FRESHNESS CHECKS")
    print("=" * 70)
    manifest = load_protocol()
    test_documentation_freshness(manifest)
    test_undeclared_firmware_signals(manifest)
    test_undeclared_host_aliases(manifest)
    print("=" * 70)
    print("ALL GENERATED ARTIFACT & PROTOCOL CHECKS PASSED.")
    print("=" * 70)


if __name__ == "__main__":
    main()
