# Phyloplate

**How much of the tree of life is on your plate?**

Phyloplate scores a meal by the phylogenetic diversity of the organisms in it. You paste a recipe or name a dish; the app maps each ingredient to the species it came from, prunes a dated tree of edible eukaryotes down to those species, and adds up the branch lengths. The result is Faith's phylogenetic diversity (PD) in millions of years of evolution, reported alongside plain species richness, a coverage percentage, and a drawing of the meal's tree.

A cheeseburger with fries is about 3.7 billion years of branch length. A Japanese set meal with kombu, nori, and miso is about 7.7. A pinch of nori adds more than the entire spice rack, because red algae split from land plants about 1.4 billion years ago and thyme split from oregano about 12 million years ago.

![The meal tree for a Japanese set meal](docs/images/meal_tree.png)

## The idea

Dietary species richness (the number of species eaten) has been proposed as a measure of food biodiversity and shown to track nutrient adequacy (Lachat et al. 2018, *PNAS*). Phyloplate is the phylogenetic version of that count, in the same way that Faith's PD (1992) was the phylogenetic version of species richness in conservation biology. Whether PD on a plate predicts anything nutritionally is an open question; the point here is that it is computable, visual, and fun, and that it makes deep time tangible. Two meals with the same number of species can differ tenfold in PD, and the difference is always the same story: seaweed, mushrooms, and the odd invertebrate.

Prokaryotes are excluded on purpose (they are on everything). Amounts are ignored in the current version; an abundance-weighted score (Chao, Chiu & Jost's phylogenetic Hill numbers) is the planned next step.

## What is in this repository

| Path | What it is |
|---|---|
| `data/edible_eukaryotes.txt` | The curated list of eukaryotes people eat: 3,279 species with common names and families, grouped by clade. **This is the primary data product.** Edit this file; the CSV is generated from it. |
| `data/edible_eukaryotes_candidates.csv` | The same list as a CSV (species, common name, genus, family, clade, group). |
| `curation/curation.py` | Synonym map for names as TimeTree and other sources return them; the table of hand-placed families (anchor groups and stem ages); higher-clade node names; tree version and changelog. |
| `curation/anchor_review.csv` | One row per hand-placed family with the basis for the placement, a confidence rating, and blank columns for expert review. |
| `scripts/assemble_tree.py` | Takes any dated Newick plus the species list and produces the app's tree: matches species, applies synonyms, gap-fills missing species next to congeners, at family nodes, or by anchor, names internal nodes, and writes a report. Pure Python, no dependencies. |
| `scripts/bake.py` | Builds the single-file app from a tree and the HTML template. |
| `scripts/make_placeholder_tree.py` | Generates the 289-taxon placeholder tree used in the demo build, from hand-set node ages. |
| `app/template.html` | The app: ingredient parsing, PD and richness, meal phylogram, radial coverage view, meal log, custom-tree loader. |
| `app/phyloplate_demo.html` | A working demo built on the placeholder tree. Open it in a browser. |
| `tree/` | The placeholder tree (`food_tree.newick`, `taxa.csv`) and its version stamp. |

![Coverage of the edible tree](docs/images/coverage.png)

## About the tree and its ages

**The demo tree in this repository uses placeholder ages.** Deep nodes follow published ranges loosely; shallow nodes are educated guesses. It exists so the pipeline and the app can be run and inspected. Do not quote numbers from it.

The working version of Phyloplate runs on a tree with divergence times from TimeTree 5 (Kumar et al. 2022) for 2,607 of the 3,279 species, with the rest placed by the rules in `curation.py`. TimeTree's terms of use restrict redistribution of its data and transformations of it, so that tree is **not** included here, and no file derived from it will be committed. A fully open replacement assembled from published, redistributable chronograms (Smith & Brown 2018 for seed plants, Rabosky et al. 2018 for fishes, Upham et al. 2019 for mammals, Jetz et al. 2012 for birds, Varga et al. 2019 for mushrooms, Yang et al. 2016 for red algae, and others) on an OpenTree backbone is planned; the pipeline is source-agnostic and will regenerate from it unchanged.

Every hand-placed family is listed in `curation/anchor_review.csv` with its basis and confidence. Corrections from specialists are welcome as pull requests to `curation.py` or as filled-in rows of that sheet. Every change to the tree bumps `TREE_VERSION` and gets a changelog line.

## Running the pipeline

```
# regenerate the CSV from the text list
python3 scripts/build_candidates.py data/edible_eukaryotes.txt data/edible_eukaryotes_candidates.csv

# assemble an app tree from any dated Newick (tips = species names)
python3 scripts/assemble_tree.py dated.nwk data/edible_eukaryotes_candidates.csv out/

# build the app
python3 scripts/bake.py out/food_tree.newick out/taxa.csv app/template.html phyloplate.html
```

`assemble_tree.py` imports `curation.py` from the working directory if present. The report it writes (`assembly_report.txt`) lists every species that was matched, renamed, gap-filled, or left out.

Ingredient parsing in the app uses a language model to turn recipe text into Latin binomials, which the page then resolves against its own taxon table; nothing outside the table can be scored. In the demo build the model call is unavailable, and the app falls back to keyword matching against the table's alias column.

## Status and roadmap

- [x] Working prototype: parsing, PD, richness, coverage, meal phylogram, radial coverage, meal log
- [x] Species list (3,279) and placement tables
- [x] Assembly pipeline with synonyms, gap-filling, node naming, versioning
- [ ] Open, redistributable dated tree
- [ ] Standalone hosting with the tree server-side
- [ ] Abundance-weighted PD (phylogenetic Hill numbers)
- [ ] Per-week aggregation and a richness-controlled coverage score

## Citing

Hickerson, M.J. (2026). Phyloplate: phylogenetic diversity of what you eat. Software and data, version 0.1.0. https://github.com/<user>/phyloplate

Code is MIT-licensed; the species list and curation tables are CC BY 4.0 (see `data/LICENSE`).

## Acknowledgements

Faith (1992) for PD; Lachat et al. (2018) for dietary species richness; TimeTree (Kumar et al. 2022) for the divergence times in the working build. The idea dates from about 2015, when a grad student sensibly declined to build it.
