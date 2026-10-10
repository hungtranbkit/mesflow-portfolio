#!/usr/bin/env python3
"""Run real-browser smoke checks against the public GitHub Pages portfolio.

Requires the optional local package playwright and installed Chromium.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = os.environ.get("PORTFOLIO_URL", "https://hungtranbkit.github.io/mesflow-portfolio/")
OUT = Path(os.environ.get("SCREENSHOT_DIR", "/tmp/portfolio-browser-evidence"))
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, height in [(1366, 768), (390, 844)]:
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        resp = page.goto(URL, wait_until="networkidle", timeout=45000)
        assert resp and resp.status == 200, f"Home HTTP {resp.status if resp else 'none'}"
        page.locator("#project-grid .catalog-card").first.wait_for(timeout=15000)
        total = page.locator("#project-grid .catalog-card").count()
        assert total == 25, (width, total)
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 1, f"Horizontal overflow at {width}px: {overflow}px"
        page.screenshot(path=str(OUT / f"home-{width}.png"), full_page=False)

        if width == 390:
            menu = page.locator("#menu-toggle")
            assert menu.is_visible(), "Mobile nav trigger invisible"
            menu.click()
            assert menu.get_attribute("aria-expanded") == "true"
            menu.click()

        page.locator('button[data-filter="ai"]').click()
        filtered = page.locator("#project-grid .catalog-card").count()
        assert 1 <= filtered < 25, (width, filtered)
        page.locator('button[data-filter="all"]').click()
        page.locator("#project-search").fill("Hint")
        assert page.locator("#project-grid .catalog-card").count() == 1
        page.locator("#project-grid h3 a").click()
        assert page.url.rstrip("/").endswith("/projects/hint")
        assert page.locator("h1").inner_text().strip().startswith("Hint")
        page.locator('a[href$="/projects/hint/demo/"]').first.click()
        assert page.url.rstrip("/").endswith("/projects/hint/demo")
        for _ in range(4):
            page.locator("#demo-next").click()
        assert page.locator("#demo-status").inner_text() == "HOÀN THÀNH"
        assert page.locator("#demo-percent").inner_text() == "100%"
        with page.expect_download() as info:
            page.locator("#demo-export").click()
        assert info.value.suggested_filename == "hint-demo.json"
        page.locator("#demo-reset").click()
        assert page.locator("#demo-percent").inner_text() == "0%"
        page.screenshot(path=str(OUT / f"demo-{width}.png"), full_page=False)
        assert not errors, errors
        print(f"PASS {width}x{height}: 25 cards, filter={filtered}, search/detail/demo/run/reset/export, overflow={overflow}, JS errors={len(errors)}")
        page.close()
    browser.close()
print("BROWSER_SMOKE_OK")
