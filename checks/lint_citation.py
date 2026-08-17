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

# Percentages are a separate alternative on purpose: "47%" followed by a space has
# no word boundary after the "%", so folding it into the unit group below silently
# stops matching every percentage in the corpus. Found by tests/seeded_defects.py.
FIGURE = re.compile(
    r"\$[1-9][\d,.]*"                                                   # $120, $1.5
    r"|\b\d+(?:\.\d+)?\s?%"                                             # 47%, 12.5 %
    r"|\b\d+(?:\.\d+)?\s?(?:TFLOPS|GFLOPS|GB/s|TB/s|ms|MB|GB|TB)\b"     # hardware units
    r"|\b\d{2,}(?:\.\d+)?\s?(?:percent|billion|million|users|seats)\b")  # spelled-out
SOURCE = re.compile(
    r"(?i)https?://|\[source|\bcite|citation|source:|according to"
    r"|estimated?|analyst|unverified|directional|reported|per ")
# Policy thresholds ("100% coverage", "cap is 20%") are rules, not empirical claims,
# and demanding a citation for them is noise. A check that cries wolf trains its
# operator to ignore it, which is worse than having no check.
POLICY = re.compile(r"(?i)coverage|\bcaps?\b|threshold|\bquorum\b|sampling")

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
                if SOURCE.search(window) or POLICY.search(line):
                    continue
                findings.append(f"{p}:{i+1}: {line.strip()[:90]}")
    if findings:
        print(f"CITATION LINT: {len(findings)} unsourced-figure candidate(s)")
        for f in findings[:60]:
            print("  " + f)
        sys.exit(1 if "--strict" in sys.argv else 0)
    print("CITATION LINT: clean")


if __name__ == "__main__":
    main()
