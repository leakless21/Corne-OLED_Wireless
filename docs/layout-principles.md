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

## Shared semantic invariants

- BASE remains Colemak-DH with bilateral home-row modifiers.
- Physical `A R S T` positions (`LM4`–`LM1`) mean `Cmd Alt Ctrl Shift` on
  functional layers that expose left modifiers.
- Physical `N E I O` positions (`RM1`–`RM4`) mean `Shift Ctrl Alt Cmd` on
  functional layers that expose right modifiers.
- Physical `N E I O` positions mean `← ↓ ↑ →` on directional layers.
- The same columns on the bottom row are the secondary directional bank.
- A left-thumb-held layer places its main actions on the right hand and its
  modifiers on the left. A right-thumb-held layer does the inverse.
- NUM, SYM, and FUN share one left-hand physical grid. SYM is NUM's shifted
  counterpart; FUN is its function-key counterpart.
- NAV, MOUSE, and MEDIA share one right-hand navigation geometry.
- Thumb bindings on functional layers are explicit single actions. They MUST
  NOT use transparent fall-through when that would inherit BASE layer-taps.
- Unused positions are `&none`. `&trans` is reserved for intentional fall-through
  documented beside the binding.
- HOST emits semantic high-function-key signals. Host configuration decides
  whether those signals mean AeroSpace, GlazeWM, or another window manager.
- ADJUST is the only layer for destructive or device-management actions.

## Layer grammar

| Layer | Left-hand role | Right-hand role | Explicit thumb role |
| --- | --- | --- | --- |
| BASE | Colemak-DH and HRMs | Colemak-DH and HRMs | Six layer-taps |
| NAV | Cmd/Alt/Ctrl/Shift | Clipboard, cursor, line/page navigation | Esc/Space/Tab and Enter/Bspc/Delete |
| MOUSE | Cmd/Alt/Ctrl/Shift | Clipboard, pointer, scroll, buttons | Right/left/middle click |
| MEDIA | Cmd/Alt/Ctrl/Shift | Prev, volume, next | Stop/play/mute |
| NUM | Numpad geometry | Shift/Ctrl/Alt/Cmd | `.`, `0`, `-` |
| SYM | Shifted NUM geometry | Shift/Ctrl/Alt/Cmd | `(`, `)`, `_` |
| FUN | F-key geometry | Shift/Ctrl/Alt/Cmd | App, Space, Tab |
| HOST | Workspace and move-to-workspace signals | Directional and window signals | Resize entry/exit and context actions |
| GAME | Plain tap-only QWERTY | Plain tap-only QWERTY | Ctrl/Alt/Space and Enter/RCtrl/Base |
| ADJUST | Device administration | Device administration | Device administration |

## HOST protocol

The firmware protocol is intentionally independent of macOS key choices:

| Signal | Meaning in the reference AeroSpace adapter |
| --- | --- |
| `F13`–`F17` | Focus WEB/DEV/COMMS/RUN/AUX |
| `Shift+F13`–`Shift+F17` | Move the window to WEB/DEV/COMMS/RUN/AUX and follow |
| `Ctrl+F13`–`Ctrl+F16` | Focus left/down/up/right |
| `Ctrl+Shift+F13`–`Ctrl+Shift+F16` | Move the window left/down/up/right |
| `Shift+F18` | Enter resize mode |
| `F18` | Previous workspace |
| `F19` | Fullscreen |
| `F20` | Toggle floating/tiling |

In AeroSpace resize mode, the same `Ctrl+F13`–`Ctrl+F16` direction signals are
interpreted as resize commands. A Windows adapter may assign the same semantic
signals to GlazeWM without changing firmware.

## Change control

Before changing a shared layer family:

1. Update this contract and the affected source comments.
2. Regenerate `keymap-drawer/corne.yaml` and `keymap-drawer/corne.svg`.
3. Build both firmware halves.
4. Exercise the changed layer and every relevant modifier/direction boundary.
5. Freeze the layout until physical use provides evidence for another change.
