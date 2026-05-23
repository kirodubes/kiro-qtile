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

## License

See [LICENSE](./LICENSE).
