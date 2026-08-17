#!/usr/bin/env python3
"""G3 security gate: secret scan. UNWAIVABLE (spec §3.3).
Usage: python g3_secret_scan.py [path] [--history]
Scans tracked/working files for secret patterns, committed .env files,
and key patterns in built client bundles. --history also greps git history.
Exit 1 on any finding (SEV1)."""
import re, sys, subprocess
from pathlib import Path

PATTERNS = {
    "Google API key": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    "OpenAI/Anthropic-style key": re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9\-_]{20,}"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Generic assignment": re.compile(r"(?i)(?:api_key|apikey|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9\-_/+]{16,}['\"]"),
}
ALLOW = re.compile(r"(?i)YOUR_|\bMY_|example|placeholder|xxxx|<[^>]+>|process\.env|os\.environ|getenv")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
TEXT_EXT = {".js", ".ts", ".tsx", ".jsx", ".py", ".html", ".css", ".json", ".yaml", ".yml",
            ".md", ".txt", ".env", ".sh", ".toml", ".cfg", ".ini", ".xml", ".svelte", ".vue"}
BUNDLE_DIRS = {"dist", "build", "docs", "out", ".next", "public"}

def files(root: Path):
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name.endswith(".example") or p.name.endswith(".sample"):
            continue  # sanctioned placeholder convention (.env.example etc.)
        if p.is_file() and (p.suffix.lower() in TEXT_EXT or p.name.startswith(".env")):
            yield p

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0]) if args else Path(".")
    findings = []
    for p in files(root):
        if p.name.startswith(".env") and p.suffix != ".example":
            tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(p)],
                                     cwd=root, capture_output=True)
            if tracked.returncode == 0:
                findings.append(f"[COMMITTED ENV FILE] {p}")
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        in_bundle = any(d in p.parts for d in BUNDLE_DIRS)
        for name, pat in PATTERNS.items():
            for m in pat.finditer(text):
                line = text[:m.start()].count("\n") + 1
                ctx = text.splitlines()[line - 1][:120]
                if ALLOW.search(ctx):
                    continue
                tag = " [IN CLIENT BUNDLE]" if in_bundle else ""
                findings.append(f"[{name}]{tag} {p}:{line}: {ctx.strip()[:80]}")
    if "--history" in sys.argv:
        log = subprocess.run(["git", "log", "-p", "--all", "--no-color"],
                             cwd=root, capture_output=True, text=True, errors="ignore")
        for name, pat in PATTERNS.items():
            for m in pat.finditer(log.stdout or ""):
                snippet = log.stdout[max(0, m.start()-40):m.end()+10].replace("\n", " ")
                if not ALLOW.search(snippet):
                    findings.append(f"[HISTORY: {name}] …{snippet[:100]}…")
    if findings:
        print("G3 SECRET SCAN: FAIL (SEV1 — file X1 defect)")
        for f in findings[:50]:
            print("  " + f)
        sys.exit(1)
    print("G3 SECRET SCAN: PASS")

if __name__ == "__main__":
    main()
