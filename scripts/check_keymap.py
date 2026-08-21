#!/usr/bin/env python3
"""
Static regression test suite for Corne ZMK firmware keymap.
Enforces layer indices, gaming access, bootloader routing, and physical layout invariants.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KEYMAP_PATH = REPO_ROOT / "config" / "corne.keymap"
CONF_PATH = REPO_ROOT / "config" / "corne.conf"

EXPECTED_LAYERS = [
    ("L_BASE", 0, "BASE"),
    ("L_NAV", 1, "NAV"),
    ("L_MOUSE", 2, "MOUSE"),
    ("L_MEDIA", 3, "MEDIA"),
    ("L_NUM", 4, "NUM"),
    ("L_SYM", 5, "SYM"),
    ("L_FUN", 6, "FUN"),
    ("L_HOST", 7, "HOST"),
    ("L_GAME", 8, "GAME"),
    ("L_ADJUST", 9, "ADJUST"),
    ("L_GAME_AUX", 10, "GAME_AUX"),
]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_keymap_content(content: str) -> dict:
    # 1. Parse defines
    defines = {}
    for match in re.finditer(r"#define\s+(L_\w+)\s+(\d+)", content):
        defines[match.group(1)] = int(match.group(2))

    # 2. Extract keymap layers
    layer_matches = re.finditer(
        r"([A-Z_]+)\s*\{\s*label\s*=\s*\"([^\"]+)\";\s*display-name\s*=\s*\"([^\"]+)\";[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;\s*\};",
        content,
    )
    layers = {}
    for m in layer_matches:
        node_name = m.group(1)
        label = m.group(2)
        display_name = m.group(3)
        raw_bindings = m.group(4)
        tokens = raw_bindings.split()
        layers[node_name] = {
            "node_name": node_name,
            "label": label,
            "display_name": display_name,
            "raw_bindings": raw_bindings,
            "tokens": tokens,
        }

    return {"defines": defines, "layers": layers}


def test_layer_indices(parsed: dict) -> None:
    defines = parsed["defines"]
    layers = parsed["layers"]

    for define_name, expected_idx, layer_name in EXPECTED_LAYERS:
        if define_name not in defines:
            fail(f"Missing define: {define_name}")
        if defines[define_name] != expected_idx:
            fail(f"{define_name} has value {defines[define_name]}, expected {expected_idx}")
        if layer_name not in layers:
            fail(f"Missing layer node: {layer_name}")

        layer_data = layers[layer_name]
        if layer_data["label"] != layer_name:
            fail(f"Layer {layer_name} has label '{layer_data['label']}', expected '{layer_name}'")
        if layer_data["display_name"] != layer_name:
            fail(f"Layer {layer_name} has display-name '{layer_data['display_name']}', expected '{layer_name}'")
        raw_b = layer_data["raw_bindings"]
        binding_count = len(re.findall(r"&[a-zA-Z_]+", raw_b))
        if binding_count != 42:
            fail(f"Layer {layer_name} has {binding_count} bindings, expected exactly 42")
    if len(layers) != len(EXPECTED_LAYERS):
        fail(f"Expected {len(EXPECTED_LAYERS)} layers, found {len(layers)}")

    print(f"PASS: All {len(EXPECTED_LAYERS)} layer indices and names verified.")


def test_game_layer(parsed: dict) -> None:
    game = parsed["layers"].get("GAME")
    if not game:
        fail("GAME layer missing")

    raw = game["raw_bindings"]

    # Prohibited on GAME
    if "hml" in raw or "hmr" in raw:
        fail("GAME layer contains home-row mods (hml/hmr)")
    if "&sk" in raw:
        fail("GAME layer contains sticky keys")

    # Plain keys required for gaming
    required_tokens = ["&kp Q", "&kp W", "&kp E", "&kp R", "&kp T",
                       "&kp A", "&kp S", "&kp D", "&kp F", "&kp G",
                       "&kp LEFT_SHIFT", "&kp LCTRL", "&kp SPACE", "&kp LALT"]
    for tok in required_tokens:
        if tok not in raw:
            fail(f"GAME layer missing required gaming token: {tok}")

    # Esc hold-tap
    if "&game_aux_lt L_GAME_AUX ESCAPE" not in raw:
        fail("GAME layer missing dedicated Esc/AUX hold-tap on top-left: '&game_aux_lt L_GAME_AUX ESCAPE'")

    # RH1 momentary AUX
    if "&mo L_GAME_AUX" not in raw:
        fail("GAME layer missing momentary GAME_AUX on right-middle thumb: '&mo L_GAME_AUX'")

    # No naked exit to BASE on GAME
    if "&to L_BASE" in raw:
        fail("GAME layer must not contain direct '&to L_BASE' exit")

    print("PASS: GAME layer invariants verified (no HRMs, dedicated Esc/AUX hold-tap, momentary RH1, no direct exit).")


def test_game_aux_layer(parsed: dict) -> None:
    aux = parsed["layers"].get("GAME_AUX")
    if not aux:
        fail("GAME_AUX layer missing")

    raw = aux["raw_bindings"]

    # Numbers 1-0
    for num in range(10):
        tok = f"&kp NUMBER_{num}"
        if tok not in raw:
            fail(f"GAME_AUX missing number key: {tok}")

    # F1-F10
    for f in range(1, 11):
        tok = f"&kp F{f}"
        if tok not in raw:
            fail(f"GAME_AUX missing function key: {tok}")

    # Missing gaming punctuation
    for sym in ["&kp GRAVE", "&kp MINUS", "&kp EQUAL", "&kp LEFT_BRACKET", "&kp RIGHT_BRACKET"]:
        if sym not in raw:
            fail(f"GAME_AUX missing punctuation key: {sym}")

    # Deliberate exit to BASE behind GAME_AUX
    if "&to L_BASE" not in raw:
        fail("GAME_AUX layer missing deliberate '&to L_BASE' exit")

    print("PASS: GAME_AUX layer invariants verified (1-0, F1-F10, punctuation, deliberate exit to BASE).")


def test_bootloader_shortcuts(parsed: dict) -> None:
    nav = parsed["layers"].get("NAV")
    num = parsed["layers"].get("NUM")
    adjust = parsed["layers"].get("ADJUST")

    if not nav or not num or not adjust:
        fail("NAV, NUM, or ADJUST layer missing")

    # NAV left-side bootloader (LT5 is the first binding)
    nav_raw = nav["raw_bindings"].strip()
    if not nav_raw.startswith("&bootloader"):
        fail("NAV layer must have '&bootloader' at LT5 (first binding)")

    # NUM right-side bootloader (RT5 is in the first row, right half)
    if "&bootloader" not in num["raw_bindings"]:
        fail("NUM layer must have '&bootloader' on the right half (RT5)")

    # ADJUST must preserve both left and right bootloader & sys_reset
    adjust_raw = adjust["raw_bindings"]
    bootloader_count = adjust_raw.count("&bootloader")
    sys_reset_count = adjust_raw.count("&sys_reset")

    if bootloader_count < 2:
        fail(f"ADJUST layer must contain 2 &bootloader bindings (left and right), found {bootloader_count}")
    if sys_reset_count < 2:
        fail(f"ADJUST layer must contain 2 &sys_reset bindings (left and right), found {sys_reset_count}")

    print("PASS: Bootloader routing invariants verified (NAV LT5, NUM RT5, ADJUST mirrored left/right).")


def test_conf_constraints() -> None:
    if not CONF_PATH.exists():
        fail(f"Config file not found: {CONF_PATH}")

    content = CONF_PATH.read_text(encoding="utf-8")

    # Debounce checks
    if "CONFIG_ZMK_KSCAN_DEBOUNCE" in content:
        fail("corne.conf contains CONFIG_ZMK_KSCAN_DEBOUNCE setting (prohibited)")

    # NKRO checks
    if "CONFIG_ZMK_HID_REPORT_TYPE_NKRO" in content:
        fail("corne.conf contains CONFIG_ZMK_HID_REPORT_TYPE_NKRO (prohibited)")

    print("PASS: corne.conf constraints verified (no debounce or NKRO changes).")


def main() -> None:
    if not KEYMAP_PATH.exists():
        fail(f"Keymap file not found: {KEYMAP_PATH}")

    content = KEYMAP_PATH.read_text(encoding="utf-8")
    parsed = parse_keymap_content(content)

    test_layer_indices(parsed)
    test_game_layer(parsed)
    test_game_aux_layer(parsed)
    test_bootloader_shortcuts(parsed)
    test_conf_constraints()

    print("\nALL STATIC KEYMAP INVARIANTS PASSED.")


if __name__ == "__main__":
    main()
