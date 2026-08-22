#!/usr/bin/env python3
"""
End-to-end static validation for the multi-keyboard semantic host protocol.

Validates the full architecture:
  Producers:
    - Corne firmware (config/corne.keymap)
    - Sofle firmware (config/sofle.keymap)
  macOS Consumers:
    - Karabiner-Elements translation (hosts/macos/karabiner.json)
    - AeroSpace window manager (hosts/macos/aerospace.toml)
  Windows Consumers:
    - AutoHotkey v2 bridge (hosts/windows/keyboard.ahk)
    - GlazeWM window manager (hosts/windows/glazewm.yaml)

Enforces that every emitted firmware signal has a corresponding host translation on both OSes.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CORNE_KEYMAP_PATH = REPO_ROOT / "config" / "corne.keymap"
SOFLE_KEYMAP_PATH = REPO_ROOT / "config" / "sofle.keymap"
KARABINER_PATH = REPO_ROOT / "hosts" / "macos" / "karabiner.json"
AEROSPACE_PATH = REPO_ROOT / "hosts" / "macos" / "aerospace.toml"
AHK_PATH = REPO_ROOT / "hosts" / "windows" / "keyboard.ahk"
GLAZEWM_PATH = REPO_ROOT / "hosts" / "windows" / "glazewm.yaml"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


# -----------------------------------------------------------------------------
# Layer A: Firmware Protocol Producers (Corne & Sofle)
# -----------------------------------------------------------------------------

EXPECTED_HOST_SIGNALS = [
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
    "&kp LA(F13)",  # SYSTEM_LAUNCHER (Spotlight / Windows Search)
    "&kp LA(F14)",  # QUICK_TERMINAL (Ghostty scratchpad / Quake)
    "&kp LA(F15)",  # NEW_TERMINAL (Ghostty / Windows Terminal)
    "&kp LA(F16)",  # PREVIOUS_WINDOW (focus-back-and-forth / Alt+Tab)
    "&kp LA(F18)",  # SERVICE_MODE (AeroSpace / GlazeWM service)
]

EXPECTED_EDITING_SIGNALS = [
    "&kp F21",      # Copy
    "&kp F22",      # Paste
    "&kp F23",      # Cut
    "&kp F24",      # Undo
    "&kp LS(F24)",  # Redo
]


def validate_keymap_producer(path: Path, board_name: str) -> None:
    """Verify that all expected semantic signals exist on the HOST and NAV/MOUSE layers."""
    if not path.exists():
        fail(f"Keymap file not found for {board_name}: {path}")

    content = path.read_text(encoding="utf-8")

    # Find HOST layer bindings
    host_match = re.search(
        r"HOST\s*\{\s*label\s*=\s*\"HOST\";[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;",
        content,
    )
    if not host_match:
        fail(f"{board_name}: HOST layer not found in {path}")

    host_raw = host_match.group(1)

    for signal in EXPECTED_HOST_SIGNALS:
        if signal not in host_raw:
            fail(f"{board_name}: Missing signal '{signal}' in HOST layer")

    # Find NAV and MOUSE layer editing signals
    nav_match = re.search(
        r"NAV\s*\{\s*label\s*=\s*\"NAV\";[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;",
        content,
    )
    mouse_match = re.search(
        r"MOUSE\s*\{\s*label\s*=\s*\"MOUSE\";[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;",
        content,
    )
    if not nav_match or not mouse_match:
        fail(f"{board_name}: NAV or MOUSE layer not found in {path}")

    for sig in EXPECTED_EDITING_SIGNALS:
        if sig not in nav_match.group(1):
            fail(f"{board_name}: Missing editing signal '{sig}' in NAV layer")
        if sig not in mouse_match.group(1):
            fail(f"{board_name}: Missing editing signal '{sig}' in MOUSE layer")

    print(f"PASS: Firmware Producer ({board_name}) validated ({len(EXPECTED_HOST_SIGNALS)} HOST signals + {len(EXPECTED_EDITING_SIGNALS)} editing signals).")


# -----------------------------------------------------------------------------
# Layer B: macOS Host (Karabiner & AeroSpace)
# -----------------------------------------------------------------------------

def validate_karabiner_translator(karabiner_data: dict) -> None:
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
            fail(f"Layer B (Karabiner): Manipulator #{idx} ({m.get('from')}) is missing 'device_if' condition scoping to keyboard")

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

    print(f"PASS: macOS Karabiner Translation validated ({len(expected_translations)} mappings verified with device_if scoping).")


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

    main_bindings = sections.get("mode.main.binding", {})
    required_main_bindings = [
        "alt-1", "alt-2", "alt-3", "alt-4", "alt-5",
        "alt-shift-1", "alt-shift-2", "alt-shift-3", "alt-shift-4", "alt-shift-5",
        "alt-h", "alt-j", "alt-k", "alt-l",
        "alt-shift-h", "alt-shift-j", "alt-shift-k", "alt-shift-l",
        "alt-r", "alt-shift-semicolon", "alt-f", "alt-shift-space",
        "alt-tab", "alt-backtick", "alt-enter",
    ]
    for b in required_main_bindings:
        if b not in main_bindings:
            fail(f"Layer C (AeroSpace Consumer): Missing binding '{b}' in [mode.main.binding]")

    resize_bindings = sections.get("mode.resize.binding", {})
    required_resize_bindings = [
        "alt-h", "alt-j", "alt-k", "alt-l",
        "h", "j", "k", "l",
        "enter", "esc",
    ]
    for b in required_resize_bindings:
        if b not in resize_bindings:
            fail(f"Layer C (AeroSpace Consumer): Missing binding '{b}' in [mode.resize.binding]")

    service_bindings = sections.get("mode.service.binding", {})
    required_service_bindings = [
        "h", "j", "k", "l",
        "alt-h", "alt-j", "alt-k", "alt-l",
        "shift-h", "shift-j", "shift-k", "shift-l",
        "alt-shift-h", "alt-shift-j", "alt-shift-k", "alt-shift-l",
        "b", "r", "t", "a",
        "m", "shift-m",
        "enter", "esc",
    ]
    for b in required_service_bindings:
        if b not in service_bindings:
            fail(f"Layer C (AeroSpace Consumer): Missing binding '{b}' in [mode.service.binding]")

    if "com.mitchellh.ghostty" in content and "move-node-to-workspace" in content:
        if re.search(r"com\.mitchellh\.ghostty[\s\S]*?move-node-to-workspace", content):
            fail("Layer C (AeroSpace Consumer): Ghostty must NOT have automatic workspace routing in on-window-detected")

    print("PASS: macOS AeroSpace Consumer validated (main, resize, service modes, and no Ghostty auto-routing).")


# -----------------------------------------------------------------------------
# Layer C: Windows Host (AutoHotkey & GlazeWM)
# -----------------------------------------------------------------------------

def validate_windows_ahk(content: str) -> None:
    """Verify AutoHotkey translates all required editing and desktop signals."""
    required_ahk_bindings = [
        ("+F24::", "^y", "Redo -> Ctrl+Y"),
        ("F24::", "^z", "Undo -> Ctrl+Z"),
        ("F21::", "^c", "Copy -> Ctrl+C"),
        ("F22::", "^v", "Paste -> Ctrl+V"),
        ("F23::", "^x", "Cut -> Ctrl+X"),
        ("!F13::", "#s", "Launcher -> Win+S"),
        ("!F14::", "wt", "Quick Terminal"),
        ("!F15::", "wt.exe", "New Terminal -> wt.exe"),
        ("!F16::", "Tab", "Previous Window -> Alt+Tab"),
    ]

    for trigger, target, desc in required_ahk_bindings:
        if trigger not in content:
            fail(f"Windows AutoHotkey: Missing hotkey trigger '{trigger}' for {desc}")

    # Ensure +F24 appears before bare F24
    idx_shift_f24 = content.find("+F24::")
    idx_bare_f24 = content.find("F24::")
    if idx_shift_f24 == -1 or idx_bare_f24 == -1 or idx_shift_f24 > idx_bare_f24:
        fail("Windows AutoHotkey: +F24:: (Redo) must precede bare F24:: (Undo)")

    print("PASS: Windows AutoHotkey Bridge validated (editing F21-F24, launchers Alt+F13-F16, and hotkey precedence).")


def validate_glazewm_consumer(content: str) -> None:
    """Verify GlazeWM binds all semantic window management signals."""
    required_glazewm_bindings = [
        # Workspaces 1-5
        "f13", "f14", "f15", "f16", "f17",
        "shift+f13", "shift+f14", "shift+f15", "shift+f16", "shift+f17",
        # Directional focus
        "ctrl+f13", "ctrl+f14", "ctrl+f15", "ctrl+f16",
        # Directional move
        "ctrl+shift+f13", "ctrl+shift+f14", "ctrl+shift+f15", "ctrl+shift+f16",
        # Modals & context
        "f18", "f19", "f20",
        "shift+f18",  # Resize mode
        "alt+f18",    # Service mode
    ]

    for b in required_glazewm_bindings:
        # Check if the binding exists in a bindings list (e.g. "f13" or 'f13')
        pattern = rf'[\"\']{re.escape(b)}[\"\']'
        if not re.search(pattern, content, re.IGNORECASE):
            fail(f"Windows GlazeWM: Missing keybinding '{b}' in glazewm.yaml")

    # Check resize binding mode
    if 'name: "resize"' not in content and "name: resize" not in content:
        fail("Windows GlazeWM: Missing 'resize' binding mode in glazewm.yaml")

    # Check service binding mode
    if 'name: "service"' not in content and "name: service" not in content:
        fail("Windows GlazeWM: Missing 'service' binding mode in glazewm.yaml")

    print("PASS: Windows GlazeWM Consumer validated (workspaces, navigation, resize mode, and service mode).")


# -----------------------------------------------------------------------------
# Main Runner
# -----------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("RUNNING MULTI-KEYBOARD & MULTI-HOST PROTOCOL VALIDATION")
    print("=" * 70)

    # 1. Producers
    validate_keymap_producer(CORNE_KEYMAP_PATH, "Corne")
    validate_keymap_producer(SOFLE_KEYMAP_PATH, "Sofle")

    # 2. macOS Host
    if not KARABINER_PATH.exists():
        fail(f"Karabiner file not found: {KARABINER_PATH}")
    if not AEROSPACE_PATH.exists():
        fail(f"AeroSpace file not found: {AEROSPACE_PATH}")

    karabiner_data = json.loads(KARABINER_PATH.read_text(encoding="utf-8"))
    aerospace_content = AEROSPACE_PATH.read_text(encoding="utf-8")
    validate_karabiner_translator(karabiner_data)
    validate_aerospace_consumer(aerospace_content)

    # 3. Windows Host
    if not AHK_PATH.exists():
        fail(f"AutoHotkey file not found: {AHK_PATH}")
    if not GLAZEWM_PATH.exists():
        fail(f"GlazeWM file not found: {GLAZEWM_PATH}")

    ahk_content = AHK_PATH.read_text(encoding="utf-8")
    glazewm_content = GLAZEWM_PATH.read_text(encoding="utf-8")
    validate_windows_ahk(ahk_content)
    validate_glazewm_consumer(glazewm_content)

    print("=" * 70)
    print("ALL MULTI-KEYBOARD & MULTI-HOST PROTOCOL CHECKS PASSED.")
    print("=" * 70)


if __name__ == "__main__":
    main()
