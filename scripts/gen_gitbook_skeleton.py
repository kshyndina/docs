#!/usr/bin/env python3
"""Generate GitBook-shaped skeletons (titles only) from Mintlify docs.json.

Emits two layouts under gitbook/:
  gitbook/combined/                 -> Version C: single space, everything nested
  gitbook/sections/<section>/       -> Version A: one space per section

Schematic only: page bodies are just '# Title' placeholders so the nav tree
is visible in GitBook. No content conversion happens here.
"""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "gitbook")

def title_of(page_path):
    """Read frontmatter title from a nav page ref; fallback to humanized slug."""
    for ext in (".mdx", ".md"):
        fp = os.path.join(ROOT, page_path + ext)
        if os.path.exists(fp):
            with open(fp, encoding="utf-8") as f:
                head = f.read(4000)
            m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', head, re.M)
            if m:
                return m.group(1).strip()
    slug = page_path.rstrip("/").split("/")[-1]
    return slug.replace("-", " ").replace("_", " ").strip().capitalize() or "Page"

# ---- nav model -------------------------------------------------------------
# node = {"title": str, "page": str|None (nav ref), "children": [node]}

def make_leaf(page_ref):
    return {"title": title_of(page_ref), "page": page_ref, "children": []}

def parse_pages(pages):
    out = []
    for p in pages:
        if isinstance(p, str):
            out.append(make_leaf(p))
        elif isinstance(p, dict):
            # nested group, possibly with a root landing page
            node = {"title": p.get("group", "Section"),
                    "page": p.get("root"), "children": parse_pages(p.get("pages", []))}
            if node["page"]:
                node["title"] = p.get("group") or title_of(node["page"])
            out.append(node)
    return out

def parse_groups(groups):
    out = []
    for g in groups:
        node = {"title": g.get("group", "Group"),
                "page": g.get("root"),
                "children": parse_pages(g.get("pages", []))}
        out.append(node)
    return out

def parse_container(c):
    """A tab or dropdown body: may have groups[] or pages[]."""
    if c.get("groups"):
        return parse_groups(c["groups"])
    if c.get("pages"):
        return parse_pages(c["pages"])
    return []

def build_sections(docs):
    """Return ordered list of top sections.
    Each section -> {"key","title","children"} where children are groups/pages.
    Solana's tabs each become their own section (Version A spaces)."""
    sections = []
    for dd in docs["navigation"]["dropdowns"]:
        name = dd.get("dropdown")
        if dd.get("tabs"):
            for t in dd["tabs"]:
                sections.append({
                    "key": slugify(f"{name}-{t.get('tab')}"),
                    "drop": name,
                    "tab": t.get("tab"),
                    "title": f"{name} {chr(183)} {t.get('tab')}",
                    "children": parse_container(t),
                })
        else:
            sections.append({
                "key": slugify(name),
                "drop": name,
                "tab": None,
                "title": name,
                "children": parse_container(dd),
            })
    return sections

def build_dropdowns(docs):
    """For Version C: one node per dropdown. Tabs become nested index nodes so
    Solana shows as a single collapsible group containing its 4 tabs."""
    tops = []
    for dd in docs["navigation"]["dropdowns"]:
        name = dd.get("dropdown")
        if dd.get("tabs"):
            children = [{"title": t.get("tab"), "page": None,
                         "children": parse_container(t)} for t in dd["tabs"]]
        else:
            children = parse_container(dd)
        tops.append({"key": slugify(name), "title": name, "children": children})
    return tops

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# ---- emitters --------------------------------------------------------------

def write_md(path, title, note=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = f"# {title}\n"
    if note:
        body += f"\n_{note}_\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)

def emit_tree(nodes, base_dir, rel_prefix, summary_lines, depth, counter):
    """Write placeholder md files for nodes; append nested bullets to summary."""
    indent = "  " * depth
    for n in nodes:
        counter[0] += 1
        slug = slugify(n["title"]) or f"page-{counter[0]}"
        if n["children"]:
            # group/index page lives at <slug>/README.md
            rel = f"{rel_prefix}{slug}/README.md"
            write_md(os.path.join(base_dir, rel), n["title"], "schematic placeholder")
            summary_lines.append(f"{indent}* [{n['title']}]({rel})")
            emit_tree(n["children"], base_dir, f"{rel_prefix}{slug}/", summary_lines, depth + 1, counter)
        else:
            rel = f"{rel_prefix}{slug}.md"
            write_md(os.path.join(base_dir, rel), n["title"], "schematic placeholder")
            summary_lines.append(f"{indent}* [{n['title']}]({rel})")

def gitbook_yaml():
    return "root: ./\nstructure:\n  readme: README.md\n  summary: SUMMARY.md\n"

def emit_combined(tops):
    base = os.path.join(OUT, "combined")
    write_md(os.path.join(base, "README.md"), "Triton One docs (schematic - combined)",
             "Version C: everything in one space. Structure only, no content.")
    summary = ["# Table of contents", "", "* [Overview](README.md)", ""]
    for sec in tops:
        summary.append(f"## {sec['title']}")
        summary.append("")
        counter = [0]
        emit_tree(sec["children"], base, f"{sec['key']}/", summary, 0, counter)
        summary.append("")
    with open(os.path.join(base, "SUMMARY.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(summary).rstrip() + "\n")
    with open(os.path.join(base, ".gitbook.yaml"), "w") as f:
        f.write(gitbook_yaml())

def emit_sections(sections):
    for sec in sections:
        base = os.path.join(OUT, "sections", sec["key"])
        write_md(os.path.join(base, "README.md"), sec["title"], "schematic placeholder space")
        summary = ["# Table of contents", "", "* [Overview](README.md)", ""]
        # top-level children become ## groups if they themselves have children,
        # else flat bullets under an Overview.
        counter = [0]
        for n in sec["children"]:
            if n["children"]:
                summary.append(f"## {n['title']}")
                summary.append("")
                emit_tree(n["children"], base, f"{slugify(n['title'])}/", summary, 0, counter)
                summary.append("")
            else:
                # leaf at section root
                counter[0] += 1
                slug = slugify(n["title"]) or f"page-{counter[0]}"
                rel = f"{slug}.md"
                write_md(os.path.join(base, rel), n["title"], "schematic placeholder")
                summary.append(f"* [{n['title']}]({rel})")
        with open(os.path.join(base, "SUMMARY.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(summary).rstrip() + "\n")
        with open(os.path.join(base, ".gitbook.yaml"), "w") as f:
            f.write(gitbook_yaml())

def main():
    docs = json.load(open(os.path.join(ROOT, "docs.json")))
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    sections = build_sections(docs)
    emit_combined(build_dropdowns(docs))
    emit_sections(sections)
    # report
    print("sections (Version A spaces):")
    for s in sections:
        print(f"  {s['key']:30s} {s['title']}")
    print(f"\ncombined dir: gitbook/combined")
    total = sum(len(files) for _, _, files in os.walk(OUT))
    print(f"total files emitted: {total}")

if __name__ == "__main__":
    main()
