<p align="center">
  <img src="kiro.jpg" alt="Kiro" width="220" />
</p>

# kiro-qtile

Educational / tutorial repository for [Qtile](https://qtile.org/) — a fully-Python tiling window manager, configurable and extensible in Python. This is the **X11** configuration Kiro ships. Part of the `~/EDU/` learning series.

## What's in this repo

- `etc/skel/` — Qtile user config that lands in `/etc/skel/`.
- `setup.sh`, `up.sh`, `cleanup.sh` — standard EDU bash scaffold.

All keybindings are native Qtile `Key()` bindings in `config.py` — Qtile binds keys itself, so there is no sxhkd config to keep in sync. Screenshots use `scrot` / `xfce4-screenshooter` / `gnome-screenshot` / `flameshot`, brightness uses `xbacklight`, the wallpaper is set with `feh` and rotated by `variety`, and `fastcompmgr` provides transparency and shadows.

## Keybindings

Press **`Super + Ctrl + S`** to open the searchable **kiro-keybindings** cheatsheet — an on-screen, type-to-filter list of every shortcut, identical across all Kiro desktops. The full list also ships as a plain-text [`keybindings.txt`](etc/skel/.config/qtile/keybindings.txt) in the config directory.

## Installation

### From `nemesis_repo` (recommended)

```ini
[nemesis_repo]
SigLevel = Never
Server = https://erikdubois.github.io/$repo/$arch
```

```bash
sudo pacman -Syu
sudo pacman -S kiro-qtile
```

The package pulls in Qtile and the helper tools this config calls, so there is nothing else to install by hand.

### Manual

```bash
git clone https://github.com/kirodubes/kiro-qtile.git
cd kiro-qtile
sudo cp -r etc/skel/. /etc/skel/
```

Existing users can pull the config into their own home:

```bash
cp -rT /etc/skel ~/
```

## Languages

`scripts/theme-switcher.sh` follows the system language: Dutch, German, Spanish, French, Portuguese (Brazil), Russian, Hungarian, Italian, Turkish, Polish, Japanese,
Chinese (simplified) and Romanian, with English as the fallback. The translations live in `po/`
(gettext); after changing the script's text run `bash po/make-mo.sh`.

## Websites

Information : https://erikdubois.be

## Social Media

Youtube : https://www.youtube.com/erikdubois

<!-- KIRO-FUNDING-FOOTER:START — managed by Kiro-HQ/cascade-readme-footer.sh -->
## Help fund Kiro

Everything I build here stays free and open — always. If Kiro or any of these
tools have ever saved you time or taught you something, a small monthly
contribution helps keep the work going. Donations target break-even, nothing
more — the core always stays free for everyone.

- GitHub Sponsors: https://github.com/sponsors/erikdubois
- Patreon: https://www.patreon.com/c/kiroproject
- YouTube memberships: https://www.youtube.com/@ErikDubois/join
- Ko-fi: https://ko-fi.com/erikdubois
- PayPal: https://www.paypal.me/erikdubois
<!-- KIRO-FUNDING-FOOTER:END -->

## License

See [LICENSE](./LICENSE).
