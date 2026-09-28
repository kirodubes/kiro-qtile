# Changelog

## 2026.09.28

### What Changed
- Added `ruff.toml` pinning ruff to the classic rule set. ruff 0.16 widened its implicit rules, so the
  global pre-commit hook started rejecting commits over untouched code (BLE001, PLW1510, I001, ...).

### Technical Details
- Same file as archlinux-tweak-tool: `line-length = 120`, `select = ["E4", "E7", "E9", "F"]`, `E402`
  ignored for `gi.require_version()`. `ruff check .` passes with no code changes.

### Files Modified
- `ruff.toml` (new)

## 2026.09.27

### What Changed
- Reworded the `keybindings.txt` header: dropped "DO NOT EDIT BY HAND" and the generator name, added a line telling users it lists the default bindings and they can edit it to match their own. A user changed a binding, expected the file to update itself, and went looking for a generator that isn't part of Kiro.

### Technical Details
- `Generated:` now carries only the date, so the kiro-keybindings HTML/PDF footer (which prints everything after `Generated:`) shows a clean date. The new line is a `#` comment, which both kiro-keybindings parsers skip. Bindings unchanged.

### Files Modified
- `etc/skel/.config/qtile/keybindings.txt`

## 2026.09.11

### What Changed

- **Fixed "Qtile does not log in".** Arch `qtile` 0.37.0-1 changed its session files to
  `Exec=/bin/sh -c "systemctl --user import-environment ...; exec systemctl --user start --wait qtile.service"`.
  SDDM's `/usr/share/sddm/scripts/Xsession` ends in a bare `exec $@` — word splitting, no `eval` —
  so the quotes are never processed, `sh -c` receives the literal token `"systemctl` and dies with
  `unexpected EOF while looking for matching "`. The session lasted under a second and SDDM went
  straight back to the greeter. `qtile.service` never started, so nothing appeared in the journal,
  which is why it looked like nothing happened at all.
- **The fix now ships with the package** as `kiro-qtile-fix-session` plus a pacman hook, so it is
  re-applied after every `qtile` upgrade instead of being a hand-edit that the next upgrade undoes.
- **The Wayland session entry is hidden** (`NoDisplay=true`), the same treatment `kiro-xfce` gives
  `xfce-wayland.desktop`. This also removes the second, indistinguishable `Name=Qtile` row that
  SDDM was showing.
- **Restored the X11 config.** Commit `b233ae3` (2026-06-17) converted this repo from X11 to
  Wayland — its own entry opens with *"The repo was a byte-for-byte copy of the X11 kiro-qtile"*,
  so that pass was written for a `kiro-qtile-wayland` repo and landed here. Kiro ships qtile on
  X11, so the package has been handing X11 users Wayland-only tooling: `grim`/`slurp` screenshots,
  a `swaybg` wallpaper, a `StatusNotifier` tray and no compositor. All of that is back on X11
  tooling.
- **Keybindings stay native.** sxhkd is not coming back — qtile binds keys itself, `keybindings.txt`
  already documents the native set, and the last two passes maintained the bindings in `config.py`.
  Both READMEs said otherwise and have been corrected.
- **The `depends=()` list is no longer just `qtile`**, matching how `ohmychadwm` declares its
  runtime set, so a fresh install actually gets the tools the config calls.

> **The Wayland qtile session is now non-functional, not merely hidden.** `wl_input_rules` /
> `InputConfig` are gone and the tray is `widget.Systray`, which is X11-only — un-setting
> `NoDisplay=true` will not give anyone a working session. Reviving Wayland means a new
> `kiro-qtile-wayland` repo seeded from commit `c8513ca`, which is where the Wayland variant is
> preserved.

### Technical Details

- `usr/bin/kiro-qtile-fix-session`: POSIX `sh`. Rewrites the `Exec=` line of
  `/usr/share/xsessions/qtile.desktop` to `Exec=qtile start -b x11`, anchored on `^Exec=` rather
  than on upstream's current wrapper so it keeps working if the wrapper changes again. Appends
  `NoDisplay=true` to the Wayland entry unless already present. The Wayland file being absent is
  fine (`exit 0`); the xsessions file being absent prints to stderr and exits non-zero, so a
  silent revert to the broken session cannot happen unnoticed. Verified idempotent.
- `usr/share/libalpm/hooks/kiro-qtile-fix-session.hook`: `Install`/`Upgrade`, `Type = Path`,
  targets both `qtile.desktop` paths, `PostTransaction`. `readme.install` also calls the script
  from `post_install`/`post_upgrade`, because a hook only fires when one of its target paths is in
  the transaction — installing `kiro-qtile` onto a box that already has `qtile` would otherwise
  miss it.
- `config.py`: dropped `from libqtile.backend.wayland import InputConfig` and the
  `wl_input_rules` / `wl_xcursor_theme` / `wl_xcursor_size` block; `detect_layout()` reads
  `setxkbmap -query` again (the live X server, which is what the AZERTY group keysyms must match)
  instead of `localectl`; `tray_widget()` returns `widget.Systray` again, which drops the
  `python-dbus-fast` requirement; restored the `@hook.subscribe.startup` cursor hook
  (`xsetroot -cursor_name left_ptr`); screenshots follow the ohmychadwm house pattern —
  `Print` → `scrot` into Pictures, `ctrl+Print` → `xfce4-screenshooter`,
  `ctrl+shift+Print` → `gnome-screenshot -i`, `super+ctrl+Print` → `flameshot gui`.
- `scripts/autostart.sh`: kept the current `run()` helper and section dividers, swapped `swaybg`
  for `feh --bg-fill` plus `variety`, and added `fastcompmgr -c` and `numlockx on`. The
  `$HOME/.screenlayout/erik.sh` block from the old X11 version was deliberately not restored — a
  personal filename does not belong in `/etc/skel`.
- PKGBUILD: added a `_destname2="/usr/"` copy step so the hook and script ship; merged the two
  competing `conflicts=()` lines (the second silently overrode the first, dropping
  `cachyos-qtile-settings`); `pkgver`/`pkgrel` left alone, `build.sh` bumps them.
- Verified on picard: config loads clean under qtile 0.37.0 / Python 3.14 with no
  `StatusNotifier` dependency warning, `ruff check` matches the pre-change baseline exactly
  (13 pre-existing findings, none new), `codespell` clean, both shell scripts pass `-n`.

### Files Modified

- `etc/skel/.config/qtile/config.py`
- `etc/skel/.config/qtile/scripts/autostart.sh`
- `etc/skel/.config/qtile/keybindings.txt`
- `etc/skel/.config/qtile/README.md`
- `README.md`
- `KIRO-PKG-BUILD-APPS/kiro-qtile/PKGBUILD` (separate repo)
- `KIRO-PKG-BUILD-APPS/kiro-qtile/readme.install` (separate repo)

### Files Added

- `usr/bin/kiro-qtile-fix-session`
- `usr/share/libalpm/hooks/kiro-qtile-fix-session.hook`

### Files Removed

- `wayland-deps.sh`

## 2026.06.30

### What Changed
- Removed the `update-system` keybinding (`Ctrl + Alt + Shift + F1` and `Super + Ctrl + Shift + F1`). `update-system` is a personal maintenance script that had slipped into ohmychadwm and propagated across every Kiro environment; it is not part of the shipped desktop, so the binding is gone. The cheatsheet `keybindings.txt` was updated to match.
- Deleted the generated `keybindings.html` / `keybindings.pdf` cheatsheets — these will be regenerated by a different process.
- **Grouped the `super + F1`–`F12` app-launchers into one contiguous ascending block** in the cheatsheet (they were scattered among the other launchers), per the new ordering rule in `/kiro-create-keybindings`.
- **Guardrail against shipping generated cheatsheets:** added a `.gitignore` rule for `keybindings.html`/`keybindings.pdf` plus an `up.sh` commit-guard that aborts the push if either is ever tracked — they are generated on demand by the kiro-keybindings app, never committed.

### Technical Details
- Removed the `# SYSTEM UPDATE` comment and the two `Key(... lazy.spawn("update-system"))` bindings from `config.py`.

### Files Modified
- `etc/skel/.config/qtile/config.py`
- `etc/skel/.config/qtile/keybindings.txt`
- `.gitignore`
- `up.sh`

### Files Removed
- `etc/skel/.config/qtile/keybindings.html`
- `etc/skel/.config/qtile/keybindings.pdf`

## 2026.06.11

### What Changed
- **Ported the config from X11 to a Wayland-native qtile session.** The repo was a byte-for-byte copy of the X11 `kiro-qtile`; on a `qtile-wayland` session none of the X11 pieces worked. This pass makes it Wayland-only (X11 code paths stripped, not gated).
- **sxhkd keybindings migrated into `config.py`.** sxhkd does not run on Wayland, so every application / launcher / multimedia / screenshot binding that lived in `sxhkd/sxhkdrc` is now a native qtile `Key()` / `lazy.spawn()` binding. Window-management bindings were already native.
- **X11-only tools swapped for Wayland equivalents:** screenshots `scrot`/`flameshot` → `grim` + `slurp`; brightness `xbacklight` → `brightnessctl`; wallpaper `feh`/`variety` → `swaybg`; compositor `picom` → dropped (qtile *is* the Wayland compositor).
- **X11-only bindings dropped:** `xkill` (Super+Escape), the picom/fastcompmgr compositor toggles (Super+p / Super+g), the variety wallpaper-rotation + pywal keys, and the sxhkd reload key — none have a Wayland role.
- **Keyboard layout** is now detected with `localectl` (was `setxkbmap`, X11-only) and applied to the session via `wl_input_rules` / `InputConfig(kb_layout=…)`.
- **README** updated for the Wayland variant (title, deps, "qtile is the compositor" note).
- Added `wayland-deps.sh` (repo root, not shipped to `/etc/skel`) — a test toggle to install/remove the Wayland-only runtime packages (`grim slurp swaybg brightnessctl python-dbus-fast`) so a Wayland session can be tried on a box and then reverted.
- Out of scope this pass: regenerating the `keybindings.txt`/`.html`/`.pdf` cheatsheet.

### Technical Details
- `config.py`: removed `IS_WAYLAND`/`IS_X11` and the Systray branch (tray is always `widget.StatusNotifier`); replaced `detect_group_names()` (`setxkbmap -query`) with `detect_layout()` (`localectl status` → `X11 Layout:`) feeding both the AZERTY-vs-QWERTY group keysyms and `wl_input_rules`; added `from libqtile.backend.wayland import InputConfig`. Removed the X11 `startup` hook (`xsetroot`) and the `set_floating` hook (used the X11 Window API `get_wm_transient_for`/`get_wm_type`); qtile's `default_float_rules` + the existing `Match(...)` list in `floating_layout` cover floats cross-backend. Appended a `keys.extend([...])` block with the ported launcher/multimedia/screenshot bindings (grim/slurp shots via `bash -c`).
- `scripts/autostart.sh`: removed the xrandr/arandr screen-layout block, the VirtualBox resolution line, `picom`, `numlockx`, `sxhkd`, and `variety`; wallpaper now via `swaybg -m fill`; tray/dbus applets (nm-applet, pamac-tray, xfce4-power-manager, blueberry-tray, xfce4-notifyd, polkit-gnome, volctl) kept (they run under XWayland / dbus).
- Deleted `sxhkd/sxhkdrc`, `scripts/picom.conf`, `scripts/picom-toggle.sh`, `scripts/fastcompmgr-toggle.sh`, `scripts/set-screen-resolution-in-virtualbox.sh`.
- Verified: `python -m py_compile config.py` OK, `ruff check` clean, `qtile check` reports the config as valid Python (the `StatusNotifier` line is a dependency warning — needs `python-dbus-fast` on the target — not a config error). Live Wayland-session boot to be confirmed by Erik (no Wayland tooling on the dev box).

### Files Modified
- `etc/skel/.config/qtile/config.py`
- `etc/skel/.config/qtile/scripts/autostart.sh`
- `README.md`
- `wayland-deps.sh` (new)
- Deleted: `etc/skel/.config/qtile/sxhkd/sxhkdrc`, `scripts/picom.conf`, `scripts/picom-toggle.sh`, `scripts/fastcompmgr-toggle.sh`, `scripts/set-screen-resolution-in-virtualbox.sh`

## 2026.06.08

### What Changed
- Rebound `Super + F9` from `lollypop` to `virt-manager`, matching the distro-wide change applied across all Kiro environments (ohmychadwm, chadwm, leftwm, i3, bspwm, awesome, xfce).

### Technical Details
- Edited the `Super + F9` entry in `qtile/sxhkd/sxhkdrc` (comment + command) and regenerated the cheatsheet (`keybindings.txt` → `keybindings.html` + `keybindings.pdf` via `kiro-keybindings-html.py`).

### Files Modified
- `etc/skel/.config/qtile/sxhkd/sxhkdrc`
- `etc/skel/.config/qtile/keybindings.txt`
- `etc/skel/.config/qtile/keybindings.html`
- `etc/skel/.config/qtile/keybindings.pdf`

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
