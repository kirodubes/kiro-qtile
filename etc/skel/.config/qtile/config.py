# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Kiro qtile config (X11):
#   - Visual design (DoomOne colours, bar, widgets) follows the DTOS/CachyOS qtile.
#   - All keybindings are native qtile Key() bindings. qtile binds keys itself,
#     so the application/multimedia/screenshot launchers live in the `keys` list
#     below rather than in an sxhkd config.

import os
import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

import colors

# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser("~")

myTerm = "alacritty"

# Full-screen shot, saved straight to the user's Pictures directory. scrot hands
# the -e string to /bin/sh, which is what expands $f and $(xdg-user-dir ...).
_shot_full = ("scrot 'Kiro-%Y-%m-%d-%s_screenshot_$wx$h.jpg' "
              "-e 'mv $f $(xdg-user-dir PICTURES)'")

# ── Keybindings ───────────────────────────────────────────────────────────
# Window-management bindings live in this list; the application / multimedia /
# screenshot launchers are appended further down (ported from sxhkd).
keys = [

    # SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),


    # SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "t", lazy.spawn(home + "/.config/qtile/scripts/theme-switcher.sh"),
        desc="Pick a qtile colour theme (rofi)"),

    # ALT + SHIFT KEYS
    Key(["mod1", "shift"], "r", lazy.reload_config()),


    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


    # MAXIMIZE (fills screen but keeps the bar; super+f is true fullscreen)
    Key([mod, "shift"], "f", lazy.window.toggle_maximize()),

    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    # shift+Left/Right are NOT bound here on purpose: they move a window to the
    # previous/next screen (see keys.extend below). Binding them twice made the
    # swap_left/swap_right dead (qtile kept the later move-to-screen binding).
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),

    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]


# ── Application / launcher / multimedia keys (ported from sxhkd) ───────────
# sxhkd does not run on Wayland, so the bindings that used to live in
# sxhkd/sxhkdrc are native qtile Key() bindings here. X11-only tools were
# swapped for Wayland equivalents (grim/slurp screenshots, brightnessctl) and
# the X11-only entries (xkill, picom/fastcompmgr toggles, variety wallpaper
# rotation, sxhkd reload) were dropped.
keys.extend([
    # SUPER + FUNCTION KEYS
    Key([mod], "F1", lazy.spawn("vivaldi-stable")),
    Key([mod], "F2", lazy.spawn("code")),
    Key([mod], "F3", lazy.spawn("inkscape")),
    Key([mod], "F4", lazy.spawn("gimp")),
    Key([mod], "F5", lazy.spawn("meld")),
    Key([mod], "F6", lazy.spawn("vlc --video-on-top")),
    Key([mod], "F7", lazy.spawn("virtualbox")),
    Key([mod], "F8", lazy.spawn("thunar")),
    Key([mod], "F9", lazy.spawn("virt-manager")),
    Key([mod], "F10", lazy.spawn("spotify")),
    Key([mod], "F11", lazy.spawn("rofi -theme-str 'window {width: 100%;height: 100%;}' -show drun")),
    Key([mod], "F12", lazy.spawn("rofi -show drun")),

    # SUPER + KEYS
    Key([mod, "control"], "s", lazy.spawn("kiro-keybindings")),
    Key([mod], "e", lazy.spawn("code")),
    Key([mod], "x", lazy.spawn("archlinux-logout")),
    Key([mod, "shift"], "x", lazy.spawn("kiro-powermenu")),
    Key([mod], "r", lazy.spawn(
        "rofi -no-config -no-lazy-grab -show drun -modi drun "
        f"-theme {home}/.config/qtile/rofi/launcher2.rasi")),
    Key([mod], "d", lazy.spawn(
        "rofi -no-config -no-lazy-grab -show drun -modi drun "
        f"-theme {home}/.config/qtile/rofi/launcher2.rasi")),
    Key([mod], "v", lazy.spawn("pavucontrol")),
    Key([mod], "t", lazy.spawn(myTerm)),
    Key([mod], "Return", lazy.spawn(myTerm)),
    Key([mod], "KP_Enter", lazy.spawn(myTerm)),
    Key([mod, "shift"], "Return", lazy.spawn("thunar")),
    Key([mod, "shift"], "d", lazy.spawn(
        "dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' "
        "-fn 'NotoMonoRegular:bold:pixelsize=14'")),

    # CONTROL + ALT KEYS
    Key(["control", "mod1"], "e", lazy.spawn("archlinux-tweak-tool")),
    Key(["control", "mod1"], "d", lazy.spawn("obs")),
    Key(["control", "mod1"], "q", lazy.spawn("alacritty-tweak-tool")),
    Key(["control", "mod1"], "o", lazy.spawn("opera")),
    Key(["control", "mod1"], "comma", lazy.spawn("mintstick -m iso")),
    Key(["control", "mod1"], "End", lazy.spawn(myTerm + " -e btop")),
    Key(["control", "mod1"], "b", lazy.spawn("brave --password-store=basic")),
    Key(["control", "mod1"], "c", lazy.spawn("chromium -no-default-browser-check")),
    Key(["control", "mod1"], "g", lazy.spawn("chromium -no-default-browser-check")),
    Key(["control", "mod1"], "i", lazy.spawn("kiro-iso-builder")),
    Key(["control", "mod1"], "f", lazy.spawn("firefox")),
    Key(["control", "mod1"], "k", lazy.spawn("archlinux-logout")),
    Key(["control", "mod1"], "l", lazy.spawn("archlinux-logout --settings")),
    Key(["control", "mod1"], "p", lazy.spawn("pamac-manager")),
    Key(["control", "mod1"], "m", lazy.spawn("mintstick -m iso")),
    Key(["control", "mod1"], "u", lazy.spawn("pavucontrol")),
    Key(["control", "mod1"], "s", lazy.spawn("fish-tweak-tool")),
    Key(["control", "mod1"], "Return", lazy.spawn(myTerm)),
    Key(["control", "mod1"], "t", lazy.spawn(myTerm)),
    Key(["control", "mod1"], "v", lazy.spawn("vivaldi-stable")),
    Key(["control", "mod1"], "a", lazy.spawn("alacritty-tweak-tool")),

    # ALT + KEYS
    Key(["mod1"], "r", lazy.spawn("rofi-theme-selector")),
    Key(["mod1"], "F2", lazy.spawn("xfce4-appfinder --collapsed")),
    Key(["mod1"], "F3", lazy.spawn("xfce4-appfinder")),

    # CONTROL + SHIFT KEYS
    Key(["control", "shift"], "Escape", lazy.spawn("xfce4-taskmanager")),

    # SCREENSHOTS
    Key([], "Print", lazy.spawn(_shot_full)),
    Key(["control"], "Print", lazy.spawn("xfce4-screenshooter")),
    Key(["control", "shift"], "Print", lazy.spawn("gnome-screenshot -i")),
    Key(["control", mod], "Print", lazy.spawn("flameshot gui")),

    # MULTIMEDIA KEYS
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 10")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 10")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),

    Key([mod, "shift"], "Escape", lazy.spawn("xkill")),
    Key([mod, "shift"], "KP_Enter", lazy.spawn("thunar")),
    Key(["control", "mod1"], "z", lazy.spawn("fastfetch-tweak-tool")),
    Key(["control", "mod1"], "w", lazy.spawn("fastfetch-tweak-tool")),
    Key(["control", "mod1"], "r", lazy.spawn("archlinux-betterlockscreen")),
    Key(["mod1"], "t", lazy.spawn("variety -t")),
    Key(["mod1"], "n", lazy.spawn("variety -n")),
    Key(["mod1"], "p", lazy.spawn("variety -p")),
    Key(["mod1"], "f", lazy.spawn("variety -f")),
    Key(["mod1"], "Left", lazy.spawn("variety -p")),
    Key(["mod1"], "Right", lazy.spawn("variety -n")),
    Key(["mod1"], "Up", lazy.spawn("variety --toggle-pause")),
    Key(["mod1"], "Down", lazy.spawn("variety --resume")),
    Key([mod, "control"], "space", lazy.spawn("variety --selector")),
    Key([], "F12", lazy.spawn("alacritty")),
    Key([mod, "control"], "a", lazy.spawn("pavucontrol")),
    Key([mod, "control", "shift"], "a", lazy.spawn("alacritty -e claude")),
    Key([mod, "shift"], "b", lazy.spawn("vivaldi-stable")),
    Key([mod, "shift"], "n", lazy.spawn("code")),
    Key([mod, "shift"], "m", lazy.spawn("spotify")),
    Key([], "XF86AudioMicMute", lazy.spawn("pamixer --default-source -t")),
    Key(["mod1"], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 1")),
    Key(["mod1"], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 1")),
])


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen:
            qtile.to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen:
            qtile.to_screen(i + 1)


keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod, "shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod, "shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])


def drag_window(qtile, x, y):
    """Super+drag handler. Floating windows are repositioned as before; a tiled
    window dragged onto another screen re-tiles there (joins that screen's group)
    instead of floating."""
    win = qtile.current_window
    if win is None:
        return
    if win.floating:
        win.set_position_floating(x, y)
        return
    px, py = qtile.core.get_mouse_position()
    for idx, screen in enumerate(qtile.screens):
        if (screen.x <= px < screen.x + screen.width
                and screen.y <= py < screen.y + screen.height):
            if screen is not qtile.current_screen:
                win.togroup(screen.group.name)
                qtile.focus_screen(idx, warp=False)
                # qtile suppresses focus/relayout mid-drag (see Group.focus);
                # force it so the window tiles and paints immediately instead
                # of waiting for the next click.
                win.group.focus(win, warp=False, force=True)
            break

# ── Groups (qtile-erik bindings, DoomOne circle labels from DTOS) ─────────
groups = []

def detect_layout():
    """Return the active keyboard layout code (e.g. 'be', 'us').

    setxkbmap reports what the running X server actually has loaded, which is
    what the group bindings below have to match. Falls back to 'us' on any error.
    """
    try:
        out = subprocess.check_output(["setxkbmap", "-query"], text=True)
        for line in out.splitlines():
            if line.startswith("layout:"):
                return line.split()[1].split(",")[0]
    except Exception:
        pass
    return "us"


def group_names_for(layout_code):
    """Group names matching the keyboard layout.

    Belgian AZERTY ('be') emits these keysyms on the unshifted number row, so
    Super+<physical 1..0> only reaches the group bindings when the names match
    them. Every other layout (QWERTY) just uses plain digits.
    """
    azerty_be = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft",
                 "section", "egrave", "exclam", "ccedilla", "agrave",]
    qwerty = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
    return azerty_be if layout_code == "be" else qwerty


kb_layout = detect_layout()
group_names = group_names_for(kb_layout)

# Circle labels from the DTOS design.
group_labels = ["⬤", "⬤", "⬤", "⬤", "⬤", "⬤", "⬤", "⬤", "⬤", "⬤",]
# group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
# group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall",
                 "monadtall", "monadtall", "monadtall", "monadtall",
                 "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

# CYCLE GROUPS (registered once, not per-group)
keys.extend([
    Key([mod], "Tab", lazy.screen.next_group()),
    Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
    Key(["mod1"], "Tab", lazy.screen.next_group()),
    Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
])

for i in groups:
    keys.extend([

        # CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            lazy.group[i.name].toscreen()),
    ])

# ── Theme selection (default DoomOne; honored from the switcher if set) ──────
# scripts/theme-switcher.sh (Super+Shift+T) writes a palette name to
# ~/.config/qtile/active_theme. Missing or invalid → the shipped DoomOne
# default is used untouched.
_active_theme_file = os.path.expanduser("~/.config/qtile/active_theme")
_palette = "DoomOne"
try:
    with open(_active_theme_file) as _fh:
        _pick = _fh.read().strip()
    if _pick and hasattr(colors, _pick):
        _palette = _pick
except OSError:
    pass
colors = getattr(colors, _palette)

layout_theme = {"border_width": 2,
                "margin": 12,
                "border_focus": colors[8],
                "border_normal": colors[0],
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
]

# ── Widgets / bar (DTOS DoomOne design) ──────────────────────────────────
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=12,
    padding=0,
    background=colors[0],
)

extension_defaults = widget_defaults.copy()


def tray_widget():
    return widget.Systray(padding=6)


def init_widgets_list(include_tray=True):
    widgets_list = [
        widget.Spacer(length=8),
        widget.Image(
                 filename="~/.config/qtile/icons/favicon-32.png",
                 scale="False",
                 mouse_callbacks={"Button1": lambda: qtile.spawn(
                     "rofi -no-config -no-lazy-grab -show drun -modi drun "
                     f"-theme {home}/.config/qtile/rofi/launcher2.rasi")},
                 ),
        widget.Prompt(
                 font="Ubuntu Mono",
                 fontsize=14,
                 foreground=colors[1],
        ),
        widget.GroupBox(
                 fontsize=8,
                 margin_y=5,
                 margin_x=10,
                 padding_y=0,
                 padding_x=2,
                 borderwidth=3,
                 active=colors[8],
                 inactive=colors[9],
                 rounded=False,
                 highlight_color=colors[0],
                 highlight_method="line",
                 this_current_screen_border=colors[7],
                 this_screen_border=colors[4],
                 other_current_screen_border=colors[7],
                 other_screen_border=colors[4],
                 ),
        widget.TextBox(
                 text='|',
                 font="Ubuntu Mono",
                 foreground=colors[9],
                 padding=2,
                 fontsize=14,
                 ),
        widget.LaunchBar(
                 progs=[("🦁", "brave", "Brave web browser"),
                        ("🚀", "alacritty", "Alacritty terminal"),
                        ("📁", "thunar", "Thunar file manager"),
                        ("🎸", "vlc", "VLC media player")
                        ],
                 fontsize=12,
                 padding=5,
                 foreground=colors[3],
        ),
        widget.TextBox(
                 text='|',
                 font="Ubuntu Mono",
                 foreground=colors[9],
                 padding=2,
                 fontsize=14,
                 ),
        widget.CurrentLayout(
                 foreground=colors[1],
                 padding=5,
                 ),
        widget.TextBox(
                 text='|',
                 font="Ubuntu Mono",
                 foreground=colors[9],
                 padding=2,
                 fontsize=14,
                 ),
        widget.WindowName(
                 foreground=colors[6],
                 padding=8,
                 max_chars=40,
                 ),
        widget.CPU(
                 foreground=colors[4],
                 padding=8,
                 mouse_callbacks={"Button1": lambda: qtile.spawn(myTerm + " -e btop")},
                 format='Cpu: {load_percent:03.0f}%',
                 ),
        widget.GenPollText(
                 update_interval=300,
                 func=lambda: subprocess.check_output("printf $(uname -r)", shell=True, text=True),
                 foreground=colors[3],
                 padding=8,
                 fmt='{}',
                 ),
        widget.Memory(
                 foreground=colors[8],
                 padding=8,
                 mouse_callbacks={"Button1": lambda: qtile.spawn(myTerm + " -e btop")},
                 format='{MemUsed: .0f}{mm}',
                 fmt='Mem: {}',
                 ),
        widget.DF(
                 update_interval=60,
                 foreground=colors[5],
                 padding=8,
                 mouse_callbacks={"Button1": lambda: qtile.spawn(
                     myTerm + ' -e bash -c "df -hT; read -n1 -s"')},
                 partition='/',
                 format='{uf:.0f}{m} free',
                 fmt='Disk: {}',
                 visible_on_warn=False,
                 ),
        widget.Volume(
                 foreground=colors[7],
                 padding=8,
                 fmt='Vol: {}',
                 ),
        widget.Clock(
                 foreground=colors[8],
                 padding=8,
                 mouse_callbacks={"Button1": lambda: qtile.spawn("yad --calendar --no-buttons --title=Calendar")},
                 format="%I:%M %p  %a %d %b %Y",
                 ),
    ]

    if include_tray:
        widgets_list.extend([
            tray_widget(),
            widget.Spacer(length=8),
        ])

    return widgets_list


def init_widgets_screen1():
    return init_widgets_list()


# All other monitors' bars display everything but the systray and its spacer.
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[16:17]
    return widgets_screen2


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), margin=[8, 12, 0, 12], size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), margin=[8, 12, 0, 12], size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), margin=[8, 12, 0, 12], size=30))]


if __name__ in ["config", "__main__"]:
    screens = init_screens()

# ── Mouse ────────────────────────────────────────────────────────────────
mouse = [
    Drag([mod], "Button1", lazy.function(drag_window),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []

main = None


# ── Hooks (archlinux-logout bar hide/show, autostart.sh on first start) ───
# hides the top bar when the archlinux-logout widget is opened
@hook.subscribe.client_new
def new_client(window):
    if window.name == "ArchLinux Logout":
        qtile.hide_show_bar()


# shows the top bar when the archlinux-logout widget is closed
@hook.subscribe.client_killed
def logout_killed(window):
    if window.name == "ArchLinux Logout":
        qtile.hide_show_bar()


@hook.subscribe.startup_once
def start_once():
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


@hook.subscribe.startup
def start_always():
    # X leaves the root cursor as the default X shape until something sets it
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[8],
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
        Match(wm_class='confirm'),
        Match(wm_class='dialog'),
        Match(wm_class='download'),
        Match(wm_class='error'),
        Match(wm_class='file_progress'),
        Match(wm_class='notification'),
        Match(wm_class='splash'),
        Match(wm_class='toolbar'),
        Match(wm_class='Arandr'),
        Match(wm_class='feh'),
        Match(wm_class='Galculator'),
        Match(wm_class='archlinux-logout'),
        Match(wm_class='xfce4-terminal'),
    ],
)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
