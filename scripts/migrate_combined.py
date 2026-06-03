#!/usr/bin/env python3
"""Build the single-row-header VERSION: one combined space (all chains in the
sidebar, no section tab row). Reuses the converter from migrate_to_gitbook.py."""
import importlib.util, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mig", os.path.join(HERE, "migrate_to_gitbook.py"))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

ROOT = M.ROOT
docs = json.load(open(os.path.join(ROOT, "docs.json")))

# ---- build combined nav tree: chains -> (tabs ->) groups/pages -----------
def chain_nodes():
    tops = []
    for dd in docs["navigation"]["dropdowns"]:
        name = dd.get("dropdown")
        if name == "Reference":
            continue                      # internal templates, excluded
        if name == "Pyth":
            name = "Pythnet"
        if name == "SUI":
            name = "Sui"
        if dd.get("tabs"):
            children = [{"kind": "group", "title": t.get("tab"), "ref": None,
                         "children": M.parse_container(t)} for t in dd["tabs"]]
        else:
            children = M.parse_container(dd)
        tops.append({"kind": "group", "title": name, "ref": None, "children": children})
    return tops

def main():
    M.scan_icons()
    top = chain_nodes()
    M.assign_paths(top, "", True)
    # link map: every ref resolves within the single "combined" space (relative)
    cmap = {}
    def walk(nodes):
        for n in nodes:
            if n.get("ref") and n.get("file"):
                cmap[n["ref"].strip("/")] = ("combined", n["file"])
            walk(n["children"])
    walk(top)
    M.LINKMAP = cmap
    M.OUT = os.path.join(ROOT, "gitbook")          # so emit_section -> gitbook/combined
    sec = {"key": "combined", "title": "Triton One Docs", "children": top}
    # clean + emit
    import shutil
    cdir = os.path.join(ROOT, "gitbook", "combined")
    if os.path.exists(cdir):
        shutil.rmtree(cdir)
    M.emit_section(sec)
    M.copy_images()
    n = sum(len(f) for _, _, f in os.walk(cdir))
    print(f"combined files: {n}")
    print("top groups:", [t["title"] for t in top])

if __name__ == "__main__":
    main()
