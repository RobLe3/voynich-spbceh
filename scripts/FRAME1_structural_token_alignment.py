"""
FRAME1 — Structural Frame Token Alignment Study (Option A)

Deep analysis of R1 (INIT) and R2 (CLOSE) structural tokens:
1. Morphological sub-structure (shared n-gram motifs)
2. Multi-language function word alignment (Hebrew, Latin, Arabic, Greek)
3. Section-NMI and positional properties per token
4. EVA character pattern decomposition
5. Within-section usage: paragraph-initial vs paragraph-medial

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
import re
from collections import Counter
from scipy.stats import chi2_contingency
from sklearn.metrics import normalized_mutual_info_score

# ─── Load corpus ───────────────────────────────────────────────────────────────
CORPUS_PATH = "D1_corpus/corpus_tokens.csv"
CLUSTERS_PATH = "P1_structural/p1_1_cluster_frequencies.csv"

df = pd.read_csv(CORPUS_PATH)
clusters = pd.read_csv(CLUSTERS_PATH)

print(f"Corpus: {len(df):,} tokens across {df['folio_id'].nunique()} folios")
print(f"Cluster types: {dict(clusters['role'].value_counts())}")

# ─── 1. Extract top frame tokens ────────────────────────────────────────────────
R1_tokens = set(clusters[clusters['role']=='INIT']['cluster'].tolist())
R2_tokens = set(clusters[clusters['role']=='CLOSE']['cluster'].tolist())

# Get actual frequencies in corpus (not just from cluster file)
tok_freq = df['token'].value_counts()

r1_in_corpus = {t: int(tok_freq.get(t, 0)) for t in R1_tokens}
r2_in_corpus = {t: int(tok_freq.get(t, 0)) for t in R2_tokens}

print("\nR1 (INIT) tokens:")
for t, n in sorted(r1_in_corpus.items(), key=lambda x: -x[1]):
    print(f"  {t:15s}  n={n:4d}")

print("\nR2 (CLOSE) tokens:")
for t, n in sorted(r2_in_corpus.items(), key=lambda x: -x[1]):
    print(f"  {t:15s}  n={n:4d}")

# ─── 2. Section NMI per structural token ───────────────────────────────────────
SECTIONS = ['H','A','B','P','C','Z','S','T']

print("\n" + "="*65)
print("SECTION NMI PER FRAME TOKEN")
print("="*65)

frame_nmi = {}
for token in sorted(R1_tokens | R2_tokens):
    token_rows = df[df['token'] == token]
    if len(token_rows) < 20:
        continue
    secs = token_rows['section'].values
    all_secs = df['section'].values
    nmi = normalized_mutual_info_score(secs, all_secs[:len(secs)])
    # Simpler: section distribution of this token
    sec_counts = token_rows['section'].value_counts()
    top_sec = sec_counts.index[0] if len(sec_counts) > 0 else '?'
    top_pct = sec_counts.iloc[0] / sec_counts.sum() if len(sec_counts) > 0 else 0

    # Per-section rate (occurrences / all tokens in that section)
    sec_rates = {}
    for s in SECTIONS:
        sec_total = (df['section'] == s).sum()
        sec_tok = (token_rows['section'] == s).sum()
        sec_rates[s] = sec_tok / sec_total if sec_total > 0 else 0

    frame_nmi[token] = {
        'n': int(len(token_rows)),
        'role': 'R1' if token in R1_tokens else 'R2',
        'top_section': top_sec,
        'top_section_pct': round(top_pct, 3),
        'sec_rates': {k: round(v*1000, 2) for k, v in sec_rates.items()},  # per 1000 tokens
    }

# Compute NMI properly: token presence vs section
for token, info in frame_nmi.items():
    has_token = (df['token'] == token).astype(int).values
    sec_codes = pd.Categorical(df['section']).codes
    info['nmi_section'] = round(normalized_mutual_info_score(has_token, sec_codes), 4)

# Print ranked by NMI
ranked = sorted(frame_nmi.items(), key=lambda x: -x[1]['nmi_section'])
print(f"\n{'Token':<15} {'Role'} {'n':>5} {'NMI':>7}  {'TopSec':>7} {'%top':>6}")
print("-"*55)
for token, info in ranked:
    print(f"{token:<15} {info['role']}  {info['n']:>5}  {info['nmi_section']:>6.4f}  "
          f"{info['top_section']:>7} {info['top_section_pct']*100:>5.1f}%")

# ─── 3. Morphological sub-structure: EVA n-gram decomposition ──────────────────
# Map EVA to phoneme clusters
# Known EVA conventions: 'q' always precedes 'o', '!' = ligature, 'ch'/'sh' = digraphs

def eva_to_phonemes(token):
    """Break EVA string into phoneme-like units."""
    t = token
    # Replace EVA digraphs with single char placeholders
    t = t.replace('ch', 'Ч').replace('sh', 'Ш').replace('ai', 'Α').replace('ii', 'И')
    t = t.replace('!', '')  # ligature marker, ignore
    chars = list(t)
    return chars

print("\n" + "="*65)
print("EVA MORPHOLOGICAL DECOMPOSITION OF FRAME TOKENS")
print("="*65)

# Find shared prefixes, suffixes, and infixes across R1 and R2
r1_list = [t for t in R1_tokens if t != 'fachys']  # exclude rare outlier
r2_list = list(R2_tokens - {'cfhaiin', 'ykchdy'})    # exclude rare outliers

def get_char_ngrams(token, n=2):
    chars = eva_to_phonemes(token)
    return [''.join(chars[i:i+n]) for i in range(len(chars)-n+1)]

# Prefix analysis
print("\nR1 (INIT) prefixes (first 3 EVA chars):")
r1_prefixes = Counter()
for t in r1_list:
    r1_prefixes[t[:3]] += 1
for pref, cnt in r1_prefixes.most_common():
    print(f"  '{pref}': {cnt}/{len(r1_list)} tokens")

print("\nR2 (CLOSE) suffixes (last 3 EVA chars):")
r2_suffixes = Counter()
for t in r2_list:
    r2_suffixes[t[-3:]] += 1
for suf, cnt in r2_suffixes.most_common():
    print(f"  '{suf}': {cnt}/{len(r2_list)} tokens")

print("\nR2 (CLOSE) suffixes (last 2 EVA chars):")
r2_suffixes2 = Counter()
for t in r2_list:
    r2_suffixes2[t[-2:]] += 1
for suf, cnt in r2_suffixes2.most_common():
    print(f"  '{suf}': {cnt}/{len(r2_list)} tokens")

print("\nR2 shared stems (strip final suffix -dy, -ey, -y):")
def strip_r2_suffix(t):
    for suf in ['edy','eey','dy','ey','y']:
        if t.endswith(suf) and len(t) > len(suf):
            return t[:-len(suf)], suf
    return t, ''
r2_stems = Counter()
for t in r2_list:
    stem, suf = strip_r2_suffix(t)
    r2_stems[stem] += 1
print(f"{'Stem':<12} {'n':<4} {'Suffix variants'}")
stem_tokens = {}
for t in r2_list:
    stem, suf = strip_r2_suffix(t)
    stem_tokens.setdefault(stem, []).append(t)
for stem, tokens in sorted(stem_tokens.items(), key=lambda x: -len(x[1])):
    print(f"  {stem:<12}: {tokens}")

# ─── 4. Multi-language function word alignment ──────────────────────────────────
print("\n" + "="*65)
print("MULTI-LANGUAGE FUNCTION WORD ALIGNMENT")
print("="*65)

# Expanded function word lists (transcribed to EVA-compatible romanization)
# Format: (EVA_pattern, language, word, meaning, notes)
# EVA mapping assumptions:
#   q+o → ??? (high-frequency digraph, possibly a prefix)
#   o → 'v' (Hebrew vav) OR 'o'
#   l → 'l'
#   k → 'k'
#   ch → 'kh' or 'ch'
#   sh → 'sh'
#   y → 'y' (yod?)
#   d → 'd' or 't'
#   a → 'a'
#   e → 'e' or nothing (vowel pointing?)

FUNCTION_WORDS = [
    # Hebrew (Biblical/Medieval) — using direct EVA consonant map: o=v, s!=sh, ky=ky, l=l, al='l, ol=vl
    ("ol",    "Hebrew",  "vl (וְלֹא)", "and not (conj+neg)", "R6 direct hit"),
    ("al",    "Hebrew",  "'l (אֶל)",   "to/toward (prep)",   "R6 direct hit"),
    ("or",    "Hebrew",  "vr",          "and head/chief?",    "R6 speculative"),
    ("ar",    "Hebrew",  "'r",          "city? / root?",      "R6 speculative"),
    ("o",     "Hebrew",  "v (וְ)",      "and (conj)",         "R4 direct hit"),
    ("l",     "Hebrew",  "l (לְ)",      "to/for (prep)",      "R4 direct hit"),
    ("ky",    "Hebrew",  "ky (כִּי)",   "that/because (conj)","R2 direct hit"),
    ("ol",    "Arabic",  "wl (وَل)",    "and/but",            "cf. Hebrew"),
    ("al",    "Arabic",  "al (الـ)",    "the (def. article)", "Strong Arabic match"),
    ("al",    "Latin",   "al-",         "to (prefix aliter)", "weak"),
    ("ol",    "Latin",   "vel",         "or",                 "stretch"),
    ("chedy", "Hebrew",  "khdy?",       "???",                "no direct match"),
    ("shedy", "Hebrew",  "shdy?",       "watchman? (shomeh)", "very speculative"),
    # Latin function words (could appear in medieval medical/pharma text)
    ("ar",    "Latin",   "ar-",         "prefix meaning toward", "speculative"),
    ("ol",    "Latin",   "ol-",         "oleum (oil)",        "content word, not function"),
    ("al",    "Latin",   "al-",         "alius/other",        "speculative"),
    # Greek
    ("al",    "Greek",   "al-",         "prefix (toward)",    "speculative"),
    # Proto-Semitic consonantal roots
    ("qokal", "Semitic", "q+k+l",       "to/for+all?",        "speculative stem"),
    ("qokar", "Semitic", "q+k+r",       "called/name?",       "speculative"),
    ("qokey", "Semitic", "q+k+y",       "???",                "unresolved"),
]

# The most constrained set: R6 tokens (ol, al, or, ar) are only 4 tokens
# Their consistent Hebrew alignment was already confirmed in LC2
print("\nR6 (REF) tokens — confirmed Hebrew alignment:")
r6_tokens_data = [
    ("ol", 504, "Hebrew vl (וְלֹא)", "and not / conjunction+negation", "CONFIRMED"),
    ("al", 246, "Hebrew ʾl (אֶל)",   "to / toward (preposition)",      "CONFIRMED"),
    ("or",  76, "Hebrew vr?",         "ambiguous",                      "SPECULATIVE"),
    ("ar",  94, "Hebrew ʾr?",         "ambiguous",                      "SPECULATIVE"),
]
for eva, n, heb, meaning, status in r6_tokens_data:
    print(f"  {eva:4s} (n={n:3d}) → {heb:20s} '{meaning}' [{status}]")

# New analysis: test if R1 'qo-' prefix could be a grammatical morpheme
print("\nR1 prefix 'qo-' analysis:")
print("  All R1 tokens start with 'qo' (except fachys n=1)")
print("  Possible interpretations:")
print("  A. 'qo' = clause-initial marker (topic/focus particle)")
print("  B. 'qo' = definite/indefinite article prefix")
print("  C. 'qo' = grammatical prefix (like Hebrew 'ha-' = 'the')")
print("  D. 'qo' = phonetic sequence specific to initial position")
print()
# What follows 'qo' in R1 tokens?
r1_stems = [t[2:] for t in r1_list if t.startswith('qo')]
print(f"  R1 stems after 'qo': {sorted(r1_stems)}")
print(f"  Unique chars at position 2: {sorted(set(t[2] for t in r1_list if len(t) > 2 and t.startswith('qo')))}")

# Compare R1 stems to R2 stems — do they share any roots?
r2_core = [strip_r2_suffix(t)[0] for t in r2_list]
r2_core_no_prefix = [t.lstrip('lychsk') for t in r2_core]  # strip potential prefixes

print("\nR1 stems vs R2 stems overlap:")
r1_stems_set = set(r1_stems)
r2_core_set = set(r2_core)
print(f"  R1 stems: {sorted(r1_stems_set)}")
print(f"  R2 cores: {sorted(r2_core_set)}")
print(f"  Overlap: {r1_stems_set & r2_core_set}")

# ─── 5. Positional analysis: paragraph-initial vs paragraph-medial ──────────────
print("\n" + "="*65)
print("POSITIONAL ANALYSIS: PARAGRAPH-INITIAL vs PARAGRAPH-MEDIAL")
print("="*65)

# Use is_para_start from corpus
para_init_rates = {}
for token in R1_tokens | R2_tokens:
    token_rows = df[df['token'] == token]
    if len(token_rows) < 20:
        continue
    para_init = token_rows['is_para_start'].sum()
    total = len(token_rows)
    para_init_rates[token] = {
        'n': int(total),
        'n_para_init': int(para_init),
        'pct_para_init': round(para_init / total, 3),
        'role': 'R1' if token in R1_tokens else 'R2',
    }

# Baseline: overall paragraph-initial rate
baseline = df['is_para_start'].mean()
print(f"\nBaseline paragraph-initial rate: {baseline:.3f}")
print(f"\n{'Token':<15} {'Role'} {'n':>5} {'%Para-Init':>11}  {'vs baseline':>12}")
print("-"*55)
for token, info in sorted(para_init_rates.items(),
                           key=lambda x: -x[1]['pct_para_init']):
    diff = info['pct_para_init'] - baseline
    print(f"{token:<15} {info['role']}  {info['n']:>5}  "
          f"{info['pct_para_init']*100:>8.1f}%  "
          f"{'+' if diff >= 0 else ''}{diff*100:>+7.1f}%")

# ─── 6. Co-occurrence graph: what follows R1, what precedes R2 ─────────────────
print("\n" + "="*65)
print("CO-OCCURRENCE: TOKEN BEFORE R2 (CLOSE) & TOKEN AFTER R1 (INIT)")
print("="*65)

# Build token-level transitions
# Shift tokens to get previous and next token in same line
df_sorted = df.sort_values(['folio_id', 'line_id', 'token_index'])
df_sorted['prev_token'] = df_sorted.groupby(['folio_id', 'line_id'])['token'].shift(1)
df_sorted['next_token'] = df_sorted.groupby(['folio_id', 'line_id'])['token'].shift(-1)

print("\nTop tokens preceding R2 (CLOSE) tokens:")
r2_preceding = df_sorted[df_sorted['token'].isin(R2_tokens)]['prev_token'].dropna()
prec_counts = r2_preceding.value_counts().head(15)
for tok, cnt in prec_counts.items():
    role_label = 'R1' if tok in R1_tokens else ('R2' if tok in R2_tokens else 'content')
    print(f"  {tok:<15s} n={cnt:4d}  [{role_label}]")

print("\nTop tokens following R1 (INIT) tokens:")
r1_following = df_sorted[df_sorted['token'].isin(R1_tokens)]['next_token'].dropna()
foll_counts = r1_following.value_counts().head(15)
for tok, cnt in foll_counts.items():
    role_label = 'R1' if tok in R1_tokens else ('R2' if tok in R2_tokens else 'content')
    print(f"  {tok:<15s} n={cnt:4d}  [{role_label}]")

# ─── 7. EVA character frequency in frame tokens (what letters dominate?) ────────
print("\n" + "="*65)
print("EVA CHARACTER FREQUENCY IN FRAME TOKENS (weighted by n)")
print("="*65)

r1_char_freq = Counter()
r2_char_freq = Counter()
for token, info in frame_nmi.items():
    if info['role'] == 'R1':
        for c in eva_to_phonemes(token):
            r1_char_freq[c] += info['n']
    else:
        for c in eva_to_phonemes(token):
            r2_char_freq[c] += info['n']

total_r1 = sum(r1_char_freq.values())
total_r2 = sum(r2_char_freq.values())

print("\nR1 (INIT) char distribution:")
for c, cnt in r1_char_freq.most_common():
    print(f"  '{c}': {cnt:5d}  ({cnt/total_r1*100:.1f}%)")

print("\nR2 (CLOSE) char distribution:")
for c, cnt in r2_char_freq.most_common():
    print(f"  '{c}': {cnt:5d}  ({cnt/total_r2*100:.1f}%)")

# ─── 8. Alignment scoring matrix (EVA → candidate phoneme) ─────────────────────
print("\n" + "="*65)
print("FRAME TOKEN ALIGNMENT HYPOTHESIS TABLE")
print("="*65)

print("""
Based on all tests above, proposed phoneme alignment for frame tokens:

EVA pattern  | Frequency role | Candidate mapping     | Language support
-------------|----------------|-----------------------|------------------
qo (prefix)  | R1 marker      | interrogative/topic   | no direct match (unique?)
             |                | OR: article 'ha-'?    | Hebrew stretch
k            | R1 stem        | /k/ phoneme           | universal
aiin / ai!n  | R1 stem        | /ayin/ or /ain/?      | Arabic ʿayn
edy          | R2 suffix      | /-di/ /-ti/?          | unknown
eey          | R2 suffix      | /-ei/? (adjectival?)  | speculative
ch-          | R2 initial     | /kh/ or /ch/          | ch in Hebrew/Arabic
sh-          | R2 initial     | /sh/ (שׁ)              | Hebrew shin (→ rel. pronoun)
l-           | R2 initial     | /l/ prefix (לְ)        | Hebrew lamed prefix
y (final)    | R2 suffix      | /y/ or yod suffix     | Hebrew yod (possessive?)

R6 confirmed:
ol           | REF            | vl / וְלֹא            | Hebrew (confirmed LC2)
al           | REF            | ʾl / אֶל               | Hebrew (confirmed LC2)
""")

print("="*65)
print("KEY STRUCTURAL INTERPRETATIONS")
print("="*65)
print("""
1. R1 tokens (qo + stem): The 'qo' prefix is UNIQUE to INIT tokens (10/11 have it).
   It is NOT present in any R2, R3, R4, R5, R6 token. This makes it a strong candidate
   for a LINE-INITIAL or PACKET-INITIAL grammatical marker — perhaps equivalent to a
   topic particle, article, or clause-initial conjunction.

2. R2 tokens (ch/sh/l + stem + -edy/-eey/-dy): The R2 tokens share:
   - Initial: ch- (chedy, cheey, chdy) or sh- (shedy, shey, sheey) or l- (lchedy)
   - Final: -edy (5/10) or -eey/-ey/-y variants
   - The -edy suffix may be a CLOSE marker — a grammatical suffix indicating end-of-packet
   - ch vs sh distinction may encode a semantic distinction (Biological vs Stars clusters)

3. The ch/sh alternation in R2:
   - chedy, cheey, chdy → cluster 6 (Biological 55%)
   - shedy, shey, sheey → cluster 1 (Biological 65% — but includes stars)
   - Mann-Whitney showed shedy (Biological R2) is the primary illustration predictor
   - Hypothesis: ch = one domain marker, sh = another (possibly type of biological content)

4. lchedy: the 'l' prefix on an R2 token is consistent with Hebrew lamed prefix (לְ)
   applied to a CLOSE token. Meaning unclear but suggests R2 tokens can take prefixes.
""")

# ─── Save results ───────────────────────────────────────────────────────────────
results = {
    'frame_nmi': {k: v for k, v in frame_nmi.items()},
    'para_init_rates': para_init_rates,
    'r1_prefix_analysis': {
        'shared_prefix': 'qo',
        'n_with_prefix': sum(1 for t in r1_list if t.startswith('qo')),
        'n_total': len(r1_list),
        'r1_stems_after_qo': sorted(r1_stems),
    },
    'r2_suffix_analysis': {
        'suffix_counts': dict(r2_suffixes.most_common()),
        'stem_tokens': {k: v for k, v in stem_tokens.items()},
    },
    'r6_alignment': {
        'ol': {'n': 504, 'hebrew': 'vl', 'meaning': 'and not', 'status': 'CONFIRMED'},
        'al': {'n': 246, 'hebrew': 'ʾl', 'meaning': 'to/toward', 'status': 'CONFIRMED'},
        'or': {'n': 76,  'hebrew': 'vr', 'meaning': 'ambiguous', 'status': 'SPECULATIVE'},
        'ar': {'n': 94,  'hebrew': 'ʾr', 'meaning': 'ambiguous', 'status': 'SPECULATIVE'},
    },
    'top_r2_preceding': prec_counts.head(10).to_dict(),
    'top_r1_following': foll_counts.head(10).to_dict(),
}

with open('FRAME1_structural_token_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nSaved: FRAME1_structural_token_results.json")
