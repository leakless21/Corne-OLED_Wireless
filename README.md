# Corne ZMK Firmware

ZMK firmware configuration for a Corne split keyboard on **nice\_nano\_v2**
controllers with **nice\_oled** displays. The GitHub Actions workflow builds
`.uf2` firmware images that you flash over USB.

## Quick Start

1. Fork / clone this repo.
2. Edit `config/corne.keymap` (see [docs/setup.md](docs/setup.md) for first
   flash, recovery, and Bluetooth re-pairing; [docs/usage.md](docs/usage.md)
   for daily use and the firmware change workflow).
3. Push — GitHub Actions builds `corne-left.uf2`, `corne-right.uf2`, and
   `settings-reset.uf2`, then merges them into a single downloadable
   `firmware` archive (`.zip`) on the Actions run.
4. Download the archive, extract the `.uf2` files, flash both halves
   (see guide), and start typing.

## Prerequisites

- **Hardware:** Corne split keyboard with two nice\_nano\_v2 controllers and
  nice\_oled displays.
- **GitHub account** (to run the Actions workflow and download artifacts).
- **USB-C cable** for each half during flashing.
- **Bluetooth-capable host** (macOS, Linux, Windows, etc.) for wireless use
  after the initial flash. macOS is specifically required for the AeroSpace
  tiling-window-manager guide.

## Documentation

| Guide | What it covers |
|-------|---------------|
| [docs/setup.md](docs/setup.md) | Initial setup: first flash of both halves, recovery / settings-reset, Bluetooth re-pairing. |
| [docs/usage.md](docs/usage.md) | Daily use & development workflow: layers, Bluetooth profiles, ZMK Studio, firmware change workflow, smoke-test checklist, decision table. |
| [docs/corne-keymaps.md](docs/corne-keymaps.md) | Keymap & layers reference: all 10 layers, home-row mods, sticky keys, layer-taps, pointing, OLED/ZMK Studio settings. |
| [docs/macos-aerospace.md](docs/macos-aerospace.md) | macOS AeroSpace tiling-window-manager guide: the Corne HOST/F13–F20 bridge, workspace bindings, app routing, install, and troubleshooting. |

## Notes

- Firmware artifacts are **`.uf2`** files (not `.urf2`). The GitHub Actions
  workflow builds them individually, then the upstream reusable workflow merges
  them into a single `firmware` archive for download.
- The keymap editor (visual) is available at
  <https://nickcoutsos.github.io/keymap-editor/>.
- The boards (`nice_nano_v2`, shields `corne_left`/`corne_right`) are
  **upstream** ZMK targets. This repo only contains the keymap, config, and
  build definitions.
- Local builds are **not** covered by this guide. Use the GitHub Actions
  workflow instead.
