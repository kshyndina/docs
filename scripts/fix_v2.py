#!/usr/bin/env python3
"""Re-import the v2 spaces from the corrected branch and copy the MAIN site's
exact customization (logo, colours, everything) onto v2 - only the title differs."""
import json, os, time, urllib.request, urllib.error

GB = os.environ["GB"]; ORG = "z7eEj3vw2lWeBtVPERxu"
REPO = "https://github.com/kshyndina/docs.git"; REF = "refs/heads/gitbook-schematic"
MAIN = json.load(open("/tmp/gb_version_a.json"))["site_id"]
V2 = json.load(open("/tmp/gb_v2.json")); SITE = V2["site"]; SP = V2["spaces"]

def call(m, p, b=None):
    data = json.dumps(b).encode() if b is not None else None
    r = urllib.request.Request("https://api.gitbook.com/v1" + p, data=data, method=m,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as x:
            raw = x.read(); return x.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:160]}

def imp(sid, key):
    for _ in range(5):
        st, _ = call("POST", f"/spaces/{sid}/git/import",
                     {"url": REPO, "ref": REF,
                      "repoProjectDirectory": f"gitbook-migrated/sections/{key}", "force": True})
        if st in (200, 202, 204):
            return st
        time.sleep(6)
    return st

# 1. re-import corrected content
for key, sid in SP.items():
    print(f"reimport {key}: {imp(sid, key)}"); time.sleep(3)

# 2. copy main customization onto v2 (keeps logo identical), retitle only
st, cust = call("GET", f"/orgs/{ORG}/sites/{MAIN}/customization")
cust.pop("object", None)
cust["title"] = "Triton One Docs"   # same title; v2 distinguished by URL
st2, _ = call("PUT", f"/orgs/{ORG}/sites/{SITE}/customization", cust)
print("copied main customization -> v2:", st2)
call("POST", f"/orgs/{ORG}/sites/{SITE}/publish", {})
st, s2 = call("GET", f"/orgs/{ORG}/sites/{SITE}")
print("URL:", s2.get("urls", {}).get("published"))
