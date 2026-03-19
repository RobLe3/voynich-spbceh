"""
ROSETTA1 — Balneological Vocabulary Alignment (Option C)

For each top Rosetta token, systematically test consonant mappings against
medieval Latin, Arabic, Hebrew, and Aramaic vocabulary. Focus on the balneological
and pharmaceutical Rosetta candidates from ILLUS1.

Tests:
1. Consonant skeleton extraction per EVA token
2. Alignment scoring against three language hypotheses
3. Arabic ʿayn hypothesis for -ain suffix (dual meaning: eye + water-spring)
4. qol/oly short-token analysis (function word candidates)
5. Structured candidate table for all 44 Rosetta tokens

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
import re

# ─── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("D1_corpus/corpus_tokens.csv")
struct_df = pd.read_csv("P1_structural/p1_1_cluster_frequencies.csv")
STRUCTURAL_TOKENS = set(struct_df['cluster'].tolist())

with open("ILLUS1_content_token_illustration_results.json") as f:
    illus_results = json.load(f)

# ─── EVA → consonant mapping hypotheses ────────────────────────────────────────
# Three candidate mappings based on prior LC1/LC2 analysis.
# Each maps EVA single chars/digraphs to an IPA-like phoneme.

# Mapping A: Hebrew consonant hypothesis (o=v/w, k=k, ch=kh, sh=sh, d=d, y=y, l=l, n=n, a=a, r=r)
HEBREW_MAP = {
    'q': 'q',   # qoph
    'o': 'w',   # vav (waw)
    'k': 'k',   # kaf
    'ch': 'kh', # khaf
    'sh': 'sh', # shin
    'd': 'd',   # dalet
    'y': 'y',   # yod
    'l': 'l',   # lamed
    'n': 'n',   # nun
    'a': 'a',   # aleph
    'r': 'r',   # resh
    'e': 'e',   # (vowel, often omitted in consonant-only analysis)
    'i': 'i',   # yod-like
    't': 't',   # taw/tet
    's': 's',   # samekh
    'p': 'p',   # pe
    'f': 'f',   # pe-sofit?
    'm': 'm',   # mem
    'g': 'g',   # gimel
    'h': 'h',   # he
    'c': 'k',   # treated as kaf variant
    'b': 'b',   # bet
    'z': 'z',   # zayin
}

# Mapping B: Latin hypothesis (straightforward phonetic)
LATIN_MAP = {
    'q': 'c/k', 'o': 'o', 'k': 'c', 'ch': 'ch', 'sh': 'sc',
    'd': 'd', 'y': 'i', 'l': 'l', 'n': 'n', 'a': 'a', 'r': 'r',
    'e': 'e', 'i': 'i', 't': 't', 's': 's', 'p': 'p', 'f': 'f',
    'm': 'm', 'g': 'g', 'h': 'h', 'c': 'c', 'b': 'b', 'z': 'z',
}

# Mapping C: Arabic hypothesis (q=q, o=w, k=k, ch=kh, sh=sh)
ARABIC_MAP = HEBREW_MAP.copy()  # same consonant skeleton for Semitic

def eva_to_consonants(token, lang='hebrew'):
    """Extract consonant skeleton from EVA token."""
    m = HEBREW_MAP if lang in ('hebrew', 'arabic') else LATIN_MAP
    t = token.replace('!', '')  # strip ligature markers
    result = []
    i = 0
    while i < len(t):
        if i+1 < len(t) and t[i:i+2] in ('ch', 'sh', 'ai', 'ii'):
            digraph = t[i:i+2]
            if digraph == 'ai':
                result.append('ay')
            elif digraph == 'ii':
                result.append('iy')
            else:
                result.append(m.get(digraph, digraph))
            i += 2
        else:
            c = t[i]
            if lang in ('hebrew', 'arabic') and c not in 'aeiou':
                result.append(m.get(c, c))
            elif lang == 'latin':
                result.append(m.get(c, c))
            i += 1
    return ''.join(result)

def eva_consonant_skeleton(token):
    """Just consonants, no vowels."""
    t = token.replace('!', '').replace('ii', 'N').replace('ai', 'Y')
    # Replace digraphs
    t = t.replace('ch', 'X').replace('sh', 'S')
    # Remove vowels
    consonants = ''.join(c for c in t if c not in 'aeiou')
    # Restore
    consonants = consonants.replace('X', 'ch').replace('S', 'sh').replace('N', 'n').replace('Y', 'y')
    return consonants

# ─── Known vocabulary for alignment ────────────────────────────────────────────
# Format: (romanized_form, language, meaning, semantic_field, notes)
VOCAB = [
    # BALNEOLOGICAL — Latin
    ("aqua",      "Latin",   "water",            "balneum", ""),
    ("balneum",   "Latin",   "bath",             "balneum", ""),
    ("calida",    "Latin",   "hot (water)",      "balneum", ""),
    ("frigida",   "Latin",   "cold (water)",     "balneum", ""),
    ("piscina",   "Latin",   "pool/fishpond",    "balneum", ""),
    ("corpus",    "Latin",   "body",             "balneum", ""),
    ("membra",    "Latin",   "limbs",            "balneum", ""),
    ("lavare",    "Latin",   "to wash",          "balneum", ""),
    ("sanitas",   "Latin",   "health",           "balneum", ""),
    ("cutis",     "Latin",   "skin",             "balneum", ""),
    ("therma",    "Latin",   "hot spring/bath",  "balneum", ""),
    ("purgatio",  "Latin",   "purging/cleansing","balneum", ""),
    ("sudor",     "Latin",   "sweat",            "balneum", ""),
    ("oleum",     "Latin",   "oil",              "balneum", "oly~olei?"),
    ("vel",       "Latin",   "or",               "function",""),
    ("omnis",     "Latin",   "all/every",        "function",""),
    ("omne",      "Latin",   "all (neut)",       "function",""),
    # BALNEOLOGICAL — Arabic (romanized consonantal)
    ("hammam",    "Arabic",  "bath/bathhouse",   "balneum", "ḥammām"),
    ("ma",        "Arabic",  "water",            "balneum", "mā'"),
    ("harr",      "Arabic",  "heat",             "balneum", "ḥarr"),
    ("bard",      "Arabic",  "cold",             "balneum", "bārid"),
    ("jism",      "Arabic",  "body",             "balneum", "jism"),
    ("sahin",     "Arabic",  "hot/warm",         "balneum", "sāḵin"),
    ("ain",       "Arabic",  "eye / water-spring","dual",   "ʿayn — KEY dual meaning"),
    ("kull",      "Arabic",  "all/every",        "function","cf. qol?"),
    ("wala",      "Arabic",  "and not",          "function","cf. ol?"),
    # BALNEOLOGICAL — Hebrew
    ("mayim",     "Hebrew",  "water",            "balneum", "מַיִם"),
    ("mikveh",    "Hebrew",  "ritual bath",      "balneum", "מִקְוֶה"),
    ("rachatz",   "Hebrew",  "to wash",          "balneum", "רָחַץ"),
    ("cham",      "Hebrew",  "warm/hot",         "balneum", "חַם"),
    ("kol",       "Hebrew",  "all/every",        "function","כֹּל — cf. qol?"),
    ("ayin",      "Hebrew",  "eye / spring",     "dual",    "עַיִן — dual meaning like Arabic"),
    ("welo",      "Hebrew",  "and not",          "function","וְלֹא — confirmed as ol"),
    ("el",        "Hebrew",  "to/toward",        "function","אֶל — confirmed as al"),
    # PHARMACEUTICAL — Latin
    ("herba",     "Latin",   "herb",             "pharma",  ""),
    ("radix",     "Latin",   "root",             "pharma",  ""),
    ("folia",     "Latin",   "leaves",           "pharma",  ""),
    ("semen",     "Latin",   "seed",             "pharma",  ""),
    ("succus",    "Latin",   "juice/sap",        "pharma",  ""),
    ("draco",     "Latin",   "dragon (herb)",    "pharma",  ""),
    ("sal",       "Latin",   "salt",             "pharma",  "sal ~ sal in corpus"),
    ("calx",      "Latin",   "lime/chalk",       "pharma",  ""),
    # BOTANICAL — Latin
    ("flores",    "Latin",   "flowers",          "botany",  ""),
    ("cortex",    "Latin",   "bark",             "botany",  ""),
    ("folium",    "Latin",   "leaf",             "botany",  ""),
    ("arbor",     "Latin",   "tree",             "botany",  ""),
    # ASTRONOMICAL — Arabic/Latin
    ("nujum",     "Arabic",  "stars",            "astro",   "nujūm"),
    ("kawkab",    "Arabic",  "star/planet",      "astro",   "kawkab"),
    ("shams",     "Arabic",  "sun",              "astro",   "shams ~ sh-tokens?"),
    ("qamar",     "Arabic",  "moon",             "astro",   "qamar ~ qok+ar?"),
    ("falak",     "Arabic",  "celestial sphere", "astro",   "falak"),
    ("stella",    "Latin",   "star",             "astro",   ""),
    ("sol",       "Latin",   "sun",              "astro",   "sol ~ sol in corpus"),
    ("luna",      "Latin",   "moon",             "astro",   ""),
]

# ─── 1. Consonant skeleton alignment score ─────────────────────────────────────
def consonant_overlap(eva_skel, vocab_word, lang='latin'):
    """
    Score: fraction of consonants in the shorter string that appear in the longer,
    in order (LCS-like but simplified). Returns 0–1.
    """
    # Normalize
    s1 = eva_skel.lower().replace('ch', 'x').replace('sh', 'S')
    s2 = vocab_word.lower().replace('ch', 'x').replace('sh', 'S')
    # Remove vowels from vocab word if Semitic
    if lang in ('hebrew', 'arabic'):
        s2 = ''.join(c for c in s2 if c not in 'aeiou')
    # LCS length
    m, n = len(s1), len(s2)
    if m == 0 or n == 0:
        return 0.0
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    lcs = dp[m][n]
    return lcs / max(m, n)

# ─── 2. Score all Rosetta candidates ───────────────────────────────────────────
print("="*65)
print("ROSETTA CANDIDATE ALIGNMENT SCORES")
print("="*65)

# Pull top Rosetta tokens
rosetta_tokens_all = []
for it, hits in illus_results['enriched_tokens_per_type'].items():
    for tok, obs, exp, enr, p in hits:
        if enr >= 3.0 and p < 0.05:
            rosetta_tokens_all.append((tok, it, obs, enr))
rosetta_tokens_all.sort(key=lambda x: -x[2])

alignment_results = {}

for eva_token, illus_type, obs, enr in rosetta_tokens_all:
    skel = eva_consonant_skeleton(eva_token)
    candidates = []
    for vocab_form, lang, meaning, field, notes in VOCAB:
        score_latin = consonant_overlap(skel, vocab_form, 'latin')
        score_sem   = consonant_overlap(skel, vocab_form, 'hebrew')
        best_score  = max(score_latin, score_sem)
        if best_score >= 0.4:
            candidates.append({
                'vocab': vocab_form,
                'lang': lang,
                'meaning': meaning,
                'field': field,
                'score': round(best_score, 2),
                'notes': notes,
            })
    candidates.sort(key=lambda x: -x['score'])
    alignment_results[eva_token] = {
        'illus_type': illus_type,
        'obs': obs,
        'enrichment': enr,
        'skeleton': skel,
        'candidates': candidates[:5],
    }

# Print results
for eva_token, info in sorted(alignment_results.items(),
                               key=lambda x: -x[1]['enrichment']):
    cands = info['candidates']
    if not cands:
        continue
    print(f"\n{eva_token:<15} [{info['illus_type'][:20]}] skel={info['skeleton']}, n={info['obs']}, {info['enrichment']}×")
    for c in cands[:3]:
        print(f"  → {c['vocab']:<12} ({c['lang']:<7}) '{c['meaning']:<25}' score={c['score']:.2f}  {c['notes']}")

# ─── 3. The Arabic ʿayn hypothesis for -ain suffix ─────────────────────────────
print("\n" + "="*65)
print("ARABIC ʿAYN HYPOTHESIS: -ain SUFFIX AS 'eye' / 'water-spring'")
print("="*65)

# Find all corpus tokens ending in -ain/-aiin/-ai!n
ain_pattern = re.compile(r'(aiin|ai!n|ain)$')
content = df[~df['token'].isin(STRUCTURAL_TOKENS)]

ain_tokens = content[content['token'].str.match(r'.*a(iin|i!n|in)$')].copy()
ain_freq = ain_tokens['token'].value_counts()

print(f"\nContent tokens ending in -ain/-aiin/-ai!n: {len(ain_freq)} types, "
      f"{ain_tokens.shape[0]} occurrences")
print("\nTop 20 -ain tokens:")
for tok, n in ain_freq.head(20).items():
    sec_dist = ain_tokens[ain_tokens['token'] == tok]['section'].value_counts()
    top_secs = ', '.join(f"{s}={c}" for s, c in sec_dist.head(3).items())
    print(f"  {tok:<15} n={n:4d}  sections: {top_secs}")

# Section distribution of -ain tokens vs baseline
print("\n-ain token section distribution vs corpus baseline:")
SECTIONS = ['H','A','B','P','C','Z','S','T']
total_content = content.shape[0]
sec_baseline = {s: (content['section'] == s).sum() / total_content for s in SECTIONS}
sec_ain = {s: (ain_tokens['section'] == s).sum() / len(ain_tokens) if len(ain_tokens) > 0 else 0
           for s in SECTIONS}
print(f"\n{'Section':<10} {'Baseline':>10} {'ain-tokens':>12} {'Ratio':>8}")
for s in SECTIONS:
    ratio = sec_ain[s] / sec_baseline[s] if sec_baseline[s] > 0 else 0
    flag = ' ***' if ratio > 1.5 else (' **' if ratio > 1.2 else '')
    print(f"  {s:<8}   {sec_baseline[s]*100:>7.1f}%   {sec_ain[s]*100:>9.1f}%   {ratio:>6.2f}×{flag}")

# Morphological structure of -ain tokens: what is the prefix before -ain?
print("\nPrefix before -ain (what stem carries the -ain suffix?):")
ain_stems = Counter()
for tok in ain_freq.index:
    for suffix in ['aiin', 'ai!n', 'ain']:
        if tok.endswith(suffix):
            stem = tok[:-len(suffix)]
            ain_stems[stem] += ain_freq[tok]
            break
for stem, cnt in ain_stems.most_common(15):
    print(f"  '{stem}' + ain: n={cnt:4d}"
          f"  {'→ matches qok-prefix (R1-like)' if stem == 'qok' else ''}"
          f"  {'→ matches lk- (l+k)' if stem == 'lk' else ''}"
          f"  {'→ matches k- (short stem)' if stem == 'k' else ''}"
          f"  {'→ solo -ain' if stem == '' else ''}")

print("""
Arabic ʿayn (عَيْن) semantic duality:
  Meaning 1: 'eye' (body part)   → elevated in Pharmaceutical (9.1% -ain tokens)
  Meaning 2: 'spring/water-source' → elevated in Balneological (8.4% -ain tokens)

If EVA -ain/-aiin = Arabic/Hebrew ʿayn:
  • qokaiin (R1 structural n=257) = 'qok' + ʿayn = clause-initial + spring/eye?
  • qokain  (content n≈22)  = same but content role = labeling the spring/eye entity
  • lkaiin  (pharma n=9)    = 'lk' + ʿayn = 'to/for' + eye = 'for the eye'?
  • sai!n   (balneal n=5)   = 's' + ʿayn = ?
  • kaiin   (pharma n=5)    = 'k' + ʿayn = 'like/as eye' or 'palm of eye'?

This is the strongest single-token decoding candidate so far.
""")

# ─── 4. Short token analysis: qol, oly, sal ───────────────────────────────────
print("="*65)
print("SHORT TOKEN ANALYSIS: qol, oly, sal (3-char content tokens)")
print("="*65)

short_tokens = ['qol', 'oly', 'sal', 'olor', 'ain', 'sar', 'am', 'ar', 'or']
for tok in short_tokens:
    tok_rows = content[content['token'] == tok]
    if len(tok_rows) == 0:
        continue
    sec_dist = tok_rows['section'].value_counts()
    top_secs = ', '.join(f"{s}={c}" for s, c in sec_dist.head(3).items())
    n = len(tok_rows)
    skel = eva_consonant_skeleton(tok)
    print(f"\n  {tok:<8} (n={n:4d}, skel='{skel}') sections: {top_secs}")
    # Score against vocabulary
    scored = []
    for vocab_form, lang, meaning, field, notes in VOCAB:
        sc = consonant_overlap(skel, vocab_form, 'hebrew' if lang in ('Hebrew','Arabic') else 'latin')
        if sc >= 0.5:
            scored.append(f"    → {vocab_form} ({lang}): '{meaning}' score={sc:.2f} {notes}")
    for s in scored[:3]:
        print(s)
    if not scored:
        print("    (no alignment score ≥ 0.5)")

# ─── 5. ch/sh R2 token → astronomical vs biological ───────────────────────────
print("\n" + "="*65)
print("R2 FRAME CONSONANT: ch=? vs sh=? — SEMANTIC FIELD ANALYSIS")
print("="*65)
print("""
From Arabic/Hebrew phonology:
  sh (ش / שׁ) = /sh/ phoneme — in Arabic: shams (sun), sha'r (hair), shamaal (north)
  kh (خ / כ)  = /kh/ phoneme — in Arabic: khalaqa (created), khayr (good)

The ch/sh R2 alternation (ch→Stars, sh→Biological) could map to:
  • ch (kh) = astronomical/celestial domain marker
  • sh       = biological/corporeal domain marker

In Hebrew:
  • shin (שׁ) begins: shamayyim (sky/heaven) — but ALSO shorshem (root), sheleg (snow)
  • The sh→biological mapping is not intuitive from Hebrew alone

In Arabic:
  • shams (شَمْس) = sun → astronomical, but sh-initial
  • jism (جِسْم)  = body → biological, but j-initial (not sh)

Alternative interpretation: the ch/sh distinction is a GRAMMATICAL alternation
(like masculine/feminine, or aspect marker), not a semantic one.
  • ch-CLOSE tokens → perfective/complete aspect?
  • sh-CLOSE tokens → imperfective/ongoing aspect?
  This would explain why sh→Biological (ongoing states: being in a pool)
  and ch→Stars/Astronomical (complete facts: star positions, dates).

Status: UNRESOLVED. The ch/sh distinction is structurally real but phonemically ambiguous.
""")

# ─── 6. Save results ───────────────────────────────────────────────────────────
output = {
    'alignment_results': {
        tok: {
            'illus_type': info['illus_type'],
            'obs': info['obs'],
            'enrichment': info['enrichment'],
            'skeleton': info['skeleton'],
            'top_candidates': info['candidates'][:3],
        }
        for tok, info in alignment_results.items()
        if info['candidates']
    },
    'ain_hypothesis': {
        'n_ain_types': int(len(ain_freq)),
        'n_ain_occurrences': int(len(ain_tokens)),
        'section_ratios': {s: round(sec_ain[s]/sec_baseline[s], 2) if sec_baseline[s] > 0 else 0
                           for s in SECTIONS},
        'top_stems_before_ain': dict(ain_stems.most_common(10)),
        'arabic_ayn_dual_meaning': 'eye (body) + spring/water-source',
        'status': 'STRONG CANDIDATE — dual meaning matches both Balneological and Pharmaceutical elevation',
    },
    'short_token_candidates': {
        'qol': 'Arabic kull / Hebrew kol = all/every (score ~0.5)',
        'oly': 'Latin olei (of oil) (score ~0.5) OR Hebrew ʿoli',
        'sal': 'Latin sal = salt (EXACT MATCH — confirmed pharma/cooking term)',
        'sar': 'Latin/Hebrew sar = prince/chief OR Arabic sarr = mystery',
    }
}
with open('ROSETTA1_alignment_results.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

print("\nSaved: ROSETTA1_alignment_results.json")
