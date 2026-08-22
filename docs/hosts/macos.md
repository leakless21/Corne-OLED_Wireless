# macOS Host Integration Guide

This guide documents the macOS host configuration for the semantic keyboard protocol using Karabiner-Elements, AeroSpace, Ghostty, and Spotlight.

---

## 1. Architecture Overview

```text
Keyboard (Corne / Sofle)
      ↓
Semantic F13–F24 HID Signals
      ↓
Karabiner-Elements (hosts/macos/karabiner.json)
      ↓
Native macOS Chords (Alt + Cmd shortcuts)
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
  AeroSpace          Ghostty          Spotlight
(Window Manager)   (Terminal)        (Launcher)
```

---

## 2. Installation & Prerequisites

### 1. Karabiner-Elements (Host Bridge)
- Install [Karabiner-Elements](https://karabiner-elements.pqrs.org/).
- Copy `hosts/macos/karabiner.json` to `~/.config/karabiner/assets/complex_modifications/karabiner.json`.
- In Karabiner-Elements Settings $\rightarrow$ **Complex Modifications** $\rightarrow$ **Add rule**:
  - Enable **"Keyboard Semantic Host Bridge"** (F13–F20 $\rightarrow$ AeroSpace).
  - Enable **"Keyboard Semantic Editing"** (F21–F24 $\rightarrow$ Cmd+C/V/X/Z).

### 2. AeroSpace (Tiling Window Manager)
- Install [AeroSpace](https://nikitabobko.github.io/AeroSpace/).
- Grant **Accessibility** permission in macOS System Settings $\rightarrow$ Privacy & Security $\rightarrow$ Accessibility.
- Symlink or copy `hosts/macos/aerospace.toml` to `~/.config/aerospace/aerospace.toml`:
  ```bash
  mkdir -p ~/.config/aerospace
  ln -sfn "$(pwd)/hosts/macos/aerospace.toml" ~/.config/aerospace/aerospace.toml
  ```
- Reload with `aerospace reload-config`.

### 3. Ghostty Terminal
- Install [Ghostty](https://ghostty.org/).
- Symlink or copy `hosts/macos/ghostty.config` to `~/.config/ghostty/config`:
  ```bash
  mkdir -p ~/.config/ghostty
  ln -sfn "$(pwd)/hosts/macos/ghostty.config" ~/.config/ghostty/config
  ```
- This sets up the dropdown Quick Terminal on `Ctrl+``` (`Alt+F14`).

---

## 3. Workspaces & Modal Operations

AeroSpace operates with five persistent virtual workspaces:
- `WEB` (Slot 1 / `F13` / `Alt-1`)
- `DEV` (Slot 2 / `F14` / `Alt-2`)
- `COMMS` (Slot 3 / `F15` / `Alt-3`)
- `RUN` (Slot 4 / `F16` / `Alt-4`)
- `AUX` (Slot 5 / `F17` / `Alt-5`)

### Binding Modes:
- **`main` Mode:** Standard workspace focus, window focus (`Alt-H/J/K/L`), and window moving (`Alt-Shift-H/J/K/L`).
- **`resize` Mode (`Shift+F18` / `Alt-R`):** Directional window dimension adjustments ($\pm 50$ px). Exit with `Esc` or `Enter`.
- **`service` Mode (`Alt+F18` / `Alt-Shift-;`):** Tree surgery, joining, swapping, and monitor movements. One-shot commands automatically return to `main`.
