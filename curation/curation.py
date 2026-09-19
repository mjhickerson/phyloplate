# Curation tables for assemble_tree.py. Edit freely; the script imports this file if present.

# Bump TREE_VERSION whenever anything below (or the species list, or the TimeTree export) changes,
# and add a CHANGELOG line: (date, who, what changed, source). Both are written into the report and shown in the app.
TREE_VERSION = "2026-09-19.2"
CHANGELOG = [
    ("2026-09-19", "Claude/MH", "First TimeTree 5 build: 2,607 dated species; 49 synonyms; 63 families anchored by hand", "TimeTree 5 export of the 3,279-name list"),
    ("2026-09-19", "Claude", "Red algae anchors revised: Gigartinales families to the Gigartinales crown; Gelidiales, Bonnemaisoniales, Ceramiales, Nemaliales to subclass stems", "Yang et al. 2016 Sci Rep 6:21361"),
    ("2026-09-19", "Claude", "Suillaceae to 130 Ma; Naematelia to 100 Ma; jellyfish to 650 Ma; Mucoromycota kept at 900 Ma", "Varga et al. 2019 Nat Ecol Evol 3:668; Park et al. 2012 Mol Phylogenet Evol; fungal timetree Nat Ecol Evol 2025"),
]

# Names as TimeTree returned them -> names in the candidate CSV.
SYNONYMS = {
    "Neopyropia yezoensis": "Pyropia yezoensis",
    "Neoporphyra haitanensis": "Pyropia haitanensis",
    "Urochloa deflexa": "Brachiaria deflexa",
    "Stipa hymenoides": "Eriocoma hymenoides",
    "Inga feuillei": "Inga feuilleei",
    "Chaenomeles sinensis": "Pseudocydonia sinensis",
    "Rhaphiolepis bibas": "Eriobotrya japonica",
    "Cormus domestica": "Sorbus domestica",
    "Juglans ailanthifolia": "Juglans ailantifolia",
    "Morella esculenta": "Myrica esculenta",
    "Morella rubra": "Myrica rubra",
    "Sicyos edulis": "Sechium edule",
    "Benincasa fistulosa": "Praecitrullus fistulosus",
    "Cucumis metulifer": "Cucumis metuliferus",
    "Chamaenerion angustifolium": "Chamerion angustifolium",
    "Zanthoxylum asiaticum": "Toddalia asiatica",
    "Vasconcellea cundinamarcensis": "Vasconcellea pubescens",
    "Corynandra viscosa": "Cleome viscosa",
    "Gynandropsis gynandra": "Cleome gynandra",
    "Lucuma campechiana": "Pouteria campechiana",
    "Wollastonia biflora": "Melanthera biflora",
    "Pseudopodospermum hispanicum": "Scorzonera hispanica",
    "Cicerbita muralis": "Mycelis muralis",
    "Ixeridium dentatum": "Ixeris dentata",
    "Anethum ridolfia": "Ridolfia segetum",
    "Anethum foeniculum": "Foeniculum vulgare",
    "Azorella polaris": "Stilbocarpa polaris",
    "Alkekengi officinarum": "Physalis alkekengi",
    "Mesosphaerum suaveolens": "Hyptis suaveolens",
    "Erythranthe guttata": "Mimulus guttatus",
    "Nopalea cochenillifera": "Opuntia cochenillifera",
    "Ceodes grandis": "Pisonia grandis",
    "Cinnamomum burmanni": "Cinnamomum burmannii",
    "Cinnamomum aromaticum": "Cinnamomum cassia",
    "Rochia nilotica": "Tectus niloticus",
    "Grimothea gregaria": "Munida gregaria",
    "Tragelaphus oryx": "Taurotragus oryx",
    "Phoca groenlandica": "Pagophilus groenlandicus",
    "Pelophylax lessonae": "Pelophylax kl. esculentus",
    "Megaleporinus obtusidens": "Leporinus obtusidens",
    "Myzopsetta ferruginea": "Limanda ferruginea",
    "Pentaceros wheeleri": "Pseudopentaceros wheeleri",
    "Pagrus auratus": "Chrysophrys auratus",
    "Lepista saeva": "Lepista personata",
    "Melothria sphaerocarpa": "Melothria scabra",
    "Galactites tomentosa": "Galactites tomentosus",
    "Planiliza haematocheilus": "Planiliza haematocheila",
    "Helostoma temminkii": "Helostoma temminckii",
    "Pseudotolithus senegallus": "Pseudotolithus senegalensis",
}

# Families with no dated member in TimeTree. Each entry: anchor families already in the tree, and
# an optional age (Myr). Without an age the family attaches as a child of the anchors' MRCA (crown).
# With an age it attaches on the stem above that MRCA at that age (i.e. as its sister clade).
PLACEMENTS = {
    # brown algae
    "Chordariaceae":      (["Laminariaceae", "Fucaceae"], None),
    "Scytosiphonaceae":   (["Laminariaceae", "Fucaceae"], None),
    # red algae
    # Gigartinales families: crown of Gigartinales = MRCA(Gigartinaceae, Cystocloniaceae), 209 Ma in TimeTree
    "Phyllophoraceae":    (["Gigartinaceae", "Cystocloniaceae"], None),
    "Solieriaceae":       (["Gigartinaceae", "Cystocloniaceae"], None),
    "Kallymeniaceae":     (["Gigartinaceae", "Cystocloniaceae"], None),
    "Caulacanthaceae":    (["Gigartinaceae", "Cystocloniaceae"], None),
    "Dumontiaceae":       (["Gigartinaceae", "Cystocloniaceae"], None),
    # early-diverging Rhodymeniophycidae orders (Gelidiales, Bonnemaisoniales): on the stem above the core
    # Rhodymeniophycidae node (349 Ma), below the Ahnfeltiophycidae split (508 Ma, Yang et al. 2016; 427 in TimeTree)
    "Gelidiaceae":        (["Gigartinaceae", "Halymeniaceae"], 400),
    "Pterocladiaceae":    (["Gigartinaceae", "Halymeniaceae"], 400),
    "Bonnemaisoniaceae":  (["Gigartinaceae", "Halymeniaceae"], 400),
    # Ceramiales: crown 335 Ma (284-395) per Yang et al. 2016; its split from the rest a little older
    "Rhodomelaceae":      (["Gigartinaceae", "Halymeniaceae"], 380),
    # Nemaliales sits in Nemaliophycidae with Palmariales; subclass split 661 Ma (Yang 2016), crown age not reported
    "Liagoraceae":        (["Palmariaceae"], 500),
    # green algae
    "Monostromataceae":   (["Ulvaceae", "Caulerpaceae"], None),
    "Prasiolaceae":       (["Ulvaceae", "Chlorellaceae"], None),
    # fungi
    "Rhizopodaceae":      (["Saccharomycetaceae", "Agaricaceae"], 900),   # Mucoromycota, sister to Dikarya
    "Mucoraceae":         (["Saccharomycetaceae", "Agaricaceae"], 900),
    "Morchellaceae":      (["Tuberaceae", "Pyronemataceae"], None),        # Pezizales crown
    "Naemateliaceae":     (["Tremellaceae"], 100),                        # Tremellales; N. aurantialba was Tremella aurantialba
    "Suillaceae":         (["Boletaceae", "Gyroporaceae"], 130),           # Boletales crown 142 (133-153) Ma, Varga et al. 2019
    "Cantharellaceae":    (["Agaricaceae", "Gomphaceae", "Hericiaceae"], None),  # Agaricomycetes crown
    "Hydnaceae":          (["Agaricaceae", "Gomphaceae", "Hericiaceae"], None),
    # invertebrates
    "Rhizostomatidae":    (["Actiniidae"], 650),   # Anthozoa/Medusozoa split; Park et al. 2012 741 (686-819) Ma, capped below TimeTree's Cnidaria/Bilateria node at 716
    "Stomolophidae":      (["Actiniidae"], 650),
    "Echinidae":          (["Parechinidae", "Strongylocentrotidae"], None),
    "Eunicidae":          (["Urechidae", "Sipunculidae"], None),
    "Pharidae":           (["Solenidae", "Hiatellidae"], None),
    "Pinnidae":           (["Ostreidae", "Pectinidae"], None),
    "Pholadidae":         (["Myidae", "Hiatellidae"], None),
    "Teredinidae":        (["Myidae", "Hiatellidae"], None),
    "Achatinidae":        (["Helicidae"], 120),
    "Potamididae":        (["Littorinidae", "Buccinidae"], None),
    "Busyconidae":        (["Buccinidae", "Muricidae"], None),
    "Tegulidae":          (["Turbinidae", "Trochidae"], None),
    "Viviparidae":        (["Ampullariidae", "Littorinidae"], None),
    "Aplysiidae":         (["Helicidae"], 300),
    "Eledonidae":         (["Octopodidae", "Enteroctopodidae"], None),
    "Enoploteuthidae":    (["Loliginidae", "Ommastrephidae"], None),
    "Pandalidae":         (["Palaemonidae", "Crangonidae"], None),
    "Solenoceridae":      (["Penaeidae", "Aristeidae"], None),
    "Sergestidae":        (["Penaeidae", "Aristeidae"], None),
    "Mysidae":            (["Penaeidae", "Euphausiidae"], 420),           # Peracarida vs Eucarida, Malacostraca crown (approx.)
    "Munididae":          (["Lithodidae", "Portunidae"], None),
    "Carcinidae":         (["Portunidae", "Cancridae"], None),
    "Ucididae":           (["Gecarcinidae", "Portunidae"], None),
    "Cheiragonidae":      (["Cancridae", "Portunidae"], None),
    "Chaoboridae":        (["Stratiomyidae"], 230),                       # Culicomorpha vs Brachycera, near the Diptera crown (approx.)
    "Vespidae":           (["Apidae", "Formicidae"], None),
    "Belostomatidae":     (["Cicadidae"], 300),
    "Corixidae":          (["Cicadidae"], 300),
    "Tessaratomidae":     (["Cicadidae"], 300),
    "Pentatomidae":       (["Cicadidae"], 300),
    "Cossidae":           (["Bombycidae", "Saturniidae"], 190),           # basal ditrysian moth (approx.)
    "Hesperiidae":        (["Bombycidae", "Saturniidae"], 130),           # Papilionoidea vs Bombycoidea (approx.)
    "Theraphosidae":      (["Scorpionidae"], 450),
    # fishes
    "Lamnidae":           (["Scyliorhinidae"], 190),
    "Triakidae":          (["Scyliorhinidae"], 150),
    "Carcharhinidae":     (["Scyliorhinidae"], 150),
    "Leiognathidae":      (["Carangidae", "Sparidae"], None),
    "Gobiesocidae":       (["Gobiidae", "Carangidae"], None),
    # plants
    "Pontederiaceae":     (["Commelinaceae"], 100),
    "Humiriaceae":        (["Euphorbiaceae", "Passifloraceae"], None),
    "Caryocaraceae":      (["Euphorbiaceae", "Passifloraceae"], None),
    "Dipterocarpaceae":   (["Malvaceae", "Cistaceae"], None),
    "Icacinaceae":        (["Rubiaceae", "Boraginaceae", "Solanaceae"], None),
    "Pittosporaceae":     (["Apiaceae", "Araliaceae"], None),
}

# Higher-level node names for the tree display, defined by anchor families (MRCA of their tips).
CLADE_NAMES = {
    "Eukaryotes": ["Bovidae", "Poaceae", "Euglenaceae"],
    "Amorphea (animals + fungi)": ["Bovidae", "Agaricaceae"],
    "Diaphoretickes (plants + algae)": ["Poaceae", "Laminariaceae"],
    "Archaeplastida": ["Poaceae", "Bangiaceae"],
    "Viridiplantae": ["Poaceae", "Ulvaceae"],
    "Land plants": ["Poaceae", "Onocleaceae"],
    "Seed plants": ["Poaceae", "Pinaceae"],
    "Angiosperms": ["Poaceae", "Nymphaeaceae"],
    "Monocots": ["Poaceae", "Araceae"],
    "Eudicots": ["Fabaceae", "Papaveraceae"],
    "Rosids": ["Fabaceae", "Brassicaceae"],
    "Asterids": ["Asteraceae", "Ericaceae"],
    "Brown algae": ["Laminariaceae", "Fucaceae"],
    "Red algae": ["Bangiaceae", "Palmariaceae"],
    "Green algae": ["Ulvaceae", "Chlorellaceae"],
    "Fungi": ["Agaricaceae", "Rhizopodaceae"],
    "Dikarya": ["Agaricaceae", "Saccharomycetaceae"],
    "Basidiomycota": ["Agaricaceae", "Ustilaginaceae"],
    "Agaricomycotina": ["Agaricaceae", "Tremellaceae"],
    "Ascomycota": ["Saccharomycetaceae", "Tuberaceae"],
    "Animals": ["Bovidae", "Actiniidae"],
    "Bilateria": ["Bovidae", "Penaeidae"],
    "Vertebrates": ["Bovidae", "Petromyzontidae"],
    "Bony fishes + tetrapods": ["Bovidae", "Salmonidae"],
    "Teleost fishes": ["Salmonidae", "Anguillidae"],
    "Tetrapods": ["Bovidae", "Ranidae"],
    "Mammals": ["Bovidae", "Tachyglossidae"],
    "Therian mammals": ["Bovidae", "Macropodidae"],
    "Birds": ["Phasianidae", "Struthionidae"],
    "Molluscs": ["Ostreidae", "Octopodidae"],
    "Arthropods": ["Penaeidae", "Limulidae"],
    "Pancrustacea": ["Penaeidae", "Gryllidae"],
    "Crustaceans (decapods)": ["Penaeidae", "Portunidae"],
    "Insects": ["Gryllidae", "Apidae"],
    "Monocots + eudicots": ["Poaceae", "Fabaceae"],
    "Lamiids": ["Solanaceae", "Lamiaceae"],
    "Campanulids": ["Asteraceae", "Apiaceae"],
    "Fabids": ["Fabaceae", "Rosaceae"],
    "Malvids": ["Brassicaceae", "Malvaceae"],
    "Commelinids": ["Poaceae", "Zingiberaceae"],
    "Ruminants": ["Bovidae", "Cervidae"],
    "Even-toed ungulates": ["Bovidae", "Camelidae"],
    "Rodents": ["Caviidae", "Sciuridae"],
    "Percomorph fishes": ["Carangidae", "Sparidae"],
    "Cartilaginous fishes": ["Squalidae", "Chimaeridae"],
    "Bivalves": ["Ostreidae", "Veneridae"],
    "Gastropods": ["Helicidae", "Haliotidae"],
    "Cephalopods": ["Octopodidae", "Loliginidae"],
    "Bees, wasps and ants": ["Apidae", "Formicidae"],
    "Beetles": ["Tenebrionidae", "Curculionidae"],
    "Moths and butterflies": ["Bombycidae", "Saturniidae"],
    "Agaricales (gilled mushrooms)": ["Agaricaceae", "Omphalotaceae"],
    "Cnidarians": ["Actiniidae", "Rhizostomatidae"],
    "Echinoderms": ["Strongylocentrotidae", "Stichopodidae"],
}
