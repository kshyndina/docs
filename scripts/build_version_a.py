#!/usr/bin/env python3
"""Version A assembly: per-section spaces + a Site mirroring Mintlify dropdowns.

Creates 8 spaces, git-imports each from its skeleton subdir, then builds a
GitBook Site where a "Solana" section group holds the 4 Solana tab-spaces and
Pyth/SUI/Monad/Reference are standalone sections.
"""
import json, time, urllib.request, urllib.error, os

GB = os.environ["GB"]
ORG = "z7eEj3vw2lWeBtVPERxu"
API = "https://api.gitbook.com/v1"
REPO = "https://github.com/kshyndina/docs.git"
REF = "refs/heads/gitbook-schematic"

def call(method, path, body=None):
    url = API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}

# section key, display title, skeleton subdir, dropdown group
SECTIONS = [
    ("solana-documentation", "Documentation",  "gitbook/sections/solana-documentation", "Solana"),
    ("solana-guides",        "Guides",         "gitbook/sections/solana-guides",        "Solana"),
    ("solana-api-reference", "API reference",  "gitbook/sections/solana-api-reference", "Solana"),
    ("solana-faqs",          "FAQs",           "gitbook/sections/solana-faqs",          "Solana"),
    ("pyth",                 "Pyth",           "gitbook/sections/pyth",                 None),
    ("sui",                  "SUI",            "gitbook/sections/sui",                  None),
    ("monad",                "Monad",          "gitbook/sections/monad",                None),
    ("reference",            "Reference",      "gitbook/sections/reference",            None),
]

def main():
    spaces = {}
    print("== creating + importing spaces ==")
    for key, title, subdir, group in SECTIONS:
        full = title if group is None else f"{group} · {title}"
        st, sp = call("POST", f"/orgs/{ORG}/spaces", {"title": full})
        sid = sp.get("id")
        spaces[key] = sid
        st2, _ = call("POST", f"/spaces/{sid}/git/import",
                      {"url": REPO, "ref": REF, "repoProjectDirectory": subdir, "force": True})
        print(f"  {key:24s} space={sid} create={st} import={st2}")

    # poll all imports
    print("== waiting for imports ==")
    for _ in range(12):
        time.sleep(7)
        pending = []
        for key, sid in spaces.items():
            _, rev = call("GET", f"/spaces/{sid}/content/pages")
            if not rev.get("pages"):
                pending.append(key)
        print(f"  pending: {pending or 'none'}")
        if not pending:
            break

    # build site
    print("== creating site ==")
    st, site = call("POST", f"/orgs/{ORG}/sites",
                    {"title": "Version A — Site (space per section)", "type": "basic"})
    site_id = site.get("id")
    print("  site:", site_id, "status", st, site.get("error", ""))
    if not site_id:
        print("  SITE CREATE FAILED:", site); return

    # Solana section group
    st, grp = call("POST", f"/orgs/{ORG}/sites/{site_id}/section-groups", {"title": "Solana"})
    grp_id = grp.get("id")
    print("  section-group Solana:", grp_id, "status", st, grp.get("error", ""))

    # add sections
    print("== adding sections ==")
    for key, title, subdir, group in SECTIONS:
        sid = spaces[key]
        body = {"spaceId": sid, "title": title}
        if group == "Solana" and grp_id:
            body["siteSectionGroupId"] = grp_id
        st, sec = call("POST", f"/orgs/{ORG}/sites/{site_id}/sections", body)
        print(f"  section {title:16s} status={st} {sec.get('error','')}")

    # publish
    st, pub = call("POST", f"/orgs/{ORG}/sites/{site_id}/publish", {})
    print("== publish status", st, pub.get("error", ""))

    # fetch URLs
    st, site2 = call("GET", f"/orgs/{ORG}/sites/{site_id}")
    urls = site2.get("urls", {})
    print("\nSITE URLS:", json.dumps(urls, indent=1))
    out = {"site_id": site_id, "spaces": spaces, "urls": urls}
    json.dump(out, open("/tmp/gb_version_a.json", "w"))
    print("saved /tmp/gb_version_a.json")

if __name__ == "__main__":
    main()
