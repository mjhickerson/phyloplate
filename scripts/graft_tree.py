#!/usr/bin/env python3
"""Stitch pruned, published chronograms onto a cited backbone.

    python3 graft_tree.py backbone.py edible_eukaryotes_candidates.csv stitched.nwk [seam_report.txt]

backbone.py defines TREE using:
    N(name, age, source, *children)   a backbone node with a published age (Ma) and a citation string
    S(path, label, synonyms=None)     graft a source chronogram: it is pruned to candidate species and
                                      hung from the enclosing node at its own crown age (its internal ages are kept)
    T(species)                        a single candidate species hung directly from the enclosing node

Output: a dated Newick whose tips are species names. Run assemble_tree.py on it to apply synonyms,
gap-fill missing species next to congeners / at family nodes / by anchor, name nodes, and build the app.
The seam report lists every source: tips found, crown age, stem length to its backbone node, and conflicts
(a source crown older than the node it hangs from is flagged and the stem clamped to 1 Myr).
"""
import csv, os, re, sys, threading
sys.setrecursionlimit(1_000_000)
threading.stack_size(512 * 1024 * 1024)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assemble_tree import Node, parse_newick, write_newick, set_heights, norm_species

CAND_GROUP = {}
CAND_GENERA = set()
def N(name, age, source, *children): return {"kind": "N", "name": name, "age": float(age), "source": source, "children": list(children)}
def S(path, label, synonyms=None, groups=None): return {"kind": "S", "path": path, "label": label, "synonyms": synonyms or {}, "groups": groups}
def T(species): return {"kind": "T", "species": species}

def prune_to(root, keep_norm):
    keep_norm = set(keep_norm) | {norm_species(t.label) for t in root.tips() if t.label.startswith("__helper__")}
    """Keep only tips whose normalised label is in keep_norm; collapse unary nodes; return new root (or None)."""
    def rec(n):
        if n.is_tip():
            return n if norm_species(n.label) in keep_norm else None
        kept = [c for c in (rec(c) for c in n.children) if c is not None]
        if not kept: return None
        if len(kept) == 1:
            c = kept[0]; c.bl += n.bl; c.parent = n.parent; return c
        n.children = kept
        for c in kept: c.parent = n
        return n
    r = rec(root)
    if r is not None: r.parent = None; r.bl = 0.0
    return r

def graft_source(spec, cand_norm, report):
    if spec.get("groups"):
        cand_norm = {k for k, g in CAND_GROUP.items() if any(g.startswith(p) for p in spec["groups"])}
    txt = open(spec["path"], encoding="utf-8").read()
    root = parse_newick(txt)
    # relabel by synonyms (source name -> candidate name), underscores -> spaces
    syn = {norm_species(k): v for k, v in spec["synonyms"].items()}
    n_all = 0
    seen = {}   # normalised candidate name -> (tip, was_exact)
    helper_seen = set()
    for t in root.tips():
        n_all += 1
        lab = t.label.replace("_", " ").strip("'")
        lab = syn.get(norm_species(lab), lab)
        toks = norm_species(lab).split()
        exact = " ".join(toks) in cand_norm
        if not exact and len(toks) > 2 and " ".join(toks[:2]) in cand_norm:   # Genus_species_FAMILY_ORDER or infraspecific labels
            lab = " ".join(lab.split()[:2]); toks = toks[:2]
        key = " ".join(toks)
        if key not in cand_norm and len(toks) >= 2 and toks[0] in CAND_GENERA and toks[0] not in helper_seen:
            helper_seen.add(toks[0]); t.label = "__helper__" + " ".join(lab.split()[:2]); continue   # one non-food congener per needed genus
        if key in cand_norm:
            if key in seen:
                prev_tip, prev_exact = seen[key]
                if exact and not prev_exact:      # this one is the exact species tip; demote the earlier one
                    prev_tip.label = "__dup__" + prev_tip.label; seen[key] = (t, True)
                else:
                    lab = "__dup__" + lab
            else:
                seen[key] = (t, exact)
        t.label = lab
    dups = sum(1 for t in root.tips() if t.label.startswith("__dup__"))
    if dups: report.append(f"[{spec['label']}] {dups} duplicate tips for the same species dropped (infraspecific labels)")
    sub = prune_to(root, cand_norm)
    if sub is None:
        report.append(f"[{spec['label']}] {n_all} tips in source, NONE matched candidates"); return None
    set_heights(sub)
    tips = sub.tips()
    report.append(f"[{spec['label']}] {n_all} tips in source; {len(tips)} candidate species kept; crown {sub.height:.1f} Ma")
    return sub

def build(spec, cand_norm, report, parent_age=None):
    if spec["kind"] == "N":
        node = Node(spec["name"]); node.height = spec["age"]
        for ch in spec["children"]:
            c = build(ch, cand_norm, report, spec["age"])
            if c is None: continue
            stem = spec["age"] - c.height
            if stem <= 0:
                report.append(f"  SEAM CONFLICT: '{getattr(c, 'label', '?') or '(subtree)'}' crown {c.height:.1f} >= node {spec['name']} {spec['age']:.0f}; stem clamped to 1 Myr")
                stem = 1.0
            c.bl = stem; node.add(c)
        if not node.children:
            ph = Node("__placeholder__" + spec["name"]); ph.height = 0.0; ph.bl = spec["age"]; node.add(ph)
        return node
    if spec["kind"] == "S":
        sub = graft_source(spec, cand_norm, report)
        if sub is not None and parent_age is not None:
            report.append(f"  hung from node at {parent_age:.0f} Ma; stem {max(parent_age - sub.height, 1):.1f} Myr")
        return sub
    if spec["kind"] == "T":
        if norm_species(spec["species"]) not in cand_norm:
            report.append(f"  backbone tip '{spec['species']}' is not in the candidate list; skipped"); return None
        t = Node(spec["species"]); t.height = 0.0; return t
    raise ValueError(spec)

def main():
    bb_path, csv_path, out_path = sys.argv[1:4]
    rep_path = sys.argv[4] if len(sys.argv) > 4 else None
    ns = {"N": N, "S": S, "T": T}
    exec(open(bb_path, encoding="utf-8").read(), ns)
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    cand = [r["species"] for r in rows]
    cand_norm = {norm_species(s) for s in cand}
    global CAND_GROUP, CAND_GENERA
    CAND_GROUP = {norm_species(r["species"]): r["group"] for r in rows}
    CAND_GENERA = {norm_species(r["species"]).split()[0] for r in rows}
    report = []
    root = build(ns["TREE"], cand_norm, report)
    # heights: backbone nodes carry explicit ages, subtrees carry their own; recompute branch lengths from heights
    def fix(n):
        for c in n.children:
            c.bl = n.height - c.height
            if c.bl < 0: c.bl = 1.0
            fix(c)
    fix(root)
    tips = [t for t in root.tips() if not (t.label.startswith("__placeholder__") or t.label.startswith("__helper__"))]
    with open(out_path, "w", encoding="utf-8") as f: f.write(write_newick(root) + "\n")
    placed = {norm_species(t.label) for t in tips}
    missing = [s for s in cand if norm_species(s) not in placed]
    head = [f"stitched tree: {len(tips)} candidate species placed of {len(cand)}; root {root.height:.0f} Ma", ""]
    lines = head + report + ["", f"== not yet in any source ({len(missing)}); assemble_tree.py will gap-fill those with a congener or family member present, and list the rest"]
    if rep_path:
        open(rep_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:2] + report))

if __name__ == "__main__":
    t = threading.Thread(target=main); t.start(); t.join()
