"""
PILOT2 — Stars -ain Folio-Anchor Alignment Test
Phase 2 Step 5

For each Stars/Recipes folio:
- Extract dominant -ain token (threshold ≥ 5 occurrences)
- Record stems, token types, frequencies
- Cross-reference with known illustration subjects from voynich.nu catalogue
  (Zodiac months + Star/Astronomical figures from f103r–f116v range)
- Score: exact match / partial root match / no match

Known Stars section folio subjects (from Zandbergen catalogue + D'Imperio):
f103r–f103v: Aries (Ram)
f104r–f104v: Taurus (Bull)
f105r–f105v: Gemini (Twins)
f106r–f106v: Cancer (Crab)
f107r–f107v: Leo (Lion)
f108r–f108v: Virgo (Maiden)
f109r–f109v: Libra (Scales)
f110r–f110v: Scorpio (Scorpion)
f111r: Sagittarius (Archer)
f111v: (astronomical / star catalog)
f112r: Capricorn (Goat)
f112v: Aquarius (Water-bearer)
f113r: Pisces (Fish)
f113v: Aries (second occurrence / alternate)
f114r: star charts
f114v: star charts
f115r: star charts
f115v: star charts / text-heavy
f116r: star charts / text-heavy
f116v: recipes (text)

Arabic constellation/zodiac consonant skeletons for LCS matching:
Aries (Hamal/Kawaakib): hml / kwkb
Taurus (Thawr/Thurayya): twr / try
Gemini (Jawzaa): jwz
Cancer (Saratan): srt
Leo (Asad): asd
Virgo (Sunbula): snbl
Libra (Mizan): mzn
Scorpio (Aqrab): qrb
Sagittarius (Qaws): qws
Capricorn (Jady): jdy
Aquarius (Dalw): dlw
Pisces (Hut): ht

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict

df = pd.read_csv("D1_corpus/corpus_tokens.csv")
struct_df = pd.read_csv("P1_structural/p1_1_cluster_frequencies.csv")
STRUCT = set(struct_df['cluster'].tolist())

content = df[~df['token'].isin(STRUCT)].copy()
stars = content[content['section'] == 'S'].copy()

AIN_SUFFIXES = ['aiin', 'ai!n', 'ain']

def get_ain_stem(tok):
    for suf in sorted(AIN_SUFFIXES, key=len, reverse=True):
        if tok.endswith(suf) and len(tok) > len(suf):
            return tok[:-len(suf)], suf
    if tok in AIN_SUFFIXES:
        return '', tok
    return None, None

stars['ain_stem'], stars['ain_suf'] = zip(*stars['token'].apply(get_ain_stem))
stars_ain = stars[stars['ain_stem'].notna()].copy()

# Known folio subjects
FOLIO_SUBJECTS = {
    'f103r': ('Aries', 'Ram', 'hml'),
    'f103v': ('Aries', 'Ram', 'hml'),
    'f104r': ('Taurus', 'Bull', 'twr'),
    'f104v': ('Taurus', 'Bull', 'twr'),
    'f105r': ('Gemini', 'Twins', 'jwz'),
    'f105v': ('Gemini', 'Twins', 'jwz'),
    'f106r': ('Cancer', 'Crab', 'srt'),
    'f106v': ('Cancer', 'Crab', 'srt'),
    'f107r': ('Leo', 'Lion', 'asd'),
    'f107v': ('Leo', 'Lion', 'asd'),
    'f108r': ('Virgo', 'Maiden', 'snbl'),
    'f108v': ('Virgo', 'Maiden', 'snbl'),
    'f109r': ('Libra', 'Scales', 'mzn'),
    'f109v': ('Libra', 'Scales', 'mzn'),
    'f110r': ('Scorpio', 'Scorpion', 'qrb'),
    'f110v': ('Scorpio', 'Scorpion', 'qrb'),
    'f111r': ('Sagittarius', 'Archer', 'qws'),
    'f111v': ('Star catalog', 'Stars', None),
    'f112r': ('Capricorn', 'Goat', 'jdy'),
    'f112v': ('Aquarius', 'Water-bearer', 'dlw'),
    'f113r': ('Pisces', 'Fish', 'ht'),
    'f113v': ('Aries-alt', 'Ram', 'hml'),
    'f114r': ('Star charts', 'Stars', None),
    'f114v': ('Star charts', 'Stars', None),
    'f115r': ('Star charts', 'Stars', None),
    'f115v': ('Star charts', 'Stars', None),
    'f116r': ('Star charts / text', 'Stars', None),
    'f116v': ('Recipes', 'Text', None),
}

def lcs_length(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1,m+1):
        for j in range(1,n+1):
            if s1[i-1]==s2[j-1]: dp[i][j]=dp[i-1][j-1]+1
            else: dp[i][j]=max(dp[i-1][j],dp[i][j-1])
    return dp[m][n]

def consonants(s):
    return ''.join(c for c in s.lower() if c not in 'aeiouAEIOU!-')

print("="*70)
print("PILOT2: Stars -ain Folio-Anchor Alignment Test")
print("="*70)

print(f"\nTotal Stars -ain occurrences: {len(stars_ain)}")
print(f"Total Stars -ain types: {stars_ain['token'].nunique()}")

print("\n" + "="*70)
print("FOLIO-BY-FOLIO DOMINANT -ain TOKEN vs ILLUSTRATION SUBJECT")
print("="*70)

results = []
stars_ain_folios = stars_ain.groupby(['folio_id','token']).size().reset_index(name='n')

print(f"\n{'Folio':<8} {'Subject':<20} {'Dominant -ain':<15} {'n':>4}  {'Stem cons':<10} {'Align score':>12}")
print("-"*80)

for folio in sorted(stars_ain['folio_id'].unique()):
    folio_data = stars_ain_folios[stars_ain_folios['folio_id']==folio].sort_values('n',ascending=False)
    if len(folio_data) == 0:
        continue
    top_tok = folio_data.iloc[0]['token']
    top_n = folio_data.iloc[0]['n']

    if top_n < 3:  # skip folios with no dominant token
        continue

    stem, suf = get_ain_stem(top_tok)
    stem_cons = consonants(stem) if stem else ''

    subject_info = FOLIO_SUBJECTS.get(folio, ('Unknown', 'Unknown', None))
    subject_name, subject_common, subject_arabic_cons = subject_info

    # Alignment score
    if subject_arabic_cons and stem_cons:
        lcs = lcs_length(stem_cons, subject_arabic_cons)
        score = lcs / max(len(stem_cons), len(subject_arabic_cons), 1)
        score_str = f"{score:.2f}"
    else:
        score = None
        score_str = "N/A (star chart)"

    results.append({
        'folio': folio,
        'subject': subject_name,
        'dominant_ain': top_tok,
        'n': top_n,
        'stem': stem,
        'stem_cons': stem_cons,
        'subject_arabic': subject_arabic_cons,
        'align_score': score,
        'top3': folio_data.head(3)[['token','n']].values.tolist(),
    })
    print(f"  {folio:<8} {subject_name:<20} {top_tok:<15} {top_n:>4}  {stem_cons:<10} {score_str:>12}")

# Summary statistics
print("\n" + "="*70)
print("ALIGNMENT SCORE SUMMARY")
print("="*70)

zodiac_results = [r for r in results if r['align_score'] is not None]
if zodiac_results:
    scores = [r['align_score'] for r in zodiac_results]
    print(f"\nFolios with known zodiac subject: {len(zodiac_results)}")
    print(f"Mean alignment score: {np.mean(scores):.3f}")
    print(f"Max alignment score: {np.max(scores):.3f}")
    print(f"Scores ≥ 0.50: {sum(s>=0.50 for s in scores)}")
    print(f"Scores ≥ 0.33: {sum(s>=0.33 for s in scores)}")

    print(f"\nBest alignments:")
    for r in sorted(zodiac_results, key=lambda x: -x['align_score'])[:5]:
        print(f"  {r['folio']}: {r['dominant_ain']} → {r['subject']} "
              f"[stem: {r['stem_cons']} vs Arabic: {r['subject_arabic']}] score={r['align_score']:.2f}")

print("\n" + "="*70)
print("FOLIO-ANCHOR CONSISTENCY TEST")
print("="*70)
print("\nDoes the dominant -ain token CHANGE between folios with different subjects?")
print("(Key prediction of entity-labeling hypothesis)")

folio_to_dominant = {r['folio']: r['dominant_ain'] for r in results}
subject_to_folios = defaultdict(list)
for r in results:
    subject_to_folios[r['subject']].append(r['folio'])

# Check: same subject → same dominant token?
consistency_hits = 0
consistency_total = 0
for subject, folios in subject_to_folios.items():
    if len(folios) > 1:
        dominants = [folio_to_dominant[f] for f in folios if f in folio_to_dominant]
        if len(dominants) > 1:
            all_same = len(set(dominants)) == 1
            consistency_total += 1
            if all_same:
                consistency_hits += 1
            print(f"  {subject}: folios {folios} → tokens {dominants} → {'CONSISTENT ✓' if all_same else 'VARIES ✗'}")

if consistency_total > 0:
    print(f"\n  Same-subject consistency: {consistency_hits}/{consistency_total} = {consistency_hits/consistency_total*100:.0f}%")

# Save
with open('PILOT2_stars_ain_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
print("\nSaved: PILOT2_stars_ain_results.json")
