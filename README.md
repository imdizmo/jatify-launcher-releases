# Jatify Launcher

Downloads of **Jatify Launcher**: one window that installs, updates and launches Jatify's tools (Asset Shelf,
Groundwork and more), checks for their updates, and keeps them in step with GitHub releases.

This repository holds the releases only; the source is private. See [jatify.com](https://jatify.com).

## Install

- **Linux x64:** download `JatifyLauncher-<version>-linux-x64.tar.gz` from the [latest release](../../releases/latest),
  unpack it where it should stay, then run `./install.sh` in that folder: it adds `jatify-launcher` to `~/.local/bin`
  and **Jatify Launcher** to the applications menu. Needs systemd (it starts each tool as a user service with a memory
  cap) and `tar`.
- **Windows x64:** download `JatifyLauncher-<version>-win-x64.zip`, unzip it somewhere you can write to (such as
  `%LOCALAPPDATA%\Programs`, not Program Files, so it can update itself) and run `JatifyLauncher.exe`. Its first start
  adds it to the Start Menu.

No .NET needed. The launcher updates itself from this repository.

Each release lists its SHA-256 on the release page; check a download with `sha256sum <file>`.

Bugs and ideas: open an issue, see [CONTRIBUTING.md](CONTRIBUTING.md).
