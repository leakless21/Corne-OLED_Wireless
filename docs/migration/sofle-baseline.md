# Sofle v2 Migration Baseline & Architecture Modernization

This document captures the historical baseline of `leakless21/sofle-v2-oled-zmk` prior to migration into the unified `keyboard-config` repository.

---

## 1. Historical Sofle Configuration Baseline

### Repository Origin
- **Source:** `leakless21/sofle-v2-oled-zmk` (forked from `ergomechstore/sofle-v2-nicenano-oled`)
- **Hardware:** Ergomech Sofle V2 Wireless (60 keys: 6×4+5 per side) with two nice!nano v2 controllers and two SSD1306 OLED displays (128×32).
- **Firmware framework:** ZMK Firmware

### Historical Dependency Tracking (`config/west.yml`)
The old repository followed floating `main` branches across all remotes:
```yaml
manifest:
  remotes:
    - name: zmkfirmware
      url-base: https://github.com/zmkfirmware
    - name: mctechnology17
      url-base: https://github.com/mctechnology17
    - name: urob
      url-base: https://github.com/urob
  projects:
    - name: zmk
      remote: zmkfirmware
      revision: main
      import: app/west.yml
    - name: zmk-nice-oled
      remote: mctechnology17
      revision: main
    - name: zmk-helpers
      remote: urob
      revision: main
  self:
    path: config
```

### Historical Layer Mapping (Old Indices)
```c
#define BASE    0
#define NAV     1
#define MOUSE   2
#define BUTTON  3  // Obsolete: shifted all subsequent layer indices
#define MEDIA   4
#define NUM     5
#define SYM     6
#define FUNC    7
#define GAME    8
```

### Historical Deficiencies Identified
1. **Obsolete `BUTTON` Layer (Index 3):** Layer 3 was dedicated to duplicate cut/copy/paste/undo/redo and mouse clicks, shifting all subsequent layer numbers.
2. **Older Single-Behavior HRMs (`bhm`):** Used generic `bhm: balanced_homerow_mods` (220 ms, `tap-preferred`, no positional hold-trigger checks, no prior idle requirement).
3. **Alpha-Key Layer-Taps:** Scattered layer-taps under normal typing letters:
   - Hold `Z` → BUTTON (layer 3)
   - Hold `V` → MEDIA (layer 4)
   - Hold `K` → FUNC (layer 7)
   - Hold `/` → BUTTON (layer 3)
4. **Incorrect Key-Position Helper:** Sourced `zmk-helpers/key-labels/glove80.h` rather than the proper 60-key matrix header (`zmk-helpers/key-labels/sofle.h`).
5. **No HOST Layer:** Had no semantic `F13`–`F20` host protocol.
6. **No Proper ADJUST Model:** Used broken conditional layer (`if-layers = <1 1>; then-layer = <1>;`) and lacked structured device administration / Studio unlock.
7. **Disabled Studio Locking:** Explicitly set `CONFIG_ZMK_STUDIO_LOCKING=n` and lacked modern deep sleep configuration (`CONFIG_ZMK_SLEEP`, `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT`).
8. **Direct Exit on GAME:** GAME layer had a direct `&to 0` thumb tap on right half, prone to accidental drops out of gaming mode.

---

## 2. Target Modernized Architecture

### Modern Layer Mapping (Zero-Indexed)
```c
#define L_BASE    0
#define L_NAV     1
#define L_MOUSE   2
#define L_MEDIA   3
#define L_NUM     4
#define L_SYM     5
#define L_FUN     6
#define L_HOST    7
#define L_GAME    8
#define L_ADJUST  9
```

### Key Modernization Rules
- **BUTTON layer removed:** Editing shortcuts (`F21`–`F24`) live on NAV and MOUSE; mouse clicks live on MOUSE.
- **Bilateral Positional HRMs:** Symmetrical `hml` / `hmr` (280 ms balanced, 175 ms quick-tap, 150 ms prior idle, `hold-trigger-on-release`, opposite-hand + thumb positional triggers).
- **Pure Alpha Core:** `Z`, `V`, `K`, `/` are standard alphanumeric keys (`&kp`).
- **Canonical Thumb Architecture:** Six layer-taps on the 3 primary thumb keys per half (`MOUSE`, `NAV`, `HOST` on left; `SYM`, `NUM`, `FUN` on right), with dedicated outer thumb modifiers (`LGUI`/`LALT` on left; `RALT`/`RGUI` on right).
- **Outer-Left Home Key:** `LM5` acts as momentary hold for `MEDIA` (`&mo L_MEDIA`).
- **Unified Semantic Protocol:** Complete `F13`–`F24` protocol on HOST, NAV, and MOUSE identical to Corne.
- **Single Complete GAME Layer:** Full QWERTY alpha + number row + gaming modifiers. Deliberate exit via right encoder press (`REC` → `&to L_BASE`). No `GAME_AUX` needed due to physical number row.
- **Proper ADJUST Layer:** Activated via conditional layer `NAV + NUM → ADJUST`. Contains Bluetooth, power, reset, bootloader, Studio unlock, and GAME entry.
- **Single Pinned Manifest:** Builds against the canonical pinned `config/west.yml` shared with Corne.

---

## 3. Mandatory Migration Notice

> **IMPORTANT:** Because modern Sofle firmware completely modernizes layer numbering (removing `BUTTON`), switches to ZMK Studio locking, updates hold-tap behaviors, and changes power-management settings, **flashing this firmware requires a full settings reset and Bluetooth re-pair**.
>
> Do not attempt to flash modern firmware on top of persisted old Sofle state without flashing `settings-reset.uf2` first.
