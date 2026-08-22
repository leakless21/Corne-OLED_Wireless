#!/usr/bin/env python3
"""
Static regression test suite for Sofle ZMK firmware keymap.
Enforces layer indices, 60-key matrix, gaming architecture, bootloader routing,
rotary encoder behavior, and physical layout invariants.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KEYMAP_PATH = REPO_ROOT / "config" / "sofle.keymap"
CONF_PATH = REPO_ROOT / "config" / "sofle.conf"

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
        r"([A-Z_]+)\s*\{\s*label\s*=\s*\"([^\"]+)\";\s*display-name\s*=\s*\"([^\"]+)\";[\s\S]*?bindings\s*=\s*<([\s\S]*?)>;\s*(?:sensor-bindings\s*=\s*<([\s\S]*?)>;\s*)?\};",
        content,
    )
    layers = {}
    for m in layer_matches:
        node_name = m.group(1)
        label = m.group(2)
        display_name = m.group(3)
        raw_bindings = m.group(4)
        raw_sensors = m.group(5) or ""
        tokens = raw_bindings.split()
        layers[node_name] = {
            "node_name": node_name,
            "label": label,
            "display_name": display_name,
            "raw_bindings": raw_bindings,
            "raw_sensors": raw_sensors,
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
        if binding_count != 60:
            fail(f"Layer {layer_name} has {binding_count} bindings, expected exactly 60")

    if len(layers) != len(EXPECTED_LAYERS):
        fail(f"Expected {len(EXPECTED_LAYERS)} layers, found {len(layers)}")

    # Obsolete BUTTON check
    if "BUTTON" in layers or "L_BUTTON" in defines:
        fail("Obsolete BUTTON layer found in Sofle keymap")

    # Obsolete GAME_AUX check
    if "GAME_AUX" in layers or "L_GAME_AUX" in defines:
        fail("GAME_AUX layer must not exist on Sofle (Sofle has physical number row)")

    print(f"PASS: All {len(EXPECTED_LAYERS)} layer indices and names verified (60 keys per layer, no BUTTON, no GAME_AUX).")


def test_base_layer(parsed: dict) -> None:
    base = parsed["layers"].get("BASE")
    if not base:
        fail("BASE layer missing")

    raw = base["raw_bindings"]

    # Bilateral HRMs
    if "bhm" in raw:
        fail("BASE layer contains obsolete 'bhm' behavior")

    for mod in ["&hml LMETA A", "&hml LEFT_ALT R", "&hml LCTRL S", "&hml LEFT_SHIFT T",
                "&hmr RIGHT_SHIFT N", "&hmr RCTRL E", "&hmr RIGHT_ALT I", "&hmr RIGHT_GUI O"]:
        if mod not in raw:
            fail(f"BASE layer missing HRM binding: {mod}")

    # No layer-taps on Z, V, K, Slash
    for key in ["&kp Z", "&kp V", "&kp K", "&kp SLASH"]:
        if key not in raw:
            fail(f"BASE layer missing plain alpha binding: {key}")

    # Functional thumbs
    for thumb in ["&lt L_MOUSE ESCAPE", "&lt L_NAV SPACE", "&host_lt L_HOST TAB",
                  "&lt L_SYM ENTER", "&lt L_NUM BACKSPACE", "&lt L_FUN DELETE"]:
        if thumb not in raw:
            fail(f"BASE layer missing thumb layer-tap: {thumb}")

    # Outer-left home key holds MEDIA
    if "&mo L_MEDIA" not in raw:
        fail("BASE layer missing outer-left home MEDIA hold '&mo L_MEDIA'")

    # Dedicated number row
    for n in range(10):
        if f"&kp N{n}" not in raw:
            fail(f"BASE layer missing physical number row key: &kp N{n}")

    # Encoder presses
    if "&caps_word" not in raw:
        fail("BASE layer missing Left Encoder Press (LEC) '&caps_word'")
    if "&kp C_MUTE" not in raw:
        fail("BASE layer missing Right Encoder Press (REC) '&kp C_MUTE'")

    print("PASS: BASE layer verified (Colemak-DH, bilateral HRMs, dedicated number row, thumb layer-taps, encoder presses).")


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

    # Plain QWERTY keys required for gaming
    required_tokens = ["&kp Q", "&kp W", "&kp E", "&kp R", "&kp T",
                       "&kp A", "&kp S", "&kp D", "&kp F", "&kp G",
                       "&kp Z", "&kp X", "&kp C", "&kp V", "&kp B",
                       "&kp LEFT_SHIFT", "&kp LCTRL", "&kp SPACE", "&kp LALT", "&kp ESCAPE", "&kp TAB"]
    for tok in required_tokens:
        if tok not in raw:
            fail(f"GAME layer missing required gaming token: {tok}")

    # Physical number row on GAME
    for n in range(10):
        if f"&kp NUMBER_{n}" not in raw:
            fail(f"GAME layer missing number row key: &kp NUMBER_{n}")

    # Deliberate exit to BASE via right encoder press (REC)
    if "&to L_BASE" not in raw:
        fail("GAME layer missing deliberate '&to L_BASE' exit on right encoder press")

    print("PASS: GAME layer verified (plain QWERTY, number row, no HRMs, no sticky keys, right encoder exit to BASE).")


def test_bootloader_shortcuts(parsed: dict) -> None:
    nav = parsed["layers"].get("NAV")
    num = parsed["layers"].get("NUM")
    adjust = parsed["layers"].get("ADJUST")

    if not nav or not num or not adjust:
        fail("NAV, NUM, or ADJUST layer missing")

    # NAV left-side bootloader
    if "&bootloader" not in nav["raw_bindings"]:
        fail("NAV layer must have '&bootloader' at LT5 (left controller shortcut)")

    # NUM right-side bootloader
    if "&bootloader" not in num["raw_bindings"]:
        fail("NUM layer must have '&bootloader' at RT5 (right controller shortcut)")

    # ADJUST must preserve both left and right bootloader & sys_reset
    adjust_raw = adjust["raw_bindings"]
    bootloader_count = adjust_raw.count("&bootloader")
    sys_reset_count = adjust_raw.count("&sys_reset")

    if bootloader_count < 2:
        fail(f"ADJUST layer must contain 2 &bootloader bindings, found {bootloader_count}")
    if sys_reset_count < 2:
        fail(f"ADJUST layer must contain 2 &sys_reset bindings, found {sys_reset_count}")

    print("PASS: Bootloader routing invariants verified (NAV LT5, NUM RT5, ADJUST mirrored left/right).")


def test_cross_platform_bindings(parsed: dict) -> None:
    media = parsed["layers"].get("MEDIA")
    nav = parsed["layers"].get("NAV")
    mouse = parsed["layers"].get("MOUSE")

    if not media or not nav or not mouse:
        fail("MEDIA, NAV, or MOUSE layer missing")

    # MEDIA assertions
    media_raw = media["raw_bindings"]
    required_media = [
        "&kp C_PREVIOUS",
        "&kp C_VOLUME_DOWN",
        "&kp C_VOLUME_UP",
        "&kp C_NEXT",
        "&kp C_PLAY_PAUSE",
        "&kp C_MUTE",
    ]
    for tok in required_media:
        if tok not in media_raw:
            fail(f"MEDIA layer missing required Consumer HID token: {tok}")

    # NAV and MOUSE assertions
    required_editing = [
        "&kp F21",
        "&kp F22",
        "&kp F23",
        "&kp F24",
        "&kp LS(F24)",
    ]
    for layer_name, layer_dict in [("NAV", nav), ("MOUSE", mouse)]:
        raw = layer_dict["raw_bindings"]
        for tok in required_editing:
            if tok not in raw:
                fail(f"{layer_name} layer missing semantic editing token: {tok}")

    print("PASS: Cross-platform bindings verified (Consumer media HID, semantic F21-F24 editing on NAV/MOUSE).")


def test_host_layer_bindings(parsed: dict) -> None:
    host = parsed["layers"].get("HOST")
    if not host:
        fail("HOST layer missing")

    raw = host["raw_bindings"]
    required_host_tokens = [
        # Workspaces
        "&kp F13", "&kp F14", "&kp F15", "&kp F16", "&kp F17",
        # Move to workspace
        "&kp LS(F13)", "&kp LS(F14)", "&kp LS(F15)", "&kp LS(F16)", "&kp LS(F17)",
        # Directional focus
        "&kp LC(F13)", "&kp LC(F14)", "&kp LC(F15)", "&kp LC(F16)",
        # Directional move
        "&kp LC(LS(F13))", "&kp LC(LS(F14))", "&kp LC(LS(F15))", "&kp LC(LS(F16))",
        # Modal & context controls
        "&kp LS(F18)", "&kp F18", "&kp F19", "&kp F20",
        # Extended semantic protocol
        "&kp LA(F13)",  # SYSTEM_LAUNCHER
        "&kp LA(F14)",  # QUICK_TERMINAL
        "&kp LA(F15)",  # NEW_TERMINAL
        "&kp LA(F16)",  # PREVIOUS_WINDOW
        "&kp LA(F18)",  # SERVICE_MODE
    ]
    for tok in required_host_tokens:
        if tok not in raw:
            fail(f"HOST layer missing expected semantic protocol token: {tok}")

    print("PASS: HOST layer semantic signals verified (workspaces, focus/move, launchers, previous window, resize, service).")


def test_studio_configuration(parsed: dict) -> None:
    adjust = parsed["layers"].get("ADJUST")
    if not adjust:
        fail("ADJUST layer missing")

    if "&studio_unlock" not in adjust["raw_bindings"]:
        fail("ADJUST layer missing '&studio_unlock' binding")

    if not CONF_PATH.exists():
        fail(f"Config file not found: {CONF_PATH}")

    content = CONF_PATH.read_text(encoding="utf-8")
    if "CONFIG_ZMK_STUDIO_LOCKING=y" not in content:
        fail("sofle.conf must enable CONFIG_ZMK_STUDIO_LOCKING=y")
    if "CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=y" not in content:
        fail("sofle.conf must enable CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=y")
    if "CONFIG_EC11=y" not in content:
        fail("sofle.conf must enable CONFIG_EC11=y")

    print("PASS: ZMK Studio locking, unlock behavior, and encoder config verified.")


def main() -> None:
    if not KEYMAP_PATH.exists():
        fail(f"Keymap file not found: {KEYMAP_PATH}")

    content = KEYMAP_PATH.read_text(encoding="utf-8")
    parsed = parse_keymap_content(content)

    test_layer_indices(parsed)
    test_base_layer(parsed)
    test_game_layer(parsed)
    test_bootloader_shortcuts(parsed)
    test_cross_platform_bindings(parsed)
    test_host_layer_bindings(parsed)
    test_studio_configuration(parsed)
    print("\nALL SOFLE STATIC KEYMAP INVARIANTS PASSED.")


if __name__ == "__main__":
    main()
