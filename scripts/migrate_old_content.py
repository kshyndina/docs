#!/usr/bin/env python3
"""Build the 'migrated' version: pull real content from the OLD docs
(docs.triton.one) into the matching NEW-structure pages, and report which new
pages have NO old source (need writing)."""
import json, os, re, sys, shutil, urllib.request, openpyxl
sys.path.insert(0, "scripts")
import migrate_to_gitbook as M

ROOT = M.ROOT
OLD_BASE = "https://docs.triton.one"

# ---- new structure: (title, section_key, file, full_path) ------------------
M.scan_icons()
docs = json.load(open(os.path.join(ROOT, "docs.json")))
secs = M.build_sections(docs); M.inject_pyth_into_streaming(secs); M.fix_guides(secs); M.apply_kate_edits(secs)
for s in secs:
    M.assign_paths(s["children"], "", True)
LABEL = {"solana-documentation": "Documentation", "solana-guides": "Guides",
         "solana-api-reference": "API reference", "solana-faqs": "FAQs",
         "sui": "Other chains > SUI", "monad": "Other chains > Monad"}
new_pages = []   # (title, key, file, fullpath)
def walk(key, nodes, prefix):
    for n in nodes:
        fp = n.get("file")
        path = prefix + " > " + n["title"]
        if (n["kind"] == "leaf" or n.get("ref")) and fp:
            new_pages.append((n["title"], key, fp, path))
        walk(key, n["children"], path)
for s in secs:
    if s["key"] == "pyth": continue
    walk(s["key"], s["children"], LABEL.get(s["key"], s["key"]))

def norm(x): return re.sub(r"[^a-z0-9]", "", x.lower())   # space-insensitive

NT = [(norm(t), k, fp) for (t, k, fp, _) in new_pages]
def match_title(seg):
    s = norm(seg)
    if not s: return None
    best = None
    for nt, k, fp in NT:
        if nt == s: return (k, fp)
        if len(s) > 4 and (s in nt or nt in s): best = (k, fp)
    return best

def resolve_dest(goesto):
    seg = goesto.split(">")[-1].split("[")[0].split("//")[0].strip()
    return match_title(seg)

# ---- old pages: name -> [paths] (in tree order) ----------------------------
old_flat = json.load(open("/tmp/old_flat.json"))
from collections import defaultdict, deque
name_paths = defaultdict(deque)
for t, p in old_flat:
    name_paths[norm(t)].append(p)
OLD_TITLE = {norm(t): t for t, p in old_flat}

# ---- xlsx mapping ----------------------------------------------------------
wb = openpyxl.load_workbook("/Users/kate3/Downloads/Current docs mapping.xlsx")
ws = wb.active
REMOVE = ("remove", "removed", "delete", "deleted", "outdated", "internal",
          "can be removed", "of docs", "github", "separate page")

mapped = {}   # new_file -> old_path
notes = []
for r in ws.iter_rows(min_row=2, values_only=True):
    L, typ, page, goto, _ = r
    if not page: continue
    nm = norm(str(page))
    paths = name_paths.get(nm)
    old_path = paths.popleft() if paths else None
    if typ != "page" or not goto:
        continue
    g = str(goto).strip()
    if any(k in g.lower() for k in REMOVE):
        continue
    dest = resolve_dest(g) or match_title(str(page))   # goto, else direct name
    if dest and old_path:
        key, fp = dest
        mapped.setdefault((key, fp), old_path)   # first old page wins
# also map old API-method pages by direct name (their goto is blank)
for t, p in old_flat:
    d = match_title(t)
    if d and d not in mapped and "api-reference" in d[1]:
        mapped[d] = p

# ---- build migrated duplicate ---------------------------------------------
OUT = os.path.join(ROOT, "gitbook-migrated", "sections")
if os.path.exists(os.path.dirname(OUT)):
    shutil.rmtree(os.path.dirname(OUT))
shutil.copytree(os.path.join(ROOT, "gitbook", "sections"), OUT)

def fetch_md(path):
    try:
        req = urllib.request.Request(f"{OLD_BASE}/{path}.md", headers={"User-Agent": "curl/8"})
        return urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
    except Exception:
        return None

migrated_files = set()
for (key, fp), old_path in mapped.items():
    md = fetch_md(old_path)
    if not md:
        continue
    title = next((t for t, k, f, _ in new_pages if k == key and f == fp), None)
    body = re.sub(r"^#\s+.*\n", "", md, count=1).lstrip()    # drop old H1
    out = f"# {title}\n\n{body}\n" if title else md
    with open(os.path.join(OUT, key, fp), "w", encoding="utf-8") as f:
        f.write(out)
    migrated_files.add((key, fp))

# ---- status XLSX -----------------------------------------------------------
APIMETH = re.compile(r"^(get|is|send|simulate|minimum|request|ping|account|logs|program|"
                     r"root|signature|slot|subscribe|metis|titan)", re.I)
def status(t, k, fp):
    if (k, fp) in migrated_files:
        return "Migrated (copy from old)", mapped.get((k, fp), "")
    if k == "solana-api-reference" and APIMETH.match(t):
        return "TBD — copy from Solana Foundation", ""
    return "TBD — write new", ""

wb2 = openpyxl.Workbook(); wsx = wb2.active; wsx.title = "Migrated structure + status"
wsx.append(["L", "Type", "Page / section", "Full path", "Status", "Old source page"])
def emit(nodes, level, prefix):
    for n in nodes:
        name = n["title"]; path = prefix + " > " + name
        if n["kind"] == "group" and n["children"]:
            wsx.append([level, "CATEGORY", ("   " * level) + name, path, "", ""])
            emit(n["children"], level + 1, path)
        else:
            key = sec_key[0]
            st, src = status(name, key, n.get("file") or "")
            wsx.append([level, "page", ("   " * level) + name, path, st, src])
for s in secs:
    if s["key"] == "pyth": continue
    sec_key = [s["key"]]
    lbl = LABEL.get(s["key"], s["key"])
    if s["key"] in ("sui", "monad"):
        pass
    wsx.append([0, "CATEGORY", lbl, lbl, "", ""])
    emit(s["children"], 1, lbl)
outx = "/Users/kate3/Downloads/Migration status.xlsx"
wb2.save(outx)

real = [(t, k, fp) for (t, k, fp, _) in new_pages]
mig = sum(1 for t, k, fp in real if (k, fp) in migrated_files)
api = sum(1 for t, k, fp in real if (k, fp) not in migrated_files and k == "solana-api-reference" and APIMETH.match(t))
tbd = sum(1 for t, k, fp in real if (k, fp) not in migrated_files and not (k == "solana-api-reference" and APIMETH.match(t)))
print(f"NEW pages: {len(real)}")
print(f"  Migrated (copy from old): {mig}")
print(f"  TBD - copy from Solana Foundation (API methods): {api}")
print(f"  TBD - write new: {tbd}")
print("wrote", outx)
print("\n=== TBD - write new (need fresh copy) ===")
for t, k, fp in real:
    if (k, fp) not in migrated_files and not (k == "solana-api-reference" and APIMETH.match(t)):
        print(f"  {LABEL.get(k,k)} > {t}")
