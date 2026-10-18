#!/bin/bash
# =============================================================================
# autostart.sh — qtile (X11) session startup script
#
# Called BY qtile from the startup hook in config.py (not by the display
# manager directly), so it has NO window-manager loop — it just starts the
# background services and exits.
#
# To autostart your own apps, add:  run "your-app"
# To stop an autostart entry, comment it out with #
# =============================================================================

# run() — start a program only if it is not already running.
# Exact-match (-x) on the 15-char process comm name avoids false "already up"
# hits from loose substring matching.
run() {
  if ! pgrep -x "$(basename "$1" | head -c 15)" >/dev/null; then
    "$@" &
  fi
}

# ── Monitor layout ────────────────────────────────────────────────────────────
# Apply a saved arandr/xrandr screen layout named after the current user.
# Generate your layout with arandr, save it to ~/.screenlayout/<username>.sh
[ -f "$HOME/.screenlayout/$(whoami).sh" ] && sh "$HOME/.screenlayout/$(whoami).sh"

# ── Compositor ────────────────────────────────────────────────────────────────
run fastcompmgr -c                                   # Transparency and shadows

# ── System tray applets ───────────────────────────────────────────────────────
run nm-applet                                        # NetworkManager wifi/eth tray
run pamac-tray                                       # Arch package manager tray
run xfce4-power-manager                              # Battery / display power management
run blueberry-tray                                   # Bluetooth manager tray
run /usr/lib/xfce4/notifyd/xfce4-notifyd             # Desktop notification daemon
run /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1  # Polkit auth popups (sudo GUI)

# ── Volume control ────────────────────────────────────────────────────────────
run volctl                                           # PipeWire/PulseAudio volume tray

# ── Keyboard ──────────────────────────────────────────────────────────────────
numlockx on &                                        # Numpad on at login

# ── Wallpaper ─────────────────────────────────────────────────────────────────
# feh paints the default Kiro wallpaper once; variety then takes over the
# rotation (alt+n / alt+p and friends are bound in config.py).
feh --bg-fill /usr/share/backgrounds/kiro/kiro-wallpaper.jpg &
run variety                                          # Wallpaper changer
