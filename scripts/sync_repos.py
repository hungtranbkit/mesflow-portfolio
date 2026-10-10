#!/usr/bin/env python3
"""Daily safe GitHub -> static portfolio discovery. Only opted-in private repos publish.

No remote code is executed. Existing hand-curated projects are never overwritten.
"""
from __future__ import annotations
import argparse
import base64
import datetime as dt
import html
import json
import os
from pathlib import Path
import re
import sys
import unicodedata
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://hungtranbkit.github.io/mesflow-portfolio/"
API = "https://api.github.com"
CATEGORIES = {"operations": "Vận hành", "commerce": "Bán lẻ", "ai": "Dữ liệu & AI", "tools": "Công cụ", "engineering": "Kỹ thuật"}
PHASES = {"product": "Đang vận hành", "beta": "Beta công khai", "demo": "Có bản demo", "development": "Đang phát triển", "prototype": "Prototype", "internal": "Công cụ nội bộ", "research": "Nghiên cứu"}
ALIASES = {"mesflow": "mesflow", "mesflow-esp32-kiosk": "esp32-kiosk", "mesflow-qa-center": "mesflow-qa", "mesflow-agent": "deploy-agent", "projectflow-workspace-manager": "projectflow", "qr-restaurant": "qr-restaurant", "ai-design-council": "ai-design-council"}
EXCLUDED = {"mesflow-portfolio", "note"}
EXCLUDED_RE = re.compile(r"(^|[-_])(test|fixture|scratch|sandbox|playground|benchmark|backup|tmp)([-_]|$)|^fb[-_]")
SECRET_RE = re.compile(r"(?i)(ghp_[a-z0-9_]{12,}|github_pat_[a-z0-9_]{12,}|sk-[a-z0-9_-]{14,}|AIza[a-z0-9_-]{25,}|-----BEGIN .*PRIVATE KEY-----|(?:password|token|api.?key|secret)\s*[:=]\s*['\"]?\S+)")
STEPS = {
    "operations": ["Thiết lập quy trình mẫu", "Nhập thông tin vận hành", "Ghi nhận trạng thái", "Xem kết quả mô phỏng"],
    "commerce": ["Khởi tạo giao dịch mẫu", "Nhập thông tin giao dịch", "Kiểm tra luồng xử lý", "Tổng hợp kết quả"],
    "ai": ["Nhập dữ liệu phân tích", "Chuẩn hóa dữ liệu mẫu", "Chạy luồng mô phỏng", "Xem kết quả minh họa"],
    "tools": ["Tạo tác vụ thử nghiệm", "Thiết lập các thông số", "Chạy quy trình mô phỏng", "Xem nhật ký và kết quả"],
    "engineering": ["Chọn cấu hình kỹ thuật", "Thiết lập thông số mẫu", "Đánh giá quy trình minh họa", "Xem kết quả mô phỏng"],
}
CAPS = {
    "operations": ["Tổ chức quy trình vận hành", "Quản lý thông tin công việc", "Theo dõi trạng thái"],
    "commerce": ["Số hóa nghiệp vụ", "Tổ chức dữ liệu giao dịch", "Thiết kế trải nghiệm người dùng"],
    "ai": ["Xử lý và tổ chức dữ liệu", "Thiết kế luồng phân tích", "Trình bày kết quả có cấu trúc"],
    "tools": ["Công cụ hỗ trợ kỹ thuật", "Tổ chức luồng thao tác", "Theo dõi trạng thái và kết quả"],
    "engineering": ["Thiết kế cấu hình kỹ thuật", "Tổ chức quy trình kiểm tra", "Hỗ trợ phân tích và thử nghiệm"],
}
SAMPLES = {"operations": "Quy trình vận hành mẫu · 4 bước", "commerce": "Giao dịch minh họa · dữ liệu giả lập", "ai": "Yêu cầu phân tích · dữ liệu giả lập", "tools": "Tác vụ kỹ thuật · dữ liệu mẫu", "engineering": "Cấu hình thiết kế · thông số mẫu"}
TECH = [("TypeScript", r"\btypescript\b"), ("Python", r"\bpython\b"), ("React", r"\breact\b"), ("Next.js", r"\bnext\.?js\b"), ("FastAPI", r"\bfastapi\b"), ("ESP32", r"\besp32\b"), ("PostgreSQL", r"\bpostgres(ql)?\b"), ("SQLite", r"\bsqlite\b"), ("Docker", r"\bdocker\b"), ("MCP", r"\bmcp\b"), ("Playwright", r"\bplaywright\b"), ("Git", r"\bgit\b")]
CATEGORY_RULES = [
    ("engineering", r"esp32|firmware|hardware|composite|filament|winding|finite.element|structural|mechanic"),
    ("tools", r"mcp|terminal|developer|workspace|cli|deploy|testing|framework|infra|automation"),
    ("ai", r"\bai\b|\bllm\b|\bagent\b|data|radar|intelligence|vision|crawler|property|chatbot"),
    ("commerce", r"retail|restaurant|\bpos\b|commerce|shop|sale|inventory"),
    ("operations", r"mesflow|production|factory|manufactur|maintenance|industrial|kiosk"),
]

def api_json(path, token="", optional=False):
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "mesflow-portfolio-sync"}
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        with urlopen(Request(API + path, headers=headers), timeout=25) as response:
            return json.load(response)
    except HTTPError as exc:
        if optional and exc.code == 404:
            return None
        raise RuntimeError(f"GitHub API HTTP {exc.code}") from None

def github_repositories(owner, token):
    can_see_private = False
    if token:
        try:
            can_see_private = api_json("/user", token).get("login", "").lower() == owner.lower()
        except (RuntimeError, AttributeError):
            pass
    endpoint = ("/user/repos?affiliation=owner&sort=pushed&per_page=100&page=" if can_see_private
                else f"/users/{quote(owner)}/repos?type=owner&sort=pushed&per_page=100&page=")
    result = []
    for page in range(1, 11):
        chunk = api_json(endpoint + str(page), token)
        if not isinstance(chunk, list):
            raise RuntimeError("Invalid GitHub list response")
        result.extend(r for r in chunk if (r.get("owner") or {}).get("login", "").lower() == owner.lower())
        if len(chunk) < 100:
            break
    return result, can_see_private

def github_file(owner, name, filename, token):
    suffix = "readme" if filename == "README" else "contents/" + quote(filename, safe="")
    obj = api_json(f"/repos/{quote(owner)}/{quote(name)}/{suffix}", token, optional=True)
    if not isinstance(obj, dict) or obj.get("encoding") != "base64":
        return ""
    try:
        return base64.b64decode(obj["content"])[:180000].decode("utf-8", "replace")
    except (ValueError, TypeError, KeyError):
        return ""

def public_text(value, maxlen=230):
    if not isinstance(value, str):
        return ""
    if SECRET_RE.search(value):
        return ""
    value = re.sub(r"https?://\S+", "", value)
    value = re.sub(r"\[[^\]]+\]\([^)]+\)", "", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[*_~#]", "", value).replace(chr(96), "")
    value = re.sub(r"\s+", " ", "".join(c for c in value if c.isprintable())).strip(" \t;:-")
    return value[:maxlen].strip()

def public_url(value):
    if not isinstance(value, str) or len(value) > 240:
        return ""
    try:
        parsed = urlsplit(value)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            return ""
        if parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
            return ""
        return value
    except ValueError:
        return ""

def slug(value):
    s = unicodedata.normalize("NFKD", str(value))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:65]

def allowed_repo(r):
    name = str(r.get("name", "")).lower()
    return bool(re.fullmatch(r"[a-z0-9_.-]{2,80}", name) and name not in ALIASES
                and name not in EXCLUDED and not EXCLUDED_RE.search(name)
                and not any(r.get(k) for k in ["fork", "archived", "disabled", "is_template"]))

def human_title(name, readme):
    for line in readme.splitlines()[:60]:
        if line.startswith("# "):
            title = public_text(line[2:], 72)
            if len(title) >= 3:
                return title
    uppercase = {"ai", "pos", "mcp", "qa", "qr", "esp32", "cad", "crm", "api"}
    return " ".join(x.upper() if x in uppercase else x.capitalize() for x in re.split("[-_]+", name))

def readme_summary(readme):
    # Prefer product-purpose prose over setup instructions or LLM-directed notices.
    section = re.search(r"(?im)^##\s*(purpose|overview|giới thiệu|tổng quan|what it does)\s*$", readme)
    if section:
        readme = readme[section.end():]
    lines, blocks, fenced = [], [], False
    for raw in readme.splitlines()[:115]:
        s = raw.strip()
        if s.startswith(chr(96)*3) or s.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if not s or s.startswith(("#", ">", "-", "*", "|", "<", "![", "[!", "$", "./")):
            if lines:
                blocks.append(" ".join(lines))
                lines = []
            continue
        if s.startswith(("**If you", "If you are", "Read ", "**Read")) or "http" in s or "@" in s:
            continue
        if len(s) > 22:
            lines.append(s)
    if lines:
        blocks.append(" ".join(lines))
    for paragraph in blocks:
        clean = public_text(paragraph, 220)
        if len(clean) >= 50:
            return clean
    return ""

def manifest_for(repo, owner, token, fixture):
    if fixture:
        value = repo.get("manifest") or {}
        return value if isinstance(value, dict) else {}
    raw = github_file(owner, repo["name"], "portfolio.public.json", token)
    if len(raw) > 18000:
        return {}
    try:
        result = json.loads(raw) if raw else {}
        return result if isinstance(result, dict) else {}
    except ValueError:
        return {}

def select_category(name, summary, readme, manifest):
    if manifest.get("category") in CATEGORIES:
        return manifest["category"]
    haystack = (name + " " + summary + " " + readme[:1500]).lower()
    for key, pattern in CATEGORY_RULES:
        if re.search(pattern, haystack):
            return key
    return "tools"

def curated_list(manifest, key, default):
    arr = manifest.get(key)
    if isinstance(arr, list):
        clean = [public_text(x, 110) for x in arr[:6]]
        clean = [x for x in clean if x]
        if key == "steps" and len(clean) == 4:
            return clean
        if key == "capabilities" and len(clean) >= 2:
            return clean[:4]
    return list(default)

def project_for(repo, readme, manifest, owner):
    private = bool(repo.get("private"))
    name = repo["name"]
    title = public_text(manifest.get("name"), 72) or human_title(name, readme)
    desc = (public_text(manifest.get("summary"), 230)
            or ("" if private else public_text(repo.get("description"), 230) or readme_summary(readme)))
    if not desc:
        return None
    category = select_category(name, desc, "" if private else readme, manifest)
    phase = manifest.get("phase") if manifest.get("phase") in PHASES else "development"
    if "phase" not in manifest and re.search(r"(?i)do not deploy|not production.ready|experimental|prototype|proof.of.concept", readme[:3500]):
        phase = "prototype"
    name_slug = slug(manifest.get("slug") or name)
    if len(name_slug) < 2:
        return None
    acr = "".join(c[0].upper() for c in re.split(r"[-_\s]+", title) if c)
    visual = public_text(manifest.get("visual"), 6).upper() or acr[:4] or "APP"
    if isinstance(manifest.get("stack"), list):
        stack = [public_text(x, 25) for x in manifest["stack"][:4]]
        stack = [x for x in stack if x]
    else:
        stack = [tech for tech, rx in TECH if re.search(rx, readme, re.I)][:4]
    return {
        "slug": name_slug, "name": title,
        "categoryLabel": CATEGORIES[category], "category": category,
        "phase": phase, "phaseLabel": PHASES[phase],
        "tagline": public_text(manifest.get("tagline"), 120) or desc[:115].rstrip(" ,;."),
        "description": desc, "website": public_url(manifest.get("website")),
        "featured": False, "visual": visual[:6],
        "sample": public_text(manifest.get("sample"), 120) or SAMPLES[category],
        "steps": curated_list(manifest, "steps", STEPS[category]),
        "capabilities": curated_list(manifest, "capabilities", CAPS[category]),
        "stack": stack or ["Software"],
        "sourceUrl": "" if private else f"https://github.com/{owner}/{name}",
    }

def page_for(p, demo=False):
    relative = "../../../" if demo else "../../"
    title = ("Demo " if demo else "") + p["name"] + " — MESFlow Lab"
    url = BASE + "projects/" + p["slug"] + "/" + ("demo/" if demo else "")
    esc = lambda s: html.escape(str(s), quote=True)
    about = "Demo dùng dữ liệu mẫu trong trình duyệt, không kết nối hệ thống thật." if demo else p["description"]
    return (
        '<!doctype html>\n<html lang="vi"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta name="theme-color" content="#f7f8f5">\n<title>' + esc(title) + '</title>\n'
        '<meta name="description" content="' + esc(about[:230]) + '">\n'
        '<meta property="og:type" content="website"><meta property="og:locale" content="vi_VN">\n'
        '<meta property="og:title" content="' + esc(title) + '">\n'
        '<meta property="og:description" content="' + esc(p["tagline"]) + '">\n'
        '<meta property="og:url" content="' + url + '">\n'
        '<meta property="og:image" content="' + BASE + 'assets/social-card.svg">\n'
        '<link rel="canonical" href="' + url + '">\n'
        '<link rel="icon" href="' + relative + 'assets/favicon.svg" type="image/svg+xml">\n'
        '<link rel="stylesheet" href="' + relative + 'assets/style.css">\n'
        '<script src="' + relative + 'assets/app.js" defer></script>\n'
        '</head><body data-view="' + ("demo" if demo else "detail") +
        '" data-project="' + esc(p["slug"]) + '"><div id="app">\n'
        '<main class="container loading" id="main"><h1>' + esc(p["name"]) +
        '</h1><p>' + esc(about) + '</p><p>Đang tải nội dung…</p></main></div>\n'
        '<noscript><p>Cần JavaScript để xem nội dung hoặc demo tương tác.</p></noscript>\n'
        '</body></html>\n'
    )

def sitemap_for(projects):
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    urls = [BASE]
    for p in projects:
        detail = BASE + "projects/" + p["slug"] + "/"
        urls.extend([detail, detail + "demo/"])
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(f"  <url><loc>{html.escape(url)}</loc><lastmod>{today}</lastmod></url>" for url in urls)
            + "\n</urlset>\n")

def sync(root, owner, repos, token="", apply=False, fixture=False):
    file = root / "data" / "projects.json"
    existing = json.loads(file.read_text(encoding="utf-8"))
    seen = {p["slug"] for p in existing}
    seen_sources = {p.get("sourceUrl", "").rsplit("/", 1)[-1].lower()
                    for p in existing if p.get("sourceUrl")}
    additions = []
    candidate_count = 0
    skipped_private = 0
    for repo in sorted(repos, key=lambda x: str(x.get("name", ""))):
        if str((repo.get("owner") or {}).get("login", owner)).lower() != owner.lower():
            continue
        name = str(repo.get("name", ""))
        if not allowed_repo(repo) or name.lower() in seen_sources or name in seen:
            continue
        if not repo.get("private") and int(repo.get("size", 0) or 0) < 30:
            continue
        candidate_count += 1
        manifest = manifest_for(repo, owner, token, fixture)
        if manifest.get("publish") is False:
            continue
        if repo.get("private"):
            if manifest.get("publish") is not True:
                skipped_private += 1
                continue
            if not public_text(manifest.get("summary")):
                continue
            readme = ""  # do not read or publish any private README content
        else:
            readme = str(repo.get("readme", "")) if fixture else github_file(owner, name, "README", token)
            if manifest.get("publish") is not True and len(readme) < 320:
                continue
        item = project_for(repo, readme, manifest, owner)
        if not item or item["slug"] in seen:
            continue
        seen.add(item["slug"])
        additions.append(item)
    if apply and additions:
        for p in additions:
            if (root / "projects" / p["slug"]).exists():
                raise RuntimeError("Existing project route; will not overwrite: " + p["slug"])
        for p in additions:
            dest = root / "projects" / p["slug"]
            (dest / "demo").mkdir(parents=True)
            (dest / "index.html").write_text(page_for(p), encoding="utf-8")
            (dest / "demo" / "index.html").write_text(page_for(p, demo=True), encoding="utf-8")
        merged = existing + additions
        file.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (root / "sitemap.xml").write_text(sitemap_for(merged), encoding="utf-8")
    status = "UPDATED" if apply and additions else ("DRY_RUN" if not apply else "NO_CHANGES")
    print(f"{status}: existing={len(existing)}, discovered={len(additions)}, "
          f"candidates={candidate_count}, private_without_opt_in={skipped_private}")
    for p in additions:
        print(f" + {p['name']} ({p['slug']}, {p['phaseLabel']})")
    return additions

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="hungtranbkit")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--fixture", type=Path, help="JSON fixture instead of GitHub API, for offline tests")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9-]{1,39}", args.owner):
        parser.error("Invalid owner")
    token = os.getenv("PORTFOLIO_SYNC_TOKEN") or os.getenv("GITHUB_TOKEN", "")
    if args.fixture:
        repos = json.loads(args.fixture.read_text(encoding="utf-8"))["repos"]
        private_access = False
    else:
        repos, private_access = github_repositories(args.owner, token)
    print(f"Scan: {len(repos)} repositories; private_access={'yes' if private_access else 'no'}")
    sync(args.root, args.owner, repos, token, apply=args.apply, fixture=bool(args.fixture))

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"SYNC_FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
