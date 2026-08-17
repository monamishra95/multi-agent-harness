#!/usr/bin/env python3
"""Placeholder-text lint for shipped files (origin: DEF-2026-07-19-004). Gate G5.
Usage: python lint_placeholder.py [path]
Exit 1 on findings. Intentional placeholders (e.g. YOUR_GCP_PROJECT_ID convention,
schema templates) belong in an allowlist file `.placeholder-allow` (one substring per line)."""
import re, sys
from pathlib import Path

PATTERNS = [
    re.compile(r"(?i)add your (deployed )?(url|key|name|link)"),
    re.compile(r"(?i)lorem ipsum"),
    re.compile(r"(?i)\bTBD\b|\bTODO\b|\bFIXME\b"),
    re.compile(r"(?i)coming soon(?!\w)"),
    re.compile(r"_add your[^_]*_"),
]
SHIP_EXT = {".md", ".html", ".txt", ".json", ".yaml", ".yml"}
SKIP = {".git", "node_modules", "__pycache__", ".venv", "venv", "engine"}

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    allow = []
    allow_file = root / ".placeholder-allow"
    if allow_file.exists():
        allow = [l.strip() for l in allow_file.read_text().splitlines() if l.strip()]
    findings = []
    for p in root.rglob("*"):
        if any(part in SKIP for part in p.parts) or p.suffix.lower() not in SHIP_EXT or not p.is_file():
            continue
        try:
            for i, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
                if any(a in line for a in allow):
                    continue
                if any(pat.search(line) for pat in PATTERNS):
                    findings.append(f"{p}:{i}: {line.strip()[:90]}")
        except OSError:
            continue
    if findings:
        print("PLACEHOLDER LINT: FAIL")
        for f in findings[:50]:
            print("  " + f)
        sys.exit(1)
    print("PLACEHOLDER LINT: PASS")

if __name__ == "__main__":
    main()
