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
  - `zmk-nice-oled` (remote `mctechnology17`) — revision `46f824abb2bd41f1287c5c68abd14122af6042a3` — OLED display support.
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
| 0 | `BASE` | Primary typing layer (Colemak-DH). Home-row modifiers + thumb/letter layer-taps to reach every other layer. |
| 1 | `NAV` | macOS Cmd clipboard chords (Cmd+C/V/X/Z and Cmd+Shift+Z), arrows/text navigation, and the named `&to L_GAME` entry. No bootloader. |
| 2 | `MOUSE` | Pointer control: scroll (`&msc`), mouse buttons (`&mkp MB1`–`MB5`, `MCLK`), and mouse movement (`&mmv`). |
| 3 | `MEDIA` | Media-only: volume, play/pause/stop/mute. |
| 4 | `NUM` | Numpad: digits `0`–`9`, brackets, `MINUS`, `PERIOD`, `GRAVE`, `BACKSLASH`. |
| 5 | `SYM` | Symbols: brackets, braces, parentheses, and math/punctuation glyphs (`&`, `*`, `$`, `%`, `@`, `#`, `|`, etc.). |
| 6 | `FUN` | Function row: `F1`–`F12`. |
| 7 | `HOST` | Bridge to macOS AeroSpace: emits `F13`–`F20` and `Option+H/J/K/L` from the BASE physical H/J/K/L positions. Activated by a BASE combo (see §3.3). |
| 8 | `GAME` | Explicit full tap-only QWERTY. Entered via `&to L_GAME` from NAV; exits via an explicit right-thumb `&to L_BASE`. |
| 9 | `ADJUST` | Conditional layer (active only when NAV + NUM are both held). BT select/clear, output toggle, external-power toggle, bootloader, reset. |

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
80 ms timeout (`host_combo`, `&mo L_HOST`). While HOST is active, the BASE
physical H/J/K/L positions emit `Option+H/J/K/L` (`LA(H)`, `LA(J)`, `LA(K)`,
`LA(L)`) and the top rows emit `F13`–`F20` for the AeroSpace bridge (see
[docs/macos-aerospace.md](macos-aerospace.md)).

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

- **Mouse move** (`&mmv`): tuned with `acceleration-exponent = <1>`,
  `time-to-max-speed-ms = <500>`, `delay-ms = <0>`.
- **Mouse scroll** (`&msc`): scroll directions on the MOUSE layer.
- **Mouse buttons** (`&mkp`): `MB1`–`MB5` and `MCLK` on the MOUSE layer.
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
- **ZMK Studio:** enabled (`CONFIG_ZMK_STUDIO=y`) and **unlocked** for
  experimentation — Studio *locking* is disabled
  (`CONFIG_ZMK_STUDIO_LOCKING=n`) and the keyboard does **not** lock on
  disconnect (`CONFIG_ZMK_STUDIO_LOCK_ON_DISCONNECT=n`), so the keymap can be
  edited live via ZMK Studio without a lockout. The left-side build additionally
  pulls in the `studio-rpc-usb-uart` snippet so Studio can connect over
  USB-UART (see §9).

> **Studio is experimental.** The **Git-tracked `config/corne.keymap` is the
> canonical keymap.** Studio edits persist to on-device settings and can diverge
> from the file; if a Studio edit or persisted setting misbehaves, flash the
> **`settings-reset`** artifact to recover (it clears settings and Bluetooth
> bonds).

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

## 11. Safe editing & flashing guidance

1. **Edit the keymap** in `config/corne.keymap` (or via the Keymap Editor / ZMK
   Studio). Keep a copy of the last-known-good keymap before changing it. The
   Git-tracked file is canonical; Studio edits are experimental overlays.
2. **Build** by pushing/running GitHub Actions; download the `.uf2` artifacts
   (`corne-left`, `corne-right`) from the Actions run.
3. **Flash** each half:
   - Put the half into bootloader mode (double-tap the reset button, or use the
     `bootloader` key on the ADJUST layer), then copy the matching `.uf2` onto
     the mounted `NICENANO` drive.
   - Alternatively, use **ZMK Studio** (left half) for live edits without
     reflashing — note Studio changes persist to settings, so use the
     `settings-reset` artifact if you need a clean slate.
4. **Recover** with `settings-reset` if settings or a Studio edit misbehave, or
   after a layer renumbering migration (it also clears Bluetooth bonds).

---

## 12. Accuracy caveat — check the source

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

## 13. Corne HOST → AeroSpace integration (implemented)

The HOST layer (7) is **implemented in firmware** and bridges to macOS
AeroSpace. It emits `F13`–`F20` and `Option+H/J/K/L` from the BASE physical
H/J/K/L positions; AeroSpace binds those keys directly (see
[docs/macos-aerospace.md](macos-aerospace.md)). No `Alt-1`-style
intermediate mapping is used on the Corne side — the keyboard sends the F-keys
and AeroSpace binds them directly.
