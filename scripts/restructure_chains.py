#!/usr/bin/env python3
"""Restructure the site so chains are section groups (the 'chain picker'):
Solana (4 tabs) + Sui + Pythnet + Monad. Rename SUI->Sui, Pyth->Pythnet.
Drop the internal Reference section + space."""
import json, os, urllib.request, urllib.error

GB = os.environ["GB"]
ORG = "z7eEj3vw2lWeBtVPERxu"
SITE = json.load(open("/tmp/gb_version_a.json"))["site_id"]
SPACES = json.load(open("/tmp/gb_version_a.json"))["spaces"]

def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request("https://api.gitbook.com/v1" + path, data=data, method=method,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as resp:
            raw = resp.read(); return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}

def sections_index():
    """title(lower) -> section id, plus whether it's grouped."""
    st, d = call("GET", f"/orgs/{ORG}/sites/{SITE}/sections")
    idx = {}
    for s in d.get("items", []):
        idx[s["title"].lower()] = s["id"]
    return idx

def main():
    idx = sections_index()
    print("current sections:", idx)

    # 1. rename standalone sections
    if "sui" not in idx and "sui" in {k.lower() for k in idx}:
        pass
    for old, new in (("sui", "Sui"), ("pyth", "Pythnet")):
        sid = idx.get(old)
        if sid:
            st, _ = call("PATCH", f"/orgs/{ORG}/sites/{SITE}/sections/{sid}", {"title": new})
            print(f"rename {old} -> {new}: {st}")
    idx = sections_index()

    # 2. wrap each non-Solana chain in its own section group (the picker entries)
    for label in ("Sui", "Pythnet", "Monad"):
        sid = idx.get(label.lower())
        if not sid:
            print(f"  ! section {label} not found"); continue
        st, r = call("POST", f"/orgs/{ORG}/sites/{SITE}/section-groups",
                     {"title": label, "sections": [sid]})
        print(f"group {label} (section {sid}): {st} {r.get('error','')}")

    # 3. drop Reference (section + space)
    ref = sections_index().get("reference")
    if ref:
        st, _ = call("DELETE", f"/orgs/{ORG}/sites/{SITE}/sections/{ref}")
        print("delete Reference section:", st)
    refspace = SPACES.get("reference")
    if refspace:
        st, _ = call("DELETE", f"/spaces/{refspace}")
        print("delete Reference space:", st)

    # 4. publish + report final structure
    call("POST", f"/orgs/{ORG}/sites/{SITE}/publish", {})
    st, groups = call("GET", f"/orgs/{ORG}/sites/{SITE}/section-groups")
    print("\n== section groups (chain picker) ==")
    for g in groups.get("items", []):
        secs = [s.get("title") for s in g.get("sections", [])]
        print(f"  {g.get('title')}: {secs}")
    st, sections = call("GET", f"/orgs/{ORG}/sites/{SITE}/sections")
    ungrouped = [s["title"] for s in sections.get("items", []) if not s.get("sectionGroup")]
    print("ungrouped sections:", ungrouped)

if __name__ == "__main__":
    main()
