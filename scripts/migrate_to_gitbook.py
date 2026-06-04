#!/usr/bin/env python3
"""Full Mintlify -> GitBook migration for Version A (per-section spaces).

Reads docs.json + the .mdx tree, converts every Mintlify component to GitBook
markdown, resolves snippet imports, rewrites internal links, and writes a
GitBook-shaped project per section under gitbook/sections/<key>/ with SUMMARY.md.
"""
import json, os, re, shutil, textwrap, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "gitbook", "sections")
SITE_BASE = "https://kate-6.gitbook.io/triton-one-docs"

CDN = "https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic"

# Lucide (Mintlify) -> Font Awesome free icon names that GitBook understands.
FA_MAP = {
    "activity": "chart-line", "alert-triangle": "triangle-exclamation",
    "antenna": "tower-broadcast", "archive": "box-archive", "bar-chart-3": "chart-column",
    "binary": "code", "bookmark": "bookmark", "bot": "robot", "calculator": "calculator",
    "circle-help": "circle-question", "code": "code", "coins": "coins", "compass": "compass",
    "copy": "copy", "credit-card": "credit-card", "database": "database", "droplet": "droplet",
    "flame": "fire", "gamepad-2": "gamepad", "gauge": "gauge", "git-branch": "code-branch",
    "git-merge": "code-merge", "history": "clock-rotate-left", "id-card": "id-card",
    "image": "image", "key": "key", "landmark": "landmark", "layers": "layer-group",
    "link": "link", "list": "list", "lock": "lock", "messages-square": "comments",
    "package": "box", "palette": "palette", "play": "play", "plug": "plug", "radio": "radio",
    "refresh-cw": "arrows-rotate", "rocket": "rocket", "rotate-cw": "rotate-right",
    "route": "route", "rss": "rss", "send": "paper-plane", "server": "server",
    "shield": "shield", "shield-check": "shield-halved", "sliders-vertical": "sliders",
    "smartphone": "mobile-screen", "sparkles": "sparkles", "trending-up": "arrow-trend-up",
    "user": "user", "user-cog": "user-gear", "user-plus": "user-plus", "wrench": "wrench",
    "zap": "bolt", "life-buoy": "life-ring", "briefcase": "briefcase", "gear": "gear",
    "book-open": "book-open", "messages": "comments",
}

def fa_icon(name):
    fa = FA_MAP.get(name, name)
    return f'<i class="fa-{fa}">:{fa}:</i>'

# pages removed from nav -> drop any card/link that targets them (avoid broken links)
REMOVED_REFS = ("standard-rpc", "zk-compression-photon", "old-faithful-streams", "history/hydrant")
# page-title overrides
TITLE_OVERRIDE = {
    "solana-guides/getting-started/set-up-rpc/trading-or-market-making": "Trading and market making",
    "pyth/overview": "Pythnet and Hermes",
    "solana/sending-transactions/jet-sender": "Jet sender",
}

# global text renames applied to every page (catches card titles, prose, etc.)
RENAMES = {"Yellowstone Jet": "Jet sender"}
TITLE_OVERRIDE["solana/get-started/auth-and-security"] = "Authentication"

# The footer now lives in GitBook's site-footer customization (link groups), so
# external links render WITHOUT the ↗ arrow (the same reason header links don't).
# The inline content footer is therefore removed.
FOOTER_MD = "\n"

# Customer logo marquee is removed entirely (Kate's request).
LOGO_ROW = "\n"

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

PAGE_ICON = {}
def scan_icons():
    """Pre-scan all <Card icon= href=> in source so each target page gets that
    icon in frontmatter (GitBook then shows it on cards AND in the sidebar)."""
    import glob
    for fp in glob.glob(os.path.join(ROOT, "**", "*.mdx"), recursive=True):
        try:
            txt = read(fp)
        except Exception:
            continue
        for tag in re.findall(r"<Card\b([^>]*)>", txt):
            ic = attr(tag, "icon")
            hr = attr(tag, "href")
            if ic and hr and hr.startswith("/"):
                PAGE_ICON.setdefault(hr.strip("/").split("#")[0], ic)

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
    o = TITLE_OVERRIDE.get((ref or "").strip("/"))
    if o:
        return o
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
        if name == "Reference":
            continue                      # internal page templates - not published
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

def remove_div_block(text, class_substr):
    """Remove a balanced <div className=...class_substr...>...</div> block."""
    while True:
        m = re.search(r'<div\b[^>]*class[Nn]ame="[^"]*' + class_substr + r'[^"]*"[^>]*>', text)
        if not m:
            return text
        i, depth = m.end(), 1
        while i < len(text) and depth > 0:
            no, nc = text.find("<div", i), text.find("</div>", i)
            if nc == -1:
                break
            if no != -1 and no < nc:
                depth += 1; i = no + 4
            else:
                depth -= 1; i = nc + 6
        text = text[:m.start()] + text[i:]

def _flat(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip().replace("|", "\\|")

def static_calc(text):
    """Replace the interactive pricing calculator with a static rate table +
    feature list (sliders/inputs can't run in GitBook)."""
    m = re.search(r"<div\b[^>]*triton-calc\b[^>]*>", text)
    if not m:
        return text
    i, depth = m.end(), 1
    while i < len(text) and depth > 0:
        no, nc = text.find("<div", i), text.find("</div>", i)
        if nc == -1:
            break
        if no != -1 and no < nc:
            depth += 1; i = no + 4
        else:
            depth -= 1; i = nc + 6
    block = text[m.start():i]
    rows = re.findall(r'row-title">(.*?)</div>\s*<div[^>]*row-rate">(.*?)</div>', block, re.S)
    feats = re.findall(r"<li>(.*?)</li>", block, re.S)
    out = []
    seen = set()
    if rows:
        out += ["\n| Service | Rate |", "| --- | --- |"]
        for t, r in rows:
            k = (_flat(t), _flat(r))
            if k not in seen:
                seen.add(k); out.append(f"| {k[0]} | {k[1]} |")
    if feats:
        out.append("\n**Included**")
        fseen = set()
        for f in feats:
            ff = _flat(f)
            if ff and ff not in fseen:
                fseen.add(ff); out.append(f"- {ff}")
    out.append("\nMinimum deposit $125 (prepaid, non-refundable, valid for 12 months). "
               "[Get started](https://customers.triton.one/onboarding)\n")
    return text[:m.start()] + "\n".join(out) + text[i:]

def html_table_to_md(m):
    block = m.group(1)
    heads = re.findall(r"<th\b[^>]*>(.*?)</th>", block, re.S)
    out = []
    if heads:
        out.append("| " + " | ".join(_flat(h) for h in heads) + " |")
        out.append("| " + " | ".join("---" for _ in heads) + " |")
    for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr>", block, re.S):
        cells = re.findall(r"<td\b[^>]*>(.*?)</td>", tr, re.S)
        if cells:
            out.append("| " + " | ".join(_flat(c) for c in cells) + " |")
    return "\n" + "\n".join(out) + "\n"

def _balanced_div(text, start_re):
    m = re.search(start_re, text)
    if not m:
        return None
    i, depth = m.end(), 1
    while i < len(text) and depth > 0:
        no, nc = text.find("<div", i), text.find("</div>", i)
        if nc == -1:
            break
        if no != -1 and no < nc:
            depth += 1; i = no + 4
        else:
            depth -= 1; i = nc + 6
    return m.start(), i, text[m.start():i]

def stack_to_tabs(text, ctx):
    """Turn the welcome 'Triton stack overview' diagram into tabs (one per
    category), each holding a card grid. Drops links to removed pages."""
    found = _balanced_div(text, r'<div\b[^>]*class[Nn]ame="[^"]*stack-map[^"]*"[^>]*>')
    if not found:
        return text
    s, e, block = found
    branches, pos = [], 0
    while True:
        bm = re.search(r'<div\b[^>]*class[Nn]ame="stack-branch"[^>]*>', block[pos:])
        if not bm:
            break
        j, d = pos + bm.end(), 1
        while j < len(block) and d > 0:
            no, nc = block.find("<div", j), block.find("</div>", j)
            if nc == -1:
                break
            if no != -1 and no < nc:
                d += 1; j = no + 4
            else:
                d -= 1; j = nc + 6
        branches.append(block[pos + bm.end(): j])
        pos = j
    out = ["\n{% tabs %}"]
    for b in branches:
        tm = re.search(r"stack-branch-title[^>]*>([^<]+)</div>", b)
        title = tm.group(1).strip() if tm else "Other services"
        cards = []
        for lm in re.finditer(r'<a\b[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', b):
            href, txt = lm.group(1), lm.group(2).strip()
            if any(href.split("#")[0].rstrip("/").endswith(r) for r in REMOVED_REFS):
                continue
            icon = PAGE_ICON.get(href.strip("/").split("#")[0], "")
            cards.append(f"\x02CARD\x02{txt}\x02\x02{resolve_link(href, ctx)}\x02{icon}\x02\n")
        if not cards:
            continue                      # skip a category with no remaining cards
        out.append(f'{{% tab title="{title}" %}}')
        out.extend(cards)
        out.append("{% endtab %}")
    out.append("{% endtabs %}\n")
    return text[:s] + "\n".join(out) + text[e:]

def handle_html_blocks(text, ctx):
    """Convert raw-HTML blocks (logos, <a> link maps, custom diagrams, tables)
    and drop interactive widgets that can't run in GitBook."""
    text = stack_to_tabs(text, ctx)
    # drop the interactive playground + static-ify the pricing calculator
    text = remove_div_block(text, "triton-try")
    text = re.sub(r"##+ RPC playground\s*\n+[^\n<]*\n", "", text)
    text = static_calc(text)
    # MDX expression escapes
    text = text.replace('{"$"}', "$")
    text = re.sub(r"\{/\*.*?\*/\}", "", text, flags=re.S)   # {/* comments */}
    text = re.sub(r'\{"([^"}]*)"\}', r"\1", text)            # {"literal"} -> literal
    # raw <table> -> markdown table (header row preserved)
    text = re.sub(r"<table\b[^>]*>(.*?)</table>", html_table_to_md, text, flags=re.S)
    # lists + stray interactive elements
    text = re.sub(r"</?(ul|ol)\b[^>]*>", "", text)
    text = re.sub(r"<li\b[^>]*>(.*?)</li>",
                  lambda m: f"\n- {_flat(m.group(1))}", text, flags=re.S)
    text = re.sub(r"<button\b[^>]*>.*?</button>", "", text, flags=re.S)
    text = re.sub(r"<input\b[^>]*/?>", "", text)
    text = re.sub(r"<span\b[^>]*>(.*?)</span>", lambda m: m.group(1), text, flags=re.S)
    text = re.sub(r"<span\b[^>]*/>", "", text)
    text = re.sub(r"<p\b[^>]*>(.*?)</p>", lambda m: f"\n{m.group(1).strip()}\n", text, flags=re.S)
    # <a className="stack-leaf" href>txt</a> -> a card token (becomes a card grid);
    # other <a> -> normal link
    def conv_a(m):
        attrs, inner = m.group(1), m.group(2)
        hm = re.search(r'href="([^"]+)"', attrs)
        if not hm:
            return re.sub(r"<[^>]+>", "", inner).strip()
        txt = re.sub(r"<[^>]+>", "", inner).strip()
        if "stack-leaf" in attrs:
            return f"\n\x02CARD\x02{txt}\x02\x02{hm.group(1)}\x02\x02\n"
        return f"[{txt}]({hm.group(1)})"
    text = re.sub(r"<a\b([^>]*)>(.*?)</a>", conv_a, text, flags=re.S)
    # title divs -> headings (pillar) / bold (branch)
    def title_div(m):
        attrs, inner = m.group(1), m.group(2)
        txt = re.sub(r"<[^>]+>", "", inner).strip()
        return f"\n\n### {txt}\n" if "pillar-title" in attrs else f"\n\n**{txt}**\n"
    text = re.sub(r'<div\b([^>]*class[Nn]ame="[^"]*-title[^"]*"[^>]*)>(.*?)</div>',
                  title_div, text, flags=re.S)
    # <img src> -> markdown image (logos via CDN; /images handled later)
    def conv_img(m):
        src = m.group(1)
        if src.startswith("/logos/"):
            src = CDN + src
        return f"![]({src})"
    text = re.sub(r'<img\b[^>]*\bsrc="([^"]+)"[^>]*/?>', conv_img, text)
    return text

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
            t = t.split(" (")[0]   # drop parenthetical so tab labels don't truncate
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
    # cards -> card-row tokens (merged into a GitBook card grid later). Works for
    # any target (same- or cross-space) and carries an icon cover.
    def card_token(tag, body=""):
        title = _flat(attr(tag, "title") or "Card")
        href = attr(tag, "href") or ""
        icon = attr(tag, "icon") or ""
        if href and any(href.split("#")[0].rstrip("/").endswith(r) for r in REMOVED_REFS):
            return ""  # drop cards that point at removed pages
        if href:
            href = resolve_link(href, ctx)
        return f"\x02CARD\x02{title}\x02{_flat(body)}\x02{href}\x02{icon}\x02\n"
    text = re.sub(r"<Card\b([^>]*)>(.*?)</Card>",
                  lambda m: card_token(m.group(1), m.group(2)), text, flags=re.S)
    text = re.sub(r"<Card\b([^>]*)/>", lambda m: card_token(m.group(1)), text)

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

CARD_RUN = re.compile(r"(?:[ \t]*\x02CARD\x02[^\n]*\x02\n)(?:[ \t]*\n)*"
                      r"(?:(?:[ \t]*\x02CARD\x02[^\n]*\x02\n)(?:[ \t]*\n)*)*")
LUCIDE = "https://unpkg.com/lucide-static@latest/icons"

def merge_card_tables(text):
    # if a page has more than one card grid, keep them all the SAME width
    # (never mix 2-col and 3-col on one page) -> use 2-col everywhere
    multi = len([m for m in CARD_RUN.finditer(text) if "\x02CARD\x02" in m.group(0)]) > 1
    def build(run):
        cards = re.findall(r"\x02CARD\x02([^\x02]*)\x02([^\x02]*)\x02([^\x02]*)\x02([^\x02]*)\x02",
                           run.group(0))
        if not cards:
            return run.group(0)
        # single grid: 4 -> 2 cols, 6 -> 3 cols. Multi-grid page: all 2 cols.
        size = "large" if (multi or len(cards) in (1, 2, 4)) else "medium"
        head = (f"<table data-card-size=\"{size}\" data-view=\"cards\"><thead><tr><th></th><th></th>"
                "<th data-hidden data-card-target data-type=\"content-ref\"></th>"
                "</tr></thead><tbody>")
        rows = []
        for title, desc, href, icon in cards:
            tgt = f'<td><a href="{href}">{href}</a></td>' if href else "<td></td>"
            ic = (fa_icon(icon) + " ") if icon else ""
            rows.append(f"<tr><td>{ic}<strong>{title}</strong></td><td>{desc}</td>{tgt}</tr>")
        return "\n\n" + head + "".join(rows) + "</tbody></table>\n\n"
    return CARD_RUN.sub(build, text)

# NOTE: a kroki.io static-SVG mermaid renderer used to live here (it was the ONLY
# way to kill GitBook's scroll-zoom on diagrams). Kate vetoed static SVGs -- diagrams
# must stay live mermaid -- so the function was removed as dead code. Live mermaid keeps
# the GitBook zoom toolbar; that is not disableable on hosted/free GitBook.

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
        elif path.rstrip().endswith("customer-logo-marquee.mdx"):
            snippet = LOGO_ROW
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
    body = handle_html_blocks(body, ctx)
    body = convert_blocks(body, ctx)
    body = merge_param_tables(body)
    body = merge_card_tables(body)
    body = dedent_fences(body)
    body = normalize_blocks(body)
    body = rewrite_images(body, ctx)
    body = rewrite_links(body, ctx)
    body = re.sub(r"(?m)^[ \t]+$", "", body)       # blank whitespace-only lines
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    # never two horizontal rules in a row
    body = re.sub(r"(?m)^---\s*\n(\s*\n)*---\s*$", "---", body)
    # drop a markdown --- right before the footer's <hr> (avoids a literal "---")
    body = re.sub(r"(?m)^-{3,}\s*\n+(?=<hr>)", "", body)
    body = re.sub(r"\n+-{3,}\s*$", "", body)   # no dangling divider at page end
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    title = TITLE_OVERRIDE.get((ref or "").strip("/")) or meta.get("title") or fallback_title
    desc = meta.get("description", "")
    head = f"# {title}\n"
    if desc:
        head += f"\n{desc}\n"
    out = head + "\n" + body + "\n"
    for old, new in RENAMES.items():
        out = out.replace(old, new)
    return out

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
    # use the first real page as the section landing (README) - no "Overview" item
    first = [None]
    def find_first(nodes):
        for n in nodes:
            if first[0]:
                return
            if not n["children"] and n.get("ref"):
                first[0] = n
            elif n["children"]:
                find_first(n["children"])
    find_first(sec["children"])
    fnode = first[0]
    # Guides keeps its first page in-group; use a generated landing instead
    if key in ("solana-guides", "solana-api-reference"):
        fnode = None
    if fnode:
        landing_title = fnode["title"]
        landing = render_page(fnode["ref"], {"section": key, "file": "README.md"}, landing_title)
        skip = fnode["file"]
    elif key == "solana-guides":
        landing_title = "Solana guides"
        landing = "# Solana guides\n\nGuides and tutorials for building on Triton.\n"
        skip = None
    elif key == "solana-api-reference":
        landing_title = "API overview"
        landing = ("# API overview\n\nReference for Triton's Solana HTTP RPC, "
                   "Whirligig WebSocket, Yellowstone gRPC, and DAS API methods.\n")
        skip = None
    else:
        landing_title = sec["title"]
        landing = f"# {sec['title']}\n"
        skip = None
    write_file(base, "README.md", landing)
    summary = ["# Table of contents", "", f"* [{landing_title}](README.md)", ""]

    def emit_nodes(nodes, depth):
        for n in nodes:
            if n.get("file") and n["file"] == skip:
                continue                       # already the README landing
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
                if n.get("ref"):
                    content = render_page(n["ref"], ctx, n["title"])
                    for cref in n.get("combine", []):
                        extra = render_page(cref, ctx, "").replace("# ", "## ", 1)
                        content += "\n\n" + extra
                else:
                    content = f"# {n['title']}\n\n{n.get('body', '')}\n"
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

def inject_pyth_into_streaming(sections):
    """Per Kate: drop Pyth as a chain; surface Pythnet + Hermes as ONE page
    inside Solana's Streaming data group."""
    page = {"kind": "leaf", "title": "Pythnet and Hermes", "ref": "pyth/overview",
            "combine": ["pyth/pyth-hermes"], "children": []}
    for s in sections:
        if s["key"] == "solana-documentation":
            for n in s["children"]:
                if n["title"] == "Streaming data":
                    n["children"] = [c for c in n["children"]
                                     if not _ends(c, "old-faithful-streams")]
                    n["children"].append(page)

def fix_guides(sections):
    """Kate's Guides changes: rename groups, add a 'How to build a...' group."""
    howto = {"kind": "group", "title": "How to build a...", "ref": None, "children": [
        {"kind": "leaf", "title": "Wallet app", "ref": None, "children": [], "body": "Coming soon."},
        {"kind": "leaf", "title": "Trading / sniper bot", "ref": None, "children": [], "body": "Coming soon."},
        {"kind": "leaf", "title": "DEX / AMM", "ref": None, "children": [], "body": "Coming soon."},
        {"kind": "leaf", "title": "NFT marketplace", "ref": None, "children": [], "body": "Coming soon."},
        {"kind": "leaf", "title": "Solana game", "ref": None, "children": [], "body": "Coming soon."},
    ]}
    def ph(t):
        return {"kind": "leaf", "title": t, "ref": None, "children": [], "body": "Coming soon."}
    streaming = {"kind": "group", "title": "Streaming", "ref": None,
                 "children": [ph("Fumarole cluster failover"), ph("How to use Vixen + gRPC")]}
    for s in sections:
        if s["key"] != "solana-guides":
            continue
        for n in s["children"]:
            if n["title"] == "Set up your RPC for...":
                n["title"] = "Quickstart on Triton"
            elif n["title"] == "End-to-end builds":
                n["title"] = "Common workflows"
        for n in s["children"]:
            if n["title"] == "Error handling":
                n["children"].append(ph("Streams disconnecting"))
            elif n["title"] == "Common workflows":
                n["children"].append(ph("Query token program"))
        s["children"].insert(1, howto)
        ei = next((i for i, n in enumerate(s["children"]) if n["title"] == "Error handling"),
                  len(s["children"]) - 1)
        s["children"].insert(ei + 1, streaming)

def _ends(n, *suffixes):
    return (n.get("ref") or "").endswith(suffixes)

def _flatten_chain(s):
    """Sui/Monad: keep overview first, drop quickstart + API reference, flatten."""
    flat = []
    for n in s["children"]:
        kids = n["children"] if n["kind"] == "group" else [n]
        for k in kids:
            if k.get("title") == "API reference" or _ends(k, "quickstart"):
                continue
            if k["kind"] == "group" and k["title"] == "API reference":
                continue
            flat.append(k)
    # overview first
    flat.sort(key=lambda k: 0 if _ends(k, "overview") else 1)
    s["children"] = flat

def apply_kate_edits(sections):
    for s in sections:
        if s["key"] == "solana-documentation":
            for g in s["children"]:
                if g["title"] == "Get started":
                    kids = g["children"]
                    idx = next((i for i, n in enumerate(kids) if _ends(n, "auth-and-security")), len(kids))
                    kids.insert(idx, {"kind": "leaf", "title": "Endpoints and regions",
                                      "ref": None, "children": [], "body": "Coming soon."})
                    # split Auth and security -> Authentication + Privacy and security
                    auth = next((n for n in kids if _ends(n, "auth-and-security")), None)
                    if auth:
                        auth["title"] = "Authentication"
                        ai = kids.index(auth)
                        kids.insert(ai + 1, {"kind": "leaf", "title": "Privacy and security",
                                             "ref": None, "children": [], "body": "Coming soon."})
                elif g["title"] == "Reading state":
                    g["children"] = [n for n in g["children"]
                                     if not _ends(n, "standard-rpc", "zk-compression-photon")]
                elif g["title"] == "Historical data":
                    g["children"] = [n for n in g["children"] if not _ends(n, "history/hydrant")]
                elif g["title"] == "Account management API":
                    g["ref"] = None  # render as a '##' heading like Dedicated nodes (no landing page)
                    for n in g["children"]:
                        if _ends(n, "rate-tiers"):
                            n["title"] = "Rate limits"
                elif g["title"] == "Sending transactions":
                    move = [n for n in g["children"]
                            if _ends(n, "metis-swap-api", "titan-swap-api", "jito-bundles")]
                    g["children"] = [n for n in g["children"] if n not in move]
                    # move Shield MEV protection right after Yellowstone Jet
                    shield = next((n for n in g["children"] if _ends(n, "shield-mev-protection")), None)
                    if shield:
                        g["children"].remove(shield)
                        ji = next((i for i, n in enumerate(g["children"]) if _ends(n, "jet-sender")),
                                  len(g["children"]) - 1)
                        g["children"].insert(ji + 1, shield)
                    sub = {"kind": "group", "title": "3rd party APIs", "ref": None, "children": move}
                    idx = next((i for i, n in enumerate(g["children"]) if _ends(n, "priority-fees-api")),
                               len(g["children"]) - 1)
                    g["children"].insert(idx + 1, sub)
        elif s["key"] == "solana-api-reference":
            s["children"] = [g for g in s["children"] if g["title"] != "Overview and auth"]
        elif s["key"] in ("sui", "monad"):
            _flatten_chain(s)

def main():
    global LINKMAP
    docs = json.load(open(os.path.join(ROOT, "docs.json")))
    scan_icons()
    sections = build_sections(docs)
    inject_pyth_into_streaming(sections)
    fix_guides(sections)
    apply_kate_edits(sections)
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
