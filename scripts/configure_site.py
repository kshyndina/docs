#!/usr/bin/env python3
"""Configure the Triton One Docs GitBook site: title, round logo, favicon,
feedback, light/dark toggle, Mintlify-style header nav + CTA."""
import json, os, urllib.request, urllib.error

GB = os.environ["GB"]
ORG = "z7eEj3vw2lWeBtVPERxu"
SITE = json.load(open("/tmp/gb_version_a.json"))["site_id"]
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
    return {"title": title, "style": style, "links": [],
            "to": {"kind": "url", "url": url}}

def main():
    # 1. rename site title + clean URL basename
    for body in ({"title": "Triton One Docs", "basename": "triton-one-docs"},
                 {"title": "Triton One Docs"}):
        st, r = call("PATCH", f"/orgs/{ORG}/sites/{SITE}", body)
        print("PATCH site", list(body), "->", st, r.get("error", ""))
        if st in (200, 201):
            break

    # 2. customization
    st, cur = call("GET", f"/orgs/{ORG}/sites/{SITE}/customization")
    cur.pop("object", None)
    s = cur["styling"]
    cur["title"] = "Triton One Docs"
    # round transparent Triton mark for both modes (no grey background)
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
    st, r = call("PUT", f"/orgs/{ORG}/sites/{SITE}/customization", cur)
    print("PUT customization ->", st, r.get("error", ""))

    # 3. publish + report
    call("POST", f"/orgs/{ORG}/sites/{SITE}/publish", {})
    st, site = call("GET", f"/orgs/{ORG}/sites/{SITE}")
    print("title:", site.get("title"), "| basename:", site.get("basename"))
    print("URL:", site.get("urls", {}).get("published"))

if __name__ == "__main__":
    main()
