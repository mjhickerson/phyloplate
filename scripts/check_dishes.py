"""Validate data/dishes.csv against tree/taxa.csv: every species must resolve to a tip (exact binomial, or genus fallback with a warning).
Usage: python3 scripts/check_dishes.py data/dishes.csv tree/taxa.csv"""
import csv, sys, collections
dishes_csv, taxa_csv = sys.argv[1:3]
taxa = {r['species'].lower(): r for r in csv.DictReader(open(taxa_csv))}
genera = collections.defaultdict(list)
for k, r in taxa.items(): genera[k.split()[0]].append(r['species'])
rows = list(csv.DictReader(open(dishes_csv)))
names = collections.Counter()
bad = 0
for r in rows:
    for n in [r['dish']] + [a.strip() for a in r['aliases'].split(';') if a.strip()]:
        names[n.lower()] += 1
    seen = set()
    for sp in [s.strip() for s in r['species'].split(';') if s.strip()]:
        k = sp.lower()
        if k in seen: print(f"dup      {r['dish']}: {sp}"); bad += 1
        seen.add(k)
        if k in taxa: continue
        g = k.split()[0]
        if g in genera: print(f"genus    {r['dish']}: {sp} -> will use {genera[g][0]}")
        else: print(f"MISSING  {r['dish']}: {sp}"); bad += 1
for n, c in names.items():
    if c > 1: print(f"name used {c}x: {n}")
print(f"{len(rows)} dishes, {len(names)} names, {sum(len(r['species'].split(';')) for r in rows)} species slots, {bad} problems")
sys.exit(1 if bad else 0)
