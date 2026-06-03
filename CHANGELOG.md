# Changelog

## 2026.06.03

### What Changed
- **Rofi colour-theme switcher** — `Super + Shift + T` opens a rofi menu listing every palette in `colors.py` (DoomOne, Dracula, GruvboxDark, MonokaiPro, Nord, OceanicNext, Palenight, SolarizedDark, SolarizedLight, TomorrowNight), applies the pick, and restarts qtile. No more hand-editing the config to change colours — the thing users kept asking for.
- **Default palette stays untouched.** DoomOne remains the shipped default exactly as before; the switcher only ever *adds* an override in `~/.config/qtile/active_theme`, and picking "DoomOne" clears that file to return to the pristine default. `config.py` falls back to DoomOne when the file is absent or names an unknown palette.
- New palettes are picked up automatically: drop another named block into `colors.py` and it appears in the menu (downloadable palettes from DistroTube colorz / terminal.sexy / Gogh, etc.).

### Technical Details
- `scripts/theme-switcher.sh` (new, executable): derives the palette list dynamically from `colors.py` (`grep` the top-level `Name =` assignments), marks the default + currently-active entry in the rofi menu, validates the choice against the known list, writes/clears `active_theme`, then `qtile cmd-obj -o cmd -f restart`. Lightweight in-skel helper styled like the sibling `fastcompmgr-toggle.sh` (rofi reuses `rofi/launcher2.rasi` with `-no-config -dmenu`).
- `config.py`: the hardcoded `colors = colors.DoomOne` became a guarded lookup — read `~/.config/qtile/active_theme`, `getattr(colors, pick)` only when it's a real palette, else `DoomOne`. `ruff check` clean; `py_compile` clean.
- Keybinding `Super + Shift + T` chosen from [Kiro-HQ/KEYBINDINGS_FREE.md](/home/erik/Insync/Kiro/Kiro-HQ/KEYBINDINGS_FREE.md) (Super+Ctrl+T was NOT free); the free-keys ledger was updated to record the claim.
- Regenerated `keybindings.txt` via `/kiro-create-keybindings`: the new opener appears under System & Session as "theme switcher — rofi colour palette picker".

### Curated distinct palettes + dedicated rofi menu
- **Replaced the lookalike palette set in `colors.py` with 8 visually distinct schemes.** The old 10 were nearly all charcoal-bg + cyan-accent (only Gruvbox/SolarizedLight stood out), so switching looked like nothing happened. Dropped the five that were near-duplicates (MonokaiPro, OceanicNext, Palenight, SolarizedDark, TomorrowNight) and added TokyoNight, CatppuccinMocha, Everforest. Each palette now carries a **different hero accent in slot [8]** (focused-window border + active-workspace circle): DoomOne cyan, Dracula pink, Gruvbox lime, Nord frost-blue, TokyoNight blue, Catppuccin mauve, Everforest green, SolarizedLight teal — so a switch is obvious at a glance. Hex values sourced from the canonical schemes (cross-checked against the adi1090x rofi `colors/*.rasi`). **DoomOne is left byte-for-byte untouched** as the shipped default.
- **Dedicated menu theme `rofi/theme-switcher.rasi`** — a small single-column picker adapted from adi1090x's applet style, flattened to be self-contained (colours + `Iosevka` font inlined, no `~/.config/rofi` dependency). Chrome is fixed (DoomOne-based) so the picker looks the same whichever palette is active. `theme-switcher.sh` now points at it instead of the borrowed `launcher2.rasi`.

## 2026.06.02

### What Changed
- Brought `scripts/autostart.sh` in line with the canonical [TWM autostart standard](/home/erik/Insync/Kiro/Kiro-HQ/AUTOSTART_TEMPLATE.md). Documented header, `# ──` sections in standard order, no rubbish — same apps qtile already autostarted.
- Removed the dead `#xrandr --output VGA-1 …` reference lines above the monitor block and the trailing pile of commented `#run discord/firefox/spotify/...` examples.
- Adopted the standard `.fehbg`-restore wallpaper pattern (fallback to the Kiro wallpaper).
- Removed the redundant `.bin/give-me-azerty-be-qtile` script: `config.py` already auto-detects the keyboard layout at startup (`setxkbmap -query` → azerty_be / qwerty keys), so the manual switch was both unnecessary and broken (it `cp`-ed a non-existent `config-azerty.py` over the smart config).

### Technical Details
- `function run { … pgrep -x $(basename $1 | head -c 15) … }` → canonical POSIX `run()` with quoted args; dropped redundant trailing `&` on `run` lines (the helper already backgrounds). Converted bare `numlockx/blueberry-tray/notifyd/polkit` launches to `run` calls.
- Preserved qtile's documented per-WM exceptions: **picom** is the default compositor (not fastcompmgr — fullscreen rationale kept), super+p/super+g toggles intact, and there is **no WM-loop tail** (qtile calls this script from its config.py hook). qtile's native bar means no status-bar line.
- Validated with `bash -n`.

### Files Modified
- etc/skel/.config/qtile/scripts/autostart.sh
- etc/skel/.bin/give-me-azerty-be-qtile (removed)

## 2026.06.01

### What Changed
- Added a global keybinding `super + ctrl + s` that launches **kiro-keybindings**, the new searchable Qt6/PySide6 keybindings cheatsheet (a cross-desktop Kiro feature). `super + ctrl + s` is the universal cheatsheet hotkey across all Kiro tiling window managers ("S" = Shortcuts; AZERTY-safe).

### Technical Details
- `sxhkd/sxhkdrc`: new binding under the "SUPER + ... KEYS" section (qtile delegates app keys to sxhkd) → `super + ctrl + s` runs `kiro-keybindings`.
- `keybindings.txt`: fully regenerated via /kiro-keybindings-all-twms; the new opener now appears under Applications & Launchers.

### Files Modified
- etc/skel/.config/qtile/sxhkd/sxhkdrc
- etc/skel/.config/qtile/keybindings.txt

## 2026.05.26

### What Changed
- Replaced picom with **fastcompmgr** as the compositor. Boot launch and the toggle now use fastcompmgr, and the compositor-toggle keybind moved to the unified `super + g` (was `ctrl + alt + o`).

### Technical Details
- `scripts/autostart.sh`: `picom --config $HOME/.config/qtile/scripts/picom.conf &` → `fastcompmgr -c &`.
- `sxhkd/sxhkdrc`: toggle binding `ctrl + alt + o` → `super + g`, pointing at the renamed script.
- `scripts/picom-toggle.sh` renamed to `fastcompmgr-toggle.sh` (simple on/off toggle — fastcompmgr takes no config file).
- Deleted the now-unused `scripts/picom.conf`.

### Files Modified
- etc/skel/.config/qtile/scripts/autostart.sh
- etc/skel/.config/qtile/sxhkd/sxhkdrc
- etc/skel/.config/qtile/scripts/fastcompmgr-toggle.sh (created, replaces picom-toggle.sh)
- etc/skel/.config/qtile/scripts/picom-toggle.sh (deleted)
- etc/skel/.config/qtile/scripts/picom.conf (deleted)

## 2026.05.21

### What Changed
- Initial markdown scaffold added per the ecosystem MD-scaffold rule ([HQ/CLAUDE.md](/home/erik/Insync/Kiro/Kiro-HQ/CLAUDE.md#required-markdown-scaffold-every-repo)).
- Stubs created for `CHANGELOG.md`, `CLAUDE.md`, `IDEAS.md`, `TODO.md` (whichever were missing).
- README rewritten with real install/usage content (replaced earlier one-line stub) where applicable.

### Files Modified
- CHANGELOG.md (created)
- CLAUDE.md (created where missing)
- IDEAS.md (created where missing)
- TODO.md (created where missing)
- README.md (rewritten where it was a stub)
