#!/usr/bin/env python3
"""Duplicate the migrated site as 'triton-docs-final': 6 fresh spaces importing
gitbook-migrated content, same tab structure, same branding as the main site."""
import json, os, time, urllib.request, urllib.error

GB = os.environ["GB"]; ORG = "z7eEj3vw2lWeBtVPERxu"
REPO = "https://github.com/kshyndina/docs.git"; REF = "refs/heads/gitbook-schematic"
MAIN = json.load(open("/tmp/gb_version_a.json"))["site_id"]

def call(m, p, b=None):
    data = json.dumps(b).encode() if b is not None else None
    r = urllib.request.Request("https://api.gitbook.com/v1" + p, data=data, method=m,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as x:
            raw = x.read(); return x.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:160]}

SECTS = [("solana-documentation", "Documentation"), ("solana-guides", "Guides"),
         ("solana-api-reference", "API reference"), ("solana-faqs", "FAQs"),
         ("sui", "Sui"), ("monad", "Monad")]

def imp(sid, key):
    for _ in range(5):
        st, _ = call("POST", f"/spaces/{sid}/git/import",
                     {"url": REPO, "ref": REF,
                      "repoProjectDirectory": f"gitbook-migrated/sections/{key}", "force": True})
        if st in (200, 202, 204):
            return st
        time.sleep(6)
    return st

sp = {}
for key, title in SECTS:
    st, s = call("POST", f"/orgs/{ORG}/spaces", {"title": f"final {title}"})
    sp[key] = s["id"]
    print(f"space {title}: import {imp(s['id'], key)}"); time.sleep(2)

for _ in range(10):
    time.sleep(6)
    if all(len(call("GET", f"/spaces/{i}/content/pages")[1].get("pages", [])) > 1 for i in sp.values()):
        break

st, site = call("POST", f"/orgs/{ORG}/sites", {"title": "Triton One Docs - migrated content", "type": "basic"})
SITE = site["id"]
call("PATCH", f"/orgs/{ORG}/sites/{SITE}", {"basename": "triton-docs-final"})
for key, title in SECTS[:4]:
    call("POST", f"/orgs/{ORG}/sites/{SITE}/sections", {"spaceId": sp[key], "title": title}); time.sleep(1)
cids = []
for key, title in (("sui", "Sui"), ("monad", "Monad")):
    st, r = call("POST", f"/orgs/{ORG}/sites/{SITE}/sections", {"spaceId": sp[key], "title": title})
    if r.get("id"): cids.append(r["id"])
    time.sleep(1)
call("POST", f"/orgs/{ORG}/sites/{SITE}/section-groups", {"title": "Other chains", "sections": cids})

# copy main branding (logo, colours, everything)
st, cust = call("GET", f"/orgs/{ORG}/sites/{MAIN}/customization"); cust.pop("object", None)
cust["title"] = "Triton One Docs"
call("PUT", f"/orgs/{ORG}/sites/{SITE}/customization", cust)
call("POST", f"/orgs/{ORG}/sites/{SITE}/publish", {})
st, s2 = call("GET", f"/orgs/{ORG}/sites/{SITE}")
print("FINAL URL:", s2.get("urls", {}).get("published"))
json.dump({"site": SITE, "spaces": sp}, open("/tmp/gb_final.json", "w"))
