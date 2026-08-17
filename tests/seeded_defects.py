#!/usr/bin/env python3
"""Seeded-defect test: plant known defects, measure whether the gates catch them.

The harness claims its gates block bad work. This measures that claim instead of
asserting it. Each case plants one defect of a known class in a throwaway project,
runs the relevant check, and records whether it was caught. Control cases plant
something that looks suspicious but is legitimate, to measure false positives —
a check that cries wolf trains its operator to ignore it, which is worse than
having no check.

Fixtures are generated at runtime in a temp directory and deleted afterward, so
no fake credentials are ever committed to this repository.

Run:  python tests/seeded_defects.py [-v]
Exit: 0 if every case behaves as expected, 1 otherwise.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHECKS = Path(__file__).resolve().parent.parent / "checks"

# Fake credentials are assembled from fragments rather than written as literals.
# Written whole, they would sit in this file as matchable strings and the repo's
# own G3 scan would flag its own test fixtures — which it did, the first time.
_GOOGLE_KEY = "AIza" + "SyB1234567890abcdefghijklmnopqrstuv"
_PRIVATE_KEY = "-----BEGIN RSA " + "PRIVATE KEY-----\nMIIEowIBAAKCAQEA\n-----END RSA " + "PRIVATE KEY-----"
_DB_SECRET = "DATABASE_PASS" + "WORD = " + '"s3cretValue1234567890abc"'

# Each case: (id, defect_class, description, files, check, args, should_detect)
CASES = [
    (
        "X1-google-key", "X1",
        "Live-looking Google API key committed in client-side source",
        {"src/config.js": f'export const KEY = "{_GOOGLE_KEY}";\n'},
        "g3_secret_scan.py", [], True,
    ),
    (
        "X1-private-key", "X1",
        "Private key block pasted into a text file",
        {"deploy/notes.txt": _PRIVATE_KEY + "\n"},
        "g3_secret_scan.py", [], True,
    ),
    (
        "X1-generic-secret", "X1",
        "Hardcoded credential in a config assignment",
        {"app/settings.py": _DB_SECRET + "\n"},
        "g3_secret_scan.py", [], True,
    ),
    (
        "P-junk-files", "P",
        "Build artifacts committed to a public repo",
        {"__pycache__/module.cpython-311.pyc": "compiled\n", "src/main.py": "print(1)\n"},
        "lint_hygiene.py", [], True,
    ),
    (
        "J3-placeholder", "J3",
        "Template placeholder left in a shipped README",
        {"README.md": "# Project\n\n**Live demo:** _add your deployed URL here_\n"},
        "lint_placeholder.py", [], True,
    ),
    (
        "F3-uncited-figure", "F3",
        "Hard figure stated as fact in prose with no source",
        {"docs/results.md": "# Results\n\nConversion improved 47% after the redesign.\n"},
        "lint_citation.py", ["--strict"], True,
    ),
    # ---- controls: legitimate content that must NOT trip a check ----
    (
        "CONTROL-env-example", "—",
        "Placeholder credential in .env.example (sanctioned convention)",
        {".env.example": 'GEMINI_API_KEY="MY_GEMINI_API_KEY"\n'},
        "g3_secret_scan.py", [], False,
    ),
    (
        "CONTROL-cited-figure", "—",
        "Figure carrying a visible source link",
        {"docs/market.md": "# Market\n\nRevenue grew 12% last year ([source](https://example.com/report)).\n"},
        "lint_citation.py", ["--strict"], False,
    ),
]


def run_case(case, verbose):
    case_id, cls, desc, files, check, args, should_detect = case
    tmp = Path(tempfile.mkdtemp(prefix="seeded-"))
    try:
        for rel, content in files.items():
            path = tmp / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        proc = subprocess.run(
            [sys.executable, str(CHECKS / check), str(tmp), *args],
            capture_output=True, text=True,
        )
        detected = proc.returncode != 0
        ok = detected == should_detect
        if verbose:
            print(f"    check: {check} {' '.join(args)} -> exit {proc.returncode}")
            for line in proc.stdout.strip().splitlines():
                print(f"    | {line}")
        return ok, detected, proc.stdout.strip()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    verbose = "-v" in sys.argv
    print("Seeded-defect test — planting known defects and measuring detection\n")

    planted = [c for c in CASES if c[6]]
    controls = [c for c in CASES if not c[6]]
    caught = missed = false_positives = 0

    print(f"Planted defects ({len(planted)}):")
    for case in planted:
        ok, detected, _ = run_case(case, verbose)
        if detected:
            caught += 1
            print(f"  CAUGHT  [{case[1]:>3}] {case[0]:<20} {case[2]}")
        else:
            missed += 1
            print(f"  MISSED  [{case[1]:>3}] {case[0]:<20} {case[2]}")
            print(f"          ^ file a defect record: the check did not fire")

    print(f"\nControls — must not fire ({len(controls)}):")
    for case in controls:
        ok, detected, out = run_case(case, verbose)
        if detected:
            false_positives += 1
            print(f"  FALSE POSITIVE  {case[0]:<20} {case[2]}")
            print(f"                  ^ {out.splitlines()[0] if out else ''}")
        else:
            print(f"  CLEAN           {case[0]:<20} {case[2]}")

    total = len(planted)
    print("\n" + "-" * 68)
    print(f"Detection rate: {caught}/{total} planted defects caught")
    print(f"False positives: {false_positives}/{len(controls)} controls")
    print("-" * 68)

    print("\nNot covered by this test — these gates need an agent, not a script:")
    print("  G1 fact audit    — re-fetching primary sources to confirm a figure is true")
    print("  G4 judgment      — whether a claim is defensible under hostile review")
    print("  Fresh-context    — whether Verifier/Red-team were actually run uncontaminated")
    print("A green run here means the automated gates work. It does not mean the")
    print("harness is working; that requires running a real project through the loop.")

    failed = missed + false_positives
    if failed:
        print(f"\nRESULT: FAIL — {missed} missed, {false_positives} false positive(s)")
        return 1
    print(f"\nRESULT: PASS — all {total} planted defects caught, no false positives")
    return 0


if __name__ == "__main__":
    sys.exit(main())
