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

- Documenting the canonical macOS power-user configuration: workspace layout,
  key bindings, semantic F13–F24 protocol, Ghostty terminal integration, and app routing.
- Canonical macOS signal path:
  ```text
  Corne firmware (semantic HID)
      ↓ F13-F24
  Karabiner-Elements (device-scoped bridge)
      ↓ standard macOS chords
  AeroSpace / Ghostty / Spotlight / macOS
  ```
- AeroSpace modal hierarchy: `main`, `resize`, and `service` modes.
- Independent application launching vs workspace switching: `WEB` only switches to WEB;
  terminals and applications launch independently.
- Ghostty Quick Terminal (`Ctrl+``` dropdown) and normal terminal launch (`Alt+Enter`).
- Karabiner-Elements host bridge with `device_if` scoping.
- Installation prerequisites, validation, backups, rollback, and troubleshooting.

**Non-goals**

- It does not couple workspace switching with application launching (no auto-launching on workspace visit).
- It does not encode macOS-specific Option/Command shortcuts directly in ZMK firmware.
- It does not require third-party ricing bars, daemons, or Raycast.

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

| Action            | Command                                      | Laptop binding           | Corne HOST binding |
|-------------------|----------------------------------------------|--------------------------|--------------------|
| Focus direction   | `focus left/down/up/right`                   | `Alt-H/J/K/L`            | `Ctrl-F13`–`Ctrl-F16` (`RM1`–`RM4`) |
| Move window       | `move left/down/up/right`                    | `Alt-Shift-H/J/K/L`      | `Ctrl-Shift-F13`–`Ctrl-Shift-F16` (`RB1`–`RB4`) |
| Resize mode       | `mode resize`                                | `Alt-R`                  | `Shift-F18` (`RT1`) |
| Service mode      | `mode service`                               | `Alt-Shift-Semicolon`    | `Alt-F18` (`RT2`) |
| Fullscreen        | `fullscreen`                                 | `Alt-F`                  | `F19` (`RH0`) |
| Toggle floating   | `layout floating tiling`                     | `Alt-Shift-Space`        | `F20` (`RH2`) |
| Previous workspace| `workspace-back-and-forth`                  | `Alt-Tab`                | `F18` (`RH1`) |
| Previous window   | `focus-back-and-forth`                       | `Alt-` `                 | `Alt-F16` (`RM0`) |
| System Launcher   | Spotlight search / launch                    | `Cmd-Space`              | `Alt-F13` (`LB4`) |
| Quick Terminal    | Ghostty dropdown toggle                      | `Ctrl-` `                | `Alt-F14` (`LB3`) |
| New Terminal      | New Ghostty window in current workspace      | `Alt-Enter`              | `Alt-F15` (`LB2`) |

Behavior notes:

- **Focus** moves the cursor between tiled windows within the current workspace.
- **Previous window** (`focus-back-and-forth`) toggles focus back and forth between the two most recently focused windows (e.g. editor ↔ terminal, browser ↔ docs).
- **Previous workspace** (`workspace-back-and-forth`) jumps to the last-focused workspace and toggles back.
- **Move** relocates the focused window within the tree (or, with `move-node-to-workspace`, sends it to another workspace).
- **Resize** enters a temporary resize mode. Use `H/J/K/L` (laptop) or the Corne directional cluster (`Alt-H/J/K/L` via Karabiner) to adjust dimensions by 50 pixels, then `Enter` or `Esc` to return to main mode.
- **Service mode** enters a command palette for structural tree surgery operations (joining, swapping, balancing sizes, monitor management). One-shot operations automatically return to main mode.
- **Fullscreen** toggles AeroSpace's built-in fullscreen for the focused window.
- **Floating** takes a window out of the tiling grid so it can be freely positioned; toggling returns it to tiling.

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
The canonical macOS path translates Corne semantic signals via Karabiner into standard macOS chords, which AeroSpace and Ghostty consume. Direct F-key bindings in `dotfiles/aerospace.toml` are retained purely as a legacy/direct fallback for environments running without Karabiner.

| Corne HOST signal | Karabiner chord | AeroSpace / macOS Action | Purpose |
|-------------------|-----------------|--------------------------|---------|
| `F13`–`F17` | `Alt-1`–`Alt-5` | `workspace WEB..AUX` | Switch to workspace |
| `Shift-F13`–`Shift-F17` | `Alt-Shift-1`–`Alt-Shift-5` | `move-node-to-workspace ...; workspace ...` | Move window to workspace + follow |
| `Ctrl-F13`–`Ctrl-F16` | `Alt-H/J/K/L` | `focus left/down/up/right` | Focus adjacent window |
| `Ctrl-Shift-F13`–`Ctrl-Shift-F16` | `Alt-Shift-H/J/K/L` | `move left/down/up/right` | Move window directionally |
| `Shift-F18` | `Alt-R` | `mode resize` | Enter resize mode |
| `Alt-F18` | `Alt-Shift-Semicolon` | `mode service` | Enter service mode |
| `F18` | `Alt-Tab` | `workspace-back-and-forth` | Previous workspace |
| `Alt-F16` | `Alt-` ` | `focus-back-and-forth` | Previous window |
| `F19` | `Alt-F` | `fullscreen` | Fullscreen toggle |
| `F20` | `Alt-Shift-Space` | `layout floating tiling` | Float/tile toggle |
| `Alt-F13` | `Cmd-Space` | Spotlight Launcher | General application launch & search |
| `Alt-F14` | `Ctrl-` ` | Ghostty Quick Terminal | Toggle drop-down scratchpad terminal |
| `Alt-F15` | `Alt-Enter` | New Ghostty Window | Create normal terminal in current workspace |

### 7.1 Resize mode

In resize mode (`[mode.resize.binding]`), both bare letters (laptop) and Alt chords (Corne via Karabiner) are accepted:

```toml
[mode.resize.binding]
alt-h = 'resize width -50'
alt-j = 'resize height +50'
alt-k = 'resize height -50'
alt-l = 'resize width +50'
h = 'resize width -50'
j = 'resize height +50'
k = 'resize height -50'
l = 'resize width +50'
enter = 'mode main'
esc = 'mode main'
```

### 7.2 Service mode

Service mode (`[mode.service.binding]`) provides structural tree surgery operations without cluttering daily keys:

```toml
[mode.service.binding]
# Tree joining (one-shot -> returns to main)
h = ['join-with left', 'mode main']
j = ['join-with down', 'mode main']
k = ['join-with up', 'mode main']
l = ['join-with right', 'mode main']
alt-h = ['join-with left', 'mode main']
alt-j = ['join-with down', 'mode main']
alt-k = ['join-with up', 'mode main']
alt-l = ['join-with right', 'mode main']

# Window swapping (one-shot -> returns to main)
shift-h = ['swap left', 'mode main']
shift-j = ['swap down', 'mode main']
shift-k = ['swap up', 'mode main']
shift-l = ['swap right', 'mode main']
alt-shift-h = ['swap left', 'mode main']
alt-shift-j = ['swap down', 'mode main']
alt-shift-k = ['swap up', 'mode main']
alt-shift-l = ['swap right', 'mode main']

# Tree manipulation
b = ['balance-sizes', 'mode main']
r = ['flatten-workspace-tree', 'mode main']
t = ['layout tiles', 'mode main']
a = ['layout accordion', 'mode main']

# Monitor management
m = ['move-node-to-monitor --focus-follows-window next', 'mode main']
shift-m = ['move-workspace-to-monitor --wrap-around next', 'mode main']

enter = 'mode main'
esc = 'mode main'
```

### 7.3 Karabiner setup and device scoping

Karabiner-Elements translates Corne semantic signals into standard macOS chords while scoping them via `device_if` conditions so other connected keyboards are unaffected.

1. **Install Karabiner-Elements** from <https://karabiner-elements.pqrs.org/>.
2. **Copy the rule file:**
   ```sh
   mkdir -p ~/.config/karabiner/assets/complex_modifications
   cp dotfiles/karabiner-corne.json ~/.config/karabiner/assets/complex_modifications/
   ```
3. **Enable the rules in Karabiner Settings → Complex Modifications → Add rule:**
   - "Corne F13-F20 Semantic Window Management Bridge"
   - "Corne F21-F24 Semantic Editing"
4. **Device Scoping with Karabiner-EventViewer:**
   To lock rules strictly to your Corne hardware (preventing accidental triggers from other keyboards), open **Karabiner-EventViewer → Devices**, find your Corne controller (both USB and Bluetooth entries), and note its `vendor_id` and `product_id`.
   In `dotfiles/karabiner-corne.json`, each manipulator contains:
   ```json
   "conditions": [
     {
       "type": "device_if",
       "identifiers": [
         {
           "vendor_id": 7504,
           "product_id": 24926,
           "is_keyboard": true
         }
       ]
     }
   ]
   ```

### 7.4 Ghostty Terminal Configuration

Install the tracked Ghostty configuration at `~/.config/ghostty/config`:
```sh
mkdir -p ~/.config/ghostty
cp dotfiles/ghostty.config ~/.config/ghostty/config
```
This configures:
* **Global Quick Terminal:** `Ctrl+``` toggles a top dropdown scratchpad terminal from anywhere.
* **Normal Terminal Launch:** `Alt+Enter` (laptop) or `HOST + Term` (`Alt-F15`) spawns an independent Ghostty window in the active workspace.
## 8. Canonical app routing

The repository-tracked config applies conservative routing only to
hard-purpose applications:

```toml
on-window-detected = [
    {
        if = 'test %{app-bundle-id} = dev.zed.Zed',
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

* **Ghostty (`com.mitchellh.ghostty`) is intentionally unrouted:** Terminal windows are contextual (`DEV` for git/editor shells, `RUN` for watchers/logs, `AUX` for SSH/commands). Unrouted terminals open where invoked and do not pull the Quick Terminal into `DEV`.
* **Workspace switching and app launching are strictly separate:** Switching to `WEB` does not launch Zen; switching to `DEV` does not launch Zed. Application launching is an independent action via Spotlight (`Cmd-Space`) or terminal shortcuts (`Alt-Enter`).
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

**Corne HOST keys trigger brightness or do nothing**

- **Brightness changes when switching to DEV or COMMS:** In macOS, raw `F14` and
  `F15` are bound at the system level to brightness down/up. Ensure Karabiner-Elements
  is installed and running with the `Corne F13-F20 Semantic Window Management Bridge`
  enabled (Section 7.1). Karabiner intercepts `F13`–`F20` and translates them into
  AeroSpace `Alt` chords, preventing macOS from receiving raw `F14`/`F15`.
- **Karabiner permissions:** If Karabiner is running but not intercepting keys, verify
  **System Settings → Privacy & Security → Input Monitoring** has **Karabiner-Elements**
  and **Karabiner-Core-Service** enabled, and in Karabiner-Elements under **Devices**,
  the Corne keyboard has **Modify events** checked.
- Confirm the keyboard is on the HOST layer (hold the BASE `Tab` thumb
  `LH0` to engage it — see [docs/corne-keymaps.md](corne-keymaps.md)).
- Confirm AeroSpace has `alt-1`..`alt-5` and direction bindings loaded (`aerospace reload-config`).
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
