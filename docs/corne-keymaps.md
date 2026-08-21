# Corne Keymap & Layers Guide

> **Repository context.** This repository is a **ZMK firmware** project for a Corne
> split keyboard (it is **not** QMK). This guide documents the keymap, layers, and
> related firmware settings found in `config/corne.keymap`, `config/corne.conf`,
> `build.yaml`, and `config/west.yml`.
>
> **Documentation only.** This guide does **not** modify any firmware, keymap,
> build, west, or AeroSpace files. It only describes what is already present.

---

## 1. Firmware identity: ZMK, not QMK

- The keymap is written in ZMK's Devicetree/behavior syntax (`&kp`, `&lt`, `&sk`,
  `&mo`/`&to`, `&mmv`, `&msc`, `&mkp`, etc.), not QMK's C `LAYOUT` arrays.
- `config/west.yml` pulls in the **zmk** project from `github.com/zmkfirmware`
  (revision `main`), plus two helpers:
  - `zmk-nice-oled` (remote `mctechnology17`) — OLED display support.
  - `zmk-helpers` (remote `urob`) — key-label and unicode helpers used for
    visualization/editor labels.
- The board target is **`nice_nano_v2`** (see `build.yaml`), a common wireless
  Corne controller.

---

## 2. The 9 layers

The keymap defines exactly **nine** layers. ZMK layers are **0-indexed**, so the
`&lt N` / `&to N` numbers in the keymap refer to these indices:

| Index | Layer name (`label` / `display-name`) | Purpose |
|-------|----------------------------------------|---------|
| 0 | `BASE` | Primary typing layer. Home-row modifiers + thumb/letter layer-taps to reach every other layer. |
| 1 | `NAVIGATION` (`NAV`) | Arrow keys, clipboard (copy/cut/paste/undo/redo), `Caps`, `bootloader`, and the `&to 8` switch into the GAME layer. |
| 2 | `MOUSE` | Pointer control: scroll (`&msc`), mouse buttons (`&mkp`), and mouse movement (`&mmv`). |
| 3 | `BUTTON` | Mouse-button cluster (`&mkp MB1`–`MB5`, `MCLK`) plus clipboard keys. |
| 4 | `MEDIA` | Media / system: volume, play/pause/stop/mute, Bluetooth select/clear (`&bt`), output toggle (`&out`), external-power toggle (`&ext_power`). |
| 5 | `NUM` | Numpad: digits `0`–`9`, brackets, `MINUS`, `PERIOD`, `GRAVE`, `BACKSLASH`, `bootloader`. |
| 6 | `SYM` | Symbols: brackets, braces, parentheses, and math/punctuation glyphs (`&`, `*`, `$`, `%`, `@`, `#`, `|`, etc.). |
| 7 | `FUN` (`FUNC`) | Function row: `F1`–`F12`, `PRINTSCREEN`, `SCROLLLOCK`, `PAUSE_BREAK`. |
| 8 | `QWERTY` (`GAME`) | Gaming layer: number row + `Q/W/E/R`/`A/S/D/F`/`G`/`SPACE`. Entered via `&to 8` from NAVIGATION. |

> **Verify, don't assume.** The exact key *positions* for every layer live in
> `config/corne.keymap`. Always open that file to confirm a specific binding —
> this table only summarizes each layer's intent.

---

## 3. Base layer layout & layer-switch behavior

### 3.1 Base layout (as defined in `config/corne.keymap`)

The BASE layer is a 6×3-per-side grid plus a 3-per-side thumb cluster. The
actual bindings (not the template comment in the file) are:

```
Top row:     ESC  Q  W  F  P  B | J  L  U  Y  '  BSPC
Home row:    TAB  A  R  S  T  G | M  N  E  I  O  ;
Bottom row:  LSH  Z  X  C  D  V | K  H  ,  .  /  RSH
Thumbs:           LCTL SPC TAB   | ENT BSPC RCTL
```

- **Home row letters** (`A R S T` / `N E I O`) are **hold-tap modifiers** — see
  §4. The bare letters are the *tap* action.
- **`LSH`** (bottom-left) is a **sticky** left shift — see §5.
- **`Z`, `V`, `K`, `/`** are **layer-taps** — tap for the letter, hold to engage a
  layer — see §6.
- **Thumbs** `SPC`, `TAB`, `ENT`, `BSPC` are **layer-taps**; `LCTL` and `RCTL`
  are plain `&kp LCTRL` / `&kp RCTRL`.

### 3.2 How layers are reached from BASE

Layer-taps (`&lt`) are **momentary**: the target layer is active only while the
key is held. The BASE-layer layer-taps map to these layers:

| Key (tap → hold) | `&lt` target | Layer engaged (while held) |
|------------------|--------------|----------------------------|
| `SPACE`          | `&lt 1`      | NAVIGATION (1) |
| `TAB` (thumb)    | `&lt 2`      | MOUSE (2) |
| `/`              | `&lt 3`      | BUTTON (3) |
| `Z`, `V`         | `&lt 4`      | MEDIA (4) |
| `BSPC` (thumb)   | `&lt 5`      | NUM (5) |
| `ENT` (thumb)    | `&lt 6`      | SYM (6) |
| `K`              | `&lt 7`      | FUN (7) |

The **GAME** layer (8) is **not** a layer-tap. It is reached from the
NAVIGATION layer via `&to 8` — a *layer switch* (`&to`) that activates layer 8
and deactivates the others. Because `&to` is a switch rather than a momentary
hold, the GAME layer stays active. The current `QWERTY`/GAME definition contains
no `&to 0` return binding, so this is presently a one-way switch in the checked-in
keymap; add and test a separate return binding before relying on GAME as a daily
layer. The GAME layer itself is mostly `&trans`, so verify any future change in
`config/corne.keymap`.

> All other layers use `&trans` (transparent) for keys they don't define, so
> unspecified keys fall through to the layer below.

---

## 4. Home-row modifiers (`&bhm` balanced homerow mods)

A custom hold-tap behavior `balanced_homerow_mods` (`bhm`) is defined in the
keymap and applied to the home-row letters:

```devicetree
bhm: balanced_homerow_mods {
    compatible = "zmk,behavior-hold-tap";
    tapping-term-ms = <220>;
    quick-tap-ms = <180>;
    flavor = "tap-preferred";
    bindings = <&kp>, <&kp>;
};
```

| Key | Tap | Hold (modifier) |
|-----|-----|-----------------|
| `A` | `A` | `LMETA` (left GUI) |
| `R` | `R` | `LEFT_ALT` |
| `S` | `S` | `LCTRL` |
| `T` | `T` | `LEFT_SHIFT` |
| `N` | `N` | `RIGHT_SHIFT` |
| `E` | `E` | `RCTRL` |
| `I` | `I` | `RIGHT_ALT` |
| `O` | `O` | `RIGHT_GUI` |

With `flavor = "tap-preferred"` and a 220 ms tapping term, a quick tap sends the
letter and a hold sends the modifier.

---

## 5. Sticky keys (`&sk`)

The bottom-left key is a **sticky** left shift:

```devicetree
&sk {
    release-after-ms = <1000>;
    quick-release;
    lazy;
    ignore-modifiers;
};
```

- `&sk LSHFT` (BASE, bottom-left) — tap once to latch Shift for the next key,
  then it releases automatically (after 1000 ms if no key follows, or
  immediately on the next keypress with `quick-release`).
- `lazy` + `ignore-modifiers` tune the sticky behavior so it composes cleanly
  with the home-row mods.

---

## 6. Layer-taps (`&lt`)

The global layer-tap behavior is tuned as follows:

```devicetree
&lt {
    tapping-term-ms = <220>;   // default 200
    flavor = "tap-preferred";
    quick-tap-ms = <180>;
};
```

`&lt N <key>` means: tap = `<key>`, hold (past the 220 ms tapping term) = engage
layer `N`. See §3.2 for the BASE-layer mapping. `tap-preferred` means a tap is
favored when the timing is ambiguous.

---

## 7. Pointing features

Pointing is enabled (`CONFIG_ZMK_POINTING=y` in `config/corne.conf`) and used by
the MOUSE and BUTTON layers:

- **Mouse move** (`&mmv`): tuned with `acceleration-exponent = <1>`,
  `time-to-max-speed-ms = <500>`, `delay-ms = <0>`.
- **Mouse scroll** (`&msc`): scroll directions on the MOUSE layer.
- **Mouse buttons** (`&mkp`): `MB1`–`MB5`, `MB2`, `MB3`, `MCLK` on the MOUSE and
  BUTTON layers.
- Default sensitivity overrides at the top of the keymap:
  `ZMK_POINTING_DEFAULT_MOVE_VAL 800` (default 600) and
  `ZMK_POINTING_DEFAULT_SCRL_VAL 20` (default 10).

---

## 8. OLED & ZMK Studio settings

From `config/corne.conf`:

```ini
CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y
CONFIG_ZMK_SLEEP=y

# zmk studio
CONFIG_ZMK_STUDIO=y
CONFIG_ZMK_STUDIO_LOCKING=n
CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=n

CONFIG_ZMK_POINTING=y
```

- **OLED:** `CONFIG_ZMK_DISPLAY=y` with a custom status screen
  (`CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y`). The build uses the `nice_oled`
  shield (see `build.yaml`), provided by the `zmk-nice-oled` west project.
- **Sleep:** `CONFIG_ZMK_SLEEP=y` enables auto-sleep.
- **ZMK Studio:** enabled (`CONFIG_ZMK_STUDIO=y`). Studio *locking* is disabled
  (`CONFIG_ZMK_STUDIO_LOCKING=n`) and the keyboard does **not** lock on
  disconnect (`CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=n`), so the keymap can be
  edited live via ZMK Studio without a lockout. The left-side build additionally
  pulls in the `studio-rpc-usb-uart` snippet so Studio can connect over
  USB-UART (see §9).

---

## 9. Build targets & artifact workflow

`build.yaml` defines the GitHub Actions matrix. There are **three** build
targets, all on `nice_nano_v2`:

| Board | Shield(s) | Extra | Artifact |
|-------|-----------|-------|----------|
| `nice_nano_v2` | `corne_left nice_oled` | `snippet: studio-rpc-usb-uart`, `cmake-args: -DCONFIG_ZMK_STUDIO=y` | left half firmware |
| `nice_nano_v2` | `corne_right nice_oled` | — | right half firmware |
| `nice_nano_v2` | `settings_reset` | — | settings-reset image |

- Pushing to the repo (or running the workflow manually) builds these via GitHub
  Actions; download the resulting **`.uf2`** artifacts from the Actions run.
- The **left** half build enables the ZMK Studio RPC snippet so the left side can
  talk to ZMK Studio. The right half relies on the global `CONFIG_ZMK_STUDIO=y`
  from `corne.conf`.
- The **`settings_reset`** artifact clears persisted ZMK settings (layers,
  bluetooth bonds, etc.) — useful if a bad Studio edit or setting gets stuck.

---

## 10. Keymap editor

The Nick Coutsos **Keymap Editor** provides a visual editor and can produce
firmware builds from this repo's keymap:

- <https://nickcoutsos.github.io/keymap-editor/>

It reads `config/corne.keymap` (including the `zmk-helpers` key-label includes)
to render the layout. The key-label/unicode includes
(`zmk-helpers/key-labels/*.h`, `zmk-helpers/unicode-chars/german.dtsi`) only
supply **display labels and unicode glyphs** for the editor/OLED — they are not
binding macros, so they do not obscure the actual key bindings in this keymap.

---

## 11. Safe editing & flashing guidance

1. **Edit the keymap** in `config/corne.keymap` (or via the Keymap Editor / ZMK
   Studio). Keep a copy of the last-known-good keymap before changing it.
2. **Build** by pushing/running GitHub Actions; download the `.uf2` artifacts
   (left, right) from the Actions run.
3. **Flash** each half:
   - Put the half into bootloader mode (double-tap the reset button, or use the
     `bootloader` key present on the NAVIGATION and NUM layers), then copy the
     matching `.uf2` onto the mounted `NICENANO` drive.
   - Alternatively, use **ZMK Studio** (left half) for live edits without
     reflashing — note Studio changes persist to settings, so use the
     `settings_reset` artifact if you need a clean slate.
4. **Recover** with `settings_reset` if settings or a Studio edit misbehave.

> The README's existing note about downloading firmware from Actions (and the
> keymap-editor link) remains the canonical quick-start; this guide expands on it.

---

## 12. Accuracy caveat — check the source

- **Exact key positions** for every layer must be read from
  `config/corne.keymap`. This guide summarizes intent and behavior; it does not
  replace the file.
- Where a keymap uses **macros or includes** that could obscure a binding, do not
  guess — open the file and trace the definition. In this repository the active
  bindings are written out explicitly (`&kp`, `&lt`, `&sk`, `&bhm`, `&msc`,
  `&mmv`, `&mkp`, `&to`, `&trans`, `&bootloader`, `&bt`, `&out`, `&ext_power`);
  the only includes are label/unicode helpers that do not change bindings.
- Layer indices in `&lt`/`&to` are **0-based** and correspond to the table in §2.

---

## 13. Future AeroSpace WM integration — not in firmware

A future enhancement may map Corne keys (e.g. `F13`–`F20`) to macOS
[AeroSpace](https://nikitabobko.github.io/AeroSpace/) workspace/action bindings.
**This is not implemented in the firmware.** No `F13`–`F20` mappings exist in
`config/corne.keymap` today, and the AeroSpace configuration lives entirely in
the user's `~/.config/aerospace/aerospace.toml` (see
[docs/macos-aerospace.md](docs/macos-aerospace.md)). Any such integration would
require a separate firmware/keymap change and is out of scope for this
documentation.
