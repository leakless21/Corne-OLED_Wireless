# Keyboard Config

> Personal ZMK keyboard configuration with shared semantic host integration for macOS and Windows.

---

## 1. Top-Level Architecture

```text
Corne ─┐
       ├── Semantic Keyboard Protocol (F13–F24) ─┬── macOS   (Karabiner + AeroSpace + Ghostty)
Sofle ─┘                                        └── Windows (AutoHotkey + GlazeWM + Windows Terminal)
```

Both keyboards share a single, OS-neutral design language:
* Portable Colemak-DH base layer with modern bilateral home-row mods.
* Standardized 6-layer thumb model (NAV, MOUSE, HOST, SYM, NUM, FUN).
* Directional home-row navigation (`← ↓ ↑ →` on `N E I O`).
* Semantic `F13`–`F24` signals for window management, launchers, and desktop editing.
* Complete separation between firmware typing semantics and OS-level host adapters.

---

## 2. Keyboard Comparison Matrix

| Property | Corne | Sofle v2 |
|---|---|---|
| **Firmware Framework** | ZMK | ZMK |
| **Physical Layout** | 42 keys (3×6 + 3 thumbs) | 60 keys (6×4 + 5 thumbs) |
| **Alpha Base** | Colemak-DH | Colemak-DH |
| **Home-Row Mods** | Modern bilateral (`hml`/`hmr`) | Modern bilateral (`hml`/`hmr`) |
| **HOST Layer** | Yes (`F13`–`F20`) | Yes (`F13`–`F20`) |
| **Number Row** | Virtual (`NUM` layer) | Dedicated physical row |
| **Rotary Encoders** | No | 2× EC11 encoders + push switches |
| **Gaming Model** | `GAME` + `GAME_AUX` | Single complete `GAME` layer |
| **ZMK Studio** | Enabled with locking | Enabled with locking |
| **Primary Host** | macOS | Windows |
| **Cross-Platform** | Yes | Yes |

---

## 3. Host Integration Matrix

| Feature | Firmware Signal | macOS Adapter | Windows Adapter |
|---|---|---|---|
| **Workspaces 1–5** | `F13`–`F17` | AeroSpace `Alt-1..5` | GlazeWM `f13..f17` |
| **Move to Workspace** | `Shift+F13..F17` | AeroSpace `Alt-Shift-1..5` | GlazeWM `shift+f13..f17` |
| **Directional Focus** | `Ctrl+F13..F16` | AeroSpace `Alt-H/J/K/L` | GlazeWM `ctrl+f13..f16` |
| **Directional Move** | `Ctrl+Shift+F13..F16` | AeroSpace `Alt-Shift-H/J/K/L` | GlazeWM `ctrl+shift+f13..f16` |
| **Previous Workspace** | `F18` | AeroSpace `Alt-Tab` | GlazeWM `f18` |
| **Resize Mode** | `Shift+F18` | AeroSpace `Alt-R` | GlazeWM `shift+f18` |
| **Service Mode** | `Alt+F18` | AeroSpace `Alt-Shift-;` | GlazeWM `alt+f18` |
| **Fullscreen** | `F19` | AeroSpace `Alt-F` | GlazeWM `f19` |
| **Float / Tile** | `F20` | AeroSpace `Alt-Shift-Space` | GlazeWM `f20` |
| **System Launcher** | `Alt+F13` | Spotlight (`Cmd+Space`) | Windows Search (`Win+S`) |
| **Quick Terminal** | `Alt+F14` | Ghostty dropdown (`Ctrl+```) | Windows Terminal Quake (`Ctrl+Alt+```) |
| **New Terminal** | `Alt+F15` | Ghostty window (`Alt+Enter`) | Windows Terminal (`wt.exe`) |
| **Previous Window** | `Alt+F16` | AeroSpace (`Alt+```) | Windows (`Alt+Tab`) |
| **Copy / Paste / Cut** | `F21` / `F22` / `F23` | `Cmd+C` / `Cmd+V` / `Cmd+X` | `Ctrl+C` / `Ctrl+V` / `Ctrl+X` |
| **Undo / Redo** | `F24` / `Shift+F24` | `Cmd+Z` / `Cmd+Shift+Z` | `Ctrl+Z` / `Ctrl+Y` |

---

## 4. Repository Structure

```text
keyboard-config/
├── config/
│   ├── corne.keymap          # Corne 42-key layout
│   ├── corne.conf            # Corne Kconfig settings
│   ├── sofle.keymap          # Sofle 60-key layout
│   ├── sofle.conf            # Sofle Kconfig settings
│   └── west.yml              # Pinned West dependencies
├── hosts/
│   ├── macos/
│   │   ├── karabiner.json    # Complex modifications bridge
│   │   ├── aerospace.toml    # Tiling window manager config
│   │   └── ghostty.config    # Terminal & scratchpad config
│   └── windows/
│       ├── keyboard.ahk      # AutoHotkey v2 bridge
│       ├── glazewm.yaml      # Tiling window manager config
│       ├── windows-terminal-actions.jsonc
│       └── README.md
├── keymap-drawer/
│   ├── corne.svg / corne.yaml
│   └── sofle.svg / sofle.yaml
├── scripts/
│   ├── check_corne_keymap.py
│   ├── check_sofle_keymap.py
│   ├── check_host_protocol.py
│   └── check_build_config.py
└── docs/
    ├── architecture.md
    ├── host-protocol.md
    ├── setup.md
    ├── usage.md
    ├── keyboards/
    │   ├── corne.md
    │   └── sofle.md
    ├── hosts/
    │   ├── macos.md
    │   └── windows.md
    └── migration/
        └── sofle-baseline.md
```

---

## 5. Documentation & Guides

- **Architecture:** [docs/architecture.md](docs/architecture.md)
- **Semantic Protocol:** [docs/host-protocol.md](docs/host-protocol.md)
- **Setup & Flashing:** [docs/setup.md](docs/setup.md)
- **Daily Usage & Workflow:** [docs/usage.md](docs/usage.md)
- **Corne Reference:** [docs/keyboards/corne.md](docs/keyboards/corne.md)
- **Sofle Reference:** [docs/keyboards/sofle.md](docs/keyboards/sofle.md)
- **macOS Guide:** [docs/hosts/macos.md](docs/hosts/macos.md)
- **Windows Guide:** [docs/hosts/windows.md](docs/hosts/windows.md)
- **Sofle Migration Baseline:** [docs/migration/sofle-baseline.md](docs/migration/sofle-baseline.md)

---

## 6. Static Verification Suite

Run all static invariant and protocol checks locally:

```bash
python3 scripts/check_corne_keymap.py
python3 scripts/check_sofle_keymap.py
python3 scripts/check_host_protocol.py
python3 scripts/check_build_config.py
```
