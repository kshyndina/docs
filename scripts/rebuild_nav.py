#!/usr/bin/env python3
"""Rebuild site nav: Solana's 4 sections as top-level TABS (default Documentation)
+ a 'Chains' dropdown holding Sui / Pythnet / Monad."""
import json, os, urllib.request, urllib.error

GB = os.environ["GB"]
ORG = "z7eEj3vw2lWeBtVPERxu"
SITE = json.load(open("/tmp/gb_version_a.json"))["site_id"]
SP = json.load(open("/tmp/gb_version_a.json"))["spaces"]

def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request("https://api.gitbook.com/v1" + path, data=data, method=method,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as resp:
            raw = resp.read(); return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

def add_section(space_id, title, group=None):
    body = {"spaceId": space_id, "title": title}
    if group:
        body["siteSectionGroupId"] = group
    st, r = call("POST", f"/orgs/{ORG}/sites/{SITE}/sections", body)
    return st, r

def main():
    # clean slate: delete groups, then sections
    _, groups = call("GET", f"/orgs/{ORG}/sites/{SITE}/section-groups")
    for g in groups.get("items", []):
        call("DELETE", f"/orgs/{ORG}/sites/{SITE}/section-groups/{g['id']}")
    _, secs = call("GET", f"/orgs/{ORG}/sites/{SITE}/sections")
    for s in secs.get("items", []):
        call("DELETE", f"/orgs/{ORG}/sites/{SITE}/sections/{s['id']}")
    print("cleared groups + sections")

    # Solana sections as top-level tabs (order matters: Documentation first)
    for key, title in (("solana-documentation", "Documentation"),
                       ("solana-guides", "Guides"),
                       ("solana-api-reference", "API reference"),
                       ("solana-faqs", "FAQs")):
        st, _ = add_section(SP[key], title)
        print(f"tab {title}: {st}")

    # Chains dropdown: add the 3 chain sections, then group them
    chain_ids = []
    for key, title in (("sui", "Sui"), ("pyth", "Pythnet"), ("monad", "Monad")):
        st, r = add_section(SP[key], title)
        if r.get("id"):
            chain_ids.append(r["id"])
        print(f"chain {title}: {st}")
    st, g = call("POST", f"/orgs/{ORG}/sites/{SITE}/section-groups",
                 {"title": "Chains", "sections": chain_ids})
    print("Chains group:", st, g.get("error", ""))

    call("POST", f"/orgs/{ORG}/sites/{SITE}/publish", {})
    _, groups = call("GET", f"/orgs/{ORG}/sites/{SITE}/sections")
    print("tabs (root sections):", [s["title"] for s in groups.get("items", []) if not s.get("sectionGroup")])
    _, gg = call("GET", f"/orgs/{ORG}/sites/{SITE}/section-groups")
    for g in gg.get("items", []):
        print("group", g["title"], "->", [s["title"] for s in g.get("sections", [])])

if __name__ == "__main__":
    main()
