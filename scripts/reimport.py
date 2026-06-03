#!/usr/bin/env python3
"""Force re-import all 8 Version A spaces from the updated branch (sequential,
with retry on transient 403/400)."""
import json, time, os, urllib.request, urllib.error

GB = os.environ["GB"]
API = "https://api.gitbook.com/v1"
REPO = "https://github.com/kshyndina/docs.git"
REF = "refs/heads/gitbook-schematic"

# key -> space id (from version A build) ; key -> skeleton subdir
SPACES = {
    "solana-documentation": "riSjtrOksA50GE38VpH4",
    "solana-guides":        "uHdeBCXbby7cGGEw6FPl",
    "solana-api-reference": "4zcDlKAzOfvGA3RhyVQa",
    "solana-faqs":          "5HE9vJJgjN5UyWvw79Te",
    "sui":                  "7XTSDkV8e0YYDQch7Krp",
    "monad":                "Cz2cI3eYbcnJyUbl7e85",
}

def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method,
        headers={"Authorization": f"Bearer {GB}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:200]}

def do_import(key, sid):
    body = {"url": REPO, "ref": REF,
            "repoProjectDirectory": f"gitbook/sections/{key}", "force": True}
    for attempt in range(1, 5):
        st, _ = call("POST", f"/spaces/{sid}/git/import", body)
        if st in (200, 202, 204):
            return st
        print(f"    {key} import attempt {attempt} -> HTTP {st}, retrying")
        time.sleep(6)
    return st

def main():
    for key, sid in SPACES.items():
        st = do_import(key, sid)
        print(f"import {key:24s} -> HTTP {st}")
        time.sleep(4)  # space out to avoid concurrent-import throttling
    print("\n== verifying page counts ==")
    for key, sid in SPACES.items():
        n = 0
        for _ in range(8):
            time.sleep(5)
            _, rev = call("GET", f"/spaces/{sid}/content/pages")
            pages = rev.get("pages", [])
            n = len(pages)
            # consider done when >1 top page or known single-group sections
            if n > 1 or (key in ("monad",) and n >= 1):
                break
        print(f"  {key:24s} top-level groups/pages = {n}")

if __name__ == "__main__":
    main()
