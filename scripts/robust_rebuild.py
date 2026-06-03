#!/usr/bin/env python3
"""Deterministic site nav rebuild with polling (the delete API is async, which
was creating duplicates). Order: Documentation, Guides, API reference, FAQs,
then 'Other chains' group (Sui, Monad) created LAST so it renders far right."""
import json, os, time, urllib.request, urllib.error

GB = os.environ["GB"]; ORG = "z7eEj3vw2lWeBtVPERxu"
SITE = json.load(open("/tmp/gb_version_a.json"))["site_id"]
SP = json.load(open("/tmp/gb_version_a.json"))["spaces"]

def call(m, p, b=None):
    data = json.dumps(b).encode() if b is not None else None
    r = urllib.request.Request("https://api.gitbook.com/v1" + p, data=data, method=m,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as x:
            raw = x.read(); return x.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:120]}

def wait_gone(kind):
    for _ in range(10):
        _, d = call("GET", f"/orgs/{ORG}/sites/{SITE}/{kind}")
        items = d.get("items", [])
        if not items:
            return
        for x in items:
            call("DELETE", f"/orgs/{ORG}/sites/{SITE}/{kind}/{x['id']}")
        time.sleep(3)

def main():
    wait_gone("section-groups")
    wait_gone("sections")
    print("cleared.")
    for key, title in (("solana-documentation", "Documentation"), ("solana-guides", "Guides"),
                       ("solana-api-reference", "API reference"), ("solana-faqs", "FAQs")):
        st, _ = call("POST", f"/orgs/{ORG}/sites/{SITE}/sections", {"spaceId": SP[key], "title": title})
        print(f"  +tab {title}: {st}"); time.sleep(2)
    cids = []
    for key, title in (("sui", "Sui"), ("monad", "Monad")):
        st, r = call("POST", f"/orgs/{ORG}/sites/{SITE}/sections", {"spaceId": SP[key], "title": title})
        if r.get("id"):
            cids.append(r["id"])
        time.sleep(2)
    st, _ = call("POST", f"/orgs/{ORG}/sites/{SITE}/section-groups", {"title": "Other chains", "sections": cids})
    print("  +group Other chains:", st)
    time.sleep(2)
    call("POST", f"/orgs/{ORG}/sites/{SITE}/publish", {})
    _, s = call("GET", f"/orgs/{ORG}/sites/{SITE}/sections")
    print("root tabs:", [x["title"] for x in s["items"] if not x.get("sectionGroup")])
    _, g = call("GET", f"/orgs/{ORG}/sites/{SITE}/section-groups")
    print("groups:", [(x["title"], [t["title"] for t in x.get("sections", [])]) for x in g["items"]])

if __name__ == "__main__":
    main()
