#!/usr/bin/env python3
"""Gate runner. Usage: python run_gates.py [path] [--pre-commit|--release]
--pre-commit: G3 secret scan + hygiene lint (hard fails).
--release (G5): the above + placeholder lint (hard) + citation lint (advisory).
Default: release set. Exit 1 if any hard gate fails."""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent

def run(script, target, extra=None):
    cmd = [sys.executable, str(HERE / script), str(target)] + (extra or [])
    r = subprocess.run(cmd)
    return r.returncode

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = Path(args[0]) if args else Path(".")
    mode = "pre-commit" if "--pre-commit" in sys.argv else "release"
    print(f"=== Gate run ({mode}) on {target.resolve()} ===")
    hard = 0
    hard += run("g3_secret_scan.py", target)
    hard += run("lint_hygiene.py", target)
    if mode == "release":
        hard += run("lint_placeholder.py", target)
        run("lint_citation.py", target)  # advisory
    if hard:
        print("=== GATE RESULT: RED — fix and re-run; file defect records for each finding ===")
        sys.exit(1)
    print("=== GATE RESULT: GREEN (hard gates) ===")

if __name__ == "__main__":
    main()
