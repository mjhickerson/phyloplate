"""Regenerate data/edible_eukaryotes_candidates.csv from data/edible_eukaryotes.txt
(lines 'species|common name|family' under '## group | clade' headers)."""
import csv, sys
src, out = sys.argv[1], sys.argv[2]
rows, group, clade, seen = [], None, None, set()
for ln, line in enumerate(open(src, encoding='utf-8'), 1):
    line = line.rstrip('\n')
    if not line.strip(): continue
    if line.startswith('## '):
        g, c = line[3:].split('|'); group, clade = g.strip(), c.strip(); continue
    sp, common, fam = [p.strip() for p in line.split('|')]
    key = sp.lower()
    if key in seen: sys.exit(f'duplicate species at line {ln}: {sp}')
    seen.add(key)
    genus = sp.split()[0].lstrip('×').strip() or sp.split()[1]
    rows.append(dict(species=sp, common_name=common, genus=genus, family=fam, clade=clade, group=group))
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['species','common_name','genus','family','clade','group'], lineterminator='\n')
    w.writeheader(); w.writerows(rows)
print(len(rows), 'species')
