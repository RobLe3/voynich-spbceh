"""
DECODE2 — Lead 2: Stars -ain tokens as Arabic constellation eye-names

Tests:
1. Full context listing of top -ain tokens in Stars section (what precedes them?)
2. Do the pre-ain stems cluster into a small vocabulary? (potential constellation labels)
3. Alignment of pre-ain stems against Arabic constellation name romanizations
4. Internal repetition: do specific [stem + ain] pairs repeat on the same folio?
5. Comparison: Stars -ain vs Balneological -ain token identity

Arabic star/constellation names (ʿayn = eye component):
  Taurus:  ʿAyn al-Thawr (w-r → or/ar?), ain + thawr (th+w+r)
  Leo:     ʿAyn al-Asad (asad → s+d)
  Scorpio: ʿAyn al-ʿAqrab (aqrab → k+r+b?)
  Orion:   ʿAyn al-Jawzāʾ (jawza → j+z+a?)
  Aries:   no standard 'eye of Aries'
  Gemini:  no standard 'eye of Gemini'

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
import re
from collections import Counter, defaultdict
from scipy.stats import chi2_contingency

df = pd.read_csv("D1_corpus/corpus_tokens.csv")
struct_df = pd.read_csv("P1_structural/p1_1_cluster_frequencies.csv")
STRUCT = set(struct_df['cluster'].tolist())

# ── Extract Stars section -ain content tokens ──────────────────────────────────
content = df[~df['token'].isin(STRUCT)].copy()
stars = content[content['section'] == 'S'].copy()

AIN_SUFFIXES = ['aiin', 'ai!n', 'ain']
def get_ain_stem(tok):
    for suf in AIN_SUFFIXES:
        if tok.endswith(suf) and len(tok) > len(suf):
            return tok[:-len(suf)], suf
    if tok in ('aiin', 'ai!n', 'ain'):
        return '', suf
    return None, None

stars['ain_stem'], stars['ain_suf'] = zip(*stars['token'].apply(get_ain_stem))
stars_ain = stars[stars['ain_stem'].notna()].copy()

print(f"Stars section -ain content tokens: {len(stars_ain):,} occurrences, "
      f"{stars_ain['token'].nunique()} types")

# ── 1. Top -ain tokens in Stars + frequency ────────────────────────────────────
print("\n" + "="*65)
print("1. TOP -ain TOKENS IN STARS SECTION")
print("="*65)
tok_freq = stars_ain['token'].value_counts()
print(f"\n{'Token':<15} {'n':>5}  {'Stem':<10} Folio range")
print("-"*55)
for tok, n in tok_freq.head(15).items():
    stem, suf = get_ain_stem(tok)
    folios = stars_ain[stars_ain['token']==tok]['folio_id'].unique()
    folio_range = f"{min(folios)}–{max(folios)}" if len(folios) > 0 else '?'
    print(f"  {tok:<13} {n:>5}  {stem:<10}  {folio_range}")

# ── 2. Build bigram context: what immediately precedes -ain tokens in Stars? ──
print("\n" + "="*65)
print("2. WHAT PRECEDES -ain TOKENS IN STARS SECTION?")
print("="*65)

df_sorted = df.sort_values(['folio_id','line_id','token_index'])
df_sorted['prev'] = df_sorted.groupby(['folio_id','line_id'])['token'].shift(1)
df_sorted['next'] = df_sorted.groupby(['folio_id','line_id'])['token'].shift(-1)

# For top 5 Stars -ain tokens
top_ain_toks = tok_freq.head(5).index.tolist()
for ain_tok in top_ain_toks:
    rows = df_sorted[(df_sorted['token'] == ain_tok) & (df_sorted['section'] == 'S')]
    prev_counts = rows['prev'].dropna().value_counts().head(8)
    next_counts = rows['next'].dropna().value_counts().head(5)
    print(f"\n  '{ain_tok}' (n={len(rows)} in Stars):")
    print(f"    Stems: {get_ain_stem(ain_tok)[0]}")
    print(f"    Preceding: " + ', '.join(f"{t}({n})" for t,n in prev_counts.items()))
    print(f"    Following: " + ', '.join(f"{t}({n})" for t,n in next_counts.items()))

# ── 3. Stem vocabulary in Stars -ain ──────────────────────────────────────────
print("\n" + "="*65)
print("3. PRE-AIN STEM VOCABULARY IN STARS SECTION")
print("="*65)

stem_freq = stars_ain['ain_stem'].value_counts()
print(f"\nUnique stems before -ain in Stars: {len(stem_freq)}")
print(f"\n{'Stem':<12} {'n':>5}  {'tokens'}")
print("-"*55)
for stem, n in stem_freq.head(20).items():
    toks = stars_ain[stars_ain['ain_stem']==stem]['token'].value_counts().index.tolist()[:4]
    print(f"  {stem:<10} {n:>5}  {toks}")

# ── 4. Alignment: stems vs Arabic constellation names ─────────────────────────
print("\n" + "="*65)
print("4. STEM ALIGNMENT AGAINST ARABIC CONSTELLATION NAMES")
print("="*65)

# Arabic constellation/star vocabulary (romanized consonant skeleton)
# Format: (romanized, meaning, EVA-candidate-stem, note)
ARABIC_CONSTELLATIONS = [
    ("thr",  "Taurus (Thawr = bull)",       "otar?/star?",  "th+w+r → EVA tr?"),
    ("srt",  "Scorpio (Aqrab = scorpion)",   "sar?/sor?",    "ʿ+q+r+b → weak"),
    ("asd",  "Leo (Asad = lion)",            "s?",           "a+s+d → sd?"),
    ("jwz",  "Orion (Jawzāʾ)",              "qot?",         "j+w+z → weak"),
    ("hrs",  "Aries (Hamal = ram)",          "r?/ar?",       "h+m+l → weak"),
    ("dzb",  "Gemini (Jawzāʾ al-Thānī)",    "???",          "no match"),
    ("qws",  "Sagittarius (Qaws = bow)",     "ok?",          "q+w+s → ok?"),
    ("jdy",  "Capricorn (Jady = kid)",       "qot?/ot?",     "j+d+y → dy suffix?"),
    ("wr",   "Aquarius (Dalu = bucket)",     "or/ar",        "d+l+w → weak"),
    ("ht",   "Pisces (Hut = fish)",          "ot?",          "h+w+t → ot?"),
    ("snbl", "Virgo (Sunbula = ear of corn)","s?",           "s+n+b+l"),
    ("mzn",  "Libra (Mizan = scales)",       "???",          "m+z+n"),
]

def lcs_score(s1, s2):
    m, n = len(s1), len(s2)
    if m == 0 or n == 0: return 0.0
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1,m+1):
        for j in range(1,n+1):
            if s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1]+1
            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n] / max(m,n)

# Remove vowels from EVA stems for consonant comparison
def consonants(s):
    return ''.join(c for c in s if c not in 'aeiou')

print(f"\nTop Stars -ain stems vs Arabic constellation names:")
print(f"\n{'Stem':<12} {'n':>5}  Best constellation match           score")
print("-"*70)
for stem, n in stem_freq.head(15).items():
    if not stem: continue
    c_stem = consonants(stem)
    if not c_stem: continue
    best = max(ARABIC_CONSTELLATIONS, key=lambda x: lcs_score(c_stem, x[0]))
    sc = lcs_score(c_stem, best[0])
    print(f"  {stem:<10} {n:>5}  {best[1]:<35} {sc:.2f}")

# ── 5. Known Arabic star "eye" names vs top tokens ────────────────────────────
print("\n" + "="*65)
print("5. DIRECT COMPARISON: ARABIC EYE-STARS vs TOP STARS -ain TOKENS")
print("="*65)

# Specific Arabic star names containing ʿayn ("eye"):
# Ain (α Tau, ε Tau) = just 'ʿayn', no prefix
# ʿAyn al-Thawr = eye of bull (Taurus) — the star Ain (ε Tauri)
# al-Dabarān = "the follower" (Aldebaran, α Tau) — not ʿayn
# Common pattern in Voynich Stars: a token + ain_suffix

print("""
Known Arabic star names with ʿayn (eye) component:
  ʿAyn al-Thawr    = "eye of Taurus" (ε Tau, the Ain star)
     → EVA prediction: [thawr-stem] + ain = [th+r-stem] + ain
     → Possible EVA: otar+ain? star+ain? tar+ain?
  ʿAyn al-Asad     = "eye of Leo" (various Leo stars)
     → EVA: [asad-stem] + ain = [s+d-stem] + ain
     → Possible EVA: s+ain = sain? → sai!n is elevated in B not S
  ʿAyn al-Jawzāʾ   = "eye of Orion" (stars near Orion's head)
     → EVA: [jawza-stem] + ain = j+z + ain = ???
  ʿAyn al-ʿAqrab   = "eye of Scorpio"
     → EVA: [aqrab-stem] + ain = q+r+b + ain → qotaiin? (q+t+aiin)

Most likely candidates:
  qotaiin (n=39, S=39 in Stars): qot = q+t, then aiin → ʿAyn al-Jawzāʾ (Orion)?
  otai!n (n=47, S=47): ot + ain → t-stem + eye → Orion/Taurus?
  raiin (n=41, S=41): r + ain → r-stem + eye → ???
  okai!n (n=63, S=63): ok + ain → ok-stem + eye → Qaws (Sagittarius: q+w+s)?
""")

# ── 6. Folio-level repetition: does [stem+ain] repeat within Stars folios? ────
print("="*65)
print("6. FOLIO-LEVEL REPETITION: ARE -ain PAIRS CONSISTENT PER FOLIO?")
print("="*65)

# For Stars section, group by folio and see which -ain tokens dominate each folio
stars_ain_folios = stars_ain.groupby(['folio_id','token']).size().reset_index(name='n')
stars_ain_folios = stars_ain_folios.sort_values(['folio_id','n'], ascending=[True,False])

folio_top_ain = {}
for folio, grp in stars_ain_folios.groupby('folio_id'):
    folio_top_ain[folio] = grp.head(3)[['token','n']].values.tolist()

print("\nTop -ain token per Stars folio:")
for folio, top in sorted(folio_top_ain.items()):
    top_str = ', '.join(f"{t}({n})" for t,n in top)
    print(f"  {folio:8s}: {top_str}")

# ── 7. Stars vs Balneological -ain token identity ─────────────────────────────
print("\n" + "="*65)
print("7. STARS vs BALNEOLOGICAL: SAME OR DIFFERENT -ain TOKEN TYPES?")
print("="*65)

balneal = content[content['section'] == 'B']
b_ain = balneal[balneal['token'].apply(lambda t: any(t.endswith(s) for s in AIN_SUFFIXES) or t in AIN_SUFFIXES)]
s_ain_types = set(stars_ain['token'].unique())
b_ain_types = set(b_ain['token'].unique())
shared = s_ain_types & b_ain_types
print(f"\n  Stars -ain types: {len(s_ain_types)}")
print(f"  Balneological -ain types: {len(b_ain_types)}")
print(f"  Shared -ain types: {len(shared)}")
print(f"  Jaccard similarity: {len(shared)/len(s_ain_types | b_ain_types):.3f}")
print(f"\n  Top shared types (n in S, n in B):")
shared_counts = []
for tok in shared:
    ns = (stars_ain['token'] == tok).sum()
    nb = (b_ain['token'] == tok).sum()
    shared_counts.append((tok, ns, nb))
shared_counts.sort(key=lambda x: -(x[1]+x[2]))
for tok, ns, nb in shared_counts[:10]:
    print(f"    {tok:<15} S={ns:3d}, B={nb:3d}")

print(f"\n  Stars-exclusive top -ain tokens:")
s_only = [(t, int((stars_ain['token']==t).sum())) for t in s_ain_types - b_ain_types]
s_only.sort(key=lambda x: -x[1])
for t, n in s_only[:10]:
    print(f"    {t:<15} n={n:3d} (Stars only)")

print(f"\n  Balneological-exclusive top -ain tokens:")
b_only = [(t, int((b_ain['token']==t).sum())) for t in b_ain_types - s_ain_types]
b_only.sort(key=lambda x: -x[1])
for t, n in b_only[:10]:
    print(f"    {t:<15} n={n:3d} (Balneological only)")

# Save
results = {
    'stars_ain_types': int(len(s_ain_types)),
    'stars_ain_occurrences': int(len(stars_ain)),
    'top_stars_ain_tokens': tok_freq.head(10).to_dict(),
    'stem_freq_top10': stem_freq.head(10).to_dict(),
    'shared_with_balneological': int(len(shared)),
    'jaccard_S_B': round(len(shared)/len(s_ain_types | b_ain_types), 3),
}
with open('DECODE2_stars_ain_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
print("\nSaved: DECODE2_stars_ain_results.json")
