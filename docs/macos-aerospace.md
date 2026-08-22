# macOS AeroSpace Setup — User Guide

This guide documents the macOS [AeroSpace](https://nikitabobko.github.io/AeroSpace/)
tiling-window-manager setup used alongside this repository, including the
**implemented** Corne HOST/F13–F20 integration.

> **Repository context.** This repository is a **ZMK firmware** project for a Corne
> keyboard. The canonical AeroSpace configuration is tracked at
> `dotfiles/aerospace.toml`; install it at your user config path
> `~/.config/aerospace/aerospace.toml` by symlink or copy (see
> [Config location](#3-config-location-installation-backup--rollback)). Firmware and
> window-manager changes remain separate workflows.

---

## 1. Scope and non-goals

**In scope**

- Documenting the canonical AeroSpace configuration: workspace layout, key
  bindings, semantic F13–F20 / modifier+F-key protocol, and per-app routing.
- The Corne HOST bridge: how workspace, direction, move, and resize signals
  map to AeroSpace.
- Separation of responsibility: AeroSpace owns window management (`F13`–`F20`),
  while Karabiner-Elements owns semantic editing (`F21`–`F24`).
- Installation prerequisites, validation, backups, rollback, and troubleshooting.

**Non-goals**

- This guide does not ship or modify AeroSpace itself. Install it separately
  from the [official AeroSpace documentation](https://nikitabobko.github.io/AeroSpace/guide).
- It does not modify ZMK firmware. Firmware changes are a separate workflow
  documented in [docs/corne-keymaps.md](corne-keymaps.md).
- It does not make AeroSpace responsible for generating Copy/Paste/Undo/Redo shortcuts.
- It does not make the firmware encode macOS-specific Option+H/J/K/L chords.
---

## 2. Installation & Accessibility

1. **Install AeroSpace.** Download the latest release from the
   [official AeroSpace site](https://nikitabobko.github.io/AeroSpace/) or its
   GitHub Releases page, then move it to `Applications`. (Do not rely on a
   hardcoded version number here — check the official source for the current
   release.)
2. **Launch AeroSpace** and open its preferences.
3. **Grant the Accessibility permission** (required):
   - macOS **System Settings → Privacy & Security → Accessibility**.
   - Enable **AeroSpace** in the list.
   - If it was already enabled but window management misbehaves, toggle it off,
     reboot/relaunch AeroSpace, and re-enable it. macOS caches this permission,
     and AeroSpace cannot control windows without it.
4. **Start at login** (recommended): enable *Start at login* in AeroSpace
   preferences, or set `start-at-login = true` in the config.
5. **Verify** with the menu-bar icon: it should show active workspaces and respond
   to bindings.

> AeroSpace does **not** require disabling System Integrity Protection (SIP).

---

## 3. Config location, installation, backup & rollback

The canonical config is tracked in this repository at
`dotfiles/aerospace.toml`. AeroSpace reads the installed user config from
`~/.config/aerospace/aerospace.toml` (use `aerospace config --config-path` to
print the exact path).

AeroSpace also recognizes `~/.aerospace.toml` and
`${XDG_CONFIG_HOME}/aerospace/aerospace.toml` (defaulting to
`~/.config/aerospace/aerospace.toml`). Keep one active location to avoid
ambiguity. See the official
[configuration guide](https://nikitabobko.github.io/AeroSpace/guide#config-location).

### Install from a fresh clone

From the repository root, back up any existing config and symlink the canonical
file:

```sh
mkdir -p ~/.config/aerospace
if [ -e ~/.config/aerospace/aerospace.toml ] || [ -L ~/.config/aerospace/aerospace.toml ]; then
  cp -a ~/.config/aerospace/aerospace.toml \
    ~/.config/aerospace/aerospace.toml.bak.$(date +%Y%m%d-%H%M%S)
fi
ln -sfn "$(pwd)/dotfiles/aerospace.toml" \
  ~/.config/aerospace/aerospace.toml
```

If you prefer a copy rather than a symlink:

```sh
cp dotfiles/aerospace.toml ~/.config/aerospace/aerospace.toml
```

Copies must be refreshed manually after repository changes; symlinks track the
canonical file automatically.

### Validate and roll back

Validate without applying:

```sh
aerospace reload-config --dry-run
```

Restore a backup and apply it:

```sh
cp ~/.config/aerospace/aerospace.toml.bak.<timestamp> \
  ~/.config/aerospace/aerospace.toml
aerospace reload-config
```

If AeroSpace rejects a broken config, it keeps the last good in-memory config,
but always preserve a known-good backup before editing.

---

## 4. One native macOS Space (and multi-monitor note)

AeroSpace manages its **own virtual workspaces** on top of macOS. In this setup we
keep **exactly one native macOS Space (Desktop)** active and let AeroSpace's
virtual workspaces (`WEB`, `DEV`, `COMMS`, `RUN`, `AUX`) do all the organization.

Benefits of the single-Space model:

- No macOS Space-switching animations; switching is instant and handled by
  AeroSpace.
- All windows stay inside AeroSpace's tiling model, so layout rules apply
  uniformly.
- Simpler mental model: one macOS desktop, five AeroSpace workspaces.

Do not create extra macOS Desktops (Mission Control spaces) for this workflow;
AeroSpace's virtual workspaces are independent of them.

> **Multi-monitor note.** If you use more than one monitor, prefer leaving
> macOS **Displays have separate Spaces** disabled unless you specifically need
> independent native fullscreen Spaces. Test focus and performance before adding
> monitor assignment rules; tune them via the official AeroSpace documentation
> rather than creating extra macOS Desktops.

---

## 5. Workspace order and bindings

These are the bindings for the **default MacBook keyboard**. Keep the laptop
keyboard as standard QWERTY macOS: no Karabiner, Kanata, KMonad, Colemak mapping,
or modifier remapping is required. In AeroSpace configuration, `alt` means the
Mac **Option (⌥)** key. The Corne is optional and does not need to be connected
for any of these bindings to work.

The five workspaces, in order, and their `Alt` bindings:

| Order | Workspace | Binding      | Typical use            |
|-------|-----------|--------------|------------------------|
| 1     | `WEB`     | `Alt-1`      | Browsing               |
| 2     | `DEV`     | `Alt-2`      | Coding / terminals     |
| 3     | `COMMS`   | `Alt-3`      | Chat / messaging       |
| 4     | `RUN`     | `Alt-4`      | Execution / utilities  |
| 5     | `AUX`     | `Alt-5`      | Misc / auxiliary       |

Representative config snippet (uses `config-version = 2`):

```toml
config-version = 2

# 'main' binding mode must always be present.
# See: https://nikitabobko.github.io/AeroSpace/guide#binding-modes
[mode.main.binding]
    # All possible modifiers: cmd, alt, ctrl, shift
    # (only these four modifiers are supported by AeroSpace)

    # Workspace focus
    alt-1 = 'workspace WEB'
    alt-2 = 'workspace DEV'
    alt-3 = 'workspace COMMS'
    alt-4 = 'workspace RUN'
    alt-5 = 'workspace AUX'

    # Move the focused window and follow it (Alt-Shift-<n>)
    alt-shift-1 = 'move-node-to-workspace WEB; workspace WEB'
    alt-shift-2 = 'move-node-to-workspace DEV; workspace DEV'
    alt-shift-3 = 'move-node-to-workspace COMMS; workspace COMMS'
    alt-shift-4 = 'move-node-to-workspace RUN; workspace RUN'
    alt-shift-5 = 'move-node-to-workspace AUX; workspace AUX'
```

> **Modifier limitation.** AeroSpace only supports the modifiers **`cmd`, `alt`,
> `ctrl`, and `shift`** in bindings. You cannot bind, for example, `fn` or
> application-specific modifiers.

---

## 6. Focus / move / resize / fullscreen / floating / previous-workspace

These follow AeroSpace's standard command set. The bindings below are the
recommended setup (adjust to taste); full command reference:
<https://nikitabobko.github.io/AeroSpace/commands>.

On the default keyboard, use `Option` (`⌥`) for every `Alt` binding below. macOS
`Command-Tab` remains available for traditional application switching; AeroSpace
`Option-Tab` is reserved for switching between the previous and current
workspace.

| Action            | Command                                      | Suggested binding        |
|-------------------|----------------------------------------------|--------------------------|
| Focus direction   | `focus left/down/up/right`                   | `Alt-H/J/K/L`            |
| Move window       | `move left/down/up/right`                    | `Alt-Shift-H/J/K/L`      |
| Resize            | `mode resize`, then width/height commands   | `Alt-R`, then `H/J/K/L`  |
| Fullscreen        | `fullscreen`                                 | `Alt-F`                  |
| Toggle floating   | `layout floating tiling`                     | `Alt-Shift-Space`        |
| Previous workspace| `workspace-back-and-forth`                  | `Alt-Tab`                |

Behavior notes:

- **Focus** moves the cursor between tiled windows within the current workspace.
- **Move** relocates the focused window within the tree (or, with
  `move-node-to-workspace`, sends it to another workspace — see bindings above).
- **Resize** enters a temporary resize mode. Use `H/J/K/L` to change width or
  height by 50 pixels, then `Enter` or `Esc` to return to the main mode.
- **Fullscreen** toggles AeroSpace's built-in fullscreen for the focused window
  (distinct from macOS native fullscreen; use `macos-native-fullscreen` if you
  specifically need the macOS version).
- **Floating** takes a window out of the tiling grid so it can be freely
  positioned; toggling returns it to tiling.
- **Previous workspace** (`workspace-back-and-forth`) jumps to the last-focused
  workspace and toggles back — handy for quick context switches.

---

## 7. Corne HOST bridge: semantic F13–F20 protocol

The Corne **HOST** layer emits semantic high-function-key signals. AeroSpace
assigns their meaning directly; the laptop keyboard remains ordinary QWERTY.

```toml
# Workspace focus WEB/DEV/COMMS/RUN/AUX
f13 = 'workspace WEB'
f14 = 'workspace DEV'
f15 = 'workspace COMMS'
f16 = 'workspace RUN'
f17 = 'workspace AUX'

# Move the focused window and follow it
shift-f13 = 'move-node-to-workspace WEB; workspace WEB'
shift-f14 = 'move-node-to-workspace DEV; workspace DEV'
shift-f15 = 'move-node-to-workspace COMMS; workspace COMMS'
shift-f16 = 'move-node-to-workspace RUN; workspace RUN'
shift-f17 = 'move-node-to-workspace AUX; workspace AUX'

# Context and resize mode
shift-f18 = 'mode resize'
f18 = 'workspace-back-and-forth'
f19 = 'fullscreen'
f20 = 'layout floating tiling'

# Direction signals from HOST
ctrl-f13 = 'focus left'
ctrl-f14 = 'focus down'
ctrl-f15 = 'focus up'
ctrl-f16 = 'focus right'
ctrl-shift-f13 = 'move left'
ctrl-shift-f14 = 'move down'
ctrl-shift-f15 = 'move up'
ctrl-shift-f16 = 'move right'
```

The direction geometry is shared with NAV and MOUSE:

| Corne HOST signal | AeroSpace binding | Action |
|-------------------|-------------------|--------|
| `F13`–`F17` | `f13`–`f17` | Focus WEB/DEV/COMMS/RUN/AUX |
| `Shift-F13`–`Shift-F17` | `shift-f13`–`shift-f17` | Move window + follow |
| `Shift-F18` | `shift-f18` | Enter resize mode |
| `F18` | `f18` | Previous workspace |
| `F19` | `f19` | Fullscreen |
| `F20` | `f20` | Toggle floating |
| `Ctrl-F13`–`Ctrl-F16` | `ctrl-f13`–`ctrl-f16` | Focus left/down/up/right |
| `Ctrl-Shift-F13`–`Ctrl-Shift-F16` | `ctrl-shift-f13`–`ctrl-shift-f16` | Move left/down/up/right |

Resize mode reuses `Ctrl-F13`–`Ctrl-F16`:

```toml
[mode.resize.binding]
ctrl-f13 = 'resize width -50'
ctrl-f14 = 'resize height +50'
ctrl-f15 = 'resize height -50'
ctrl-f16 = 'resize width +50'
enter = 'mode main'
esc = 'mode main'
```

The firmware protocol does not encode Option+H/J/K/L. Those remain separate
laptop fallbacks in AeroSpace. A Windows/GlazeWM adapter can assign the same
semantic F-key signals without changing firmware.

---

## 7.1 macOS editing bridge (Karabiner-Elements & F21–F24)

Window management and text editing are kept strictly decoupled:

* **`F13`–`F20`** (HOST layer) $\rightarrow$ **AeroSpace** (workspaces, focus, move, resize).
* **`F21`–`F24`** (NAV & MOUSE layers) $\rightarrow$ **Karabiner-Elements** (Copy, Paste, Cut, Undo, Redo).

The repository tracks the canonical Karabiner complex modifications rule file at `dotfiles/karabiner-corne.json`.

### Karabiner setup

1. **Install Karabiner-Elements** from <https://karabiner-elements.pqrs.org/>.
2. **Copy or link the rule file** to Karabiner's complex modifications directory:
   ```sh
   mkdir -p ~/.config/karabiner/assets/complex_modifications
   cp dotfiles/karabiner-corne.json ~/.config/karabiner/assets/complex_modifications/
   ```
3. **Enable the rule in Karabiner-Elements:**
   - Open **Karabiner-Elements Settings** $\rightarrow$ **Complex Modifications** $\rightarrow$ **Add rule**.
   - Enable **"Corne F21-F24 Semantic Editing"**.
4. **Verify mapping:**
   - `F21` $\rightarrow$ `Command+C` (Copy)
   - `F22` $\rightarrow$ `Command+V` (Paste)
   - `F23` $\rightarrow$ `Command+X` (Cut)
   - `F24` $\rightarrow$ `Command+Z` (Undo)
   - `Shift+F24` $\rightarrow$ `Command+Shift+Z` (Redo)

Because standard MacBook laptop keyboards never emit F21–F24, this configuration does not alter or interfere with normal laptop typing.

## 8. Canonical app routing

The repository-tracked config applies conservative routing only to
hard-purpose applications:

```toml
on-window-detected = [
    {
        if = 'test %{app-bundle-id} = dev.zed.Zed || test %{app-bundle-id} = com.mitchellh.ghostty',
        run = ['move-node-to-workspace DEV'],
    },
    {
        if = 'test %{app-bundle-id} = app.zen-browser.zen',
        run = ['move-node-to-workspace WEB'],
    },
    {
        if = 'test %{app-bundle-id} = dev.vencord.vesktop',
        run = ['move-node-to-workspace COMMS'],
    },
]
```

Finder (`com.apple.finder`) and Obsidian (`md.obsidian`) are intentionally
unrestricted so contextual windows open where they are invoked. If a new
application deserves hard routing, add it to `dotfiles/aerospace.toml` only
after confirming its bundle ID with `aerospace list-apps`.

> To find an app's bundle ID, run `aerospace list-apps` (see below) or inspect the
> app in Finder → *Get Info*.

---

## 9. Useful commands

All commands are run from a terminal (or via `exec-and-forget` / Raycast /
Alfred). Always prefer `--dry-run` before a real reload.

- **List running apps and their bundle IDs:**

  ```sh
  aerospace list-apps
  ```

- **List all windows (with workspace/app info):**

  ```sh
  aerospace list-windows
  ```

- **Validate the config without applying it:**

  ```sh
  aerospace reload-config --dry-run
  ```

  This parses and checks the config and reports errors/warnings, but does **not**
  change the running configuration. Use it after every edit. (This guide documents
  the command only; it does not assert that a live reload was performed.)

- **Re-run `on-window-detected` callbacks for every existing window** (e.g. to
  apply routing retroactively after editing the rules):

  ```sh
  aerospace run-callback --for-every-window on-window-detected
  ```

  This re-evaluates the `on-window-detected` rules against all currently open
  windows, so newly added routing takes effect without manually closing/reopening
  apps.

- **Apply a config (for real):**

  ```sh
  aerospace reload-config
  ```

---

## 10. Troubleshooting & rollback

**Windows not being routed / bindings do nothing**

- Confirm AeroSpace has the **Accessibility** permission (Section 2) and was
  relaunched after enabling it.
- Run `aerospace reload-config --dry-run` to surface syntax errors.
- Check the bundle ID with `aerospace list-apps` — a wrong ID means the
  `on-window-detected` rule never matches.
- Remember only `cmd`/`alt`/`ctrl`/`shift` modifiers are valid; an unsupported
  modifier silently fails to bind.

**Corne HOST keys do nothing in AeroSpace**

- Confirm the keyboard is on the HOST layer (hold the BASE `Tab` thumb
  `LH0` to engage it — see [docs/corne-keymaps.md](corne-keymaps.md)).
- Confirm the semantic bindings (`f13`–`f20`, `shift-f13`–`shift-f18`,
  `ctrl-f13`–`ctrl-f16`, and `ctrl-shift-f13`–`ctrl-shift-f16`) are present in
  `~/.config/aerospace/aerospace.toml`.
- Run `aerospace reload-config --dry-run` before applying changes.
- Some macOS apps swallow F-keys or modifier+F-key events; verify with a
  known-good app first.

**Config edit broke things**

- AeroSpace keeps the last good in-memory config if parsing fails, so the session
  usually survives. Fix the file, then `aerospace reload-config --dry-run` to
  confirm, and `aerospace reload-config` to apply.
- If you need to revert entirely, restore the backup (Section 3) and reload.

**Routing didn't apply to already-open windows**

- `on-window-detected` only fires for *newly detected* windows. For existing
  windows, run `aerospace run-callback --for-every-window`.

**macOS Space confusion**

- Ensure you are using the single native macOS Space model (Section 4). Extra
  macOS Desktops interfere with AeroSpace's virtual-workspace switching.

---

## 11. Official references

- Guide: <https://nikitabobko.github.io/AeroSpace/guide>
- Commands: <https://nikitabobko.github.io/AeroSpace/commands>
- Default config: <https://nikitabobko.github.io/AeroSpace/guide#default-config>
- Releases / install: <https://nikitabobko.github.io/AeroSpace/> (check here for
  the current version — no specific release is asserted in this guide)
- Configuration locations and TOML behavior:
  <https://nikitabobko.github.io/AeroSpace/guide#config-location>
