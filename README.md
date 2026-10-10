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
