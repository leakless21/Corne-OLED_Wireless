#!/usr/bin/env python3
"""
End-to-end static validation for the Corne + Karabiner + AeroSpace host protocol.

Validates the three layers of the architecture:
  Layer A (Producer):   Semantic HID signals defined in config/corne.keymap
  Layer B (Translator): Karabiner-Elements complex rules in hosts/macos/karabiner.json
  Layer C (Consumer):   AeroSpace window manager bindings in hosts/macos/aerospace.toml

Enforces that every emitted firmware signal has a corresponding host translation,
and that every generated AeroSpace chord has an active binding in the expected mode.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KEYMAP_PATH = REPO_ROOT / "config" / "corne.keymap"
KARABINER_PATH = REPO_ROOT / "hosts" / "macos" / "karabiner.json"
AEROSPACE_PATH = REPO_ROOT / "hosts" / "macos" / "aerospace.toml"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


# -----------------------------------------------------------------------------
# Layer A: Firmware Protocol Producer (config/corne.keymap)
# -----------------------------------------------------------------------------

def validate_firmware_producer(content: str) -> dict:
    """Verify that all expected semantic signals exist on the HOST and NAV/MOUSE layers."""
    # Find HOST layer bindings
    host_match = re.search(
        r"HOST\s*\{\s*label\s*=\s*\"HOST\";[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;\s*\};",
        content,
    )
    if not host_match:
        fail("HOST layer not found in config/corne.keymap")

    host_raw = host_match.group(1)

    expected_host_signals = [
        # Workspaces 1-5 (WEB, DEV, COMMS, RUN, AUX)
        "&kp F13", "&kp F14", "&kp F15", "&kp F16", "&kp F17",
        # Move window to workspace 1-5 + follow
        "&kp LS(F13)", "&kp LS(F14)", "&kp LS(F15)", "&kp LS(F16)", "&kp LS(F17)",
        # Directional focus (Left, Down, Up, Right)
        "&kp LC(F13)", "&kp LC(F14)", "&kp LC(F15)", "&kp LC(F16)",
        # Directional move (Left, Down, Up, Right)
        "&kp LC(LS(F13))", "&kp LC(LS(F14))", "&kp LC(LS(F15))", "&kp LC(LS(F16))",
        # Context & modes
        "&kp LS(F18)",  # Resize mode
        "&kp F18",      # Previous workspace
        "&kp F19",      # Fullscreen
        "&kp F20",      # Float / tile
        # Extended semantic protocol
        "&kp LA(F13)",  # SYSTEM_LAUNCHER (Spotlight)
        "&kp LA(F14)",  # QUICK_TERMINAL (Ghostty scratchpad)
        "&kp LA(F15)",  # NEW_TERMINAL (Ghostty normal window)
        "&kp LA(F16)",  # PREVIOUS_WINDOW (focus-back-and-forth)
        "&kp LA(F18)",  # SERVICE_MODE (AeroSpace mode service)
    ]

    for signal in expected_host_signals:
        if signal not in host_raw:
            fail(f"Layer A (Firmware Producer): Missing signal '{signal}' in HOST layer")

    # Find NAV and MOUSE layer editing signals
    nav_match = re.search(
        r"NAV\s*\{\s*label\s*=\s*\"NAV\";[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;\s*\};",
        content,
    )
    mouse_match = re.search(
        r"MOUSE\s*\{\s*label\s*=\s*\"MOUSE\";[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;\s*\};",
        content,
    )
    if not nav_match or not mouse_match:
        fail("NAV or MOUSE layer not found in config/corne.keymap")

    expected_editing_signals = [
        "&kp F21",      # Copy
        "&kp F22",      # Paste
        "&kp F23",      # Cut
        "&kp F24",      # Undo
        "&kp LS(F24)",  # Redo
    ]

    for sig in expected_editing_signals:
        if sig not in nav_match.group(1):
            fail(f"Layer A (Firmware Producer): Missing editing signal '{sig}' in NAV layer")
        if sig not in mouse_match.group(1):
            fail(f"Layer A (Firmware Producer): Missing editing signal '{sig}' in MOUSE layer")

    print(f"PASS: Layer A (Firmware Producer) validated ({len(expected_host_signals)} HOST signals + {len(expected_editing_signals)} editing signals).")
    return {
        "host_signals": expected_host_signals,
        "editing_signals": expected_editing_signals,
    }


# -----------------------------------------------------------------------------
# Layer B: Karabiner Translation (hosts/macos/karabiner.json)
# -----------------------------------------------------------------------------

def validate_karabiner_translator(karabiner_data: dict) -> dict:
    """Verify that Karabiner maps all semantic signals to the intended macOS chords."""
    rules = karabiner_data.get("rules", [])
    if len(rules) < 2:
        fail("Layer B (Karabiner): Expected at least 2 rules in karabiner.json")
    # Collect all manipulators across rules
    all_manipulators = []
    for r in rules:
        for m in r.get("manipulators", []):
            all_manipulators.append(m)

    # Check device scoping conditions
    for idx, m in enumerate(all_manipulators):
        conditions = m.get("conditions", [])
        has_device_if = any(c.get("type") == "device_if" for c in conditions)
        if not has_device_if:
            fail(f"Layer B (Karabiner): Manipulator #{idx} ({m.get('from')}) is missing 'device_if' condition scoping to Corne")

    # Test matrix: (from_key, mandatory_mods_set, expected_to_key, expected_to_mods_set)
    expected_translations = [
        # Directional move
        ("f13", {"control", "shift"}, "h", {"left_alt", "left_shift"}),
        ("f14", {"control", "shift"}, "j", {"left_alt", "left_shift"}),
        ("f15", {"control", "shift"}, "k", {"left_alt", "left_shift"}),
        ("f16", {"control", "shift"}, "l", {"left_alt", "left_shift"}),
        # Directional focus
        ("f13", {"control"}, "h", {"left_alt"}),
        ("f14", {"control"}, "j", {"left_alt"}),
        ("f15", {"control"}, "k", {"left_alt"}),
        ("f16", {"control"}, "l", {"left_alt"}),
        # Move to workspace 1-5
        ("f13", {"shift"}, "1", {"left_alt", "left_shift"}),
        ("f14", {"shift"}, "2", {"left_alt", "left_shift"}),
        ("f15", {"shift"}, "3", {"left_alt", "left_shift"}),
        ("f16", {"shift"}, "4", {"left_alt", "left_shift"}),
        ("f17", {"shift"}, "5", {"left_alt", "left_shift"}),
        # Resize mode
        ("f18", {"shift"}, "r", {"left_alt"}),
        # Extended semantic protocol
        ("f13", {"option"}, "spacebar", {"left_command"}),               # LAUNCHER -> Cmd+Space
        ("f14", {"option"}, "grave_accent_and_tilde", {"left_control"}),  # QTERM -> Ctrl+`
        ("f15", {"option"}, "return_or_enter", {"left_alt"}),            # TERM -> Alt+Enter
        ("f16", {"option"}, "grave_accent_and_tilde", {"left_alt"}),      # PREV WIN -> Alt+`
        ("f18", {"option"}, "semicolon", {"left_alt", "left_shift"}),     # SERVICE -> Alt+Shift+;
        # Workspace focus 1-5
        ("f13", set(), "1", {"left_alt"}),
        ("f14", set(), "2", {"left_alt"}),
        ("f15", set(), "3", {"left_alt"}),
        ("f16", set(), "4", {"left_alt"}),
        ("f17", set(), "5", {"left_alt"}),
        # Context controls
        ("f18", set(), "tab", {"left_alt"}),                             # PREV WS -> Alt+Tab
        ("f19", set(), "f", {"left_alt"}),                               # FULL -> Alt+F
        ("f20", set(), "spacebar", {"left_alt", "left_shift"}),          # FLOAT -> Alt+Shift+Space
        # Semantic editing
        ("f24", {"shift"}, "z", {"left_command", "left_shift"}),         # Redo -> Cmd+Shift+Z
        ("f24", set(), "z", {"left_command"}),                           # Undo -> Cmd+Z
        ("f21", set(), "c", {"left_command"}),                           # Copy -> Cmd+C
        ("f22", set(), "v", {"left_command"}),                           # Paste -> Cmd+V
        ("f23", set(), "x", {"left_command"}),                           # Cut -> Cmd+X
    ]

    for from_key, from_mods, to_key, to_mods in expected_translations:
        found = False
        for m in all_manipulators:
            m_from = m.get("from", {})
            m_key = m_from.get("key_code")
            m_mods = set(m_from.get("modifiers", {}).get("mandatory", []))

            if m_key == from_key and m_mods == from_mods:
                to_list = m.get("to", [])
                if to_list:
                    t = to_list[0]
                    t_key = t.get("key_code")
                    t_mods = set(t.get("modifiers", []))
                    if t_key == to_key and t_mods == to_mods:
                        found = True
                        break
        if not found:
            fail(f"Layer B (Karabiner): Missing translation for from=({from_key}, mods={from_mods}) -> to=({to_key}, mods={to_mods})")

    print(f"PASS: Layer B (Karabiner Translation) validated ({len(expected_translations)} mappings verified with device_if scoping).")
    return {"translations": expected_translations}


# -----------------------------------------------------------------------------
# Layer C: AeroSpace Consumer (dotfiles/aerospace.toml)
# -----------------------------------------------------------------------------

def parse_toml_sections(content: str) -> dict:
    """Simple TOML section parser for mode bindings and on-window-detected."""
    sections = {}
    current_section = None

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            sections[current_section] = {}
        elif current_section and "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            sections[current_section][key] = val

    return sections


def validate_aerospace_consumer(content: str) -> None:
    """Verify AeroSpace config consumes all chords produced by Karabiner / laptop."""
    sections = parse_toml_sections(content)

    # 1. Verify mode.main.binding
    main_bindings = sections.get("mode.main.binding", {})
    required_main_bindings = [
        # Workspaces 1-5
        "alt-1", "alt-2", "alt-3", "alt-4", "alt-5",
        "alt-shift-1", "alt-shift-2", "alt-shift-3", "alt-shift-4", "alt-shift-5",
        # Directional navigation
        "alt-h", "alt-j", "alt-k", "alt-l",
        "alt-shift-h", "alt-shift-j", "alt-shift-k", "alt-shift-l",
        # Window & mode controls
        "alt-r",               # mode resize
        "alt-shift-semicolon", # mode service
        "alt-f",               # fullscreen
        "alt-shift-space",     # layout floating tiling
        "alt-tab",             # workspace-back-and-forth
        "alt-backtick",        # focus-back-and-forth
        "alt-enter",           # normal terminal launch
    ]
    for b in required_main_bindings:
        if b not in main_bindings:
            fail(f"Layer C (AeroSpace Consumer): Missing binding '{b}' in [mode.main.binding]")

    # 2. Verify mode.resize.binding (Phase 1 Regression Test!)
    resize_bindings = sections.get("mode.resize.binding", {})
    required_resize_bindings = [
        # Corne directional resize via Karabiner Alt chords
        "alt-h", "alt-j", "alt-k", "alt-l",
        # Laptop modal resize (bare letters)
        "h", "j", "k", "l",
        # Exits
        "enter", "esc",
    ]
    for b in required_resize_bindings:
        if b not in resize_bindings:
            fail(f"Layer C (AeroSpace Consumer): Missing binding '{b}' in [mode.resize.binding] (Regression: Corne resize broken!)")

    # 3. Verify mode.service.binding (Phase 11)
    service_bindings = sections.get("mode.service.binding", {})
    required_service_bindings = [
        # Tree join
        "h", "j", "k", "l",
        "alt-h", "alt-j", "alt-k", "alt-l",
        # Window swap
        "shift-h", "shift-j", "shift-k", "shift-l",
        "alt-shift-h", "alt-shift-j", "alt-shift-k", "alt-shift-l",
        # Tree manipulation
        "b", "r", "t", "a",
        # Monitor management
        "m", "shift-m",
        # Exits
        "enter", "esc",
    ]
    for b in required_service_bindings:
        if b not in service_bindings:
            fail(f"Layer C (AeroSpace Consumer): Missing binding '{b}' in [mode.service.binding]")

    # 4. Verify Ghostty is NOT automatically routed to DEV or any fixed workspace
    if "com.mitchellh.ghostty" in content and "move-node-to-workspace" in content:
        # Check if ghostty is in on-window-detected
        if re.search(r"com\.mitchellh\.ghostty[\s\S]*?move-node-to-workspace", content):
            fail("Layer C (AeroSpace Consumer): Ghostty must NOT have automatic workspace routing in on-window-detected (Phase 4)")

    print("PASS: Layer C (AeroSpace Consumer) validated (main, resize, service modes, and no Ghostty auto-routing).")


# -----------------------------------------------------------------------------
# Main Runner
# -----------------------------------------------------------------------------

def main() -> None:
    if not KEYMAP_PATH.exists():
        fail(f"Keymap file not found: {KEYMAP_PATH}")
    if not KARABINER_PATH.exists():
        fail(f"Karabiner file not found: {KARABINER_PATH}")
    if not AEROSPACE_PATH.exists():
        fail(f"AeroSpace file not found: {AEROSPACE_PATH}")

    keymap_content = KEYMAP_PATH.read_text(encoding="utf-8")
    karabiner_data = json.loads(KARABINER_PATH.read_text(encoding="utf-8"))
    aerospace_content = AEROSPACE_PATH.read_text(encoding="utf-8")

    print("=" * 70)
    print("RUNNING END-TO-END HOST PROTOCOL VALIDATION")
    print("=" * 70)

    validate_firmware_producer(keymap_content)
    validate_karabiner_translator(karabiner_data)
    validate_aerospace_consumer(aerospace_content)

    print("=" * 70)
    print("ALL END-TO-END HOST PROTOCOL VALIDATION CHECKS PASSED.")
    print("=" * 70)


if __name__ == "__main__":
    main()
