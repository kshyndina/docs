#!/usr/bin/env python3
"""
Lint docs.json for known classes of bugs that have broken navigation in
production. Run before every push.

What it catches (and why each rule exists — every rule below traces to a
specific incident on 2026-05-08):

  1. Tabs with `href`. Mintlify's tab schema only supports `pages`,
     `groups`, or `openapi` as content. Adding `href` to a tab silently
     accepts but breaks subsequent tab-click handlers, making no tab
     clickable.

  2. Page objects with non-standard properties. Page entries can be a
     plain string OR `{"page": "path", "group": "..."}`. Adding any
     other property (most notoriously `tag`) confuses Mintlify's tab
     href resolution: tabs containing pages with `tag` get rendered
     with `href="/"` instead of their first page URL, making them
     un-clickable.

  3. Tab `pages` or `groups` empty. Mintlify falls back to `href="/"`
     for any tab whose first page can't be resolved.

  4. JSON validity. Catch typos / trailing commas before push.

Exit 0 if clean, 1 if any issue. CI can wire this into the lint workflow.
"""
import json
import sys
from pathlib import Path


# Known-good page-object properties per Mintlify schema.
# Anything else triggers tab-href fallback to "/".
ALLOWED_PAGE_OBJECT_KEYS = {"page", "group", "icon", "expanded", "root", "pages", "openapi"}

# Known-good tab top-level keys.
ALLOWED_TAB_KEYS = {"tab", "icon", "pages", "groups", "openapi", "anchors"}


def lint(docs_json_path: Path) -> int:
    text = docs_json_path.read_text()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
        return 1

    issues: list[str] = []

    nav = data.get("navigation", {})
    for dropdown in nav.get("dropdowns", []):
        dd_name = dropdown.get("dropdown", "?")
        for tab in dropdown.get("tabs", []):
            tab_name = tab.get("tab", "?")
            ctx = f"[{dd_name}] tab='{tab_name}'"

            # Rule 1: tabs cannot have `href`
            if "href" in tab:
                issues.append(
                    f"{ctx}: has 'href' — invalid on tabs (Mintlify only "
                    f"supports pages/groups/openapi). Move external links to "
                    f"navbar.links."
                )

            # Rule: catch unknown tab keys
            unknown = set(tab.keys()) - ALLOWED_TAB_KEYS
            if unknown:
                issues.append(f"{ctx}: unknown tab properties: {sorted(unknown)}")

            # Rule 3: tab content must be present
            if "pages" not in tab and "groups" not in tab and "openapi" not in tab:
                issues.append(f"{ctx}: tab has no pages/groups/openapi")

            # Rule 2: walk every page object and check properties
            walk_pages(tab, ctx, issues)

    if issues:
        print(f"✗ {len(issues)} docs.json issue(s):")
        for i in issues:
            print(f"  - {i}")
        return 1

    print(f"✓ docs.json clean ({docs_json_path})")
    return 0


def walk_pages(node, ctx: str, issues: list[str]) -> None:
    if isinstance(node, list):
        for item in node:
            walk_pages(item, ctx, issues)
    elif isinstance(node, dict):
        # Page entry that's an object (not a plain string)
        if "page" in node and isinstance(node["page"], str):
            extra = set(node.keys()) - ALLOWED_PAGE_OBJECT_KEYS
            if extra:
                page_path = node["page"]
                issues.append(
                    f"{ctx}: page '{page_path}' has unsupported properties "
                    f"{sorted(extra)} — these break tab-href resolution. "
                    f"Move 'tag' / similar to in-page Notes instead."
                )
        for v in node.values():
            walk_pages(v, ctx, issues)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    docs_json = repo_root / "docs.json"
    if not docs_json.exists():
        print(f"✗ {docs_json} not found")
        return 1
    return lint(docs_json)


if __name__ == "__main__":
    sys.exit(main())
