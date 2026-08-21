# Setup & Usage Guide

> **Scope.** This guide walks you through editing the ZMK keymap, building
> firmware via GitHub Actions, flashing both halves of the Corne, recovering
> from bad settings, and re-pairing Bluetooth. It does **not** cover local
> builds or AeroSpace configuration (see
> [docs/macos-aerospace.md](macos-aerospace.md) for the latter).

---

## 1. Project Overview

This repository is a **ZMK firmware** project for the Corne split keyboard.
It is **not** QMK. The firmware is configured in ZMK's Devicetree/behavior
syntax and built automatically via GitHub Actions.

Key files:

| File | Purpose |
|------|---------|
| `config/corne.keymap` | The keymap: all 10 layers, home-row mods, layer-taps, pointing, and combos. |
| `config/corne.conf` | Kconfig toggles: OLED display, sleep, ZMK Studio, pointing. |
| `build.yaml` | GitHub Actions build matrix: board + shield combinations and artifact names. |
| `config/west.yml` | West manifest: pins ZMK, nice\_oled, and helper modules at fixed revision SHAs. |
| `.github/workflows/build.yml` | The Actions workflow — delegates to the upstream ZMK build workflow. |

For the full keymap/layers reference, see
[docs/corne-keymaps.md](corne-keymaps.md).

---

## 2. Hardware Assumptions

- **Keyboard:** Corne (CRKBD) split layout, 42 keys (3×6 + 3 thumb per side).
- **Controllers:** Two **nice\_nano\_v2** (one per half).
- **Display:** **nice\_oled** on each half.
- **Connection:** Bluetooth wireless after initial USB flash.

The `build.yaml` defines these shields:

| Artifact | Board | Shield(s) | Extra |
|----------|-------|-----------|-------|
| `corne-left` | `nice_nano_v2` | `corne_left` + `nice_oled` | ZMK Studio RPC snippet enabled |
| `corne-right` | `nice_nano_v2` | `corne_right` + `nice_oled` | — |
| `settings-reset` | `nice_nano_v2` | `settings_reset` | — |

---

## 3. Editing the Keymap

The canonical keymap lives in `config/corne.keymap`. All edits go there (or via
the visual [Keymap Editor](https://nickcoutsos.github.io/keymap-editor/)).

**Before editing:**

1. Open `config/corne.keymap` and familiarize yourself with the layer structure
   (see [docs/corne-keymaps.md](corne-keymaps.md) §2).
2. Keep a copy of the last-known-good keymap. Use Git: commit your working
   state before making changes, or manually back up the file.

**What to edit:**

- To **remap a key**, change the `&kp`/`&lt`/`&sk`/etc. binding at the
  corresponding position in the `bindings = <...>;` block for the relevant
  layer.
- To **add or remove layers**, update the `#define L_*` constants at the top of
  the keymap and the `keymap { ... }` block. Layer indices are 0-based and
  **persisted on the keyboard** — renaming or renumbering layers changes the
  ZMK state. After renumbering, flash both halves and consider a
  `settings-reset` (see §6).
- To **change behavior tuning** (tapping terms, sticky-key timeout, pointer
  sensitivity), edit the `&lt`, `&sk`, or `&mmv`/`&msc` property blocks near
  the top of the file.

**After editing:** push to the repo (or open a PR) to trigger the build
workflow.

---

## 4. GitHub Actions Build & Artifacts

### How the build works

The workflow (`.github/workflows/build.yml`) triggers on **push**, **pull
request**, and **manual dispatch**. It calls the upstream ZMK build workflow,
which reads `build.yaml` for the matrix and `config/west.yml` for dependency
pins.

### What gets built

Three `.uf2` firmware images are built individually:

| Artifact | Contents |
|----------|----------|
| `corne-left` | Left-half firmware. Includes ZMK Studio RPC over USB-UART (via `studio-rpc-usb-uart` snippet). |
| `corne-right` | Right-half firmware. Standard build. |
| `settings-reset` | Temporary utility firmware that erases persisted Zephyr/ZMK settings on boot (see §6 for details). |

The upstream reusable workflow then **merges** these into a single downloadable
archive named **`firmware`** (a `.zip` file containing all three `.uf2` files).

### Downloading artifacts

1. Go to the **Actions** tab of the repository on GitHub.
2. Click the most recent successful workflow run (green checkmark).
3. Scroll to **Artifacts** at the bottom of the run summary.
4. Download the **`firmware`** archive (`.zip`). It contains all three `.uf2`
   files: `corne-left.uf2`, `corne-right.uf2`, and `settings-reset.uf2`.

> **Important:** The firmware file extension is **`.uf2`**, not `.urf2`.

---

## 5. First Flash of Both Halves

You will flash each half **separately** over USB. The keyboard does not need to
be assembled or connected to the other half during flashing.

### Step-by-step

1. **Connect the left half** to your computer with a USB-C cable.

2. **Put the nice\_nano\_v2 into bootloader mode.** There are a few ways:
   - **Quickly double-press the reset button** on the nice\_nano\_v2 board. The
     board enters its UF2 bootloader.
   - **For a bare controller** (no reset button wired to a key): briefly short
     the RST pin to GND twice in quick succession.
   - **Use the firmware:** if the board already has a working keymap, hold the
     ADJUST layer (NAV + NUM held simultaneously) and press the key mapped to
     `&bootloader` (top row, second position). Then release.

3. **A removable USB drive appears** on your computer. The drive is typically
   named `NICENANO`, though the name can vary depending on the bootloader
   version.

4. **Copy the left `.uf2` file** (`corne-left.uf2`) onto the bootloader drive.
   The board will automatically reboot and run the new firmware.

5. **Disconnect the left half.**

6. **Connect the right half** and repeat steps 2–5 with `corne-right.uf2`.

7. **Disconnect the right half.** Both halves are now flashed.

### Verifying

- The OLED screens should display the ZMK status screen (layer info, battery).
- Pair with your computer via Bluetooth (see §7).

---

## 6. Recovery & Settings Reset

If the keymap behaves unexpectedly — for example after a layer renumbering,
a bad ZMK Studio edit, or corrupted Bluetooth bonds — use the
**`settings-reset`** artifact.

### What settings-reset does

The `settings-reset` image is a **temporary firmware** — not a standalone
utility that runs alongside your normal firmware. When flashed, it
**replaces** the current firmware on the controller. On the next boot it:

- **Erases all persisted Zephyr/ZMK settings**: Bluetooth bond keys, split
  pairing information, output/power state, and any Studio-edited overrides.
- Runs with **BLE and the display disabled**, so the board does not attempt to
  advertise or render a status screen — it simply wipes the settings partition
  and halts.

Because it replaces the normal firmware, you **must reflash** with the
appropriate `corne-left.uf2` or `corne-right.uf2` after running
settings-reset on each half. The keyboard will not function normally until the
normal firmware is restored.

### How to use it

1. Download `settings-reset.uf2` from the GitHub Actions artifacts.
2. Put the half into bootloader mode (double-tap reset, or use
   `&bootloader` on the ADJUST layer if the current firmware is still
   functional).
3. Copy `settings-reset.uf2` onto the bootloader drive. The board reboots.
4. **Repeat for the other half.**
5. After both halves have been reset, **re-flash** with the correct firmware
   (`corne-left.uf2` / `corne-right.uf2`). This is required — the keyboard
   will not function normally until the normal firmware is restored.
6. **Re-pair Bluetooth** (see §7).

> **When to use settings-reset:**
> - After changing the number or order of layers in the keymap.
> - After ZMK Studio edits that caused unexpected behavior.
> - When Bluetooth connections are stuck or won't pair.
> - As a clean-slate step before re-pairing all devices.

---

## 7. Bluetooth Re-pairing

After flashing for the first time, or after a settings-reset, you need to pair
the keyboard with your computer.

### Pairing procedure

1. **Put the keyboard into pairing mode.** On the ADJUST layer (hold NAV +
   NUM), press the key mapped to `&bt BT_CLR` to clear existing bonds, then
   press `&bt BT_SEL 0` to start advertising on profile 0.

2. **On your computer**, open Bluetooth settings and look for the keyboard
   (it will appear as something like "ZMK" or "Corne"). Select it to pair.

3. **Verify** by typing — the keyboard should now work over Bluetooth.

### Switching between paired devices

The ADJUST layer has bindings for `&bt BT_SEL 0` through `&bt BT_SEL 3`,
allowing you to switch between four paired devices. Hold NAV + NUM and press
the corresponding key.

### Clearing all bonds

Hold NAV + NUM and press `&bt BT_CLR`. This removes all stored pairings,
forcing a fresh pairing on the next connection attempt.

---

## 8. ZMK Studio Caveats

ZMK Studio is **enabled** in this configuration (`CONFIG_ZMK_STUDIO=y` in
`config/corne.conf`). Studio allows live keymap editing without reflashing.

### What to know

- **Studio edits persist to on-device settings**, not to the Git-tracked
  `config/corne.keymap`. The file in Git is the **canonical** source of truth.
  Studio changes can diverge from it.
- **Studio locking is disabled** (`CONFIG_ZMK_STUDIO_LOCKING=n`), so the
  keymap can be edited live without a lockout.
- **Studio connects over USB-UART** on the left half (via the
  `studio-rpc-usb-uart` snippet). The right half relies on the global config.
- If Studio edits cause problems, **flash `settings-reset`** to clear all
  persisted Studio overrides, then re-flash the standard firmware.

### Practical recommendation

Use Studio for quick experiments. For anything you want to keep, edit
`config/corne.keymap` directly and commit the change. That way the keymap is
version-controlled and reproducible.

---

## 9. Links to Other Guides

- **Keymap & layers reference** (detailed layer-by-layer documentation):
  [docs/corne-keymaps.md](corne-keymaps.md)
- **macOS AeroSpace setup** (the HOST/F13–F20 bridge, workspace bindings,
  troubleshooting): [docs/macos-aerospace.md](macos-aerospace.md)

---

## 10. What This Guide Does Not Cover

- **Local builds.** Building ZMK locally requires a West workspace and toolchain
  setup that is not documented here. Use the GitHub Actions workflow instead.
- **Board/shield upstream.** The `nice_nano_v2` board and `corne_left`/`corne_right`
  shields are maintained by the ZMK project. This repo only provides the keymap
  and build configuration that references them.
- **AeroSpace configuration.** See [docs/macos-aerospace.md](macos-aerospace.md).
