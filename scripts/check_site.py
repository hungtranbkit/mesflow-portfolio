#!/usr/bin/env python3
"""Verify static portfolio route coverage and public-safety labeling."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
projects = json.loads((root / "data" / "projects.json").read_text())
assert len(projects) >= 20, "Expected 20+ projects"
slugs = [p["slug"] for p in projects]
assert len(set(slugs)) == len(slugs), "Duplicate slug"
assert (root / "index.html").exists()
js = (root / "assets" / "app.js").read_text()
assert "demo-warning" in js and "Đặt lại dữ liệu mẫu" in js
assert "https://zalo.me/0942591888" in js
for p in projects:
    assert p["phase"] in {"product", "beta", "demo", "development", "prototype", "internal", "research"}
    assert len(p["steps"]) == 4
    assert p["sample"] and p["description"] and p["capabilities"]
    for rel in [f"projects/{p['slug']}/index.html", f"projects/{p['slug']}/demo/index.html"]:
        txt = (root / rel).read_text()
        assert 'data-project="'+p["slug"]+'"' in txt
        assert "app.js" in txt and "style.css" in txt
screenshot_projects = 0
screenshot_files = set()
for p in projects:
    shots = p.get("screenshots", [])
    assert isinstance(shots, list), f"Invalid screenshots array in {p['slug']}"
    if shots:
        screenshot_projects += 1
    for shot in shots:
        src = shot.get("src", "")
        assert src.startswith("assets/screenshots/") and ".." not in src, src
        assert src.endswith(".png") and len(src) <= 120, src
        path = root / src
        assert path.is_file() and path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), src
        assert shot.get("kind") in {"public_demo", "test_evidence"}, src
        assert shot.get("caption") and shot.get("source") and shot.get("note"), src
        screenshot_files.add(src)
assert screenshot_projects >= 10, "Real screenshots need coverage of 10+ projects"
assert len(screenshot_files) >= 15, "Expected at least 15 verified screenshot assets"

for f in ["robots.txt", "sitemap.xml", ".nojekyll", "assets/favicon.svg"]:
    assert (root / f).exists()
assert len((root / "sitemap.xml").read_text().split("<url>")) - 1 == len(projects) * 2 + 1
print(f"PASS: {len(projects)} projects, {len(projects)*2} routes, {screenshot_projects} screenshot-covered projects ({len(screenshot_files)} photos).")
