#!/usr/bin/env python3
"""Repo hygiene lint (origin: DEF-2026-07-19-002).
Usage: python lint_hygiene.py [path]
Flags junk files that must not ship; warns if .gitignore missing. Exit 1 on findings."""
import re, sys
from pathlib import Path

JUNK = [
    re.compile(r"^__pycache__$"), re.compile(r"\.pyc$"),
    re.compile(r"^~\$"),                       # Office lock files
    re.compile(r"^sed[A-Za-z0-9]{6}$"),        # sed temp artifacts (the DEF-002 culprit class)
    re.compile(r"\.swp$|\.swo$|~$"),           # editor swap/backup
    re.compile(r"^\.DS_Store$|^Thumbs\.db$"),
    re.compile(r"^npm-debug\.log|^yarn-error\.log"),
]
SKIP = {".git", "node_modules", ".venv", "venv"}

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    findings = []
    for p in root.rglob("*"):
        if any(part in SKIP for part in p.parts):
            continue
        if any(pat.search(p.name) for pat in JUNK):
            findings.append(str(p))
    warn = "" if (root / ".gitignore").exists() else "  WARN: no .gitignore at root\n"
    if findings:
        print("HYGIENE LINT: FAIL")
        print(warn, end="")
        for f in findings[:50]:
            print("  " + f)
        sys.exit(1)
    print("HYGIENE LINT: PASS")
    print(warn, end="")

if __name__ == "__main__":
    main()
