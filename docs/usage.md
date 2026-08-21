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

| Thumb key | Tap sends | Hold activates |
|-----------|-----------|----------------|
| Left outer thumb (`LH2`) | `ESCAPE` | MOUSE layer (`&lt`) |
| Left middle thumb (`LH1`) | `SPACE` | NAV layer (`&lt`) |
| Left inner thumb (`LH0`) | `TAB` | HOST layer (`&host_lt`, 200 ms balanced) |
| Right inner thumb (`RH0`) | `ENTER` | SYM layer (`&lt`) |
| Right middle thumb (`RH1`) | `BACKSPACE` | NUM layer (`&lt`) |
| Right outer thumb (`RH2`) | `DELETE` | FUN layer (`&lt`) |

Each thumb layer is **momentary** — it deactivates when you release the thumb key.
In addition, the outer-left home position (`LM5`) is a direct momentary hold for
the **MEDIA** layer (`&mo L_MEDIA`).

### Layer table

| Layer | How to reach | What it provides |
|-------|-------------|------------------|
| **NAV** | Hold left-space thumb (`LH1`) | macOS Cmd clipboard chords, Caps Lock, arrows, text navigation, line/page movement, and explicit editing thumbs. |
| **HOST** | Hold left-tab thumb (`LH0`) | Host-agnostic F13–F20 workspace signals (home row), move-to-workspace (top row), directional focus/move, and context thumbs. See [docs/macos-aerospace.md](macos-aerospace.md). |
| **MOUSE** | Hold left-escape thumb (`LH2`) | NAV-aligned clipboard, pointer movement, wheel movement, left modifiers, and MB4 (Back) / MB5 (Forward) side buttons. |
| **MEDIA** | Hold outer-left home key (`LM5`) | NAV-aligned previous/volume/next controls with right-thumb stop/play/mute controls. |
| **NUM** | Hold right-backspace thumb (`RH1`) | Standard spatial numpad and punctuation on the left; Shift/Ctrl/Alt/Cmd on the right. |
| **SYM** | Hold right-enter thumb (`RH0`) | Shifted NUM geometry with `(`, `)`, and `_` on the left thumbs. |
| **FUN** | Hold right-delete thumb (`RH2`) | NUM-aligned F1–F12 grid with mirrored modifiers and App/Space/Tab thumbs. |
| **GAME** | Hold NAV + NUM, then press GAME in ADJUST | Full plain tap-only QWERTY for gaming; hold RH1 for numbers. Exit via right outer `&to L_BASE`. |
| **GAME_NUM** | Hold right-middle thumb (`RH1`) while in GAME | Momentary top-row numbers 1–0 over tap-only QWERTY. |
| **ADJUST** | Hold NAV + NUM simultaneously | Five Bluetooth profiles in core (`LM4`–`LM0`), output/power state, mirrored reset/bootloader, and deliberate GAME entry. |
> **Verify, don't assume.** Exact positions live in `config/corne.keymap`;
> shared physical rules are recorded in [layout-principles.md](layout-principles.md).

### Daily HOST & AeroSpace workflow

HOST is entered directly by holding the **Tab thumb (`LH0`)**. Its controls are
organized strictly by usage frequency:

1. **Visit workspace (most frequent)**: Hold `Tab` + press home-row key (`A`/`R`/`S`/`T`/`G` columns → `WEB`, `DEV`, `COMMS`, `RUN`, `AUX`).
2. **Focus adjacent window**: Hold `Tab` + press right home direction (`N`/`E`/`I`/`O` columns → Focus `←`, `↓`, `↑`, `→`).
3. **Previous workspace**: Hold `Tab` + tap right middle thumb (`RH1` → Previous WS).
4. **Move window to workspace**: Hold `Tab` + press top-row key (`Q`/`W`/`F`/`P`/`B` columns → Move to `WEB`, `DEV`, `COMMS`, `RUN`, `AUX` and follow).
5. **Move window directionally**: Hold `Tab` + press right bottom direction (`K`/`H`/`,`/`.` columns → Move `←`, `↓`, `↑`, `→`).
6. **Context actions**: Hold `Tab` + right inner thumb `RH0` (Fullscreen), right outer thumb `RH2` (Float/tile), right top `RT1` (Resize mode), or `RT5` (Esc).

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
over USB-UART on the left half.

**Workflow guidance:**

- Use Studio for quick experiments. Studio edits persist to on-device settings,
  not to the Git-tracked `config/corne.keymap`.
- **Restore Stock Settings** is the normal way to discard Studio overrides and
  return to the firmware-defined keymap without clearing Bluetooth bonds.
- Durable changes belong in `config/corne.keymap` and should be committed.
- Use `settings-reset` only as a destructive fallback for broken persistent
  state, split/Bluetooth recovery, or an intentional full reset.
- `OUT_USB` with a charger-only cable can make the keyboard appear unresponsive.
  `EP_OFF` persists across reboot and can leave peripherals/displays unpowered.

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

3. **Push a branch or open a PR.** Firmware input changes (`config/**`,
   `build.yaml`, board/shield sources, or the build workflow) trigger the
   GitHub Actions build. Documentation-only changes do not. Manual dispatch is
   also available. Each run builds three `.uf2` firmware images:
   `corne-left`, `corne-right`, and `settings-reset`. The upstream reusable
   workflow merges them into a single `firmware` archive (`.zip`).

4. **Wait for the build.** Check the Actions tab — a green checkmark means
   the firmware build succeeded.

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

- [ ] **Base typing** — type a few sentences on BASE. Confirm Colemak-DH,
  punctuation, and home-row modifiers.
- [ ] **Functional grammar** — verify A/R/S/T and N/E/I/O modifier positions
  across NAV, MOUSE, MEDIA, NUM, SYM, and FUN.
- [ ] **NUM/SYM/FUN** — confirm the 7-8-9 / 4-5-6 / 1-2-3 geometry, shifted
  symbols, F-grid, and explicit thumb taps.
- [ ] **NAV/MOUSE/MEDIA** — confirm directions occupy the same N/E/I/O
  columns; NAV has Caps Lock at RM0 and Insert/Home/PgDn/PgUp/End at RB0–RB4;
  MOUSE has MB4 (Back) at RM0 and MB5 (Forward) at RM5; MEDIA is engaged via
  holding LM5 with transport controls on right thumbs only.
- [ ] **Bluetooth profile switching** — on ADJUST, cycle `BT_SEL 0`–`BT_SEL 4`
  in the five-column core (`LM4`–`LM0`) or use `BT_NXT`/`BT_PRV`; confirm host reconnects.
- [ ] **HOST / AeroSpace** — hold the left `Tab` thumb (`LH0`), then test
  home-row workspace focus (F13–F17), top-row move-to-workspace (Shift-F13–F17),
  right-home focus (Ctrl-F13–F16), right-bottom move (Ctrl-Shift-F13–F16),
  right-thumb Previous WS (F18), Fullscreen (F19), Float (F20), and Resize (Shift-F18).
- [ ] **GAME & GAME_NUM** — enter GAME from ADJUST; confirm full QWERTY with
  Space on LH1; hold RH1 to test numbers 1–0 on top alpha row; exit via right outer `&to L_BASE`.
- [ ] **OLED and power** — confirm the status screen renders on both halves,
  blanks after idle, and wakes; characterize deep-sleep reconnect behavior.
- [ ] **Recovery path** — confirm left/right ADJUST bootloader/reset bindings
  affect the intended half; use Studio Restore Stock Settings before
  `settings-reset`.

---

## 6. AeroSpace-only workflow note

The canonical AeroSpace configuration is tracked at
`dotfiles/aerospace.toml`. Install it at
`~/.config/aerospace/aerospace.toml` by copying or symlinking it.

- Validate with `aerospace reload-config --dry-run`, then apply with
  `aerospace reload-config`.
- The Corne HOST layer emits F13–F20, Shift-F13–F17, Ctrl+F13–F16, and
  Ctrl+Shift+F13–F16. AeroSpace maps those semantic signals directly.
- The laptop keyboard remains standard QWERTY with its separate Option
  bindings. No Colemak remapping is needed on the MacBook.
See [docs/macos-aerospace.md](macos-aerospace.md) for installation,
workspace layout, routing, and troubleshooting.

---

## 7. Decision table: which action to take

| Situation | Action | Reference |
|-----------|--------|-----------|
| Normal keymap/config change | Edit `config/corne.keymap`, push, flash both halves with `corne-left.uf2` and `corne-right.uf2`. | [docs/setup.md section 5](setup.md#5-first-flash-of-both-halves) |
| Layer renumber or state mismatch | Flash `settings-reset` on both halves, re-flash the normal images, then re-pair Bluetooth. | [docs/setup.md section 6](setup.md#6-recovery--settings-reset) |
| Bluetooth failure or won't pair | Flash `settings-reset` on both halves, re-flash normal firmware, then re-pair. | [docs/setup.md section 7](setup.md#7-bluetooth-re-pairing) |
| Studio edits caused divergence | Use Studio **Restore Stock Settings** first; use `settings-reset` only if that fails or a full reset is intended. | [docs/setup.md section 8](setup.md#8-zmk-studio-caveats) |
| AeroSpace bindings not working | Validate or edit `dotfiles/aerospace.toml`, install/reload the user config. No firmware change needed. | [docs/macos-aerospace.md](macos-aerospace.md) |
