# Corne Layout Principles

This document is the physical contract for `config/corne.keymap`. A layer may
change the meaning of a key, but it MUST NOT move a shared semantic family to a
new physical column without an explicit layout decision and updated diagrams.

## Physical positions

The Corne matrix is written left-to-right as six keys per half, followed by the
three left and three right thumb keys:

```text
LT5 LT4 LT3 LT2 LT1 LT0 | RT0 RT1 RT2 RT3 RT4 RT5
LM5 LM4 LM3 LM2 LM1 LM0 | RM0 RM1 RM2 RM3 RM4 RM5
LB5 LB4 LB3 LB2 LB1 LB0 | RB0 RB1 RB2 RB3 RB4 RB5
              LH2 LH1 LH0 | RH0 RH1 RH2
```

The `42.h` helper defines these names. Position-based behavior configuration
MUST use those names rather than hand-counted numeric positions.

The five-column functional core is the inner five positions of each half:

```text
left:  LT4 LT3 LT2 LT1 LT0 | right: RT0 RT1 RT2 RT3 RT4
       LM4 LM3 LM2 LM1 LM0 |        RM0 RM1 RM2 RM3 RM4
       LB4 LB3 LB2 LB1 LB0 |        RB0 RB1 RB2 RB3 RB4
```

The outer sixth positions (`LT5`, `RT5`, and their row equivalents) are extras;
they MUST NOT shift a five-column family sideways.

## Functional thumb priority & frequency

The left-thumb cluster follows strict usage-frequency hierarchy:

```text
Left-thumb functional priority:
NAV > HOST > MOUSE

MEDIA is lower-frequency and uses the Corne's sixth-column extra key (LM5).
```

BASE thumb roles:

```text
LH2 (left outer):   tap Esc        hold MOUSE
LH1 (left middle):  tap Space      hold NAV
LH0 (left inner):   tap Tab        hold HOST

RH0 (right inner):  tap Enter      hold SYM
RH1 (right middle): tap Backspace  hold NUM
RH2 (right outer):  tap Delete     hold FUN
```
## Shared semantic invariants

- BASE remains Colemak-DH with bilateral home-row modifiers.
- Outer-left home position (`LM5`) is a direct momentary hold for MEDIA (`&mo L_MEDIA`).
- Physical `A R S T` positions (`LM4`–`LM1`) mean `Cmd Alt Ctrl Shift` on
  functional layers that expose left modifiers.
- Physical `N E I O` positions (`RM1`–`RM4`) mean `Shift Ctrl Alt Cmd` on
  functional layers that expose right modifiers.
- Physical `N E I O` positions mean `← ↓ ↑ →` on directional layers (NAV, MOUSE, HOST).
- The same columns on the bottom row (`RB1`–`RB4`) are the aligned secondary directional bank.
- A left-thumb-held layer places its main actions on the right hand and its
  modifiers on the left. A right-thumb-held layer does the inverse.
- HOST preserves spatial semantics: home row (`LM4`–`LM0`) visits workspaces; top
  row (`LT4`–`LT0`) mirrors it one row above to move the focused window there.
- NUM, SYM, and FUN share one left-hand physical grid. SYM is NUM's shifted
  counterpart; FUN is its function-key counterpart.
- NAV, MOUSE, and MEDIA share one right-hand navigation geometry.
- Thumb bindings on functional layers are explicit single actions. They MUST
  NOT use transparent fall-through when that would inherit BASE layer-taps.
- Unused positions are `&none`. `&trans` is reserved for intentional fall-through
  documented beside the binding (e.g. GAME_AUX falling through to GAME).
- Same-side bootloader access: `NAV` carries the left controller bootloader at `LT5`;
  `NUM` carries the right controller bootloader at `RT5`. `ADJUST` retains mirrored fallback controls.
- HOST emits semantic high-function-key signals (F13–F20). Host configuration decides
  whether those signals mean AeroSpace, GlazeWM, or another window manager.
- NAV and MOUSE emit semantic high-function-key signals (F21–F24) for editing actions
  (Copy, Paste, Cut, Undo, Redo). Host bridges translate them to native OS shortcuts.
- ADJUST is the only layer for destructive or device-management actions; Bluetooth
  profiles occupy the five-column core (`LM4`–`LM0`).

| Layer | Left-hand role | Right-hand role | Explicit thumb role |
| --- | --- | --- | --- |
| BASE | Colemak-DH and HRMs; LM5 holds MEDIA | Colemak-DH and HRMs | Six layer-taps (MOUSE, NAV, HOST, SYM, NUM, FUN) |
| NAV | Cmd/Alt/Ctrl/Shift; `LT5` left bootloader | Caps Lock, semantic editing (F21–F24), cursor, line/page | Esc/Space/Tab and Enter/Bspc/Delete |
| MOUSE | Cmd/Alt/Ctrl/Shift | MB4 (Back), MB5 (Fwd), semantic editing (F21–F24), pointer, scroll | Right/left/middle click |
| MEDIA | Cmd/Alt/Ctrl/Shift | Consumer HID prev, volume, next | Stop/play/pause/mute (right thumbs only) |
| NUM | Numpad geometry | Shift/Ctrl/Alt/Cmd; `RT5` right bootloader | `.`, `0`, `-` |
| SYM | Shifted NUM geometry | Shift/Ctrl/Alt/Cmd | `(`, `)`, `_` |
| FUN | F-key geometry | Shift/Ctrl/Alt/Cmd | App, Space, Tab |
| HOST | Workspace focus (home) & move (top) | Directional focus (home) & move (bottom) | Fullscreen, Previous WS, Float (right thumbs) |
| GAME | Plain tap-only QWERTY; `LT5` Esc/AUX hold-tap | Plain tap-only QWERTY | Ctrl/Space/Alt and Enter/AUX/transparent |
| GAME_AUX | Numbers 1–5, F1–F5, symbols (`` ` ``, `-`, `=`, `[`, `]`) | Numbers 6–0, F6–F10 | Fall-through to GAME, RH2 exits to BASE |
| ADJUST | Bluetooth in core (`LM4`–`LM0`), power/reset | Output/power/reset/GAME entry | None |

## Host-independent firmware & semantic protocol

The firmware maintains a strict separation between portable HID behaviors and host-dependent behaviors:

1. **Standard portable HID behaviors stay in firmware:**
   - Letters, numbers, symbols, standard modifiers.
   - Arrow keys, Home/End, Page Up/Down, Insert/Delete.
   - Mouse movement, wheel scrolling, buttons.
   - Function keys F1–F12.
   - Gaming keys.
   - Portable Consumer-page media controls (`C_PREVIOUS`, `C_VOLUME_DOWN`, `C_VOLUME_UP`, `C_NEXT`, `C_PLAY_PAUSE`, `C_MUTE`, `C_STOP`).

2. **OS-specific desktop shortcuts do not live in firmware:**
   - Firmware emits high-function-key semantic signals (`F13`–`F24`).
   - macOS and Windows translate those signals locally through host bridges (Karabiner-Elements, AutoHotkey, AeroSpace, GlazeWM).
   - Internal laptop keyboards remain completely conventional and untouched.

3. **Consumer Application Control (`C_AC_*`) warning:**
   - Although USB HID defines Consumer / Application Control usages such as `C_AC_COPY`, `C_AC_PASTE`, `C_AC_CUT`, `C_AC_UNDO`, and `C_AC_REDO` (and Keyboard-page equivalents like `K_COPY`), current OS implementations (Windows and macOS) do not provide reliable, consistent desktop-wide support.
   - The firmware explicitly avoids `C_AC_*` and `K_*` editing codes in favor of the host-bridge protocol (`F21`–`F24`).

### Protocol specification

| Signal | Semantic Action | macOS Reference (AeroSpace / Karabiner) | Windows Reference (AutoHotkey / GlazeWM) |
| --- | --- | --- | --- |
| `F13`–`F17` | Workspace focus (1–5) | Focus WEB/DEV/COMMS/RUN/AUX | Focus workspace 1–5 |
| `Shift+F13`–`Shift+F17` | Move window to workspace (1–5) | Move window to WEB..AUX and follow | Move window to workspace 1–5 |
| `Ctrl+F13`–`Ctrl+F16` | Directional focus (← ↓ ↑ →) | Focus left/down/up/right | Focus left/down/up/right |
| `Ctrl+Shift+F13`–`Ctrl+Shift+F16` | Directional window move | Move left/down/up/right | Move left/down/up/right |
| `Shift+F18` | Resize mode | Enter resize mode | Enter resize mode |
| `F18` | Previous workspace | Previous workspace | Previous workspace |
| `F19` | Fullscreen | Fullscreen toggle | Fullscreen toggle |
| `F20` | Float toggle | Floating/tiling toggle | Floating/tiling toggle |
| `F21` | Copy | `Command+C` | `Ctrl+C` |
| `F22` | Paste | `Command+V` | `Ctrl+V` |
| `F23` | Cut | `Command+X` | `Ctrl+X` |
| `F24` | Undo | `Command+Z` | `Ctrl+Z` |
| `Shift+F24` | Redo | `Command+Shift+Z` | `Ctrl+Y` |

In AeroSpace resize mode, the same `Ctrl+F13`–`Ctrl+F16` direction signals are
interpreted as resize commands.
## Change control

Before changing a shared layer family:

1. Update this contract and the affected source comments.
2. Regenerate `keymap-drawer/corne.yaml` and `keymap-drawer/corne.svg`.
3. Build both firmware halves.
4. Exercise the changed layer and every relevant modifier/direction boundary.
5. Freeze the layout until physical use provides evidence for another change.
