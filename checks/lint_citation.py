#!/usr/bin/env python3
"""Citation-coverage lint for prose + HTML. Screens gates G1/G2.
Usage: python lint_citation.py [path] [--strict]
Heuristic: flags lines containing hard figures ($X, X%, X TFLOPS/GB/ms, XM/XB users)
with no source signal (URL, [Source], cite tag, hedge word) on the same or adjacent
line. Advisory by default (exit 0 with report); --strict exits 1.
Heuristics both miss and over-flag; a human decides. Verifier treats this as a
screen, never a verdict."""
import re
import sys
from pathlib import Path

FIGURE = re.compile(
    r"\$[1-9][\d,.]*|\b\d+(\.\d+)?\s?(%|TFLOPS|GFLOPS|GB/s|TB/s|ms\b|B\b|M\b)\b"
    r"|\b\d{2,}(\.\d+)?\s?(percent|billion|million|users|seats)\b")
SOURCE = re.compile(
    r"(?i)https?://|\[source|\bcite|citation|source:|according to"
    r"|estimated?|analyst|unverified|directional|reported|per ")
SHIP_EXT = {".md", ".html", ".txt"}
SKIP = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0]) if args else Path(".")
    findings = []
    for p in root.rglob("*"):
        if any(part in SKIP for part in p.parts):
            continue
        if p.suffix.lower() not in SHIP_EXT or not p.is_file():
            continue
        try:
            lines = p.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            if FIGURE.search(line):
                window = "\n".join(lines[max(0, i - 1):i + 2])
                if not SOURCE.search(window):
                    findings.append(f"{p}:{i+1}: {line.strip()[:90]}")
    if findings:
        print(f"CITATION LINT: {len(findings)} unsourced-figure candidate(s)")
        for f in findings[:60]:
            print("  " + f)
        sys.exit(1 if "--strict" in sys.argv else 0)
    print("CITATION LINT: clean")


if __name__ == "__main__":
    main()
