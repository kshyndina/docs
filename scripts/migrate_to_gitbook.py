#!/usr/bin/env python3
"""Full Mintlify -> GitBook migration for Version A (per-section spaces).

Reads docs.json + the .mdx tree, converts every Mintlify component to GitBook
markdown, resolves snippet imports, rewrites internal links, and writes a
GitBook-shaped project per section under gitbook/sections/<key>/ with SUMMARY.md.
"""
import json, os, re, shutil, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "gitbook", "sections")
SITE_BASE = "https://kate-6.gitbook.io/version-a-site-space-per-section"

# Compact footer (replaces the <FooterLinks/> snippet). Lines end with two
# spaces = markdown hard breaks, so they render tight (no huge paragraph gaps).
FOOTER_MD = (
    "\n---\n\n"
    "Need help? Contact support by clicking the chat icon in the bottom right of your "
    "[customer dashboard](https://customers.triton.one).  \n"
    "Manage endpoints, billing, team: [Customer portal](https://customers.triton.one).  \n"
    "Sales questions? [Contact sales](https://triton.one/contact).  \n"
    "AI agent? [Read llms.txt](https://docs.triton.one/llms.txt).  \n"
    "Follow updates: [Blog](https://blog.triton.one) · [X](https://x.com/triton_one) · "
    "[YouTube](https://www.youtube.com/@triton_one_ltd) · [Telegram](https://t.me/tritonone) · "
    "[GitHub](https://github.com/rpcpool)\n"
)

# section key -> (display title, site section path)
SECTION_PATH = {
    "solana-documentation": "documentation",
    "solana-guides": "guides",
    "solana-api-reference": "api-reference",
    "solana-faqs": "faqs",
    "pyth": "pyth", "sui": "sui", "monad": "monad", "reference": "reference",
}

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def src_path(ref):
    for ext in (".mdx", ".md"):
        p = os.path.join(ROOT, ref + ext)
        if os.path.exists(p):
            return p
    return None

def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        mm = re.match(r'^(\w+):\s*["\']?(.*?)["\']?\s*$', line)
        if mm:
            meta[mm.group(1)] = mm.group(2)
    return meta, m.group(2)

# ---------------------------------------------------------------------------
# nav model: build sections with assigned md paths + global link map
# ---------------------------------------------------------------------------
def title_of(ref):
    p = src_path(ref)
    if p:
        meta, _ = frontmatter(read(p))
        if meta.get("title"):
            return meta["title"]
    return ref.rstrip("/").split("/")[-1].replace("-", " ").capitalize()

def make_leaf(ref):
    return {"kind": "leaf", "title": title_of(ref), "ref": ref, "children": []}

def parse_pages(pages):
    out = []
    for p in pages:
        if isinstance(p, str):
            out.append(make_leaf(p))
        elif isinstance(p, dict):
            out.append({"kind": "group", "title": p.get("group", "Section"),
                        "ref": p.get("root"), "children": parse_pages(p.get("pages", []))})
    return out

def parse_container(c):
    if c.get("groups"):
        return [{"kind": "group", "title": g.get("group", "Group"),
                 "ref": g.get("root"), "children": parse_pages(g.get("pages", []))}
                for g in c["groups"]]
    if c.get("pages"):
        return parse_pages(c["pages"])
    return []

def build_sections(docs):
    secs = []
    for dd in docs["navigation"]["dropdowns"]:
        name = dd.get("dropdown")
        if dd.get("tabs"):
            for t in dd["tabs"]:
                secs.append({"key": slugify(f"{name}-{t.get('tab')}"),
                             "title": f"{name} · {t.get('tab')}",
                             "children": parse_container(t)})
        else:
            secs.append({"key": slugify(name), "title": name,
                         "children": parse_container(dd)})
    return secs

def assign_paths(nodes, prefix, top_level):
    """Set node['file'] (md relpath in section) for leaves and group landing
    pages. Top-level groups without a root become headings (file=None)."""
    for n in nodes:
        slug = slugify(n["title"]) or "page"
        if n["kind"] == "group" and n["children"]:
            if top_level and not n["ref"]:
                n["file"] = None  # SUMMARY '##' heading, no page
                assign_paths(n["children"], f"{slug}/", False)
            else:
                n["file"] = f"{prefix}{slug}/README.md"
                assign_paths(n["children"], f"{prefix}{slug}/", False)
        else:
            n["file"] = f"{prefix}{slug}.md"

def url_no_ext(file):
    u = file[:-3] if file.endswith(".md") else file
    if u.endswith("/README"):
        u = u[:-7]
    return u

def build_linkmap(sections):
    """normalized nav ref -> (section_key, file relpath)."""
    m = {}
    def walk(key, nodes):
        for n in nodes:
            if n.get("ref") and n.get("file"):
                m[n["ref"].strip("/")] = (key, n["file"])
            walk(key, n["children"])
    for s in sections:
        walk(s["key"], s["children"])
    return m

# ---------------------------------------------------------------------------
# component conversion
# ---------------------------------------------------------------------------
HINT = {"Note": "info", "Info": "info", "Tip": "success", "Check": "success",
        "Warning": "warning", "Danger": "danger"}

def attr(tag, name):
    m = re.search(name + r'=\{?"([^"]*)"\}?', tag)
    if not m:
        m = re.search(name + r"=\{?'([^']*)'\}?", tag)
    return m.group(1) if m else None

def strip_unknown_jsx(s):
    # remove wrapper-only tags, keep inner text
    s = re.sub(r"</?(div|span|CardGroup|Columns|Frame|AccordionGroup|Steps|"
               r"Tabs|CodeGroup|ParamFields|ResponseField|Update)\b[^>]*>", "", s)
    s = re.sub(r"<Icon\b[^>]*/>", "", s)
    s = re.sub(r"<Icon\b[^>]*>.*?</Icon>", "", s, flags=re.S)
    s = re.sub(r"</?p>", "\n", s)  # footer paragraphs -> plain lines
    return s

def dedent_fences(text):
    """Remove leading indentation from fenced code blocks (left by grid divs)."""
    lines, out, in_f, ind = text.split("\n"), [], False, 0
    for ln in lines:
        m = re.match(r"^(\s*)```", ln)
        if m and not in_f:
            in_f, ind = True, len(m.group(1))
            out.append(ln[ind:])
        elif m and in_f:
            in_f = False
            out.append(ln[ind:] if ln[:ind].strip() == "" else ln.lstrip())
        elif in_f:
            out.append(ln[ind:] if ln[:ind].strip() == "" else ln.lstrip())
        else:
            out.append(ln)
    return "\n".join(out)

def convert_blocks(text, ctx):
    """Convert paired components. ctx used for link resolution of cards."""
    # hints
    for comp, style in HINT.items():
        text = re.sub(rf"<{comp}>\s*(.*?)\s*</{comp}>",
                      lambda m, st=style: f"\n{{% hint style=\"{st}\" %}}\n{m.group(1).strip()}\n{{% endhint %}}\n",
                      text, flags=re.S)

    # steps / step
    def steps(m):
        body = m.group(1)
        out = ["\n{% stepper %}"]
        for sm in re.finditer(r"<Step\b([^>]*)>(.*?)</Step>", body, re.S):
            t = attr(sm.group(1), "title")
            inner = textwrap.dedent(sm.group(2)).strip()
            out.append("{% step %}")
            if t:
                out.append(f"#### {t}\n")
            out.append(inner)
            out.append("{% endstep %}")
        out.append("{% endstepper %}\n")
        return "\n".join(out)
    text = re.sub(r"<Steps>(.*?)</Steps>", steps, text, flags=re.S)

    # tabs / tab  (also CodeGroup handled before this via marker)
    def tabs(m):
        body = m.group(1)
        out = ["\n{% tabs %}"]
        for tm in re.finditer(r"<Tab\b([^>]*)>(.*?)</Tab>", body, re.S):
            t = attr(tm.group(1), "title") or "Tab"
            out.append(f'{{% tab title="{t}" %}}')
            out.append(textwrap.dedent(tm.group(2)).strip())
            out.append("{% endtab %}")
        out.append("{% endtabs %}\n")
        return "\n".join(out)
    text = re.sub(r"<Tabs>(.*?)</Tabs>", tabs, text, flags=re.S)

    # CodeGroup -> tabs of code fences
    def codegroup(m):
        body = m.group(1)
        fences = re.findall(r"```([^\n]*)\n(.*?)```", body, re.S)
        if not fences:
            return body
        out = ["\n{% tabs %}"]
        for i, (info, code) in enumerate(fences):
            parts = info.strip().split()
            lang = parts[0] if parts else "text"
            title = " ".join(parts[1:]) if len(parts) > 1 else lang
            out.append(f'{{% tab title="{title}" %}}')
            out.append(f"```{lang}\n{code.rstrip()}\n```")
            out.append("{% endtab %}")
        out.append("{% endtabs %}\n")
        return "\n".join(out)
    text = re.sub(r"<CodeGroup>(.*?)</CodeGroup>", codegroup, text, flags=re.S)

    # accordions -> details
    def accordion(m):
        t = attr(m.group(1), "title") or "Details"
        inner = textwrap.dedent(m.group(2)).strip()
        return f"\n<details>\n<summary>{t}</summary>\n\n{inner}\n\n</details>\n"
    text = re.sub(r"<Accordion\b([^>]*)>(.*?)</Accordion>", accordion, text, flags=re.S)

    # cards -> content-ref (if href) or bold block
    def card(m):
        tag, body = m.group(1), m.group(2).strip()
        title = attr(tag, "title") or "Card"
        href = attr(tag, "href")
        if href:
            url = resolve_link(href, ctx)
            return f"\n{{% content-ref url=\"{url}\" %}}\n[{title}]({url})\n{{% endcontent-ref %}}\n"
        return f"\n**{title}**\n\n{body}\n"
    text = re.sub(r"<Card\b([^>]*)>(.*?)</Card>", card, text, flags=re.S)
    # self-closing card
    def card_sc(m):
        tag = m.group(1)
        title = attr(tag, "title") or "Card"
        href = attr(tag, "href")
        if href:
            url = resolve_link(href, ctx)
            return f"\n{{% content-ref url=\"{url}\" %}}\n[{title}]({url})\n{{% endcontent-ref %}}\n"
        return f"\n**{title}**\n"
    text = re.sub(r"<Card\b([^>]*)/>", card_sc, text)

    # param / response fields -> table-row tokens (merged into a table later)
    def cell(s):
        return re.sub(r"\s+", " ", (s or "").strip()).replace("|", "\\|")
    def pf_token(tag, body, kind):
        name = attr(tag, "name") or attr(tag, "path") or attr(tag, "query") or attr(tag, "body") or ""
        typ = attr(tag, "type") or ""
        req = "Yes" if ("required" in tag and "required={false}" not in tag
                        and 'required="false"' not in tag) else ""
        return f"\x01PF\x01{kind}\x01{cell(name)}\x01{cell(typ)}\x01{req}\x01{cell(body)}\x01\n"
    text = re.sub(r"<ParamField\b([^>]*)>(.*?)</ParamField>",
                  lambda m: pf_token(m.group(1), m.group(2), "param"), text, flags=re.S)
    text = re.sub(r"<ParamField\b([^>]*)/>",
                  lambda m: pf_token(m.group(1), "", "param"), text)
    text = re.sub(r"<ResponseField\b([^>]*)>(.*?)</ResponseField>",
                  lambda m: pf_token(m.group(1), m.group(2), "field"), text, flags=re.S)
    text = re.sub(r"<ResponseField\b([^>]*)/>",
                  lambda m: pf_token(m.group(1), "", "field"), text)

    # tree -> code block (parse Tree.Folder / Tree.File nesting)
    def tree(m):
        lines, base = [], None
        for ln in m.group(1).splitlines():
            mm = re.search(r'<Tree\.(Folder|File)\s+name="([^"]+)"', ln)
            if not mm:
                continue
            indent = len(ln) - len(ln.lstrip())
            if base is None:
                base = indent
            depth = max(0, (indent - base)) // 2
            name = mm.group(2) + ("/" if mm.group(1) == "Folder" else "")
            lines.append("  " * depth + name)
        return "\n```\n" + "\n".join(lines) + "\n```\n"
    text = re.sub(r"<Tree>(.*?)</Tree>", tree, text, flags=re.S)

    # badge / tooltip -> inline
    text = re.sub(r"<Badge\b[^>]*>(.*?)</Badge>", lambda m: f"`{m.group(1).strip()}`", text, flags=re.S)
    text = re.sub(r"<Tooltip\b[^>]*>(.*?)</Tooltip>", lambda m: m.group(1), text, flags=re.S)

    text = strip_unknown_jsx(text)
    return text

# ---------------------------------------------------------------------------
# links + images
# ---------------------------------------------------------------------------
LINKMAP = {}
def resolve_link(href, ctx):
    if not href or href.startswith(("http://", "https://", "#", "mailto:")):
        return href
    key = href.strip("/")
    # try exact, then without trailing fragments
    base = key.split("#")[0]
    if base in LINKMAP:
        sect, file = LINKMAP[base]
        if sect == ctx["section"]:
            rel = os.path.relpath(file, os.path.dirname(ctx["file"]))
            return rel
        return f"{SITE_BASE}/{SECTION_PATH[sect]}/{url_no_ext(file)}"
    if base == "llms.txt":
        return "https://docs.triton.one/llms.txt"
    return href  # unknown internal; leave as-is

def rewrite_links(text, ctx):
    text = re.sub(r"\]\((/[^)]+)\)", lambda m: f"]({resolve_link(m.group(1), ctx)})", text)
    text = re.sub(r'href="(/[^"]+)"', lambda m: f'href="{resolve_link(m.group(1), ctx)}"', text)
    return text

IMG_USED = set()
def rewrite_images(text, ctx):
    def repl(m):
        path = m.group(2)
        fn = os.path.basename(path)
        IMG_USED.add((path, ctx["section"]))
        rel = os.path.relpath(f"images/{fn}", os.path.dirname(ctx["file"]))
        return f"{m.group(1)}{rel}{m.group(3)}"
    text = re.sub(r"(\]\()(/images/[^)]+)(\))", repl, text)
    text = re.sub(r'(src=")(/images/[^"]+)(")', repl, text)
    return text

# ---------------------------------------------------------------------------
# post-processing: param tables + block normalization
# ---------------------------------------------------------------------------
PF_RUN = re.compile(r"(?:[ \t]*\x01PF\x01[^\n]*\x01\n)(?:[ \t]*\n)*"
                    r"(?:(?:[ \t]*\x01PF\x01[^\n]*\x01\n)(?:[ \t]*\n)*)*")

def merge_param_tables(text):
    def build(run):
        rows = re.findall(r"\x01PF\x01([^\x01]*)\x01([^\x01]*)\x01([^\x01]*)\x01([^\x01]*)\x01([^\x01]*)\x01",
                          run.group(0))
        if not rows:
            return run.group(0)
        head = "Field" if rows[0][0] == "field" else "Parameter"
        out = [f"\n| {head} | Type | Required | Description |",
               "| --- | --- | --- | --- |"]
        for _kind, name, typ, req, body in rows:
            nm = f"`{name}`" if name else ""
            tp = f"`{typ}`" if typ else ""
            out.append(f"| {nm} | {tp} | {req or '—'} | {body or ''} |")
        return "\n".join(out) + "\n"
    return PF_RUN.sub(build, text)

def normalize_blocks(text):
    """Strip leading indentation before block-level markers, but never inside
    fenced code (so indented JSX-derived headings/cards/tables land at col 0)."""
    out, in_f = [], False
    marker = re.compile(r"[ \t]+(\{%|#{1,6}\s|<details|</details>|<summary|\| )")
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            in_f = not in_f
            out.append(ln)
        elif not in_f and marker.match(ln):
            out.append(ln.lstrip())
        else:
            out.append(ln)
    return "\n".join(out)

# ---------------------------------------------------------------------------
# page rendering (with snippet inlining)
# ---------------------------------------------------------------------------
def inline_snippets(text):
    imports = dict(re.findall(r"import\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]", text))
    text = re.sub(r"^import\s+.*$", "", text, flags=re.M)
    for var, path in imports.items():
        if path.rstrip().endswith("footer-links.mdx"):
            snippet = FOOTER_MD
        else:
            sp = os.path.join(ROOT, path.lstrip("/"))
            if not os.path.exists(sp):
                snippet = ""
            else:
                _, sbody = frontmatter(read(sp))
                snippet = inline_snippets(sbody)  # recurse
        # strip leading indentation on the component's line so inlined snippet
        # markdown lands at column 0 (avoids accidental code blocks)
        text = re.sub(rf"(?m)^[ \t]*<{var}\s*/>", lambda m, s=snippet: s, text)
        text = re.sub(rf"(?m)^[ \t]*<{var}>\s*</{var}>", lambda m, s=snippet: s, text)
        text = re.sub(rf"<{var}\s*/>", lambda m, s=snippet: s, text)
    return text

def render_page(ref, ctx, fallback_title):
    p = src_path(ref) if ref else None
    if not p:
        return f"# {fallback_title}\n"
    meta, body = frontmatter(read(p))
    body = inline_snippets(body)
    body = convert_blocks(body, ctx)
    body = merge_param_tables(body)
    body = dedent_fences(body)
    body = normalize_blocks(body)
    body = rewrite_images(body, ctx)
    body = rewrite_links(body, ctx)
    body = re.sub(r"(?m)^[ \t]+$", "", body)       # blank whitespace-only lines
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    title = meta.get("title") or fallback_title
    desc = meta.get("description", "")
    head = f"# {title}\n"
    if desc:
        head += f"\n{desc}\n"
    return head + "\n" + body + "\n"

# ---------------------------------------------------------------------------
# emit section
# ---------------------------------------------------------------------------
def write_file(section_dir, relfile, content):
    fp = os.path.join(section_dir, relfile)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)

def emit_section(sec):
    key = sec["key"]
    base = os.path.join(OUT, key)
    summary = ["# Table of contents", "", "* [Overview](README.md)", ""]
    write_file(base, "README.md", f"# {sec['title']}\n\n_Documentation section._\n")

    def emit_nodes(nodes, depth):
        for n in nodes:
            indent = "  " * depth
            ctxfile = n["file"] or "README.md"
            ctx = {"section": key, "file": ctxfile}
            if n["kind"] == "group" and n["children"]:
                if n["file"] is None:
                    summary.append(f"## {n['title']}")
                    summary.append("")
                    emit_nodes(n["children"], 0)
                    summary.append("")
                else:
                    content = render_page(n["ref"], ctx, n["title"]) if n["ref"] else f"# {n['title']}\n"
                    write_file(base, n["file"], content)
                    summary.append(f"{indent}* [{n['title']}]({n['file']})")
                    emit_nodes(n["children"], depth + 1)
            else:
                content = render_page(n["ref"], ctx, n["title"])
                write_file(base, n["file"], content)
                summary.append(f"{indent}* [{n['title']}]({n['file']})")

    emit_nodes(sec["children"], 0)
    write_file(base, "SUMMARY.md", "\n".join(summary).rstrip() + "\n")
    write_file(base, ".gitbook.yaml", "root: ./\nstructure:\n  readme: README.md\n  summary: SUMMARY.md\n")

def copy_images():
    for path, section in IMG_USED:
        srcp = os.path.join(ROOT, path.lstrip("/"))
        fn = os.path.basename(path)
        dstdir = os.path.join(OUT, section, "images")
        os.makedirs(dstdir, exist_ok=True)
        if os.path.exists(srcp):
            shutil.copy2(srcp, os.path.join(dstdir, fn))

def main():
    global LINKMAP
    docs = json.load(open(os.path.join(ROOT, "docs.json")))
    sections = build_sections(docs)
    for s in sections:
        assign_paths(s["children"], "", True)
    LINKMAP = build_linkmap(sections)
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for s in sections:
        emit_section(s)
    copy_images()
    total = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"sections: {len(sections)}  files: {total}  images: {len(IMG_USED)}")
    for s in sections:
        n = sum(len(f) for _, _, f in os.walk(os.path.join(OUT, s['key'])))
        print(f"  {s['key']:24s} {n} files")

if __name__ == "__main__":
    main()
