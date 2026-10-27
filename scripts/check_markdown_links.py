#!/usr/bin/env python3
"""Check local Markdown links without requiring third-party packages."""
from __future__ import annotations
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:")

def main() -> int:
    broken: list[str] = []
    for markdown in sorted(ROOT.rglob("*.md")):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if not target or target.startswith(EXTERNAL_PREFIXES):
                continue
            local_path = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not local_path:
                continue
            resolved = (markdown.parent / local_path).resolve()
            if not resolved.exists():
                line = text.count("\n", 0, match.start()) + 1
                broken.append(f"{markdown.relative_to(ROOT)}:{line}: {target}")
    if broken:
        print("Broken local Markdown links:", file=sys.stderr)
        for item in broken:
            print(f"  {item}", file=sys.stderr)
        return 1
    print("All local Markdown links point to existing files.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
