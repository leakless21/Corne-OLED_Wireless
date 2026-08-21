# Daily Usage & Development Workflow

> **Scope.** This guide covers day-to-day keyboard use (layers, Bluetooth,
> ZMK Studio) and the edit/build/test workflow for firmware changes. For
> initial setup, first flash, and recovery procedures, see
> [docs/setup.md](setup.md). For the full keymap and layer reference, see
> [docs/corne-keymaps.md](corne-keymaps.md).

---

## 1. Daily keyboard use

### BASE layer (Colemak-DH)

The default layer is **Colemak-DH** (see `config/corne.keymap` BASE bindings).
Your base typing, punctuation, and modifier keys live here. Home-row letter
keys (`A R S T` / `N E I O`) are hold-tap modifiers — tap sends the letter,
hold engages a modifier when a key on the opposite hand is pressed.

### Layer-tap behavior (thumbs)

The six thumb keys (three per side) are **layer-taps** (`&lt`). Each key has two
actions:

- **Tap** (quick press) sends the printed base key.
- **Hold** (past the 220 ms tapping term) activates the named layer for as
  long as the key is held.

The thumb layer-tap mappings, sourced from `config/corne.keymap` BASE:

| Thumb key | Tap sends | Hold activates |
|-----------|-----------|----------------|
| Left outer thumb | `ESCAPE` | MEDIA layer |
| Left middle thumb | `SPACE` | NAV layer |
| Left inner thumb | `TAB` | MOUSE layer |
| Right inner thumb | `ENTER` | SYM layer |
| Right middle thumb | `BACKSPACE` | NUM layer |
| Right outer thumb | `DELETE` | FUN layer |

Each layer is **momentary** — it deactivates when you release the thumb key.

### Layer table

| Layer | How to reach | What it provides |
|-------|-------------|------------------|
| **NAV** | Hold left-space thumb | macOS Cmd clipboard chords (Cmd+C/V/X/Z), arrows, text navigation, Caps Lock. Also contains `&to L_GAME` to switch to GAME. |
| **MOUSE** | Hold left-tab thumb | Left-hand GUI/Alt/Ctrl/Shift modifiers; right-hand scroll, mouse buttons, and pointer movement. |
| **MEDIA** | Hold left-escape thumb | Volume up/down, play/pause, next/prev track, stop, mute. |
| **NUM** | Hold right-backspace thumb | Numpad digits and punctuation on the left, with right-hand GUI/Alt/Ctrl/Shift modifiers. |
| **SYM** | Hold right-enter thumb | Symbols: ampersand, asterisk, braces, brackets, parentheses, dollar, percent, caret, at, hash, pipe, tilde, exclamation, colon, slash, backslash, less/greater than. |
| **FUN** | Hold right-delete thumb | F1–F12 on the left, with right-hand GUI/Alt/Ctrl/Shift modifiers. |
| **HOST** | Hold BASE outer ESC + BACKSPACE combo (80 ms timeout; slow release) | AeroSpace bridge: F13–F20, Shift-F13–F17, and spatial Option+H/J/K/L focus/move controls. See [docs/macos-aerospace.md](macos-aerospace.md). |
| **GAME** | From NAV, press `&to L_GAME` | Tap-only QWERTY for gaming. Exit via right-thumb `&to L_BASE`. |
| **ADJUST** | Hold NAV + NUM simultaneously (conditional layer) | Five Bluetooth profiles, next/previous profile, selected-profile clear, explicit USB/BLE output, explicit external-power ON/OFF, mirrored reset/bootloader. |

> **Verify, don't assume.** The exact key positions for every layer live in
> `config/corne.keymap`. This table summarizes intent; always open that file
> to confirm a specific binding.

---

## 2. Bluetooth & device use

### Pairing profile selection

ZMK provides five Bluetooth profiles by default. ADJUST exposes `BT_SEL 0`
through `BT_SEL 4`; `BT_NXT` and `BT_PRV` cycle through the profiles. Hold NAV +
NUM and press the corresponding binding to switch hosts or begin pairing on an
unused profile.

### Clearing bonds

`BT_CLR` removes the bond only from the currently selected profile. After using
it, forget/remove the keyboard from that host before pairing again; otherwise
the host may retain the old security key and fail authentication. `BT_CLR_ALL`
clears every profile but is intentionally not bound in this keymap.

### Re-pairing

After clearing a bond or after first setup, use the pairing procedure in
[docs/setup.md section 7](setup.md#7-bluetooth-re-pairing).

---

## 3. ZMK Studio (day-to-day caveat)

ZMK Studio is enabled (`CONFIG_ZMK_STUDIO=y`) and allows live keymap editing
over USB-UART on the left half without reflashing.

**Workflow guidance:**

- Use Studio for **quick experiments** — try a remap, test it, iterate.
- Studio edits persist to **on-device settings**, not to the Git-tracked
  `config/corne.keymap`. The device state and the Git source can diverge.
- **Durable changes** should be made in `config/corne.keymap` (or via the
  visual [Keymap Editor](https://nickcoutsos.github.io/keymap-editor/)) and
  committed. That way the keymap is version-controlled and reproducible.
- If Studio edits cause unexpected behavior, see
  [docs/setup.md section 6](setup.md#6-recovery--settings-reset) for the
  settings-reset recovery procedure.

---

## 4. Firmware change workflow

This is the documented workflow for iterating on the keymap or firmware
configuration. Local builds are **outside this repo's documented workflow** —
use GitHub Actions instead.

### Step-by-step

1. **Edit the canonical source.** Modify `config/corne.keymap` directly, or
   use the visual [Keymap Editor](https://nickcoutsos.github.io/keymap-editor/)
   to produce changes against this repo's keymap.

2. **Review and back up.** Check your diff before pushing. If you are making
   structural changes (adding/removing layers, renumbering layer indices),
   commit the current known-good state first so you can roll back via Git.

3. **Push a branch or open a PR.** The GitHub Actions workflow triggers on
   push. Each push builds three `.uf2` firmware images: `corne-left`,
   `corne-right`, and `settings-reset`. The upstream reusable workflow merges
   them into a single `firmware` archive (`.zip`) for download.

4. **Wait for the build.** Check the Actions tab — a green checkmark means
   the build succeeded.

5. **Download the `firmware` archive.** Extract the `.uf2` files from the
   downloaded `.zip`.

6. **Flash both halves.** For any keymap, config, or behavior change, flash
   **both** `corne-left.uf2` and `corne-right.uf2`. Both targets are
   generated from the same repo config. Do **not** use `settings-reset` for
   normal updates — it is a recovery tool that erases persisted settings and
   must be followed by re-flashing the normal firmware. See
   [docs/setup.md section 5](setup.md#5-first-flash-of-both-halves) for
   flashing instructions.

7. **Smoke-test.** Verify the change works (see checklist below).

8. **Merge.** After validation, merge the branch.

> **Workflow guidance.** This workflow is how this repo is designed to be
> used. It is not a prescriptive policy — adjust to your preferences, but
> expect the documented paths to work.

---

## 5. Smoke-test checklist

After flashing a firmware change, run through this compact checklist:

- [ ] **Base typing** — type a few sentences on the BASE layer. Confirm
  Colemak-DH letters, punctuation, and outer modifiers work as expected.
- [ ] **Each changed layer-tap** — for every thumb key you modified, test both
  the tap (quick press) and hold (press and hold past 220 ms) actions.
- [ ] **Bluetooth profile switching** — on ADJUST (hold NAV + NUM), cycle through
  `BT_SEL 0`–`BT_SEL 4` or use `BT_NXT`/`BT_PRV`; confirm the expected host
  reconnects.
- [ ] **HOST / AeroSpace** — hold the BASE outer ESC + BACKSPACE combo, then
  test F13–F20, Shift-F13–F17, and both spatial H/J/K/L clusters.
- [ ] **GAME** (if applicable) — from NAV, press `&to L_GAME`. Confirm QWERTY
  layout is active. Exit via the right-thumb `&to L_BASE`.
- [ ] **OLED and power** — confirm the status screen renders on both halves,
  blanks after idle, and wakes; characterize deep-sleep reconnect behavior.
- [ ] **Recovery path** — confirm the left and right ADJUST bootloader/reset
  bindings affect the intended half; keep double-reset and settings-reset as
  fallbacks.

---

## 6. AeroSpace-only workflow note

The canonical AeroSpace configuration is tracked at
`dotfiles/aerospace.toml`. Install it at
`~/.config/aerospace/aerospace.toml` by copying or symlinking it; see
[docs/macos-aerospace.md](macos-aerospace.md). Editing that config does **not**
require a firmware rebuild or flash.

- Validate with `aerospace reload-config --dry-run`, then apply with
  `aerospace reload-config`.
- The Corne HOST layer emits F13–F20, Shift-F13–F17, and Option+H/J/K/L.
  AeroSpace maps those signals directly; no Colemak remapping is needed on the
  MacBook keyboard.

See [docs/macos-aerospace.md](macos-aerospace.md) for installation,
workspace layout, routing, and troubleshooting.

---

## 7. Decision table: which action to take

| Situation | Action | Reference |
|-----------|--------|-----------|
| Normal keymap/config change | Edit `config/corne.keymap`, push, flash both halves with `corne-left.uf2` and `corne-right.uf2`. | [docs/setup.md section 5](setup.md#5-first-flash-of-both-halves) |
| Layer renumber or state mismatch | Flash `settings-reset` on both halves, re-flash the normal images, then re-pair Bluetooth. | [docs/setup.md section 6](setup.md#6-recovery--settings-reset) |
| Bluetooth failure or won't pair | Flash `settings-reset` on both halves, re-flash normal firmware, then re-pair. | [docs/setup.md section 7](setup.md#7-bluetooth-re-pairing) |
| Studio edits caused divergence | Flash `settings-reset` to clear on-device overrides, re-flash normal firmware. | [docs/setup.md section 8](setup.md#8-zmk-studio-caveats) |
| AeroSpace bindings not working | Validate or edit `dotfiles/aerospace.toml`, install/reload the user config. No firmware change needed. | [docs/macos-aerospace.md](macos-aerospace.md) |
