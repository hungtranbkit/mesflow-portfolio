# MESFlow Lab — Project Portfolio

Public, static portfolio for **Hùng Trần / MESFlow Lab**. Lists **25 selected projects**, across production operations, retail, data/AI, developer tools, and engineering R&D.

## Public pages
- Landing page with featured work, searchable/filterable full catalogue, engineering profile and contact
- One static case-study page for each project: `/projects/<slug>/`
- One self-contained browser simulation for each: `/projects/<slug>/demo/`
- No authentication, database, tracking pixel or AI API. All demo records are visibly fictional and resettable.
- Explicit status labels: **production/beta/demo/development/prototype/internal/research** are not conflated.
- `data/projects.json` is the source of truth for all projects, including optional external site links (only when grounded).
- `sitemap.xml`, per-page SEO metadata, responsive/mobile layout and reduced-motion support.

## Development
No install or build step:
```bash
python3 -m http.server 8008
python3 scripts/check_site.py
```
Open `http://localhost:8008/`. Static route folders are generated so GitHub Pages can load details and demos directly.

## Deployment
GitHub Pages via `main` / `/`:
`https://hungtranbkit.github.io/mesflow-portfolio/`

Custom hostname such as `portfolio.mesflow.net` requires DNS configuration and a verified GitHub Pages domain; do not announce it as live before testing.

## Boundaries
Portfolio demos are **educational simulations**, not live applications. Product URLs are listed separately from demos, if known.
Private/internal tools are presented at a conceptual level without links to internal dashboards, credentials, data, or infrastructure.

## Contacts
- Zalo: 0942 591 888 (owner-provided public contact)
- GitHub: https://github.com/hungtranbkit

## Automatic daily project discovery

GitHub Actions now runs **every day at 08:17 Vietnam time** (01:17 UTC), plus manual dispatch. It discovers qualified public repositories, adds case-study/demo routes, updates the sitemap, validates the site and publishes via GitHub Pages. Existing curated projects are left untouched; no duplicate slugs.

**Private repos are never auto-publicized.** An owner-scoped read-only `PORTFOLIO_SYNC_TOKEN` and a per-repo `portfolio.public.json` containing `"publish":true` are both required. The README of a private repo is not copied or summarized.

See [Daily sync runbook](docs/DAILY_SYNC.md) for setup, exclusion policy, the opt-in manifest, tests and manual run instructions.

```bash
python3 -m unittest discover -s scripts -p 'test_repo_sync.py' -v
python3 scripts/sync_repos.py --owner hungtranbkit  # dry-run
python3 scripts/sync_repos.py --owner hungtranbkit --apply
```
