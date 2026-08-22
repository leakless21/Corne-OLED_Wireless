# Semantic Host Protocol Specification (F13–F24)

This document is the canonical source of truth for the semantic high-function key protocol (`F13`–`F24`) shared by all keyboards in this repository.

---

## 1. Canonical Protocol Matrix

| Signal | Semantic Action | macOS Host (Karabiner + AeroSpace + Ghostty + Spotlight) | Windows Host (GlazeWM + AutoHotkey + Windows Terminal + Search) |
|---|---|---|---|
| `F13` | Workspace slot 1 (WEB) | `workspace WEB` (`Alt+1`) | `focus --workspace 1` (`f13`) |
| `F14` | Workspace slot 2 (DEV) | `workspace DEV` (`Alt+2`) | `focus --workspace 2` (`f14`) |
| `F15` | Workspace slot 3 (COMMS) | `workspace COMMS` (`Alt+3`) | `focus --workspace 3` (`f15`) |
| `F16` | Workspace slot 4 (RUN) | `workspace RUN` (`Alt+4`) | `focus --workspace 4` (`f16`) |
| `F17` | Workspace slot 5 (AUX) | `workspace AUX` (`Alt+5`) | `focus --workspace 5` (`f17`) |
| `Shift+F13` | Move window to slot 1 + follow | `move-node-to-workspace WEB; workspace WEB` (`Alt+Shift+1`) | `move --workspace 1; focus --workspace 1` (`shift+f13`) |
| `Shift+F14` | Move window to slot 2 + follow | `move-node-to-workspace DEV; workspace DEV` (`Alt+Shift+2`) | `move --workspace 2; focus --workspace 2` (`shift+f14`) |
| `Shift+F15` | Move window to slot 3 + follow | `move-node-to-workspace COMMS; workspace COMMS` (`Alt+Shift+3`) | `move --workspace 3; focus --workspace 3` (`shift+f15`) |
| `Shift+F16` | Move window to slot 4 + follow | `move-node-to-workspace RUN; workspace RUN` (`Alt+Shift+4`) | `move --workspace 4; focus --workspace 4` (`shift+f16`) |
| `Shift+F17` | Move window to slot 5 + follow | `move-node-to-workspace AUX; workspace AUX` (`Alt+Shift+5`) | `move --workspace 5; focus --workspace 5` (`shift+f17`) |
| `Ctrl+F13` | Directional focus ← | `focus left` (`Alt+H`) | `focus left` (`ctrl+f13`) |
| `Ctrl+F14` | Directional focus ↓ | `focus down` (`Alt+J`) | `focus down` (`ctrl+f14`) |
| `Ctrl+F15` | Directional focus ↑ | `focus up` (`Alt+K`) | `focus up` (`ctrl+f15`) |
| `Ctrl+F16` | Directional focus → | `focus right` (`Alt+L`) | `focus right` (`ctrl+f16`) |
| `Ctrl+Shift+F13` | Directional move ← | `move left` (`Alt+Shift+H`) | `move left` (`ctrl+shift+f13`) |
| `Ctrl+Shift+F14` | Directional move ↓ | `move down` (`Alt+Shift+J`) | `move down` (`ctrl+shift+f14`) |
| `Ctrl+Shift+F15` | Directional move ↑ | `move up` (`Alt+Shift+K`) | `move up` (`ctrl+shift+f15`) |
| `Ctrl+Shift+F16` | Directional move → | `move right` (`Alt+Shift+L`) | `move right` (`ctrl+shift+f16`) |
| `F18` | Previous workspace | `workspace-back-and-forth` (`Alt+Tab`) | `focus --recent-workspace` (`f18`) |
| `Shift+F18` | Resize mode | `mode resize` (`Alt+R`) | `enable-binding-mode --name resize` (`shift+f18`) |
| `Alt+F18` | Service mode | `mode service` (`Alt+Shift+;`) | `enable-binding-mode --name service` (`alt+f18`) |
| `F19` | Fullscreen toggle | `fullscreen` (`Alt+F`) | `toggle-fullscreen` (`f19`) |
| `F20` | Float / tile toggle | `layout floating tiling` (`Alt+Shift+Space`) | `toggle-floating --centered` (`f20`) |
| `Alt+F13` | System launcher | Spotlight search (`Cmd+Space`) | Windows Search (`Win+S`) |
| `Alt+F14` | Quick terminal | Ghostty scratchpad toggle (`Ctrl+```) | Windows Terminal Quake toggle (`Ctrl+Alt+```) |
| `Alt+F15` | New terminal | New Ghostty window in workspace (`Alt+Enter`) | Launch `wt.exe` |
| `Alt+F16` | Previous window | `focus-back-and-forth` (`Alt+```) | `Alt+Tab` |
| `F21` | Copy | `Cmd+C` | `Ctrl+C` |
| `F22` | Paste | `Cmd+V` | `Ctrl+V` |
| `F23` | Cut | `Cmd+X` | `Ctrl+X` |
| `F24` | Undo | `Cmd+Z` | `Ctrl+Z` |
| `Shift+F24` | Redo | `Cmd+Shift+Z` | `Ctrl+Y` |

---

## 2. Protocol Producers

Both keyboards implement the full protocol:
1. **`config/corne.keymap`:** Emits `F13`–`F20` on `HOST`, `F21`–`F24` on `NAV` and `MOUSE`.
2. **`config/sofle.keymap`:** Emits `F13`–`F20` on `HOST`, `F21`–`F24` on `NAV` and `MOUSE`.

## 3. Protocol Consumers

1. **macOS Host Adapters:**
   - **`hosts/macos/karabiner.json`:** Device-scoped complex rules translating high-function keys to macOS chords.
   - **`hosts/macos/aerospace.toml`:** AeroSpace window manager configuration consuming `main`, `resize`, and `service` modes.
   - **`hosts/macos/ghostty.config`:** Ghostty terminal configuration with dropdown toggle.

2. **Windows Host Adapters:**
   - **`hosts/windows/keyboard.ahk`:** AutoHotkey v2 script translating clipboard, launcher, and terminal signals.
   - **`hosts/windows/glazewm.yaml`:** GlazeWM window manager configuration natively consuming `F13`–`F20` signals and binding modes.
   - **`hosts/windows/windows-terminal-actions.jsonc`:** Windows Terminal action snippet for `_quake` global summon.
