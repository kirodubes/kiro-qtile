#!/bin/bash
# theme-switcher.sh — pick a qtile colour palette via rofi and apply it live.
#
# Lists every palette defined in colors.py, lets you choose one in rofi, writes
# the choice to ~/.config/qtile/active_theme, and restarts qtile so the new
# colours take effect. Picking "DoomOne" (the shipped default) clears the file,
# returning qtile to its untouched default — the default palette is never edited.
set -euo pipefail

QTILE_DIR="$HOME/.config/qtile"
COLORS_PY="$QTILE_DIR/colors.py"
ACTIVE_FILE="$QTILE_DIR/active_theme"
ROFI_THEME="$QTILE_DIR/rofi/theme-switcher.rasi"
DEFAULT_THEME="DoomOne"

# Text goes through gettext (domain kiro-qtile, catalogs in ./locale next to this script); English is the fallback.
export TEXTDOMAIN=kiro-qtile
TEXTDOMAINDIR="$(dirname "$(readlink -f "$0")")/locale"
export TEXTDOMAINDIR
if command -v gettext &>/dev/null && command -v gettext.sh &>/dev/null; then
    _t() { gettext "$1"; }
    # shellcheck source=/dev/null
    . gettext.sh
    _tf() { eval_gettext "$1"; }
else
    _t() { printf '%s' "$1"; }
    _tf() { local _s="$1"; eval "printf '%s' \"${_s//\"/\\\"}\""; }
fi
title="$(_t "qtile theme")"
# TRANSLATORS: marker after the shipped default palette's name in the theme list.
default_mark="$(_t "(default)")"

# Palette names = the top-level assignments in colors.py (e.g. "DoomOne = [").
mapfile -t themes < <(grep -oE '^[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=' "$COLORS_PY" \
    | sed 's/[[:space:]]*=$//' | sort)
[ "${#themes[@]}" -gt 0 ] || { notify-send "$title" "$(_t "No palettes found in colors.py")"; exit 1; }

current="$DEFAULT_THEME"
[ -r "$ACTIVE_FILE" ] && current="$(tr -d '[:space:]' < "$ACTIVE_FILE")"

# Build the menu, marking the default and the currently active palette.
menu=""
for t in "${themes[@]}"; do
    label="$t"
    [ "$t" = "$DEFAULT_THEME" ] && label="$label $default_mark"
    [ "$t" = "$current" ] && label="$label  ●"
    menu+="$label"$'\n'
done

choice="$(printf '%s' "$menu" | rofi -no-config -dmenu -i -p "$title" -theme "$ROFI_THEME" || true)"
[ -n "$choice" ] || exit 0

# Strip our annotations back to the bare palette name.
choice="${choice%% "$default_mark"*}"
choice="${choice%%  ●*}"
choice="$(printf '%s' "$choice" | tr -d '[:space:]')"

# Only act on a name we actually know.
valid=false
for t in "${themes[@]}"; do [ "$t" = "$choice" ] && valid=true && break; done
$valid || exit 1

if [ "$choice" = "$DEFAULT_THEME" ]; then
    rm -f "$ACTIVE_FILE"          # back to the shipped default — nothing overridden
else
    printf '%s\n' "$choice" > "$ACTIVE_FILE"
fi

qtile cmd-obj -o cmd -f restart
