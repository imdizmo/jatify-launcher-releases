#!/usr/bin/env python3
"""Checks apps.json with the same rules Jatify Launcher applies (Manifest.cs). Any broken entry fails the check."""
import json, re, sys

OWNER = "imdizmo"
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")
FILE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9._-]{0,63}$")
REPO = re.compile(rf"^{OWNER}/[A-Za-z0-9_.-]{{1,100}}$")
PAGE = re.compile(rf"^https://github\.com/{OWNER}/[A-Za-z0-9_.-]{{1,100}}/?$")
ICON = re.compile(rf"^https://(raw\.githubusercontent\.com|github\.com)/{OWNER}/[A-Za-z0-9_./%-]{{1,300}}$")
SIZE = re.compile(r"^\d+[KMGT]?$")
VERSION = re.compile(r"^\d+\.\d+(\.\d+){0,2}$")


def problems(text):
    if len(text.encode()) > 256 << 10:
        return ["over 256 KB"]
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as e:
        return [f"not JSON: {e}"]
    if not isinstance(doc, dict) or doc.get("schema") != 1 or not isinstance(doc.get("apps"), list):
        return ['not {"schema": 1, "apps": [...]}']
    out, seen = [], set()
    for i, e in enumerate(doc["apps"]):
        def bad(why):
            out.append(f"apps[{i}] {e.get('id', '?') if isinstance(e, dict) else ''}: {why}")
        if not isinstance(e, dict):
            bad("not an object"); continue
        s = lambda k: e.get(k) if isinstance(e.get(k), str) else None
        if not SLUG.match(s("id") or ""): bad("id is not a short lowercase name")
        elif e["id"] in seen: bad("listed twice")
        else: seen.add(e["id"])
        if not 0 < len(s("name") or "") <= 60: bad("no name, or over 60 characters")
        if not REPO.match(s("releases") or ""): bad(f"releases is not a {OWNER}/… repository")
        for k in ("releaseAsset", "releaseExe"):
            v = s(k) or ("linux-x64.tar.gz" if k == "releaseAsset" else "")
            if not FILE.match(v) or ".." in v: bad(f"{k} is not a plain file name")
        if not PAGE.match(s("repo") or f"https://github.com/{s('releases')}"): bad(f"repo is not a github.com/{OWNER}/… page")
        icon = s("icon")
        if icon is not None and (".." in icon or not (ICON.match(icon) or FILE.match(icon))): bad("icon is neither an own GitHub URL nor a file name")
        if "minLauncher" in e and not VERSION.match(s("minLauncher") or ""): bad("minLauncher is not a version")
        if "memoryMax" in e and not SIZE.match((s("memoryMax") or "").upper()): bad("memoryMax is not a size")
        for k, n in (("tagline", 200), ("description", 1000), ("by", 40)):
            if k in e and (s(k) is None or len(s(k)) > n): bad(f"{k} is not text of at most {n} characters")
        for k in ("command", "checkout", "unit", "project", "source", "exe"):
            if k in e: bad(f"{k} is never read from this list; remove it")
    return out


if __name__ == "__main__":
    found = problems(open(sys.argv[1] if len(sys.argv) > 1 else "apps.json", encoding="utf-8").read())
    for p in found:
        print(p)
    sys.exit(1 if found else 0)
