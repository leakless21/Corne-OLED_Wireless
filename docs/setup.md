# Setup & Recovery Guide

This guide covers initial hardware setup, firmware flashing, clean settings resets, and Bluetooth pairing for **Corne** and **Sofle** keyboards.

---

## 1. Project Overview

This repository is a unified **ZMK firmware** configuration with shared semantic host adapters for macOS and Windows.

| File / Directory | Purpose |
|------------------|---------|
| `config/corne.keymap` / `config/corne.conf` | Corne 42-key keymap and Kconfig settings |
| `config/sofle.keymap` / `config/sofle.conf` | Sofle 60-key keymap with encoders and Kconfig settings |
| `config/west.yml` | Single canonical West manifest pinning ZMK and helpers |
| `build.yaml` | GitHub Actions matrix for Corne, Sofle, and settings-reset |
| `hosts/macos/` | macOS adapters: Karabiner, AeroSpace, Ghostty |
| `hosts/windows/` | Windows adapters: AutoHotkey v2, GlazeWM, Windows Terminal |
| `keymap-drawer/` | Generated SVG and YAML layout diagrams |

---

## 2. Hardware Targets & Artifacts

| Artifact | Hardware Target | Shield(s) | Features |
|----------|-----------------|-----------|----------|
| `corne-left.uf2` | nice!nano v2 | `corne_left nice_oled` | Central half, ZMK Studio RPC enabled |
| `corne-right.uf2` | nice!nano v2 | `corne_right nice_oled` | Peripheral half |
| `sofle-left.uf2` | nice!nano v2 | `sofle_left nice_oled` | Central half, ZMK Studio RPC enabled |
| `sofle-right.uf2` | nice!nano v2 | `sofle_right nice_oled` | Peripheral half |
| `settings-reset.uf2` | nice!nano v2 | `settings_reset` | Erases persistent storage/bonds |

---

## 3. First Flash & Migration Procedure

### Clean Migration / Reset (Mandatory for Sofle Migration)
1. Turn off power switches on both halves (or disconnect batteries).
2. Connect the **left half** via USB-C.
3. Put the controller into bootloader mode (double-press physical reset button on nice!nano v2).
4. Drag and drop `settings-reset.uf2` onto the `NICENANO` USB drive. The board wipes its settings partition and halts.
5. Double-press reset again to enter bootloader mode.
6. Drag and drop `corne-left.uf2` or `sofle-left.uf2`. The controller reboots with new firmware.
7. Disconnect left half.
8. Connect the **right half** via USB-C and repeat steps 3–6 with `settings-reset.uf2` followed by `corne-right.uf2` or `sofle-right.uf2`.
9. Power on both halves.
10. Remove any stale Bluetooth pairing from your host computer and re-pair.

---

## 4. Bluetooth Pairing & Switching

- **Select Profile:** On `ADJUST` (`NAV + NUM`), press `BT_SEL 0` through `BT_SEL 4` in the home row core.
- **Pair:** Open host Bluetooth settings and pair with "ZMK" or keyboard name.
- **Clear Bond:** On `ADJUST`, press `BT_CLR` to clear the active profile bond, then remove device from host before re-pairing.
