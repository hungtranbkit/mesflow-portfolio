# PROJECT_CONTEXT — MESFlow Portfolio

Last updated: 2026-10-10
Owner: hungtranbkit / MESFlow Lab
Repository: hungtranbkit/mesflow-portfolio
Intended public origin: https://hungtranbkit.github.io/mesflow-portfolio/

## Product definition
An editorial landing page and case-study/demo hub for 27 currently catalogued projects chosen from the owner's larger GitHub workspace. Excludes test repos, third-party experiments with no delivered implementation, and credential-sensitive workflows.

## Architecture
Pure static HTML + CSS + JavaScript. No npm dependencies, build step, server-side auth, DB or live AI calls.
- `data/projects.json` drives all visible project content, status, filters, captions and stepper simulations.
- `assets/app.js` renders home/detail/demo based on `body[data-view]` and `body[data-project]`.
- `assets/style.css` is the responsive design system.
- `projects/<slug>/{index.html,demo/index.html}` generated landing/demo routes.
- GitHub Pages base path is auto-detected; works at root custom origin as well.
- `scripts/check_site.py` verifies data and routes.

## Privacy/commercial boundary
Each demo is labelled *browser-only simulation*, seeded with fictional labels, resettable, optional JSON log export.
No internal login flow is exposed. External product URLs only when established. Technical claims sourced from repos and prior project records; status intentionally conservative.

## Verification / release checklist
- Run `python3 scripts/check_site.py`.
- Run `node --check assets/app.js`.
- Confirm GitHub Pages active and HTTP 200 for home, nested detail, nested demo, project JSON and CSS.
- Browser-check responsive 390px / 1366px, catalogue search/filter, demo run/reset/export.
- Do not claim custom hostname live until DNS + HTTPS verified.

## Future work
- Replace CSS mockups with screenshots after owner approves which live screenshots may be public.
- Add testimonials/case studies only with verified evidence and permission.
- Optionally attach a verified `portfolio.mesflow.net` DNS after public test.
- Keep project phase labels and URLs synchronized with production releases.

## Scheduled GitHub repository discovery (2026-10-10)
- Entrypoint: `scripts/sync_repos.py` standard-library-only, idempotent, does not execute remote README/code. Skips forks, archived, test/empty repos; public repo README quality gate; hand-curated existing aliases protected.
- Private: only repo-owner token and explicit `portfolio.public.json` (`publish:true` + safe summary); private README not ingested; private source links not exposed. `PORTFOLIO_SYNC_TOKEN` optional GitHub Actions secret, not configured by code. Without it the daily scan only sees public repos.
- Pages: `.github/workflows/daily-portfolio-sync.yml` scheduled at 01:17 UTC (08:17 Vietnam), push, manual dispatch. One workflow discovers/commits and deploys the same tested site artifact, avoiding GITHUB_TOKEN pushes failing to trigger legacy Pages builds.
- `scripts/build_site.py` allowlists public site files and excludes the workspace, logs, scripts, `.git`, and secrets.
- `scripts/test_repo_sync.py` covers private opt-in, rejection of unapproved private/short/fork/test repos, URL escaping, route generation and idempotency.
- Public repo case studies may show source links. Existing projects remain unchanged.
- Docs `docs/DAILY_SYNC.md` describe opt-in and runbooks.
- Release gate: unit tests + catalog route checker + `node --check assets/app.js`. Manual dry-run confirmed two previously unlisted public candidates: Terminal MCP and MESFlow Kiosk Runtime v2.
- Release verified: PR #1 merged (aabdf855), GitHub Pages build_type=workflow; manual workflow_dispatch #38023301049 completed successfully (scan + deploy), catalog now 27 entries with Terminal MCP and MESFlow Kiosk Runtime v2, live HTTP 200 on home, detail and demo. Future schedule 08:17 ICT.

## Follow-up content quality (2026-10-10)
- Corrected the two first auto-discovered project summaries into grounded Vietnamese copy, including an explicit non-production warning for Kiosk Runtime v2.
- README parser now prioritizes Purpose / Overview headings to avoid treating tool-usage instructions as product descriptions.
- Re-run the daily workflow after merging updates to publish the new content.

## Verified UI screenshot gallery (2026-10-10)
- 16 vetted PNG screenshots mapped through data/projects.json screenshots[] on 13/27 projects.
- Cards and case-study hero display real images, with a full-resolution gallery per project; missing photos have an explicit placeholder, not generated app UI.
- Each image has descriptive provenance; screenshots from private project evidence were reviewed to avoid confidential information. No private repo URLs are exposed.
- scripts/check_site.py validates PNG signature, local path, caption, source and type; GitHub Pages serves images from assets/screenshots.
- Remaining 14 projects without verified images listed in docs/SCREENSHOTS.md. Automatic daily repo sync will not extract or publish private screenshots without review.
