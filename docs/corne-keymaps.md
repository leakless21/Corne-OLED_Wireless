# Corne Keymap & Layers Guide

> **Repository context.** This repository is a **ZMK firmware** project for a Corne
> split keyboard (it is **not** QMK). This guide documents the keymap, layers, and
> related firmware settings found in `config/corne.keymap`, `config/corne.conf`,
> `build.yaml`, and `config/west.yml`. It describes what is present in those
> source files; the canonical source of truth is always the files themselves.

---

## 1. Firmware identity: ZMK, not QMK

- The keymap is written in ZMK's Devicetree/behavior syntax (`&kp`, `&lt`, `&sk`,
  `&mo`/`&to`, `&mmv`, `&msc`, `&mkp`, etc.), not QMK's C `LAYOUT` arrays.
- `config/west.yml` pins the **zmk** project from `github.com/zmkfirmware` and two
  helpers, all at **immutable revision SHAs** (do not replace these with `main`):
  - `zmk` (remote `zmkfirmware`) — revision `6e2ef41e022d555b10f116e395832913f71717b3`.
  - `zmk-nice-oled` (remote `tokyo2006`) — revision `de5b2afbd05f1a136e31ca28659373cd07d1e443` — full LVGL 9-compatible OLED display support.
  - `zmk-helpers` (remote `urob`) — revision `95edb8f15ef1d1bd8332810555f8cf5837fbdd27` — key-label and unicode helpers used for visualization/editor labels.
- The board target is **`nice_nano@2.0.0//zmk`** (see `build.yaml`), a common wireless
  Corne controller.

---

## 2. The 10 layers

The keymap defines exactly **ten** layers. ZMK layers are **0-indexed**, and the
indices below are **named constants** in `config/corne.keymap`
(`L_BASE`, `L_NAV`, … `L_ADJUST`). The `&lt N` / `&to N` numbers in the keymap
refer to these indices:

| Index | Layer name (`label` / `display-name`) | Purpose |
|-------|----------------------------------------|---------|
| 0 | `BASE` | Primary Colemak-DH layer with bilateral home-row modifiers and six thumb layer-taps. |
| 1 | `NAV` | macOS Cmd clipboard, cursor navigation, line/page navigation, and explicit editing thumbs. |
| 2 | `MOUSE` | NAV-aligned pointer movement and scrolling, left modifiers, clipboard, and thumb buttons. |
| 3 | `MEDIA` | NAV-aligned previous/volume/next controls with transport thumbs. |
| 4 | `NUM` | Standard spatial numpad and punctuation on the left, mirrored modifiers on the right. |
| 5 | `SYM` | Shifted NUM geometry with direct programming symbols on the thumbs. |
| 6 | `FUN` | NUM-aligned F-key grid with mirrored modifiers and App/Space/Tab thumbs. |
| 7 | `HOST` | Host-agnostic F13–F20 workspace protocol and Ctrl+F directional signals. |
| 8 | `GAME` | Full plain tap-only QWERTY for gaming; entered from ADJUST and exited explicitly. |
| 9 | `ADJUST` | Conditional device administration plus the deliberate GAME entry. |

> **`BUTTON` is gone.** The previous `BUTTON` layer (index 3) was removed in
> the earlier migration; `MEDIA` now occupies index 3 and the remaining layer
> numbers are persisted in ZMK state. If a device still has stale Studio
> settings, use **Restore Stock Settings** first. A layer renumbering or full
> settings mismatch requires `settings-reset`, followed by reflash and pairing.

> **Verify, don't assume.** The exact key *positions* for every layer live in
> `config/corne.keymap`. Always open that file to confirm a specific binding —
> this table only summarizes each layer's intent.

The administrative bindings follow current upstream ZMK semantics:

- ZMK provides five Bluetooth profiles by default. `BT_SEL` is zero-based;
  `BT_NXT` and `BT_PRV` cycle profiles; `BT_CLR` clears only the selected
  profile; and `BT_CLR_ALL` clears every profile. After clearing a bond, forget
  the keyboard on the host before pairing again so the host does not reuse an
  old security key. See <https://zmk.dev/docs/keymaps/behaviors/bluetooth>.
- Reset and bootloader behaviors are source-specific on split keyboards, which
  is why ADJUST contains bindings on both halves. See
  <https://zmk.dev/docs/keymaps/behaviors/reset>.
- `OUT_USB`/`OUT_BLE` and `EP_ON`/`EP_OFF` are explicit persistent states rather
  than hidden-state toggles. See
  <https://zmk.dev/docs/keymaps/behaviors/outputs> and
  <https://zmk.dev/docs/keymaps/behaviors/power>.
- The HOST combo uses `slow-release`, so its momentary layer remains active
  until both combo keys are released. See
  <https://zmk.dev/docs/keymaps/combos>.

---

## 3. Base layer layout & layer-switch behavior

### 3.1 Base layout (as defined in `config/corne.keymap`)

The BASE layer is a 6×3-per-side grid plus a 3-per-side thumb cluster. The
actual bindings (not a template comment) are:

```
Top row:     ESC  Q  W  F  P  B | J  L  U  Y  SQT  BSPC
Home row:    TAB  A  R  S  T  G | M  N  E  I  O  ;
Bottom row:  LSH  Z  X  C  D  V | K  H  ,  .  /  RSH
Thumbs:           ESC MED  SPACE NAV  TAB MOUSE | ENT SYM  BSPC NUM  DEL FUN
```

- **Colemak-DH** base letters. The **outer** keys — `ESC` (top-left), `TAB`
  (home-row left), the sticky `LSH` (bottom-left), and `BACKSPACE` (top-right),
  `;` (home-row right), `RSH` (bottom-right) — remain plain keys.
- **Home-row letters** (`A R S T` / `N E I O`) are **hold-tap modifiers** — see
  §4. The bare letters are the *tap* action.
- **`Z`, `V`, `K`, `/`** are **plain alpha/punctuation** (`&kp`) — not
  layer-taps. (Earlier revisions made these layer-taps; the current keymap does
  not.)
- **`LSH`** (bottom-left) is a **sticky** left shift — see §5. The physical
  outer shifts (`LSH`, `RSH`) remain as fallback shift keys.
### 3.2 How layers are reached from BASE

Layer-taps (`&lt`) are **momentary**: the target layer is active only while the
key is held. The BASE-layer layer-taps map to these layers:

| Key (tap → hold) | `&lt` target | Layer engaged (while held) |
|------------------|--------------|----------------------------|
| `ESC` (thumb) | `&lt 3`* | MEDIA (3) |
| `SPACE` (thumb) | `&lt 1` | NAV (1) |
| `TAB` (thumb) | `&lt 2` | MOUSE (2) |
| `ENTER` (thumb) | `&lt 5` | SYM (5) |
| `BACKSPACE` (thumb) | `&lt 4` | NUM (4) |
| `DELETE` (thumb) | `&lt 6` | FUN (6) |

*The MEDIA thumb target is `L_MEDIA` (3); the table uses the numeric index for
clarity.*

The **HOST** layer (7) is reached from BASE by the outer-key combo described in
§3.3. It is momentary.

The **GAME** layer (8) is a persistent `&to` switch, but it is deliberately
entered from ADJUST rather than from an ordinary NAV key. Its QWERTY bindings
are plain tap actions; the right outer thumb is the explicit `&to L_BASE` exit.

The **ADJUST** layer (9) is conditional: it activates automatically when both
NAV (1) and NUM (4) are held simultaneously.

Functional layers use explicit `&none` for unused positions and explicit
single-action thumb bindings. `&trans` is not used in the functional layer
thumbs, so a held Backspace or other editor key cannot inherit a BASE
layer-tap unexpectedly.


### 3.3 HOST activation combo and physical grammar

HOST is engaged by holding a BASE combo on the outer top positions:
`LT5` (outer left Escape) together with `RT5` (outer right Backspace), within an
80 ms timeout. `slow-release` keeps HOST active until both trigger keys are
released.

The layer follows the shared physical contract in
[layout-principles.md](layout-principles.md):

| HOST group | Physical positions | Emitted binding |
|------------|--------------------|-----------------|
| Workspace focus | left top core | `F13`–`F17` |
| Move + follow | left home core | `Shift-F13`–`Shift-F17` |
| Context/mode | right top core | `Shift-F18`, `F18`, `F19`, `F20` |
| Focus windows | right home core | `Ctrl+F13`–`Ctrl+F16` |
| Move windows | right bottom core | `Ctrl+Shift+F13`–`Ctrl+Shift+F16` |

The firmware emits semantic protocol keys. AeroSpace, GlazeWM, or another host
adapter assigns their meaning. The macOS adapter also keeps ordinary
Option+H/J/K/L for the laptop keyboard.

---

## 4. Home-row modifiers (two side-aware balanced behaviors)

Two custom hold-tap behaviors are defined — one per hand — and applied to the
home-row letters:

```devicetree
hml: home_row_mods_left {
    compatible = "zmk,behavior-hold-tap";
    flavor = "balanced";
    tapping-term-ms = <280>;
    quick-tap-ms = <175>;
    require-prior-idle-ms = <150>;
    hold-trigger-on-release;
    hold-trigger-key-positions = < /* opposite-hand positions */ >;
    bindings = <&kp>, <&kp>;
};

hmr: home_row_mods_right {
    compatible = "zmk,behavior-hold-tap";
    flavor = "balanced";
    tapping-term-ms = <280>;
    quick-tap-ms = <175>;
    require-prior-idle-ms = <150>;
    hold-trigger-on-release;
    hold-trigger-key-positions = < /* opposite-hand positions */ >;
    bindings = <&kp>, <&kp>;
};
```

Both are **positional balanced** hold-taps with identical timing:
**280 ms** tapping term, **175 ms** quick-tap, **150 ms** require-prior-idle, and
**`hold-trigger-on-release`**. Each behavior lists the **opposite hand's**
key positions in `hold-trigger-key-positions`, so a hold only becomes a modifier
when a key on the other hand is pressed (opposite-hand triggers). The physical
outer shifts (`LSH`/`RSH`) remain as fallback shift sources.

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

Pointing is enabled (`CONFIG_ZMK_POINTING=y`) and used by the MOUSE layer:

- **Mouse modifiers** (`LGUI`, `LALT`, `LCTRL`, `LEFT_SHIFT`) occupy the
  physical `A R S T` home positions.
- **Clipboard** is duplicated in the right top row, matching NAV.
- **Pointer movement** occupies the right-hand home-row direction positions.
- **Mouse wheel** occupies the matching right-hand bottom-row positions.
- **MB5/MB4** occupy the right-hand home-row outer positions.
- **Right/left/middle click** occupy the three right thumbs. `MB3` is the
  middle button; the redundant `MCLK` binding is removed.
- Mouse move is tuned with `acceleration-exponent = <1>`,
  `time-to-max-speed-ms = <500>`, `delay-ms = <0>`.
- Default sensitivity overrides at the top of the keymap are
  `ZMK_POINTING_DEFAULT_MOVE_VAL 800` and `ZMK_POINTING_DEFAULT_SCRL_VAL 20`.


> Changing pointing/HID support can change the Bluetooth HID descriptor. Hosts
> may cache it; after changing `CONFIG_ZMK_POINTING` or related HID features,
> forget the keyboard, clear the selected `BT_CLR` profile, and pair again.

## 8. OLED, power, and ZMK Studio settings

From `config/corne.conf`:

```ini
CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y
CONFIG_ZMK_DISPLAY_BLANK_ON_IDLE=y
CONFIG_ZMK_IDLE_TIMEOUT=30000
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000
CONFIG_ZMK_STUDIO=y
CONFIG_ZMK_POINTING=y
```

The display blanks after 30 seconds and deep sleep begins after 15 minutes.
These values remain a baseline until battery drain, wake reliability, BLE
reconnect latency, and OLED wake behavior are measured on hardware.

ZMK Studio edits persist to device settings and can override later firmware
keymap changes. To return from an experiment to Git-tracked firmware, first use
**Restore Stock Settings** in Studio. This clears Studio-specific overrides
without clearing Bluetooth bonds. Use `settings-reset` only when that recovery
path fails or a full settings/Bluetooth reset is intentional.

The current ZMK power defaults and display options are documented at
<https://zmk.dev/docs/config/power> and
<https://zmk.dev/docs/config/displays>. Deep-sleep behavior deserves physical
testing: ZMK issue
<https://github.com/zmkfirmware/zmk/issues/2686> records reports of lost
keypresses during wake/reconnect and recommends treating timeout changes as a
hardware/host trade-off, not a guarantee.

---

## 9. Build targets & artifact workflow

`build.yaml` defines the GitHub Actions matrix. There are **three** named build
targets, all on `nice_nano@2.0.0//zmk`:

| Board | Shield(s) | Extra | Artifact name |
|-------|-----------|-------|---------------|
| `nice_nano@2.0.0//zmk` | `corne_left nice_oled` | `snippet: studio-rpc-usb-uart`, `cmake-args: -DCONFIG_ZMK_STUDIO=y` | `corne-left` |
| `nice_nano@2.0.0//zmk` | `corne_right nice_oled` | — | `corne-right` |
| `nice_nano@2.0.0//zmk` | `settings_reset` | — | `settings-reset` |

- Pushing to the repo (or running the workflow manually) builds these via GitHub
  Actions; download the resulting **`.uf2`** artifacts from the Actions run.
- The **left** half build enables the ZMK Studio RPC snippet so the left side can
  talk to ZMK Studio. The right half relies on the global `CONFIG_ZMK_STUDIO=y`
  from `corne.conf`.
- The **`settings_reset`** artifact clears persisted ZMK settings (layers,
  bluetooth bonds, etc.) — the recovery path if a bad Studio edit or setting gets
  stuck.

---

## 10. Keymap editor

The Nick Coutsos [Keymap Editor](https://nickcoutsos.github.io/keymap-editor/)
provides a visual editor and can produce firmware builds from this repo's
keymap. The active keymap includes only the pinned `42.h` position labels plus
the standard ZMK behavior and binding includes; historical Glove80 and German
Unicode includes are intentionally removed.

---

## 11. Generated keymap diagram

The repository uses `keymap-drawer` to parse `config/corne.keymap` and generate:

- `keymap-drawer/corne.yaml` — parsed, reviewable keymap representation.
- `keymap-drawer/corne.svg` — visual layer reference.

`.github/workflows/draw-keymap.yml` runs on keymap/config changes and pins the
`keymap-drawer` workflow and package to v0.23.0. The generated files are the
daily visual reference; this document explains behavior and rationale.

The workflow uses the pinned v0.23.0 release and reusable-workflow commit
`a44809b8cc718cbff646641f49a8f71a9368336d`. Upstream workflow and configuration
references:
<https://github.com/caksoylar/keymap-drawer/blob/main/.github/workflows/draw-zmk.yml>,
<https://github.com/caksoylar/keymap-drawer/releases/tag/v0.23.0>.

---

## 12. Safe editing & flashing guidance

1. **Edit the keymap** in `config/corne.keymap` or use the Keymap Editor /
   ZMK Studio. The physical contract in
   [layout-principles.md](layout-principles.md) is the source for shared
   positions. Keep a known-good source revision before structural changes.
2. **Build** by pushing/running GitHub Actions; download the `.uf2` artifacts
   (`corne-left`, `corne-right`).
3. **Flash** each half with its matching artifact. Put the half into bootloader
   mode using double-tap reset or its source-local ADJUST `&bootloader` binding.
4. **Recover Studio divergence** with Studio's **Restore Stock Settings** first,
   then flash the normal firmware. This preserves Bluetooth bonds.
5. **Use `settings-reset` only for full recovery.** It clears persisted settings,
   Studio overrides, split state, Bluetooth bonds, output state, and external
   power state; reflash both normal images and re-pair afterward.
6. **Validate** the generated diagram and then run the physical smoke-test
   checklist in `docs/usage.md`.

Repository checks can establish that the keymap parses and the generated
diagram matches it. Only a physical smoke test can establish split reconnect,
Bluetooth switching, source-local reset/bootloader behavior, OLED wake, HOST
input delivery, and deep-sleep behavior on this hardware.
---

## 13. Accuracy caveat — check the source

- **Exact key positions** for every layer must be read from
  `config/corne.keymap`. This guide summarizes intent and behavior; it does not
  replace the file.
- The active bindings are written out explicitly (`&kp`, `&lt`, `&sk`, `&mo`,
  `&to`, `&msc`, `&mmv`, `&mkp`, `&none`, `&bootloader`, `&bt`, `&out`,
  `&ext_power`). The only nonstandard include is the pinned `42.h` position
  label header used for named combo and hold-trigger positions.
- Layer indices in `&lt`/`&to` are **0-based** and correspond to the named
  constants (`L_BASE`…`L_ADJUST`) and the table in §2.

---

## 14. Corne HOST → host adapter integration

HOST emits F13–F20, Shift-F13–F17, Ctrl+F13–F16, and
Ctrl+Shift+F13–F16. The reference macOS adapter is tracked at
`dotfiles/aerospace.toml`; its resize mode interprets Ctrl+F13–F16 as resize
directions. The protocol deliberately does not encode Option+H/J/K/L, so a
future Windows/GlazeWM adapter can assign the same semantic signals without a
firmware change.
