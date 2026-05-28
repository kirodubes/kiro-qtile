# Changelog

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
