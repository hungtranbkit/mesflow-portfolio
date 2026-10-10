#!/usr/bin/env python3
"""Offline regression tests for the unattended portfolio crawler."""
import json
from pathlib import Path
import tempfile
import unittest
from sync_repos import allowed_repo, page_for, project_for, public_text, readme_summary, sync

OWNER = "hungtranbkit"
README = """# Example Workflow Toolkit

## Purpose

Example Workflow Toolkit is a complete workflow management tool that offers an
interactive dashboard, a command-line interface and a clear way to inspect
operations. It has independent modules for data retrieval, logging and reporting.

## Features
- TypeScript interface
- Python service
- Docker deployment
- Audit logs and tests
"""

def repo(name, **kwargs):
    record = {
        "name": name, "private": False, "size": 100,
        "fork": False, "archived": False,
        "owner": {"login": OWNER},
        "description": "Công cụ tổ chức quy trình và quan sát trạng thái kỹ thuật.",
        "readme": README,
    }
    record.update(kwargs)
    return record

class PortfolioSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "data").mkdir()
        (self.root / "projects").mkdir()
        self.existing = {
            "slug": "mesflow", "name": "MESFlow",
            "sourceUrl": "https://github.com/hungtranbkit/mesflow",
        }
        (self.root / "data" / "projects.json").write_text(
            json.dumps([self.existing]), encoding="utf-8"
        )
        (self.root / "sitemap.xml").write_text("original", encoding="utf-8")
        self.repos = [
            repo("mesflow"),
            repo("projectflow-workspace-manager"),
            repo("note"),
            repo("tiny-repo", size=1),
            repo("fork-experiment", fork=True),
            repo("new-toolkit"),
            repo("new-private", private=True, readme="PRIVATE DATA", manifest={}),
            repo("optin-private", private=True, readme="DO NOT PUBLISH THIS README",
                 manifest={"publish": True,
                           "name": "Private Project Case Study",
                           "summary": "Mô tả công khai đã được người sở hữu duyệt để đăng.",
                           "steps": ["Bước A", "Bước B", "Bước C", "Bước D"]}),
        ]

    def test_private_guardrails(self):
        self.assertFalse(allowed_repo(repo("note")))
        self.assertFalse(allowed_repo(repo("mesflow")))
        self.assertFalse(allowed_repo(repo("fork-project", fork=True)))
        self.assertEqual(public_text("api_key=sk-SUPERSECRETSUPERSECRET"), "")
        rendered = page_for({"name": "<script>", "slug": "safe", "description": "desc",
                             "tagline": "good"}, demo=False)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn("<h1><script>", rendered)

    def test_dry_run_does_not_write(self):
        result = sync(self.root, OWNER, self.repos, fixture=True)
        self.assertEqual({x["slug"] for x in result}, {"new-toolkit", "optin-private"})
        self.assertEqual((self.root / "sitemap.xml").read_text(), "original")
        self.assertFalse((self.root / "projects/new-toolkit").exists())
        self.assertEqual(len(json.loads((self.root / "data/projects.json").read_text())), 1)

    def test_apply_generates_and_remains_idempotent(self):
        result = sync(self.root, OWNER, self.repos, apply=True, fixture=True)
        self.assertEqual(len(result), 2)
        entries = json.loads((self.root / "data/projects.json").read_text())
        self.assertEqual(len(entries), 3)
        private = next(x for x in entries if x["slug"] == "optin-private")
        self.assertEqual(private["sourceUrl"], "")
        self.assertNotIn("DO NOT PUBLISH", json.dumps(private))
        self.assertEqual(len(private["steps"]), 4)
        public = next(x for x in entries if x["slug"] == "new-toolkit")
        self.assertEqual(public["sourceUrl"], "https://github.com/hungtranbkit/new-toolkit")
        for item in entries[1:]:
            for rel in ("index.html", "demo/index.html"):
                txt = (self.root / "projects" / item["slug"] / rel).read_text()
                self.assertIn('data-project="' + item["slug"] + '"', txt)
                self.assertIn("app.js", txt)
        self.assertEqual((self.root / "sitemap.xml").read_text().count("<url>"), 7)
        first_bytes = (self.root / "data/projects.json").read_bytes()
        self.assertEqual(sync(self.root, OWNER, self.repos, apply=True, fixture=True), [])
        self.assertEqual((self.root / "data/projects.json").read_bytes(), first_bytes)

    def test_secret_manifest_not_published(self):
        bad = repo("private-secret", private=True,
                   manifest={"publish": True, "name": "Sensitive",
                             "summary": "token=ghp_FAKE_SUPER_LONG_DO_NOT_PUBLISH"})
        self.assertEqual(sync(self.root, OWNER, [bad], apply=True, fixture=True), [])
        self.assertEqual(len(json.loads((self.root / "data/projects.json").read_text())), 1)

    def test_readme_purpose_overrides_setup_notice(self):
        readme = "# Demo\n\n**If you are an agent**, run setup first.\n\nserver to USE it rather than modify it.\n\n## Purpose\n\nThis tool manages independent execution sessions and provides reliable structured status reporting for developers.\n"
        summary = readme_summary(readme)
        self.assertIn("manages independent execution", summary)
        self.assertNotIn("server to USE", summary)

    def test_prototype_label(self):
        item = project_for(repo("new-kiosk"), README + "\nDO NOT DEPLOY TO PRODUCTION.",
                           {}, OWNER)
        self.assertEqual(item["phase"], "prototype")

if __name__ == "__main__":
    unittest.main(verbosity=2)
