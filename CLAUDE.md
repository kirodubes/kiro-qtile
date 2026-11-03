# CLAUDE.md — kiro-qtile

## Project overview

See [README.md](./README.md) for the user-facing description of this repo.

## Current state

Standard EDU scaffold (`setup.sh`, `up.sh`, optional `cleanup.sh`) plus the five required markdown files. Content lives where the repo actually ships files (typically `etc/skel/` or `usr/share/`).

## Patterns & decisions

- Bash scripts follow the canonical template from Kiro-HQ — see [Kiro-HQ/CLAUDE.md](/home/erik/Insync/Kiro/Kiro-HQ/CLAUDE.md) and the canonical [up.sh](/home/erik/Insync/Kiro/Kiro-HQ/up.sh) / [setup.sh](/home/erik/Insync/Kiro/Kiro-HQ/setup.sh) / [cleanup.sh](/home/erik/Insync/Kiro/Kiro-HQ/cleanup.sh).
- README + CHANGELOG + IDEAS + TODO are the four other required scaffold files per the ecosystem MD-scaffold rule.

## Translations

- `scripts/theme-switcher.sh` speaks 13 languages via gettext (domain `kiro-qtile`, `_t`/`_tf`, same pattern as ohmychadwm). The `.mo`
  files live in skel `.config/qtile/scripts/locale/` next to the script, so they ship with the skel.
- After changing its text run `bash po/make-mo.sh` (extract, merge 13 `po/<lang>.po`, compile). Rules, registers
  and the review step: `~/Insync/Kiro/Kiro-HQ/TRANSLATIONS/README.md`.

## Next steps

See [TODO.md](./TODO.md) for active work.
