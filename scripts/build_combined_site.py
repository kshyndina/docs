#!/usr/bin/env python3
"""Create + brand the single-row-header combined site."""
import json, os, time, urllib.request, urllib.error

GB = os.environ["GB"]
ORG = "z7eEj3vw2lWeBtVPERxu"
REPO = "https://github.com/kshyndina/docs.git"
REF = "refs/heads/gitbook-schematic"
CDN = "https://cdn.jsdelivr.net/gh/kshyndina/docs@gitbook-schematic"

def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request("https://api.gitbook.com/v1" + path, data=data, method=method,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as resp:
            raw = resp.read(); return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:300]}

def link(title, url, style="link"):
    return {"title": title, "style": style, "links": [], "to": {"kind": "url", "url": url}}

def main():
    st, sp = call("POST", f"/orgs/{ORG}/spaces", {"title": "Triton One Docs (single-row header)"})
    sid = sp["id"]; print("space:", sid)
    for attempt in range(4):
        st, _ = call("POST", f"/spaces/{sid}/git/import",
                     {"url": REPO, "ref": REF, "repoProjectDirectory": "gitbook/combined", "force": True})
        if st in (200, 202, 204): break
        time.sleep(6)
    print("import:", st)
    # wait for content
    for _ in range(10):
        time.sleep(6)
        _, rev = call("GET", f"/spaces/{sid}/content/pages")
        if len(rev.get("pages", [])) > 1: break
    st, site = call("POST", f"/orgs/{ORG}/sites",
                    {"title": "Triton One Docs (single-row)", "type": "basic", "spaces": [sid]})
    site_id = site["id"]; print("site:", site_id)
    call("PATCH", f"/orgs/{ORG}/sites/{site_id}", {"basename": "triton-docs-single-row"})
    # customization
    st, cur = call("GET", f"/orgs/{ORG}/sites/{site_id}/customization")
    cur.pop("object", None)
    s = cur["styling"]
    s["primaryColor"] = {"light": "#7A4BA0", "dark": "#956FB3"}
    s["tint"] = {"color": {"light": "#7A4BA0", "dark": "#956FB3"}}
    cur["title"] = "Triton One Docs"
    cur.setdefault("header", {})
    cur["header"]["logo"] = {"light": f"{CDN}/logo/mark.svg", "dark": f"{CDN}/logo/mark.svg"}
    cur["header"]["links"] = [
        link("Blog", "https://blog.triton.one"),
        link("Log in", "https://customers.triton.one/users/sign-in"),
        link("Get an endpoint", "https://customers.triton.one/onboarding", "button-primary"),
    ]
    cur["favicon"] = {"icon": {"light": f"{CDN}/logo/mark.svg", "dark": f"{CDN}/logo/mark.svg"}}
    cur["feedback"] = {"enabled": True}
    cur["themes"] = {"default": "light", "toggeable": True}
    st, r = call("PUT", f"/orgs/{ORG}/sites/{site_id}/customization", cur)
    print("customization:", st, r.get("error", ""))
    call("POST", f"/orgs/{ORG}/sites/{site_id}/publish", {})
    st, site2 = call("GET", f"/orgs/{ORG}/sites/{site_id}")
    print("URL:", site2.get("urls", {}).get("published"))
    json.dump({"space": sid, "site": site_id}, open("/tmp/gb_combined_v2.json", "w"))

if __name__ == "__main__":
    main()
