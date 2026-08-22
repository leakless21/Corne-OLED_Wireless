# Setup & Recovery Guide

> **For daily keyboard use and the firmware change workflow**, see
> [docs/usage.md](usage.md).

> **Scope.** This guide covers the initial setup: first flash of both halves
> of the Corne, recovery via settings-reset, and Bluetooth re-pairing. It does
> **not** cover day-to-day layer usage or the complete firmware iteration workflow.
> See [docs/usage.md](usage.md) for those, and
> [docs/macos-aerospace.md](macos-aerospace.md) for AeroSpace configuration.

---

## 1. Project Overview

This repository is a **ZMK firmware** project for the Corne split keyboard.
It is **not** QMK. The firmware is configured in ZMK's Devicetree/behavior
syntax and built automatically via GitHub Actions.

| File | Purpose |
|------|---------|
| `config/corne.keymap` | The keymap: all 11 layers, home-row mods, layer-taps, host_lt, and pointing. |
| `config/corne.conf` | Kconfig toggles: OLED display, explicit idle/deep-sleep policy, ZMK Studio, pointing. |
| `build.yaml` | GitHub Actions build matrix: board + shield combinations and artifact names. |
| `config/west.yml` | West manifest: pins ZMK, nice\_oled, and helper modules at fixed revision SHAs. |
| `.github/workflows/build.yml` | The Actions workflow — delegates to the upstream ZMK build workflow. |
| `dotfiles/aerospace.toml` | Canonical macOS AeroSpace configuration for the HOST/F13–F20 bridge. |
| `.github/workflows/draw-keymap.yml` | Regenerates the committed keymap-drawer YAML/SVG reference when the keymap changes. |

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
| `corne-left` | `nice_nano@2.0.0//zmk` | `corne_left` + `nice_oled` | ZMK Studio RPC snippet enabled |
| `corne-right` | `nice_nano@2.0.0//zmk` | `corne_right` + `nice_oled` | — |
| `settings-reset` | `nice_nano@2.0.0//zmk` | `settings_reset` | — |

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

**After editing:** push to the repo or open a PR. Firmware input changes
(`config/**`, `build.yaml`, board/shield sources, or the build workflow) trigger
the build; documentation-only changes do not. Manual dispatch remains available.

---

## 4. GitHub Actions Build & Artifacts

### How the build works

The workflow (`.github/workflows/build.yml`) runs for firmware input changes on
**push** or **pull request**, and also supports **manual dispatch**. Its
concurrency group cancels superseded builds for the same ref. The workflow calls
the upstream ZMK build workflow, which reads `build.yaml` for the matrix and
`config/west.yml` for dependency pins.

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

2. **Put the nice\_nano\_v2 into bootloader mode.** Choose the appropriate method:
   - **Convenient firmware shortcuts (software):**
     - **Left controller:** Hold `NAV` thumb (`LH1`) and press the left outer/top key (`LT5`).
     - **Right controller:** Hold `NUM` thumb (`RH1`) and press the right outer/top key (`RT5`).
   - **Administrative layer (software fallback):** Hold `ADJUST` (`NAV` + `NUM`) and press the
     left-half `&bootloader` binding (`LT5`) or right-half `&bootloader` binding (`RT5`).
   - **Guaranteed standalone recovery (hardware):** Quickly double-press the physical reset button
     on the individual nice\_nano\_v2 board (or short RST to GND twice for bare controllers).
     *Note:* This hardware procedure is the **only** recovery route guaranteed to work when a half
     cannot participate in the split connection, has broken keymap firmware, or is completely isolated.
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

## 6. Recovery & settings reset

ZMK Studio stores runtime keymap overrides in persistent settings. If Studio
diverges from the Git-tracked keymap, use the least-destructive recovery first:

1. Open ZMK Studio while connected to the left half.
2. Choose **Restore Stock Settings**.
3. Flash the normal `corne-left.uf2` / `corne-right.uf2` firmware if needed.
4. Re-test the keymap before clearing Bluetooth or split state.

Restore Stock Settings clears Studio-specific settings without clearing
Bluetooth bonds. Use the **`settings-reset`** artifact only when Studio restore
fails, persisted device state is corrupted, or a full reset is intentional.

### What settings-reset does

The `settings-reset` image is a **temporary firmware** — not a standalone
utility that runs alongside normal firmware. When flashed, it replaces the
current firmware on the controller and erases persisted Zephyr/ZMK settings,
including Bluetooth bond keys, split pairing information, output/power state,
and Studio-edited overrides. It runs with BLE and the display disabled, wipes
the settings partition, and halts.

Because it replaces normal firmware, you **must reflash** the appropriate
`corne-left.uf2` or `corne-right.uf2` after running it on each half. The
keyboard will not function normally until normal firmware is restored.

### How to use it

1. Download `settings-reset.uf2` from the GitHub Actions artifacts.
2. Put the half into bootloader mode (use the convenient `NAV`/`NUM` same-side shortcuts,
   `ADJUST` `&bootloader`, or double-tap physical reset if keymap is unresponsive).
3. Copy `settings-reset.uf2` onto the bootloader drive. The board reboots.
4. Repeat for the other half.
5. Re-flash the matching normal firmware on both halves.
6. Re-pair Bluetooth (see §7).

> `OUT_USB` selects USB output explicitly. If the cable is connected to a
> charger-only port, the keyboard may appear to stop typing because no usable
> host is present. `EP_OFF` is also persistent; a peripheral or display that
> stays blank after reboot may simply have external power disabled.
---

## 7. Bluetooth Re-pairing

After flashing for the first time, or after a settings-reset, you need to pair
the keyboard with your computer.

### Pairing procedure

1. **Select a profile.** On ADJUST (hold NAV + NUM), press `BT_SEL 0` for a
   first host, or select another unused profile (`BT_SEL 1` through `BT_SEL 4`).
   Selecting an unpaired profile starts advertising for a new pairing.
2. **On your computer**, open Bluetooth settings and look for the keyboard
   (it will appear as something like "ZMK" or "Corne"). Select it to pair.
3. **Verify** by typing — the keyboard should now work over Bluetooth.

### Switching between paired devices

ADJUST exposes five default Bluetooth profiles: `BT_SEL 0` through `BT_SEL 4`.
`BT_NXT` and `BT_PRV` cycle through them. Hold NAV + NUM and press the
corresponding binding.

### Clearing a bond

`BT_CLR` clears **only the currently selected profile**. After clearing a
profile, forget/remove the keyboard from that host before pairing again; the
host may retain the old security key and repeatedly fail authentication.
`BT_CLR_ALL` clears every profile and is intentionally not bound in this
keymap. Use the `settings-reset` recovery artifact when a full clean slate is
needed.

---

## 8. ZMK Studio Caveats

ZMK Studio is **enabled with locking** in this configuration (`CONFIG_ZMK_STUDIO=y`,
`CONFIG_ZMK_STUDIO_LOCKING=y`, `CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=y`) to ensure
the Git-tracked `config/corne.keymap` remains the canonical source of truth.

### What to know

- **Studio Unlock:** To unlock Studio for live editing over USB-UART, hold NAV + NUM to activate
  the `ADJUST` layer, then press the `Unlock` key on `RM0` (`&studio_unlock`).
- Studio edits persist to on-device settings, not to the Git-tracked `config/corne.keymap`.
- **Restore Stock Settings:** If you flash a newly updated keymap and your changes do not appear,
  an old Studio runtime configuration is overriding firmware. In ZMK Studio, click **Restore Stock Settings**
  to clear the on-device override and return to Git-authored bindings without clearing Bluetooth bonds.
- `settings-reset` is the destructive fallback: it clears Studio overrides, Bluetooth bonds,
  split state, output selection, and external-power state.

### Practical recommendation

Use Studio for quick experiments. For durable changes, edit `config/corne.keymap` directly and commit it.
When returning from Studio to Git firmware, use **Restore Stock Settings** before considering `settings-reset`.
## 9. Host Platform Setup (macOS & Windows)

The Corne keyboard emits host-agnostic semantic signals for editing (`F21`–`F24`) and window management (`F13`–`F20`). Basic typing, media controls, and mouse features work without any host tools, but desktop editing and tiling window management use lightweight host bridges.

### macOS setup

1. **Host Bridge (Karabiner-Elements):**
   - Install [Karabiner-Elements](https://karabiner-elements.pqrs.org/).
   - Copy the rule file from `dotfiles/karabiner-corne.json` into `~/.config/karabiner/assets/complex_modifications/`.
   - Enable **"Corne F13-F20 Semantic Window Management Bridge"** and **"Corne F21-F24 Semantic Editing"**.
   - Translates Corne high-function keys into macOS `Alt` and `Cmd` chords with `device_if` scoping.
2. **Window Management & Terminal (AeroSpace & Ghostty):**
   - Install [AeroSpace](https://nikitabobko.github.io/AeroSpace/) and [Ghostty](https://ghostty.org/).
   - Install `dotfiles/aerospace.toml` to `~/.config/aerospace/aerospace.toml`.
   - Install `dotfiles/ghostty.config` to `~/.config/ghostty/config`.
   - See [docs/macos-aerospace.md](macos-aerospace.md) for full configuration, Quick Terminal, and application routing.
### Windows setup

1. **Editing bridge (AutoHotkey v2):**
   - Install [AutoHotkey v2](https://www.autohotkey.com/).
   - Run `dotfiles/corne-windows.ahk` (or place a shortcut to it in your Windows Startup folder `shell:startup`).
   - Translates `F21`–`F24` and `Shift+F24` to `Ctrl+C`, `Ctrl+V`, `Ctrl+X`, `Ctrl+Z`, `Ctrl+Y`.
2. **Window management:**
   - Can be mapped to a tiling window manager such as GlazeWM when window management integration is configured on the host.

---

## 10. Links to Other Guides

- **Layout contract and physical invariants:**
  [docs/layout-principles.md](layout-principles.md)
- **Keymap & layers reference** (detailed layer-by-layer documentation):
  [docs/corne-keymaps.md](corne-keymaps.md)
- **macOS AeroSpace setup** (the semantic HOST bridge, workspace bindings,
  troubleshooting):
  [docs/macos-aerospace.md](macos-aerospace.md)

---

## 11. What This Guide Does Not Cover

- **Local builds.** Building ZMK locally requires a West workspace and toolchain
  setup that is not documented here. Use the GitHub Actions workflow instead.
- **Board/shield upstream.** The `nice_nano_v2` board and `corne_left`/`corne_right`
  shields are maintained by the ZMK project. This repo only provides the keymap
  and build configuration that references them.
- **AeroSpace configuration.** See [docs/macos-aerospace.md](macos-aerospace.md).
