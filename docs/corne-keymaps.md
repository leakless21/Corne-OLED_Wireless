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

## 2. The 11 layers

The keymap defines exactly **eleven** layers. ZMK layers are **0-indexed**, and the
indices below are **named constants** in `config/corne.keymap`
(`L_BASE`, `L_NAV`, … `L_GAME_AUX`). The `&lt N` / `&mo N` / `&to N` numbers in the keymap
refer to these indices:

| Index | Layer name (`label` / `display-name`) | Purpose |
|-------|----------------------------------------|---------|
| 0 | `BASE` | Primary Colemak-DH layer with bilateral home-row modifiers, LM5 momentary MEDIA, and six thumb layer-taps. |
| 1 | `NAV` | Semantic editing shortcuts (Copy / Paste / Cut / Undo / Redo via F21–F24), Caps Word (`&caps_word` on `RM0`), cursor navigation, line/page navigation, explicit editing thumbs, and same-side left bootloader (`LT5`). |
| 2 | `MOUSE` | NAV-aligned pointer movement and scrolling, left modifiers, semantic editing (Copy / Paste / Cut / Undo / Redo), MB4/MB5 side buttons, and thumb clicks. |
| 3 | `MEDIA` | NAV-aligned Consumer HID previous/volume/next controls with right-thumb stop/play/mute controls. |
| 4 | `NUM` | Standard spatial numpad and punctuation on the left, mirrored modifiers on the right, and same-side right bootloader (`RT5`). |
| 5 | `SYM` | Shifted NUM geometry with direct programming symbols on the thumbs. |
| 6 | `FUN` | NUM-aligned F-key grid with mirrored modifiers, `RT0` Caps Lock fallback, and App/Space/Tab thumbs. |
| 7 | `HOST` | Host-agnostic F13–F20 workspace protocol, move-to-workspace, directional focus/move, Launchers, Previous Window, Resize, and Service mode. |
| 8 | `GAME` | Full plain tap-only QWERTY for gaming; dedicated left-hand Esc/AUX hold-tap, momentary RH1 AUX, and protected exit. |
| 9 | `ADJUST` | Conditional device administration, mirrored reset/bootloader, Studio Unlock (`&studio_unlock` on `RM0`), plus deliberate GAME entry. |
| 10 | `GAME_AUX` | Auxiliary gaming layer over GAME: numbers 1–0, F1–F10, missing symbols, and deliberate exit to BASE (`RH2`). |
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
- HOST uses a dedicated `host_lt` hold-tap behavior (200 ms balanced, no
  quick-tap or require-prior-idle) on the left `TAB` thumb (`LH0`), allowing
  immediate, reliable activation after typing.
---

## 3. Base layer layout & layer-switch behavior

### 3.1 Base layout (as defined in `config/corne.keymap`)

The BASE layer is a 6×3-per-side grid plus a 3-per-side thumb cluster. The
actual bindings (not a template comment) are:

```
Top row:     ESC  Q  W  F  P  B | J  L  U  Y  SQT  BSPC
Home row:    MED  A  R  S  T  G | M  N  E  I  O  ;
Bottom row:  LSH  Z  X  C  D  V | K  H  ,  .  /  RSH
Thumbs:           ESC MOUSE SPACE NAV TAB HOST | ENT SYM  BSPC NUM  DEL FUN
```

- **Colemak-DH** base letters. The **outer** keys — `ESC` (top-left), the
  momentary `MED` hold (`LM5`, home-row left), the sticky `LSH` (bottom-left),
  `BACKSPACE` (top-right), `;` (home-row right), and `RSH` (bottom-right) —
  provide direct actions.
  §4. The bare letters are the *tap* action.
- **`Z`, `V`, `K`, `/`** are **plain alpha/punctuation** (`&kp`) — not
  layer-taps. (Earlier revisions made these layer-taps; the current keymap does
  not.)
- **`LSH`** (bottom-left) is a **sticky** left shift — see §5. The physical
  outer shifts (`LSH`, `RSH`) remain as fallback shift keys.
### 3.2 How layers are reached from BASE

Layer-taps (`&lt`) are **momentary**: the target layer is active only while the
key is held. The BASE-layer layer-taps map to these layers:

| Key (tap → hold) | Behavior | Target layer | Layer engaged (while held) |
|------------------|----------|--------------|----------------------------|
| `ESC` (LH2 thumb) | `&lt` | `L_MOUSE` (2) | MOUSE |
| `SPACE` (LH1 thumb) | `&lt` | `L_NAV` (1) | NAV |
| `TAB` (LH0 thumb) | `&host_lt` | `L_HOST` (7) | HOST |
| `ENTER` (RH0 thumb) | `&lt` | `L_SYM` (5) | SYM |
| `BACKSPACE` (RH1 thumb) | `&lt` | `L_NUM` (4) | NUM |
| `DELETE` (RH2 thumb) | `&lt` | `L_FUN` (6) | FUN |
| `LM5` (outer home) | `&mo` | `L_MEDIA` (3) | MEDIA |

The **HOST** layer (7) is engaged directly by holding the `TAB` thumb (`LH0`).

The **GAME** layer (8) is a persistent `&to` switch entered deliberately from
ADJUST. While on GAME, **GAME_AUX** (10) can be engaged from either hand:
- **Left-hand mouse gaming:** Hold top-left `Escape` (`&game_aux_lt L_GAME_AUX ESCAPE`) + `Q`/`W`/`E`/`R`/`T` for numbers `1`–`5`.
- **Two-handed access:** Hold right-middle thumb `RH1` (`&mo L_GAME_AUX`) + top row for numbers `1`–`0`.

To prevent accidental exits during gameplay, GAME has no naked single-key exit;
exit to BASE is protected behind **`GAME_AUX` + right outer thumb (`RH2`)** (`&to L_BASE`).

The **ADJUST** layer (9) is conditional: it activates automatically when both
NAV (1) and NUM (4) are held simultaneously.
Functional layers use explicit `&none` for unused positions and explicit
single-action thumb bindings. `&trans` is not used in the functional layer
thumbs, so a held Backspace or other editor key cannot inherit a BASE
layer-tap unexpectedly.


### 3.3 HOST thumb activation & physical grammar

HOST is engaged directly by holding the left inner thumb (`LH0`, `Tab`). There
is no combo; thumb hold is the single canonical activation path.

The layer organizes controls by usage frequency:

| HOST group | Physical positions | Emitted binding | Action |
|------------|--------------------|-----------------|--------|
| Workspace focus | left home core (`LM4`–`LM0`) | `F13`–`F17` | Visit WEB / DEV / COMMS / RUN / AUX |
| Move to workspace | left top core (`LT4`–`LT0`) | `Shift-F13`–`Shift-F17` | Move window to workspace + follow |
| Launchers & Terminal | left bottom core (`LB4`–`LB2`) | `Alt+F13`–`Alt+F15` | Launcher (Spotlight), Quick Terminal (Ghostty dropdown), New Terminal (Ghostty) |
| Previous Window | right home inner (`RM0`) | `Alt+F16` | Toggle focus between last two windows (`focus-back-and-forth`) |
| Window focus | right home core (`RM1`–`RM4`) | `Ctrl+F13`–`Ctrl+F16` | Focus Left / Down / Up / Right |
| Window move | right bottom core (`RB1`–`RB4`) | `Ctrl+Shift+F13`–`Ctrl+Shift+F16` | Move window Left / Down / Up / Right |
| Resize mode | right top (`RT1`) | `Shift+F18` | Enter AeroSpace resize mode |
| Service mode | right top (`RT2`) | `Alt+F18` | Enter AeroSpace service mode |
| Esc | right top (`RT5`) | `ESCAPE` | Dismiss mode / escape |
| Context actions | right thumbs (`RH0`–`RH2`) | `F19`, `F18`, `F20` | Fullscreen (`RH0`), Previous WS (`RH1`), Float (`RH2`) |
---

### 3.4 GAME and GAME_AUX layouts

```text
GAME (Layer 8)

ESC/AUX  Q      W      E      R      T   |  Y      U      I      O      P      BSPC
TAB      A      S      D      F      G   |  H      J      K      L      ;      ENTER
SHIFT    Z      X      C      V      B   |  N      M      ,      .      /      SHIFT
                CTRL   SPACE  ALT        |  ENTER  AUX    _
```

```text
GAME_AUX (Layer 10)

_        1      2      3      4      5   |  6      7      8      9      0      _
_        F1     F2     F3     F4     F5  |  F6     F7     F8     F9     F10    _
_        `      -      =      [      ]   |  _      _      _      _      _      _
                _      _      _          |  _      _      BASE
```

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

### 6.1 HOST hold-tap (`&host_lt`)

HOST uses a dedicated hold-tap behavior rather than generic `&lt`:

```devicetree
host_lt: host_lt {
    compatible = "zmk,behavior-hold-tap";
    #binding-cells = <2>;
    flavor = "balanced";
    tapping-term-ms = <200>;
    bindings = <&mo>, <&kp>;
};
```

- **`tapping-term-ms = <200>`** with **`flavor = "balanced"`** allows fast,
  reliable layer entry.
- **No `quick-tap-ms` or `require-prior-idle-ms`** is set, so HOST can be entered
  immediately after typing without timing lockouts.
---

### 6.2 GAME Esc/AUX hold-tap (`&game_aux_lt`)

GAME uses a dedicated hold-tap on the top-left `Escape` position (`LT5`) designed
specifically for rapid chord resolution during mouse + keyboard gaming:

```devicetree
game_aux_lt: game_aux_lt {
    compatible = "zmk,behavior-hold-tap";
    #binding-cells = <2>;
    flavor = "hold-preferred";
    tapping-term-ms = <200>;
    bindings = <&mo>, <&kp>;
};
```

- **`flavor = "hold-preferred"`**: Pressing another key while Escape is held
  immediately resolves as hold (`&mo L_GAME_AUX`), sending numbers (e.g. `Esc + Q` → `1`)
  without sending an accidental Escape tap.
- **Tapping Escape** alone (press and release) reliably sends `Escape`.
- Independent of opposite-hand triggers, home-row-mod timing, or idle requirements.

## 7. Pointing features

Pointing is enabled (`CONFIG_ZMK_POINTING=y`) and used by the MOUSE layer:

- **Mouse modifiers** (`LGUI`, `LALT`, `LCTRL`, `LEFT_SHIFT`) occupy the
  physical `A R S T` home positions.
- **Semantic editing** (Copy, Paste, Cut, Undo, Redo via F21–F24) is duplicated in the right top row, matching NAV.
- **Pointer movement** occupies the right-hand home-row direction positions.
- **Mouse wheel** occupies the matching right-hand bottom-row positions.
- **MB4/MB5** occupy the right-hand home-row positions (`RM0` = MB4 Back, `RM5` = MB5 Forward).
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
CONFIG_ZMK_STUDIO_LOCKING=y
CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=y
CONFIG_ZMK_POINTING=y
```

The display blanks after 30 seconds and deep sleep begins after 15 minutes.
Studio locking is enabled (`CONFIG_ZMK_STUDIO_LOCKING=y`, `CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=y`)
to enforce that the Git-tracked `config/corne.keymap` remains authoritative.
When runtime experimentation in ZMK Studio is desired, holding NAV + NUM activates ADJUST,
where the `&studio_unlock` key on `RM0` unlocks Studio for live tuning.

**Important Studio Source-of-Truth Workflow:**
ZMK Studio runtime changes persist in on-device storage independently of newly flashed
firmware images. If you edit `config/corne.keymap`, flash new firmware, and wonder why
your changes do not appear, an active Studio runtime override is active on the device.
To restore the Git-authored firmware keymap, use **Restore Stock Settings** in ZMK Studio.
This clears runtime overrides without clearing Bluetooth bonds.
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
   mode using:
   - **Convenient firmware shortcuts:** `NAV` + left outer/top key (`LT5`) for left half;
     `NUM` + right outer/top key (`RT5`) for right half.
   - **Administrative layer:** `ADJUST` + mirrored `&bootloader` bindings.
   - **Guaranteed standalone recovery:** double-tap the physical reset button on the individual nice!nano.
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

## 14. Semantic host integration (HOST & Editing)

The firmware uses semantic high-function keys to keep physical muscle memory identical across operating systems:

1. **Window management (`F13`–`F20`):**
   - Emitted from the HOST layer.
   - macOS: Managed by AeroSpace (`dotfiles/aerospace.toml`).
   - Windows: Can be mapped to GlazeWM or another tiling window manager.
   - Emits `F13`–`F20`, `Shift-F13`–`Shift-F17`, `Ctrl+F13`–`Ctrl+F16`, and `Ctrl+Shift+F13`–`Ctrl+Shift+F16`.

2. **Cross-platform editing (`F21`–`F24`):**
   - Emitted from NAV and MOUSE (`RT0`–`RT4`).
   - `F21` = Copy (`Command+C` on macOS / `Ctrl+C` on Windows)
   - `F22` = Paste (`Command+V` on macOS / `Ctrl+V` on Windows)
   - `F23` = Cut (`Command+X` on macOS / `Ctrl+X` on Windows)
   - `F24` = Undo (`Command+Z` on macOS / `Ctrl+Z` on Windows)
   - `Shift+F24` = Redo (`Command+Shift+Z` on macOS / `Ctrl+Y` on Windows)
   - macOS adapter: Karabiner-Elements (`dotfiles/karabiner-corne.json`).
   - Windows adapter: AutoHotkey v2 (`dotfiles/corne-windows.ahk`).

3. **Consumer media (`C_*`):**
   - Emitted directly from the MEDIA layer using portable Consumer HID codes (`C_PREVIOUS`, `C_VOLUME_DOWN`, `C_VOLUME_UP`, `C_NEXT`, `C_PLAY_PAUSE`, `C_MUTE`, `C_STOP`).
   - Works natively on both macOS and Windows without extra host configuration.
