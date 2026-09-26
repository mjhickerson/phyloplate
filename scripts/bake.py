"""Convert the assembled food_tree.newick + taxa.csv into the nested JSON the page embeds, add the dish table, then build the page.
Usage: bake.py food_tree.newick taxa.csv template.html out.html [dishes.csv]"""
import sys, os, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assemble_tree import parse_newick, set_heights
nwk, tcsv, template, out = sys.argv[1:5]
dishes_csv = sys.argv[5] if len(sys.argv) > 5 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'dishes.csv')
root = parse_newick(open(nwk).read()); set_heights(root)
meta = {r['id']: r for r in csv.DictReader(open(tcsv))}
def conv(n):
    if n.is_tip():
        r = meta[n.label]
        return {"id": r['id'], "common": r['common_name'], "species": r['species'], "lineage": r['lineage'],
                "clade": r['clade'], "aliases": r['aliases'], "age": 0.0}
    return {"name": n.label, "age": round(n.height, 3), "children": [conv(c) for c in n.children]}
tree = conv(root)
import os
vpath = os.path.join(os.path.dirname(nwk), 'tree_version.txt')
version = open(vpath).read().strip() if os.path.exists(vpath) else 'unversioned'
tree['version'] = version
js = json.dumps(tree, separators=(',', ':')).replace('</script>', '<\\/script>')
def _read(name, default):
    q = os.path.join(os.path.dirname(nwk), name)
    return open(q).read().strip() if os.path.exists(q) else default
provenance = _read('provenance.txt', 'Node ages in this build are approximate placeholders: deep splits follow published ranges loosely, shallow ones are educated guesses. Do not quote them.')
credit = _read('credit.txt', 'Tree data: placeholder ages, not citable.')
# dish lookup table: name + aliases -> species list; species resolved by the page against its taxon table
dishes = []
if os.path.exists(dishes_csv):
    for r in csv.DictReader(open(dishes_csv)):
        names = [r['dish'].strip()] + [a.strip() for a in r.get('aliases', '').split(';') if a.strip()]
        sps = [x.strip() for x in r['species'].split(';') if x.strip()]
        if names[0] and sps: dishes.append({"n": names, "c": r.get('cuisine', '').strip(), "s": sps})
dv = os.path.join(os.path.dirname(dishes_csv), 'dishes_version.txt')
dishes_version = open(dv).read().strip() if os.path.exists(dv) else 'unversioned'
djs = json.dumps({"version": dishes_version, "dishes": dishes}, separators=(',', ':'), ensure_ascii=False).replace('</script>', '<\\/script>')
html = (open(template).read().replace('__TREE_JSON__', js).replace('__DISHES_JSON__', djs).replace('__DISHES_VERSION__', dishes_version).replace('__TREE_VERSION__', version)
        .replace('__TREE_PROVENANCE__', provenance).replace('__TREE_CREDIT__', credit))
open(out, 'w').write(html)
print('tips', len(meta), 'json bytes', len(js), 'dishes', len(dishes), 'html bytes', len(html))
