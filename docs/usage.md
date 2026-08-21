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
| **NAV** | Hold left-space thumb | macOS Cmd clipboard chords (Cmd+C/V/X/Z), arrows, Home/End/PgUp/PgDn, Caps Lock. Also contains `&to L_GAME` to switch to GAME layer. |
| **MOUSE** | Hold left-tab thumb | Pointer control: mouse movement, scroll (up/down/left/right), mouse buttons 1-5 and middle-click. Pointing is enabled via `CONFIG_ZMK_POINTING=y`. |
| **MEDIA** | Hold left-escape thumb | Volume up/down, play/pause, next/prev track, stop, mute. |
| **NUM** | Hold right-backspace thumb | Numpad digits 0-9, brackets, minus, period, grave, backslash, equal. |
| **SYM** | Hold right-enter thumb | Symbols: ampersand, asterisk, braces, brackets, parentheses, dollar, percent, caret, at, hash, pipe, tilde, exclamation, colon, slash, backslash, less/greater than. |
| **FUN** | Hold right-delete thumb | Function keys F1-F12. |
| **HOST** | Hold BASE outer ESC + BACKSPACE combo (80 ms timeout) | AeroSpace bridge: emits F13-F20 and Option+H/J/K/L for macOS workspace switching. See [docs/macos-aerospace.md](macos-aerospace.md). |
| **GAME** | From NAV, press `&to L_GAME` | Tap-only QWERTY for gaming. Exit via right-thumb `&to L_BASE`. |
| **ADJUST** | Hold NAV + NUM simultaneously (conditional layer) | Bluetooth profile select (0-3), clear bonds, output toggle, external power toggle, bootloader, reset. Destructive actions kept out of daily layers. |

> **Verify, don't assume.** The exact key positions for every layer live in
> `config/corne.keymap`. This table summarizes intent; always open that file
> to confirm a specific binding.

---

## 2. Bluetooth & device use

### Pairing profile selection

The ADJUST layer provides `&bt BT_SEL 0` through `&bt BT_SEL 3` — four
Bluetooth profiles. Hold NAV + NUM and press the corresponding key to switch
to a profile. The keyboard can remember four paired hosts.

### Clearing bonds

Hold NAV + NUM and press `&bt BT_CLR`. This removes all stored Bluetooth
pairings from the keyboard's settings. You will need to re-pair with your
host device after clearing.

### Re-pairing

After clearing bonds or on first setup, put the keyboard into pairing mode
(see [docs/setup.md section 7](setup.md#7-bluetooth-re-pairing) for the
first-time pairing procedure and recovery steps).

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
  Colemak-DH letters, punctuation, and outer modifiers (Shift, Ctrl, etc.)
  work as expected.
- [ ] **Each changed layer-tap** — for every thumb key you modified, test
  both the tap (quick press) and hold (press and hold past 220 ms) actions.
- [ ] **Bluetooth profile switching** — on ADJUST (hold NAV + NUM), cycle
  through `BT_SEL 0`-`BT_SEL 3` and confirm the keyboard reconnects to the
  expected host on each profile.
- [ ] **HOST / AeroSpace** (if applicable) — hold the BASE outer ESC +
  BACKSPACE combo to enter HOST, then press F13-F20 and confirm AeroSpace
  responds. See [docs/macos-aerospace.md](macos-aerospace.md).
- [ ] **GAME** (if applicable) — from NAV, press `&to L_GAME`. Confirm
  QWERTY layout is active. Exit via the right-thumb `&to L_BASE`.
- [ ] **OLED** — confirm the status screen renders on both halves (layer
  name, battery indicator).
- [ ] **Recovery path** — if anything is wrong, you can flash
  `settings-reset.uf2` to erase persisted settings, then re-flash the normal
  firmware and re-pair Bluetooth. See
  [docs/setup.md section 6](setup.md#6-recovery--settings-reset).

---

## 6. AeroSpace-only workflow note

Changes to the AeroSpace configuration (`~/.config/aerospace/aerospace.toml`)
are **entirely separate** from firmware. Editing that file does **not** require
a firmware rebuild or flash.

- Edit `~/.config/aerospace/aerospace.toml` directly.
- Validate with `aerospace reload-config --dry-run`, then apply with
  `aerospace reload-config`.
- The Corne HOST layer (F13-F20, Option+H/J/K/L) bridges to AeroSpace
  automatically — no firmware changes needed when adjusting bindings.

See [docs/macos-aerospace.md](macos-aerospace.md) for the full AeroSpace
guide, including installation, workspace layout, and troubleshooting.

---

## 7. Decision table: which action to take

| Situation | Action | Reference |
|-----------|--------|-----------|
| Normal keymap/config change | Edit `config/corne.keymap`, push, flash both halves with `corne-left.uf2` and `corne-right.uf2`. | [docs/setup.md section 5](setup.md#5-first-flash-of-both-halves) |
| Layer renumber or state mismatch | Flash `settings-reset` on both halves, re-flash the normal images, then re-pair Bluetooth. | [docs/setup.md section 6](setup.md#6-recovery--settings-reset) |
| Bluetooth failure or won't pair | Flash `settings-reset` on both halves, re-flash normal firmware, then re-pair. | [docs/setup.md section 7](setup.md#7-bluetooth-re-pairing) |
| Studio edits caused divergence | Flash `settings-reset` to clear on-device overrides, re-flash normal firmware. | [docs/setup.md section 8](setup.md#8-zmk-studio-caveats) |
| AeroSpace bindings not working | Edit `~/.config/aerospace/aerospace.toml`, reload config. No firmware change needed. | [docs/macos-aerospace.md](macos-aerospace.md) |
