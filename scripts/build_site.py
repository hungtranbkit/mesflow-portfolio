#!/usr/bin/env python3
"""Build allowlisted static site artifact; never publish .git, scripts, or secrets."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for name in ["index.html", "404.html", "robots.txt", "sitemap.xml",
             "manifest.webmanifest", ".nojekyll"]:
    src = ROOT / name
    if src.is_file():
        shutil.copy2(src, OUT / name)
shutil.copytree(ROOT / "assets", OUT / "assets")
(OUT / "data").mkdir()
shutil.copy2(ROOT / "data" / "projects.json", OUT / "data" / "projects.json")
for project_dir in (ROOT / "projects").iterdir():
    if not project_dir.is_dir():
        continue
    for relative in ["index.html", "demo/index.html"]:
        src = project_dir / relative
        if src.is_file():
            target = OUT / "projects" / project_dir.name / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
assert not (OUT / ".git").exists()
assert not (OUT / "scripts").exists()
assert not (OUT / "PROJECT_CONTEXT.md").exists()
assert (OUT / "assets" / "app.js").is_file()
print("Static publish artifact:", OUT)
