#!/usr/bin/env python3
"""Apply Triton brand (colours + Work Sans) to the Version A GitBook site."""
import json, os, urllib.request, urllib.error

GB = os.environ["GB"]
ORG = "z7eEj3vw2lWeBtVPERxu"
SITE = json.load(open("/tmp/gb_version_a.json"))["site_id"]
API = f"https://api.gitbook.com/v1/orgs/{ORG}/sites/{SITE}/customization"

def req(method, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(API, data=data, method=method,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}

WORK_SANS = {
    "id": "work-sans", "custom": True, "fontFamily": "Work Sans",
    "fontFaces": [
        {"weight": w, "sources": [{
            "url": f"https://cdn.jsdelivr.net/npm/@fontsource/work-sans/files/work-sans-latin-{w}-normal.woff2",
            "format": "woff2"}]}
        for w in (400, 500, 600, 700)
    ],
}

# Triton palette (light = brand hex, dark = a lighter shade from Kate's scales)
COLORS = {
    "primaryColor": {"light": "#7A4BA0", "dark": "#956FB3"},
    "infoColor":    {"light": "#259DD0", "dark": "#51B1D9"},
    "successColor": {"light": "#73975E", "dark": "#8FAC7E"},
    "warningColor": {"light": "#FF680A", "dark": "#FF863B"},
    "dangerColor":  {"light": "#BA2D0B", "dark": "#C85439"},
}

def main():
    st, cur = req("GET")
    cur.pop("object", None)
    cur["styling"].update(COLORS)
    orig_font = cur["styling"].get("font", "Inter")

    cur["styling"]["font"] = WORK_SANS
    st, resp = req("PUT", cur)
    if st in (200, 201):
        print("✅ brand applied WITH Work Sans font, HTTP", st)
        return
    print("⚠ font PUT failed HTTP", st, resp.get("error", "")[:250])
    cur["styling"]["font"] = orig_font  # fallback: colours only
    st2, resp2 = req("PUT", cur)
    if st2 in (200, 201):
        print("✅ brand colours applied (font kept as built-in), HTTP", st2)
    else:
        print("❌ colours PUT failed HTTP", st2, resp2.get("error", "")[:350])

if __name__ == "__main__":
    main()
