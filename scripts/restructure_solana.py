#!/usr/bin/env python3
"""Restructure the experiment site to: Get started | Solana (dropdown: Docs,
Guides, FAQs, API reference) | Sui | Monad. Get started is its own space."""
import json, os, time, urllib.request, urllib.error

GB = os.environ["GB"]; ORG = "z7eEj3vw2lWeBtVPERxu"
REPO = "https://github.com/kshyndina/docs.git"; REF = "refs/heads/solana-experiment"
sol = json.load(open("/tmp/gb_solana.json")); SITE = sol["site"]; SP = dict(sol["spaces"])

def call(m, p, b=None):
    d = json.dumps(b).encode() if b is not None else None
    r = urllib.request.Request("https://api.gitbook.com/v1" + p, data=d, method=m,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as x: raw = x.read(); return x.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e: return e.code, {"error": e.read().decode()[:140]}

def imp(sid, key):
    for _ in range(5):
        st, _ = call("POST", f"/spaces/{sid}/git/import",
                     {"url": REPO, "ref": REF, "repoProjectDirectory": f"gitbook-migrated/sections/{key}", "force": True})
        if st in (200, 202, 204): return st
        time.sleep(6)
    return st

# 1. create + import the Get started space
st, s = call("POST", f"/orgs/{ORG}/spaces", {"title": "solana Get started"})
SP["get-started"] = s["id"]
print("get-started space import:", imp(s["id"], "get-started"))
for _ in range(10):
    time.sleep(6)
    if len(call("GET", f"/spaces/{s['id']}/content/pages")[1].get("pages", [])) >= 1: break

# 2. clear existing nav (groups first, then sections), with polling
def clear(kind):
    for _ in range(10):
        items = call("GET", f"/orgs/{ORG}/sites/{SITE}/{kind}")[1].get("items", [])
        if not items: return
        for x in items: call("DELETE", f"/orgs/{ORG}/sites/{SITE}/{kind}/{x['id']}")
        time.sleep(3)
clear("section-groups"); clear("sections"); print("cleared nav")

# 3. recreate in visual order: Get started, [Solana group], Sui, Monad
def mksec(space, title):
    st, r = call("POST", f"/orgs/{ORG}/sites/{SITE}/sections", {"spaceId": SP[space], "title": title})
    time.sleep(1); return r.get("id")
mksec("get-started", "Get started")
docs = mksec("solana-documentation", "Docs")
guides = mksec("solana-guides", "Guides")
faqs = mksec("solana-faqs", "FAQs")
apiref = mksec("solana-api-reference", "API reference")
st, g = call("POST", f"/orgs/{ORG}/sites/{SITE}/section-groups",
             {"title": "Solana", "sections": [docs, guides, faqs, apiref]})
print("Solana group:", st); time.sleep(2)
mksec("sui", "Sui")
mksec("monad", "Monad")

call("POST", f"/orgs/{ORG}/sites/{SITE}/publish", {})
# verify
secs = call("GET", f"/orgs/{ORG}/sites/{SITE}/sections")[1]["items"]
grps = call("GET", f"/orgs/{ORG}/sites/{SITE}/section-groups")[1]["items"]
print("flat tabs:", [x["title"] for x in secs if not x.get("sectionGroup")])
print("groups:", [(x["title"], [t["title"] for t in x.get("sections", [])]) for x in grps])
sol["spaces"] = SP; json.dump(sol, open("/tmp/gb_solana.json", "w"))
print("URL: https://kate-6.gitbook.io/triton-docs-solana/")
