# PROJECT_CONTEXT — MESFlow Portfolio

Last updated: 2026-10-10
Owner: hungtranbkit / MESFlow Lab
Repository: hungtranbkit/mesflow-portfolio
Intended public origin: https://hungtranbkit.github.io/mesflow-portfolio/

## Product definition
An editorial landing page and case-study/demo hub for 25 meaningful projects chosen from the owner's larger GitHub workspace. Excludes test repos, third-party experiments with no delivered implementation, and credential-sensitive workflows.

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
