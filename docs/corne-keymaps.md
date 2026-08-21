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
| 0 | `BASE` | Primary typing layer (Colemak-DH). Home-row modifiers + thumb/letter layer-taps reach the other layers. |
| 1 | `NAV` | macOS Cmd clipboard chords, arrows/text navigation, Caps Lock, and the named `&to L_GAME` entry. |
| 2 | `MOUSE` | Left-hand GUI/Alt/Ctrl/Shift modifiers; right-hand scroll, mouse buttons, and pointer movement. |
| 3 | `MEDIA` | Media-only: volume, play/pause/stop/mute. |
| 4 | `NUM` | Numpad and punctuation on the left, with right-hand modifiers. |
| 5 | `SYM` | Symbols: brackets, braces, parentheses, and math/punctuation glyphs. |
| 6 | `FUN` | F1–F12 on the left, with right-hand modifiers. |
| 7 | `HOST` | Direct AeroSpace bridge: F13–F20, Shift-F13–F17, and spatial Option+H/J/K/L focus/move clusters. |
| 8 | `GAME` | Explicit full tap-only QWERTY. Entered via `&to L_GAME` from NAV; exits via `&to L_BASE`. |
| 9 | `ADJUST` | Conditional admin layer: five BT profiles, explicit I/O power actions, and mirrored reset/bootloader bindings. |

> **`BUTTON` is gone.** The previous `BUTTON` layer (index 3) has been removed;
> `MEDIA` now occupies index 3 and `NUM`/`SYM`/`FUN`/`HOST`/`GAME`/`ADJUST` shift
> up accordingly. Because **layer numbers are part of the persisted ZMK keymap
> state**, deleting/renumbering a layer changes any Studio-persisted layer state
> on the keyboard. After migrating, flash both halves and, if the persisted
> settings or Bluetooth bonds look wrong, flash the **`settings-reset`** artifact
> (it clears settings **and** Bluetooth bonds) to start clean.

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
- **Thumbs** are all **layer-taps** (`&lt`): tap for the printed key, hold to
  engage the named layer — see §3.2.

### 3.2 How layers are reached from BASE

Layer-taps (`&lt`) are **momentary**: the target layer is active only while the
key is held. The BASE-layer layer-taps map to these layers:

| Key (tap → hold) | `&lt` target | Layer engaged (while held) |
|------------------|--------------|----------------------------|
| `ESC` (thumb)    | `&lt 3`*     | MEDIA (3) |
| `SPACE` (thumb)  | `&lt 1`      | NAV (1) |
| `TAB` (thumb)    | `&lt 2`      | MOUSE (2) |
| `ENTER` (thumb)  | `&lt 5`      | SYM (5) |
| `BACKSPACE` (thumb) | `&lt 4`  | NUM (4) |
| `DELETE` (thumb) | `&lt 6`      | FUN (6) |

\* The MEDIA thumb target is `L_MEDIA` (3); the table uses the numeric index for
clarity.

The **GAME** layer (8) is **not** a layer-tap. It is reached from the **NAV**
layer via `&to L_GAME` — a *layer switch* (`&to`) that activates layer 8 and
deactivates the others. Because `&to` is a switch rather than a momentary hold,
GAME stays active until you exit. The GAME layer includes an **explicit
right-thumb `&to L_BASE`** exit binding, so it is a round-trip switch.

The **HOST** layer (7) is reached from BASE by a **combo** (see §3.3), not a
layer-tap.

The **ADJUST** layer (9) is **conditional**: it activates automatically when both
NAV (1) and NUM (4) are held simultaneously (see `conditional_layers` in the
keymap).

> Transparent fall-through is used only where the source explicitly contains
> `&trans` (for example NAV, NUM, SYM, and FUN thumb positions). MOUSE, MEDIA,
> HOST, GAME, and ADJUST use explicit `&none` entries for unused positions so
> those domain layers do not leak BASE actions unexpectedly.

### 3.3 HOST activation combo

HOST is engaged by holding a **combo** on the BASE layer: the outer `ESC`
(key-position `0`) together with `BACKSPACE` (key-position `11`), within an
80 ms timeout (`host_combo`, `&mo L_HOST`). The combo has `slow-release`, so
HOST remains held until both trigger keys are released.

HOST is arranged as a control surface rather than a Colemak-shaped copy of the
base letters:

| HOST group | Physical positions | Emitted binding |
|------------|--------------------|-----------------|
| Workspace focus | left top, F13–F17 | `F13`–`F17` → WEB/DEV/COMMS/RUN/AUX |
| Move + follow | left home | `Shift-F13`–`Shift-F17` → move window and follow |
| Context actions | right top | `F18` previous workspace, `F19` fullscreen, `F20` floating |
| Focus windows | right home, left/down/up/right | `Option+H/J/K/L` |
| Move windows | right bottom, left/down/up/right | `Option+Shift+H/J/K/L` |

The firmware emits these protocol keys; AeroSpace assigns their meaning. The
MacBook keyboard remains ordinary QWERTY and does not need Colemak remapping.

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

Pointing is enabled (`CONFIG_ZMK_POINTING=y` in `config/corne.conf`) and used by
the MOUSE layer:

- **Mouse modifiers** (`LGUI`, `LALT`, `LCTRL`, `LEFT_SHIFT`) occupy the
  left-hand home row.
- **Mouse scroll** (`&msc`) occupies the right-hand top row.
- **Mouse buttons** (`&mkp MB1`–`MB5`, `MCLK`) occupy the right-hand home row.
- **Mouse move** (`&mmv`) occupies the right-hand bottom row.
- Mouse move is tuned with `acceleration-exponent = <1>`,
  `time-to-max-speed-ms = <500>`, `delay-ms = <0>`.
- Default sensitivity overrides at the top of the keymap:
  `ZMK_POINTING_DEFAULT_MOVE_VAL 800` (default 600) and
  `ZMK_POINTING_DEFAULT_SCRL_VAL 20` (default 10).

---

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
CONFIG_ZMK_STUDIO_LOCKING=n
CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=n

CONFIG_ZMK_POINTING=y
```

- **OLED:** `CONFIG_ZMK_DISPLAY=y` with a custom status screen. The build uses
  the `nice_oled` shield (see `build.yaml`), provided by the pinned
  `zmk-nice-oled` west project.
- **Power policy:** blank the display after 30 seconds of inactivity and enter
  deep sleep after 15 minutes. These are explicit baseline values; characterize
  wake latency, reconnect behavior, OLED reliability, and left/right battery
  balance over several charge cycles before tuning them.
- **ZMK Studio:** enabled and unlocked for experimentation. Studio edits
  persist to on-device settings and can diverge from the Git-tracked
  `config/corne.keymap`; flash `settings-reset` if an overlay misbehaves.

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

The Nick Coutsos **Keymap Editor** provides a visual editor and can produce
firmware builds from this repo's keymap:

- <https://nickcoutsos.github.io/keymap-editor/>

It reads `config/corne.keymap` (including the `zmk-helpers` key-label includes)
to render the layout. The key-label/unicode includes
(`zmk-helpers/key-labels/*.h`, `zmk-helpers/unicode-chars/german.dtsi`) only
supply **display labels and unicode glyphs** for the editor/OLED — they are not
binding macros, so they do not obscure the actual key bindings in this keymap.

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

1. **Edit the keymap** in `config/corne.keymap` (or via the Keymap Editor /
   ZMK Studio). Keep a copy of the last-known-good keymap before changing it.
   The Git-tracked file is canonical; Studio edits are experimental overlays.
2. **Build** by pushing/running GitHub Actions; download the `.uf2` artifacts
   (`corne-left`, `corne-right`) from the Actions run.
3. **Flash** each half:
   - Put the half into bootloader mode (double-tap the reset button, or use the
     matching left/right `bootloader` key on ADJUST), then copy the matching
     `.uf2` onto the mounted `NICENANO` drive.
   - Alternatively, use **ZMK Studio** (left half) for live edits without
     reflashing — note Studio changes persist to settings, so use the
     `settings-reset` artifact if you need a clean slate.
4. **Recover** with `settings-reset` if settings or a Studio edit misbehave, or
   after a layer renumbering migration (it also clears Bluetooth bonds).

Repository checks can establish that the keymap parses and the generated
diagram matches it. Only a physical smoke test can establish split reconnect,
Bluetooth switching, source-local reset/bootloader behavior, OLED wake, HOST
input delivery, and deep-sleep behavior on this hardware.

---

## 13. Accuracy caveat — check the source

- **Exact key positions** for every layer must be read from
  `config/corne.keymap`. This guide summarizes intent and behavior; it does not
  replace the file.
- Where a keymap uses **macros or includes** that could obscure a binding, do not
  guess — open the file and trace the definition. In this repository the active
  bindings are written out explicitly (`&kp`, `&lt`, `&sk`, `&mo`, `&to`,
  `&msc`, `&mmv`, `&mkp`, `&trans`, `&bootloader`, `&bt`, `&out`, `&ext_power`);
  the only includes are label/unicode helpers that do not change bindings.
- Layer indices in `&lt`/`&to` are **0-based** and correspond to the named
  constants (`L_BASE`…`L_ADJUST`) and the table in §2.

---

## 14. Corne HOST → AeroSpace integration (implemented)

The HOST layer (7) is implemented in firmware and bridges to macOS AeroSpace.
It emits F13–F20, Shift-F13–F17, and spatial Option+H/J/K/L focus/move chords;
AeroSpace binds those signals directly (see
[docs/macos-aerospace.md](macos-aerospace.md)). No Alt-1-style intermediate
mapping is used on the Corne side, and the MacBook remains ordinary QWERTY.
