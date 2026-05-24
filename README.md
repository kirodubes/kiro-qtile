<p align="center">
  <img src="kiro.jpg" alt="Kiro" width="220" />
</p>

# edu-qtile

Educational / tutorial repository for [Qtile](https://qtile.org/), a fully-Python tiling window manager that's both configurable in Python and extensible in Python. Part of the `~/EDU/` learning series.

## What's in this repo

- `etc/skel/` — Qtile user config that lands in `/etc/skel/`.
- `setup.sh`, `up.sh`, `cleanup.sh` — standard EDU bash scaffold.

## Installation

### From `nemesis_repo` (recommended)

```ini
[nemesis_repo]
SigLevel = Never
Server = https://erikdubois.github.io/$repo/$arch
```

```bash
sudo pacman -Syu
sudo pacman -S edu-qtile-git
```

You'll also need Qtile itself:

```bash
sudo pacman -S qtile
```

### Manual

```bash
git clone https://github.com/erikdubois/edu-qtile.git
cd edu-qtile
sudo cp -r etc/skel/. /etc/skel/
```

Existing users can pull the config into their own home:

```bash
cp -rT /etc/skel ~/
```

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
