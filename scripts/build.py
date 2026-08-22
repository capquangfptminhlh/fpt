import os
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    os.environ["PYTHONUTF8"] = "1"

root = Path(__file__).resolve().parent.parent
site_dir = root / "_site"

print("--> 1. Cleaning and preparing _site folder...")
if site_dir.exists():
    shutil.rmtree(site_dir)
site_dir.mkdir(parents=True, exist_ok=True)

# Copy assets and files
for item in root.iterdir():
    if item.name in [".git", ".github", "_site", "node_modules", "scripts", "seo", "data", ".gitignore", "package.json", "package-lock.json", "server.js", "README.md", "QA_REPORT.md"]:
        continue
    if item.is_dir():
        shutil.copytree(item, site_dir / item.name)
    else:
        shutil.copy2(item, site_dir / item.name)

# Ensure data and seo exist if needed by scripts
scripts = [
    ["python", "scripts/generate-local-keywords.py"],
    ["python", "scripts/generate-local-pages.py", "--site", "_site"],
    ["python", "scripts/enrich-local-silos.py", "--site", "_site"],
    ["python", "scripts/upgrade-local-catalog.py", "--site", "_site"],
    ["python", "scripts/expand-local-plan-details.py", "--site", "_site"],
    ["python", "scripts/add-local-current-offerings.py", "--site", "_site"],
    ["python", "scripts/fix-local-nav.py", "--site", "_site"],
    ["python", "scripts/prepare-pages.py", "--site", "_site"],
    ["python", "scripts/inject-trust-footer.py", "--site", "_site"],
    ["python", "scripts/inject-contact-dock.py", "--site", "_site"],
    ["python", "scripts/sync-sitemap.py", "--site", "_site", "--origin", "https://capquangfptminhlh.github.io/fpt"],
    ["python", "scripts/complete-official-catalog.py", "--site", "_site"],
    ["python", "scripts/enrich-local-editorial.py", "--site", "_site"],
    ["python", "scripts/premiumize-local-catalog.py", "--site", "_site"],
]

for cmd in scripts:
    print(f"--> Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=root, env={**os.environ, "PYTHONUTF8": "1"}, capture_output=True, text=True, encoding="utf-8")
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0:
        print(f"ERROR: {res.stderr.strip()}", file=sys.stderr)
        sys.exit(res.returncode)

print("\n✅ BUILD COMPLETE! Total pages in _site:")
html_count = len(list(site_dir.rglob("*.html")))
print(f"Total HTML files: {html_count}")
