# Jatify Launcher

Downloads of **Jatify Launcher**: one window that installs, updates and launches Jatify's tools (Asset Shelf,
Groundwork, Job Finder), checks for their updates, and keeps them in step with GitHub releases.

This repository holds the releases only; the source is private. See [jatify.com](https://jatify.com).

## Install (Linux x64)

1. Download `JatifyLauncher-<version>-linux-x64.tar.gz` from the [latest release](../../releases/latest).
2. Unpack it where it should stay, then run `./install.sh` in that folder: it adds `jatify-launcher` to
   `~/.local/bin` and **Jatify Launcher** to the applications menu.

No .NET needed. It runs on Linux with systemd (it starts each tool as a user service with a memory cap) and uses
`git` and `tar`.

Each release lists its SHA-256 on the release page; check a download with `sha256sum <file>`.
