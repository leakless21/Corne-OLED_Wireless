# macOS AeroSpace Setup — User Guide

This guide documents the macOS [AeroSpace](https://nikitabobko.github.io/AeroSpace/)
tiling-window-manager setup used alongside this repository.

> **Repository context.** This repository is a **ZMK firmware** project for a Corne
> keyboard. The AeroSpace configuration described here lives in your user
> `~/.config/aerospace/aerospace.toml` config (see [Config location](#config-location-backup--rollback)),
> **not** in this repository. **This documentation pass does not change any firmware
> or keymap files** (in particular `config/corne.keymap` is untouched). It only adds
> this guide and a link from the README.

---

## 1. Scope and non-goals

**In scope**

- Documenting the installed AeroSpace configuration: workspace layout, key bindings,
  and per-app routing.
- Installation prerequisites (including the macOS Accessibility permission).
- Where the config lives, how to back it up, and how to roll back.
- Useful CLI commands for inspection and safe reloads.
- Troubleshooting and a rollback procedure.
- A *documentation-only* preview of future Corne `F13`–`F20` integration.

**Non-goals**

- This guide does **not** ship or modify AeroSpace itself. Install it separately
  (see below).
- It does **not** modify ZMK firmware or the Corne keymap. Firmware changes are a
  separate workflow (see the README).
- It does **not** prescribe a specific AeroSpace release. Always follow the
  [official AeroSpace documentation](https://nikitabobko.github.io/AeroSpace/guide)
  for the version you have installed.
- It does **not** cover multi-monitor-specific tuning beyond the single-Space model
  described below.

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

## 3. Config location, backup & rollback

- **Config file:** `~/.config/aerospace/aerospace.toml`
  (use `aerospace config --config-path` to print the exact path AeroSpace uses).
- **Backup before editing:**

  ```sh
  cp ~/.config/aerospace/aerospace.toml \
     ~/.config/aerospace/aerospace.toml.bak.$(date +%Y%m%d-%H%M%S)
  ```

- **Validate without applying** (see [Commands](#7-useful-commands)):

  ```sh
  aerospace reload-config --dry-run
  ```

- **Rollback:**

  ```sh
  cp ~/.config/aerospace/aerospace.toml.bak.<timestamp> \
     ~/.config/aerospace/aerospace.toml
  aerospace reload-config
  ```

  If AeroSpace fails to parse a broken config it keeps the last good in-memory
  config, so a bad edit will not usually "brick" your session — but always keep a
  known-good backup.

---

## 4. One native macOS Space

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

---

## 5. Workspace order and bindings

These are the bindings for the **default MacBook keyboard**. Keep the laptop
keyboard as standard QWERTY macOS: no Karabiner, Kanata, KMonad, Colemak mapping,
or modifier remapping is required. In AeroSpace configuration, `alt` means the
Mac **Option (⌥)** key. The Corne is optional and does not need to be connected
for any of these bindings to work.

The five workspaces, in order, and their `Alt` bindings (this is the requested
swap):

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

    # Workspace focus (the requested swap)
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
> application-specific modifiers. Keep this in mind when designing Corne layers
> (see [Future integration](#9-future-corne-f13f20-integration-documentation-only)).

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

## 7. Verified current routing

The following `on-window-detected` rules are the **verified current routing** in
this setup. They use the recommended `if = 'test …'` syntax (the older
`if.app-id = …` form is soft-deprecated).

```toml
# Place on-window-detected above any [table] sections (TOML requirement).
# See: https://nikitabobko.github.io/AeroSpace/guide#on-window-detected-callback
on-window-detected = [
    # DEV: Zed and Ghostty
    {
        if = 'test %{app-bundle-id} = dev.zed.Zed || test %{app-bundle-id} = com.mitchellh.ghostty',
        run = ['move-node-to-workspace DEV'],
    },
    # WEB: Zen Browser
    {
        if = 'test %{app-bundle-id} = app.zen-browser.zen',
        run = ['move-node-to-workspace WEB'],
    },
    # COMMS: Vencord (Vesktop)
    {
        if = 'test %{app-bundle-id} = dev.vencord.vesktop',
        run = ['move-node-to-workspace COMMS'],
    },
]
```

**Intentional exceptions (unrestricted):**

- **Finder** (`com.apple.finder`) — left unrestricted so it opens on whatever
  workspace you are currently using.
- **Obsidian** (`md.obsidian`) — left unrestricted for the same reason.

If you later want these pinned, add a callback like the ones above (e.g.
`move-node-to-workspace AUX` for Obsidian).

> To find an app's bundle ID, run `aerospace list-apps` (see below) or inspect the
> app in Finder → *Get Info*.

---

## 8. Useful commands

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
  change the running configuration. Use it after every edit.

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

## 9. Troubleshooting & rollback

**Windows not being routed / bindings do nothing**

- Confirm AeroSpace has the **Accessibility** permission (Section 2) and was
  relaunched after enabling it.
- Run `aerospace reload-config --dry-run` to surface syntax errors.
- Check the bundle ID with `aerospace list-apps` — a wrong ID means the
  `on-window-detected` rule never matches.
- Remember only `cmd`/`alt`/`ctrl`/`shift` modifiers are valid; an unsupported
  modifier silently fails to bind.

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

## 10. Future Corne `F13`–`F20` integration (documentation only)

> **Documentation only.** Nothing here is implemented yet, and no firmware/keymap
> changes are made in this pass.

The Corne keyboard can emit keys up to `F24` (AeroSpace supports `f1`…`f20` as
bindable keys). A possible future enhancement is to map the Corne's top function
row to AeroSpace workspace and action keys, e.g.:

| Corne key | AeroSpace binding            | Action                    |
|-----------|------------------------------|---------------------------|
| `F13`     | `alt-1` (`workspace WEB`)    | Focus WEB                 |
| `F14`     | `alt-2` (`workspace DEV`)    | Focus DEV                 |
| `F15`     | `alt-3` (`workspace COMMS`)  | Focus COMMS               |
| `F16`     | `alt-4` (`workspace RUN`)    | Focus RUN                 |
| `F17`     | `alt-5` (`workspace AUX`)    | Focus AUX                 |
| `F18`     | `alt-tab`                    | Previous workspace        |
| `F19`     | `alt-f`                      | Fullscreen                |
| `F20`     | `alt-shift-space`            | Toggle floating           |

Constraints to respect when this is implemented:

- AeroSpace bindings may only use `cmd`, `alt`, `ctrl`, `shift` modifiers, so the
  Corne layer should send those modifier combos (not `fn` or other keys).
- The actual keycodes must be defined in `config/corne.keymap` (ZMK) in a separate
  firmware change — out of scope for this documentation task.

---

## 11. Official references

- Guide: <https://nikitabobko.github.io/AeroSpace/guide>
- Commands: <https://nikitabobko.github.io/AeroSpace/commands>
- Default config: <https://nikitabobko.github.io/AeroSpace/guide#default-config>
- Releases / install: <https://nikitabobko.github.io/AeroSpace/> (check here for
  the current version — no specific release is asserted in this guide)
