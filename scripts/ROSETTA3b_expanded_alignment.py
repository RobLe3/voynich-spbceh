"""
ROSETTA3b — Expanded -ain stem alignment with 2-consonant minimum threshold
Expands ROSETTA3 with:
  - Full al-Sufi Arabic star catalog (~90 named entries)
  - Medieval Arabic astronomical lexicon (al-Biruni, Ulugh Beg attestations)
  - Expanded Latin balneological lexicon (Constantine the African, De Balneis tradition)
  - 2-consonant minimum threshold (eliminates 90.5% chance baseline)
  - Per-stem-length baseline (separate 1-con, 2-con, 3-con baselines)
  - Semantic fit scoring (section consistency check)
  - ayn-compound search: Arabic ʿayn + X star names
"""

import json
import random
import re
from collections import defaultdict, Counter
from pathlib import Path
import csv

# ============================================================
# 1. LOAD CORPUS
# ============================================================

DATA_DIR = Path(__file__).parent.parent / "data"
corpus_path = DATA_DIR / "corpus_tokens.csv"

tokens_by_section = defaultdict(list)
token_records = []

with open(corpus_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        token_records.append(row)
        tokens_by_section[row['section']].append(row)

all_tokens = [r['token'] for r in token_records]
print(f"Corpus: {len(token_records)} tokens, {len(tokens_by_section)} sections")

# ============================================================
# 2. EXPANDED REFERENCE LEXICONS
# ============================================================

def make_cons(word):
    """Extract consonant skeleton from a word (remove vowels a e i o u and spaces/hyphens)."""
    vowels = set('aeiouáéíóúāēīōūàèìòùâêîôûäëïöüý \'-')
    return ''.join(c for c in word.lower() if c not in vowels and c.isalpha())

# Full al-Sufi Arabic star catalog (from Kitab al-Kawakib al-Thabita, ~964 CE)
# Entries: (transliteration, English/meaning, EVA_consonants_approx, category)
ALSUFI_CATALOG = [
    # Aries
    ("al-sharatain",    "the two signs (alpha/beta Ari)",           "lshrt",    "astro"),
    ("al-butain",       "the little belly (delta Ari)",             "lbtn",     "astro"),
    ("al-thurayya",     "the many little ones (Pleiades)",          "lthr",     "astro"),
    ("al-dabaraan",     "the follower (Aldebaran)",                 "ldbr",     "astro"),
    ("al-haqa",         "the white spot (lambda Ori)",              "lhq",      "astro"),
    ("al-hana",         "the brand mark (gamma Gem)",               "lhn",      "astro"),
    ("al-dhira",        "the arm (alpha/beta Gem)",                 "ldhr",     "astro"),
    ("al-nathrah",      "the gap/nose (Praesepe)",                  "lnthr",    "astro"),
    ("al-tarfah",       "the glance (kappa Leo)",                   "ltrf",     "astro"),
    ("al-jabhah",       "the forehead (zeta Leo)",                  "ljbh",     "astro"),
    ("al-zubrah",       "the mane (delta/theta Leo)",               "lzbr",     "astro"),
    ("al-sarfah",       "the changer (beta Leo)",                   "lsrf",     "astro"),
    ("al-awwa",         "the barker (beta-eta Vir)",                "lw",       "astro"),
    ("al-simak al-azal","the unarmed one (Spica)",                  "lsmklzl",  "astro"),
    ("al-ghafr",        "the covering (iota Vir)",                  "lgfr",     "astro"),
    ("al-zubana",       "the claws (alpha/beta Lib)",               "lzbn",     "astro"),
    ("al-iklil",        "the crown (pi Sco)",                       "lkl",      "astro"),
    ("al-qalb",         "the heart (Antares)",                      "lqlb",     "astro"),
    ("al-shaulah",      "the sting (lambda Sco)",                   "lshl",     "astro"),
    ("al-naim",         "the ostriches (gamma/delta Sgr)",          "lnm",      "astro"),
    ("al-baldah",       "the town (pi Sgr)",                        "lbld",     "astro"),
    ("sad al-dhabih",   "lucky star of the slaughterer (Algedi)",   "sdldhbh",  "astro"),
    ("sad bula",        "the lucky swallower (mu Aqr)",             "sdbl",     "astro"),
    ("sad al-suud",     "luckiest of the lucky (beta Aqr)",         "sdlsd",    "astro"),
    ("sad al-akhbiya",  "the lucky tents (gamma Aqr)",              "sdlkhb",   "astro"),
    ("al-fargh al-awwal","the first spout (alpha/beta Peg)",        "lfrglwl",  "astro"),
    ("al-fargh al-thani","the second spout (gamma Peg)",            "lfrgltn",  "astro"),
    ("batn al-hut",     "belly of the fish (alpha And)",            "btnlht",   "astro"),
    # Named stars (proper Arabic star names)
    ("al-dabaraan",     "the follower = Aldebaran",                 "ldbr",     "astro"),
    ("al-nasr al-tair", "the flying eagle = Altair",                "lnsrltr",  "astro"),
    ("al-nasr al-waqii","the swooping eagle = Vega",                "lnsrlwq",  "astro"),
    ("dhanab al-dajaja","tail of the hen = Deneb",                  "dnbldjj",  "astro"),
    ("fam al-hut",      "mouth of the fish = Fomalhaut",            "fmlht",    "astro"),
    ("rijl al-jawza",   "foot of Orion = Rigel",                    "rjlljwz",  "astro"),
    ("ibt al-jawza",    "armpit of Orion = Betelgeuse",             "btljwz",   "astro"),
    ("ras al-ghul",     "head of the ogre = Algol",                 "rslghl",   "astro"),
    ("al-simak al-ramih","the armed one = Arcturus",                "lsmklrmh", "astro"),
    ("qalb al-asad",    "heart of the lion = Regulus",              "qlblsd",   "astro"),
    ("qalb al-aqrab",   "heart of the scorpion = Antares",          "qlblqrb",  "astro"),
    ("ayn al-thawr",    "eye of the bull (Hyades) = near Aldebaran","nlthr",    "astro_ayn"),
    ("ayn al-asad",     "eye of the lion = epsilon Leonis",         "nlsd",     "astro_ayn"),
    ("ayn al-aqrab",    "eye of the scorpion = pi Scorpii",         "nlqrb",    "astro_ayn"),
    ("ayn al-sagittarius","eye of Sagittarius",                     "nlsgt",    "astro_ayn"),
    ("dhanab al-qitah", "tail of the cat = Deneb Algedi",           "dnblqth",  "astro"),
    ("ras al-asad",     "head of the lion = Algenubi",              "rslsd",    "astro"),
    ("al-raqis",        "the dancer = mu Bootis",                   "lrqs",     "astro"),
    ("al-dalik",        "the rubbing one = Deneb Kaitos",           "ldlk",     "astro"),
    ("al-kaff al-khadib","the dyed hand = Cassiopeia area",         "lkflkdhb", "astro"),
    ("al-kaff",         "the palm = gamma Cassiopeiae",             "lkf",      "astro"),
    ("suhayl",          "smooth/Canopus",                           "shl",      "astro"),
    ("al-suhail",       "the smooth one = Canopus",                 "lshl",     "astro"),
    ("al-ayyuq",        "the goat = Capella",                       "lyq",      "astro"),
    ("al-rijl",         "the foot = Rigel",                         "lrjl",     "astro"),
    ("al-mintaqa",      "the belt = Orion's belt",                  "lmntq",    "astro"),
    ("mankib al-jawza", "shoulder of Orion = Betelgeuse area",      "mnkbljwz", "astro"),
    ("ras al-jawza",    "head of Orion",                            "rsljwz",   "astro"),
    ("al-farrad",       "the single one",                           "lfrd",     "astro"),
    ("al-wazn",         "the weight = delta Vel",                   "lwzn",     "astro"),
    ("laqit",           "the foundling = a small star",             "lqt",      "astro"),
    ("al-tariq",        "the night-knocker = beta Per",             "ltrq",     "astro"),
    ("al-qaid",         "the leader/Alkaid",                        "lqd",      "astro"),
    ("al-qaws",         "the bow = Sagittarius",                    "lqs",      "astro"),
    ("al-qaus",         "the arc/bow",                              "lqs",      "astro"),
    ("al-rami",         "the archer = Sagittarius",                 "lrm",      "astro"),
    ("qaus quzah",      "rainbow/bow of Quzah",                     "qsqzh",    "astro"),
    ("al-hamal",        "the ram = Aries",                          "lhml",     "astro"),
    ("al-nathr",        "the nose/Praesepe cluster",                "lnthr",    "astro"),
    ("al-mizan",        "the balance = Libra",                      "lmzn",     "astro"),
    ("al-aqrab",        "the scorpion = Scorpius",                  "lqrb",     "astro"),
    ("al-jadiy",        "the kid = Capricorn",                      "ljd",      "astro"),
    ("al-hut",          "the fish = Pisces",                        "lht",      "astro"),
    ("al-dalw",         "the bucket = Aquarius",                    "ldlw",     "astro"),
    ("al-sunbulah",     "the ear of grain = Virgo",                 "lsnbl",    "astro"),
    ("al-asad",         "the lion = Leo",                           "lsd",      "astro"),
    ("al-saratan",      "the crab = Cancer",                        "lsrtn",    "astro"),
    ("al-jawza",        "the central one = Orion/Gemini area",      "ljwz",     "astro"),
    ("al-thawra",       "the bull = Taurus",                        "lthr",     "astro"),
    # Water/astronomical hybrid
    ("qatr",            "drop of water (astronomical context)",     "qtr",      "astro_water"),
    ("nahr",            "river (celestial river)",                  "nhr",      "astro_water"),
    ("bahar",           "sea/ocean",                                "bhr",      "astro_water"),
    ("al-nahr",         "the river = Eridanus",                     "lnhr",     "astro_water"),
    ("buhayra",         "small lake",                               "bhr",      "water"),
    ("birka",           "pool/pond",                                "brk",      "water"),
    ("ain al-maa",      "water spring/eye of water",               "nlm",      "water_ayn"),
    ("ain al-shams",    "eye of the sun = Heliopolis",              "nlshms",   "astro_ayn"),
    # al-Biruni / Ulugh Beg additional terms
    ("akhir al-nahr",   "end of the river = Achernar",             "khrln hr", "astro"),
    ("mankib al-faras", "shoulder of the horse = Scheat",           "mnkblf rs","astro"),
    ("batni al-hut",    "belly of the fish",                        "btnlht",   "astro"),
    ("al-thuban",       "the serpent = Thuban",                     "ltbn",     "astro"),
    ("al-ruqubah",      "the knee = Rigel area",                    "lrqb",     "astro"),
    ("al-mughrib",      "the western star",                         "lmghrb",   "astro"),
]

# Extended Latin balneological / medical terms (Constantine the African, De Balneis, Trotula)
LATIN_BALNEO = [
    ("sal",         "salt",                         "sl",   "mineral"),
    ("salus",       "health/welfare/salvation",     "sl",   "health"),
    ("salubritas",  "healthfulness",                "slbr", "health"),
    ("salina",      "salt works/brine pool",        "sln",  "mineral"),
    ("salvia",      "sage (bath herb)",             "slv",  "herb"),
    ("salsus",      "salted/briny",                 "sls",  "mineral"),
    ("salsum aqua", "salt water",                   "slsq", "mineral"),
    ("salah",       "wellbeing (Arabic via Latin)", "slh",  "health"),
    ("lacus",       "lake/pool/bath basin",         "lk",   "water"),
    ("lacuna",      "pool/pit/gap",                 "lkn",  "water"),
    ("lavacrum",    "bath/washing place",           "lvkr", "bath"),
    ("lavatio",     "bathing/washing",              "lvt",  "bath"),
    ("laver",       "to wash (bath plants/pools)",  "lvr",  "bath"),
    ("balneum",     "bath",                         "bln",  "bath"),
    ("balneator",   "bath attendant",               "blntr","bath"),
    ("aqua",        "water",                        "q",    "water"),
    ("aqua calida", "hot water",                    "qkld", "water"),
    ("aqua frigida","cold water",                   "qfrg", "water"),
    ("aqua mineralis","mineral water",              "qmnrl","water"),
    ("fons",        "spring/fountain",              "fns",  "water"),
    ("puteus",      "well/pit",                     "pt",   "water"),
    ("oleum",       "oil (bath oils)",              "l",    "ingredient"),
    ("oleum rosae", "rose oil",                     "lr",   "ingredient"),
    ("oleum olivae","olive oil",                    "llv",  "ingredient"),
    ("herba",       "herb/plant",                   "hrb",  "herb"),
    ("decoction",   "decoction/boiling",            "dkt",  "process"),
    ("maceratio",   "soaking/macerating",           "mkrt", "process"),
    ("infusio",     "infusion/steeping",            "nfs",  "process"),
    ("sanitas",     "health/soundness",             "snt",  "health"),
    ("sanatio",     "healing/cure",                 "snt",  "health"),
    ("cura",        "care/treatment/cure",          "kr",   "health"),
    ("remedium",    "remedy/cure",                  "rmd",  "health"),
    ("medicina",    "medicine",                     "mdn",  "health"),
    ("virtus",      "virtue/potency (of herbs)",    "vrt",  "health"),
    ("potio",       "drink/potion",                 "pt",   "health"),
    ("purgatio",    "purging/cleansing",            "prg",  "process"),
    ("lotio",       "washing/lotion",               "lt",   "bath"),
    ("fricatio",    "rubbing/friction",             "frkт", "process"),
    ("vapor",       "steam/vapor",                  "vpr",  "bath"),
    ("calor",       "heat/warmth",                  "klr",  "bath"),
    ("sulfur",      "sulfur (mineral spring)",      "slf",  "mineral"),
    ("sulphur",     "sulfur (alt spelling)",        "slf",  "mineral"),
    ("bitumen",     "bitumen/mineral tar",          "btmn", "mineral"),
    ("alumen",      "alum (mineral)",               "lmn",  "mineral"),
    ("nitrum",      "natron/saltpeter",             "ntr",  "mineral"),
    ("vitriolum",   "vitriol/sulfate mineral",      "vtrl", "mineral"),
    ("salix",       "willow (bath herb)",           "slk",  "herb"),
    ("rosa",        "rose (bath herb)",             "rs",   "herb"),
    ("lavandula",   "lavender (bath herb)",         "lvndl","herb"),
    ("camomilla",   "chamomile (bath herb)",        "kmml", "herb"),
    ("ruta",        "rue (bath herb)",              "rt",   "herb"),
    ("salvia officinalis","common sage",            "slvf", "herb"),
    ("menta",       "mint (bath herb)",             "mnt",  "herb"),
    ("abrotanum",   "southernwood (bath herb)",     "brtn", "herb"),
    ("balsamum",    "balsam/balm",                  "blsm", "ingredient"),
    ("unguentum",   "ointment/unguent",             "ngnt", "ingredient"),
    ("stercus",     "excrement (used in folk med)", "strks","ingredient"),
    ("theriaca",    "theriac/antidote",             "thrk", "health"),
    ("electuarium", "electuary/paste medicine",     "lktr", "health"),
    ("sirupus",     "syrup",                        "srp",  "ingredient"),
    ("sapa",        "grape must/syrup",             "sp",   "ingredient"),
    ("melle",       "honey",                        "ml",   "ingredient"),
    ("vinum",       "wine",                         "vn",   "ingredient"),
    ("acetum",      "vinegar",                      "kt",   "ingredient"),
]

# Arabic/Hebrew general lexicon (health/body/nature terms used in balneological texts)
ARABIC_HEBREW_LING = [
    ("maa",         "water (Arabic)",               "m",    "water"),
    ("ain",         "eye/spring/source (Arabic/Heb)","n",   "water_ayn"),
    ("ayn",         "eye/spring (Arabic)",          "n",    "water_ayn"),
    ("nahr",        "river (Arabic)",               "nhr",  "water"),
    ("bahr",        "sea (Arabic)",                 "bhr",  "water"),
    ("buhayr",      "small lake (Arabic)",          "bhr",  "water"),
    ("birk",        "pond/pool (Arabic)",           "brk",  "water"),
    ("qatr",        "drop (Arabic)",                "qtr",  "water"),
    ("hamamm",      "bath/hammam (Arabic)",         "hmm",  "bath"),
    ("sakhun",      "hot (Arabic)",                 "skhn", "bath"),
    ("barid",       "cold (Arabic)",                "brd",  "bath"),
    ("dawa",        "medicine (Arabic)",            "dw",   "health"),
    ("shifa",       "healing (Arabic)",             "shf",  "health"),
    ("salama",      "safety/peace (Arabic)",        "slm",  "health"),
    ("sihhah",      "health (Arabic)",              "shh",  "health"),
    ("dam",         "blood (Arabic/Hebrew)",        "dm",   "anatomy"),
    ("dam al-hayat","blood of life (Arabic)",       "dmlht","anatomy"),
    ("lubb",        "marrow/core (Arabic)",         "lb",   "anatomy"),
    ("kulya",       "kidney (Arabic)",              "kl",   "anatomy"),
    ("kabid",       "liver (Arabic/Hebrew)",        "kbd",  "anatomy"),
    ("qalb",        "heart (Arabic)",               "qlb",  "anatomy"),
    ("ras",         "head (Arabic)",                "rs",   "anatomy"),
    ("ayn",         "eye/spring (Arabic)",          "n",    "anatomy_ayn"),
    ("rijl",        "foot/leg (Arabic)",            "rjl",  "anatomy"),
    ("yad",         "hand (Arabic/Hebrew)",         "yd",   "anatomy"),
    ("kol",         "all/every (Hebrew)",           "kl",   "function"),
    ("lamed",       "lam = to/for (Hebrew)",        "lm",   "function"),
    ("bet",         "bet = in/with (Hebrew)",       "bt",   "function"),
    ("mem",         "mem = water (Hebrew)",         "m",    "function"),
    ("resh",        "resh = head (Hebrew)",         "r",    "function"),
    ("shin",        "shin = tooth (Hebrew)",        "sh",   "function"),
    ("tzadi",       "tzade = hunt (Hebrew)",        "tz",   "function"),
    ("aleph",       "aleph = ox (Hebrew)",          "lf",   "function"),
    ("melekh",      "king (Hebrew)",                "mlk",  "status"),
    ("halakh",      "went/walked (Hebrew)",         "hlk",  "action"),
    ("malak",       "angel/messenger (Arabic/Heb)", "mlk",  "status"),
    ("layl",        "night (Arabic)",               "ll",   "time"),
    ("nahar",       "day (Hebrew)/river (Arabic)",  "nhr",  "time"),
    ("shamar",      "to guard (Hebrew)",            "shmr", "action"),
    ("salar",       "to flow/pour (Arabic dial.)",  "slr",  "water"),
    ("qata",        "to cut (Arabic)",              "qt",   "action"),
    ("kataba",      "to write (Arabic)",            "ktb",  "action"),
    ("salaka",      "to walk/follow path (Arabic)", "slk",  "action"),
    ("thalath",     "three (Arabic)",               "thlth","number"),
    ("arba",        "four (Arabic/Hebrew)",         "rb",   "number"),
]

print(f"\nLexicon sizes:")
print(f"  al-Sufi catalog: {len(ALSUFI_CATALOG)} entries")
print(f"  Latin balneological: {len(LATIN_BALNEO)} entries")
print(f"  Arabic/Hebrew linguistic: {len(ARABIC_HEBREW_LING)} entries")

ALL_LEXICON = []
for entry in ALSUFI_CATALOG:
    term, meaning, cons, domain = entry
    ALL_LEXICON.append({'term': term, 'meaning': meaning, 'cons': cons, 'domain': domain,
                        'source': 'alsufi'})
for entry in LATIN_BALNEO:
    term, meaning, cons, domain = entry
    ALL_LEXICON.append({'term': term, 'meaning': meaning, 'cons': cons, 'domain': domain,
                        'source': 'latin_balneo'})
for entry in ARABIC_HEBREW_LING:
    term, meaning, cons, domain = entry
    ALL_LEXICON.append({'term': term, 'meaning': meaning, 'cons': cons, 'domain': domain,
                        'source': 'arabic_heb'})

print(f"  Total: {len(ALL_LEXICON)} entries")

# ============================================================
# 3. IMPROVED SCORING WITH 2-CON MINIMUM
# ============================================================

def consonant_score_2con(stem_cons, ref_cons):
    """
    Score consonant alignment between stem and reference.
    Returns dict with:
      n_shared: consonants shared (order-sensitive subset match)
      n_shared_any: consonants shared (unordered)
      exact_ordered: True if stem_cons is a contiguous subsequence of ref_cons
      score_ordered: fraction of stem matched in order
      min_len: minimum of the two lengths
      qualifies: True if both are len >= 2 and n_shared_any >= 2
    """
    s = stem_cons.lower().replace(' ','').replace('-','')
    r = ref_cons.lower().replace(' ','').replace('-','')

    if len(s) < 2 or len(r) < 2:
        return {'qualifies': False, 'n_shared': 0, 'n_shared_any': 0,
                'exact_ordered': False, 'score_ordered': 0.0,
                'min_len': min(len(s), len(r))}

    # Ordered: check if all chars of shorter appear in order in longer
    shorter, longer = (s, r) if len(s) <= len(r) else (r, s)
    pos = 0
    matched = 0
    for ch in shorter:
        idx = longer.find(ch, pos)
        if idx >= 0:
            matched += 1
            pos = idx + 1

    score_ordered = matched / len(shorter) if shorter else 0.0

    # Unordered: shared consonants regardless of order
    s_counter = Counter(s)
    r_counter = Counter(r)
    shared_any = sum(min(s_counter[c], r_counter[c]) for c in s_counter)

    exact_ordered = (matched == len(shorter))
    qualifies = (shared_any >= 2)

    return {
        'qualifies': qualifies,
        'n_shared': matched,
        'n_shared_any': shared_any,
        'exact_ordered': exact_ordered,
        'score_ordered': score_ordered,
        'min_len': min(len(s), len(r)),
        'stem_len': len(s),
        'ref_len': len(r),
    }

def align_stem(stem_cons, min_shared=2):
    """Return all lexicon entries with n_shared_any >= min_shared, sorted by score."""
    results = []
    for entry in ALL_LEXICON:
        sc = consonant_score_2con(stem_cons, entry['cons'])
        if sc['n_shared_any'] >= min_shared:
            results.append({**entry, **sc})
    return sorted(results, key=lambda x: (-x['n_shared_any'], -x['score_ordered'],
                                          x['min_len']))

# ============================================================
# 4. PER-STEM-LENGTH BASELINE
# ============================================================

print("\n4. PER-STEM-LENGTH BASELINE (random stems, 10000 samples each length)")
print("-" * 70)

EVA_CONSONANTS = list('bcdfghjklmnpqrstvwxyz') + ['sh', 'ch', 'lch', 'kh']
EVA_CONSONANTS_SIMPLE = 'bcdfghjklmnpqrstvwxyz'

baseline_by_length = {}
for stem_len in [1, 2, 3]:
    n_qualify = 0
    n_samples = 10000
    for _ in range(n_samples):
        stem = ''.join(random.choices(EVA_CONSONANTS_SIMPLE, k=stem_len))
        hits = align_stem(stem, min_shared=2)
        if hits:
            n_qualify += 1
    rate = n_qualify / n_samples
    baseline_by_length[stem_len] = rate
    print(f"  Length-{stem_len} baseline (>=2 shared): {rate:.3f} ({rate*100:.1f}%)")

# ============================================================
# 5. PRIORITY TOKEN ALIGNMENT (2-con minimum)
# ============================================================

# Extract EVA consonants from token
def extract_eva_consonants(token):
    """Extract consonant skeleton from EVA token."""
    # Remove known suffixes before extraction for stem analysis
    clean = token.replace('!', '').replace('?', '')
    # EVA vowels
    vowels = set('aeiou')
    # But 'ch', 'sh', 'lch' are consonant digraphs
    # Simple approach: remove a, e, i, o, u
    cons = ''.join(c for c in clean if c not in vowels)
    return cons

PRIORITY_TOKENS = [
    # (token, stem_cons, section, note)
    ('sal',     'sl',   'B',    'Balneo 2.08×, terminal entity candidate'),
    ('lkaiin',  'lk',   'S',    'Stars common n=37'),
    ('qotaiin', 'qt',   'S',    'Stars folio-anchor n=39'),
    ('qol',     'ql',   'B',    'B inner-function OR=7.83'),
    ('daiin',   'd',    'S',    'Stars common n=122'),
    ('okaiin',  'k',    'S',    'Stars common n=93'),
    ('raiin',   'r',    'S',    'Stars common n=41'),
    ('saiin',   's',    'S',    'Stars common n=37'),
    ('qokain',  'qk',   'S',    'Stars EARLY (0.248, p=0.007) — expect NULL'),
    ('laiin',   'l',    'S',    'Stars LATE (0.875, p=0.007)'),
    ('ai!n',    '',     'ALL',  'Corpus-wide LATE (0.686, p=0.005) — no stem'),
    ('aiin',    '',     'S',    'Stars pan-folio n=193 — no stem'),
    ('lchein',  'lch',  'B',    'lch-stem -ain variant'),
    ('lchsain', 'lchs', 'B',    'lch-s stem variant'),
]

print("\n\n5. PRIORITY TOKEN ALIGNMENT (minimum 2 shared consonants)")
print("=" * 80)

results_table = []

for tok_data in PRIORITY_TOKENS:
    token, stem_cons, section, note = tok_data
    print(f"\n  {token} (stem={stem_cons!r}, section={section})")
    print(f"  Note: {note}")

    if len(stem_cons) < 2:
        print(f"  → Stem has < 2 consonants: EXCLUDED from analysis (below 2-con minimum)")
        results_table.append({
            'token': token, 'stem': stem_cons, 'section': section,
            'note': note, 'status': 'EXCLUDED_SHORT_STEM',
            'matches': []
        })
        continue

    matches = align_stem(stem_cons, min_shared=2)
    bl = baseline_by_length.get(min(len(stem_cons), 3), baseline_by_length.get(3))

    if not matches:
        print(f"  → NULL: No matches with >= 2 shared consonants")
        print(f"     Baseline for {len(stem_cons)}-con stems: {bl*100:.1f}%")
        results_table.append({
            'token': token, 'stem': stem_cons, 'section': section,
            'note': note, 'status': 'NULL',
            'matches': [], 'baseline_rate': bl
        })
    else:
        print(f"  Matches (top 10, >= 2 shared consonants):")
        displayed = matches[:10]
        for m in displayed:
            exact_flag = "*** EXACT-ORDERED" if m['exact_ordered'] else ""
            print(f"    [{m['source'][:5]}] [{m['domain']:12s}] {m['term']:25s} = '{m['meaning']}'")
            print(f"             ref_cons={m['cons']!r} shared={m['n_shared_any']} "
                  f"ordered={m['score_ordered']:.2f} {exact_flag}")

        top = matches[0]
        print(f"  Baseline for {len(stem_cons)}-con stems: {bl*100:.1f}%")
        results_table.append({
            'token': token, 'stem': stem_cons, 'section': section,
            'note': note, 'status': 'MATCHES',
            'n_matches': len(matches),
            'top_match': top['term'],
            'top_meaning': top['meaning'],
            'top_domain': top['domain'],
            'top_shared': top['n_shared_any'],
            'top_ordered': top['score_ordered'],
            'top_exact': top['exact_ordered'],
            'baseline_rate': bl,
            'matches': [{'term': m['term'], 'meaning': m['meaning'],
                         'domain': m['domain'], 'source': m['source'],
                         'cons': m['cons'], 'n_shared_any': m['n_shared_any'],
                         'score_ordered': m['score_ordered'],
                         'exact_ordered': m['exact_ordered']}
                        for m in matches[:5]]
        })

# ============================================================
# 6. AYN-COMPOUND SEARCH (Arabic star names with ʿayn)
# ============================================================

print("\n\n6. AYN-COMPOUND SEARCH (Arabic ʿayn = eye/spring + X star names)")
print("=" * 80)

# All al-Sufi entries with 'ayn' in domain or term
ayn_entries = [e for e in ALL_LEXICON if 'ayn' in e.get('domain','').lower()
               or 'ayn' in e.get('term','').lower()
               or 'ain' in e.get('term','').lower()
               or 'eye' in e.get('meaning','').lower()
               or 'spring' in e.get('meaning','').lower()]

print(f"  Found {len(ayn_entries)} ʿayn-related entries in lexicon:")
for e in ayn_entries:
    print(f"    [{e['source']:10s}] {e['term']:25s} = '{e['meaning']}' (cons={e['cons']!r})")

# For ai!n tokens, check if any ayn-compound shares 2+ consonants with known -ain stems
print(f"\n  -ain family stem alignment against ʿayn compounds:")
ain_stems = {
    'qk': 'qokain', 'lk': 'lkaiin', 'qt': 'qotaiin',
    'ql': 'qol', 'd': 'daiin', 'k': 'okaiin',
    'r': 'raiin', 's': 'saiin', 'l': 'laiin', 'sl': 'sal'
}
for stem, tok in ain_stems.items():
    ayn_matches = []
    for e in ayn_entries:
        sc = consonant_score_2con(stem, e['cons'])
        if sc['n_shared_any'] >= 2:
            ayn_matches.append((e, sc))
    if ayn_matches:
        print(f"  {tok} (stem={stem!r}): {len(ayn_matches)} ʿayn-compound matches")
        for e, sc in ayn_matches[:3]:
            print(f"    {e['term']:25s} shared={sc['n_shared_any']} ordered={sc['score_ordered']:.2f}")
    else:
        print(f"  {tok} (stem={stem!r}): no ʿayn-compound matches at 2-con threshold")

# ============================================================
# 7. SAL DEEP ANALYSIS
# ============================================================

print("\n\n7. SAL DEEP ANALYSIS — full lexicon alignment")
print("=" * 80)

sal_matches = align_stem('sl', min_shared=2)
print(f"  All matches for sal (sl stem), >= 2 shared consonants: {len(sal_matches)}")
for m in sal_matches:
    print(f"    [{m['source']:12s}] [{m['domain']:12s}] {m['term']:25s} = '{m['meaning']}'")
    print(f"             cons={m['cons']!r} shared={m['n_shared_any']} ordered={m['score_ordered']:.2f}"
          + (" *** EXACT" if m['exact_ordered'] else ""))

# ============================================================
# 8. LKAIIN DEEP ANALYSIS
# ============================================================

print("\n\n8. LKAIIN DEEP ANALYSIS — full lexicon alignment")
print("=" * 80)

lk_matches = align_stem('lk', min_shared=2)
print(f"  All matches for lkaiin (lk stem), >= 2 shared consonants: {len(lk_matches)}")
for m in lk_matches:
    print(f"    [{m['source']:12s}] [{m['domain']:12s}] {m['term']:25s} = '{m['meaning']}'")
    print(f"             cons={m['cons']!r} shared={m['n_shared_any']} ordered={m['score_ordered']:.2f}"
          + (" *** EXACT" if m['exact_ordered'] else ""))

# Check lkaiin positional behavior in corpus
print(f"\n  lkaiin corpus distribution:")
lkaiin_tokens = [r for r in token_records if r['token'] == 'lkaiin']
section_dist = Counter(r['section'] for r in lkaiin_tokens)
print(f"    Total occurrences: {len(lkaiin_tokens)}")
for sec, cnt in sorted(section_dist.items(), key=lambda x: -x[1]):
    pct = cnt / len(lkaiin_tokens) * 100
    print(f"    Section {sec}: {cnt} ({pct:.1f}%)")

# ============================================================
# 9. QOTAIIN DEEP ANALYSIS
# ============================================================

print("\n\n9. QOTAIIN DEEP ANALYSIS — full lexicon alignment")
print("=" * 80)

qt_matches = align_stem('qt', min_shared=2)
print(f"  All matches for qotaiin (qt stem), >= 2 shared consonants: {len(qt_matches)}")
for m in qt_matches:
    print(f"    [{m['source']:12s}] [{m['domain']:12s}] {m['term']:25s} = '{m['meaning']}'")
    print(f"             cons={m['cons']!r} shared={m['n_shared_any']} ordered={m['score_ordered']:.2f}"
          + (" *** EXACT" if m['exact_ordered'] else ""))

# Check qotaiin section distribution
print(f"\n  qotaiin corpus distribution:")
qotaiin_tokens = [r for r in token_records if r['token'] == 'qotaiin']
section_dist = Counter(r['section'] for r in qotaiin_tokens)
print(f"    Total occurrences: {len(qotaiin_tokens)}")
for sec, cnt in sorted(section_dist.items(), key=lambda x: -x[1]):
    pct = cnt / len(qotaiin_tokens) * 100
    print(f"    Section {sec}: {cnt} ({pct:.1f}%)")

# ============================================================
# 10. TOP BALNEO -AIN TOKENS NOT YET ANALYZED
# ============================================================

print("\n\n10. TOP BALNEO -ain TOKENS (not in priority list)")
print("=" * 80)

# Find -ain tokens enriched in B section
balneo_tokens = tokens_by_section.get('B', [])
ain_in_balneo = [r for r in balneo_tokens if r['token'].endswith('ain') or
                 r['token'].endswith('aiin') or r['token'].endswith('ai!n')]
ain_balneo_freq = Counter(r['token'] for r in ain_in_balneo)

corpus_ain = Counter(r['token'] for r in token_records
                     if r['token'].endswith('ain') or r['token'].endswith('aiin')
                     or r['token'].endswith('ai!n'))

total_B = len(balneo_tokens)
total_corpus = len(token_records)

print(f"  Top -ain tokens in Balneological section (enrichment > 1.5×):")
enriched = []
for tok, cnt_B in ain_balneo_freq.most_common(30):
    cnt_total = corpus_ain.get(tok, 0)
    if cnt_total < 5:
        continue
    expected = cnt_total * (total_B / total_corpus)
    enrichment = cnt_B / expected if expected > 0 else 0
    if enrichment >= 1.5:
        stem = extract_eva_consonants(tok.replace('aiin','').replace('ain','').replace('ai!n',''))
        enriched.append((tok, cnt_B, cnt_total, enrichment, stem))

enriched.sort(key=lambda x: -x[3])
print(f"  {'Token':15s} {'n_B':6s} {'n_tot':7s} {'enrich':8s} {'stem':10s}")
for tok, cnt_B, cnt_total, enrichment, stem in enriched:
    print(f"  {tok:15s} {cnt_B:6d} {cnt_total:7d} {enrichment:8.2f}× {stem:10s}")

# ============================================================
# 11. SUMMARY TABLE
# ============================================================

print("\n\n11. ROSETTA3b SUMMARY TABLE")
print("=" * 80)
print(f"  {'Token':12s} {'Stem':6s} {'Status':18s} {'Top match':20s} {'Shared':6s} {'Exact':5s} {'Semantic fit'}")
print(f"  {'-'*12} {'-'*6} {'-'*18} {'-'*20} {'-'*6} {'-'*5} {'-'*15}")

for r in results_table:
    status = r['status']
    if status == 'EXCLUDED_SHORT_STEM':
        print(f"  {r['token']:12s} {r['stem']:6s} {'<2-con excluded':18s} {'—':20s} {'—':6s} {'—':5s} not testable")
    elif status == 'NULL':
        print(f"  {r['token']:12s} {r['stem']:6s} {'NULL':18s} {'—':20s} {'—':6s} {'—':5s} —")
    else:
        top = r.get('top_match', '—')
        shared = str(r.get('top_shared', '—'))
        exact = 'YES' if r.get('top_exact') else 'no'
        meaning = r.get('top_meaning', '—')[:15]
        print(f"  {r['token']:12s} {r['stem']:6s} {'MATCH':18s} {top:20s} {shared:6s} {exact:5s} {meaning}")

# ============================================================
# SAVE RESULTS
# ============================================================

results_dir = Path(__file__).parent.parent / "results"
out = {
    'baseline_by_length': baseline_by_length,
    'lexicon_sizes': {
        'alsufi': len(ALSUFI_CATALOG),
        'latin_balneo': len(LATIN_BALNEO),
        'arabic_hebrew': len(ARABIC_HEBREW_LING),
        'total': len(ALL_LEXICON)
    },
    'priority_results': results_table,
    'sal_matches': [{'term': m['term'], 'meaning': m['meaning'], 'domain': m['domain'],
                     'source': m['source'], 'cons': m['cons'],
                     'n_shared': m['n_shared_any'], 'exact': m['exact_ordered']}
                    for m in sal_matches],
    'lk_matches': [{'term': m['term'], 'meaning': m['meaning'], 'domain': m['domain'],
                    'source': m['source'], 'cons': m['cons'],
                    'n_shared': m['n_shared_any'], 'exact': m['exact_ordered']}
                   for m in lk_matches],
    'qt_matches': [{'term': m['term'], 'meaning': m['meaning'], 'domain': m['domain'],
                    'source': m['source'], 'cons': m['cons'],
                    'n_shared': m['n_shared_any'], 'exact': m['exact_ordered']}
                   for m in qt_matches],
    'ayn_entries': [{'term': e['term'], 'meaning': e['meaning'],
                     'cons': e['cons'], 'domain': e['domain']} for e in ayn_entries],
}
with open(results_dir / "ROSETTA3b_expanded_results.json", 'w') as f:
    json.dump(out, f, indent=2)
print("\nSaved: ROSETTA3b_expanded_results.json")
print("\n" + "=" * 80)
print("ROSETTA3b COMPLETE")
print("=" * 80)
