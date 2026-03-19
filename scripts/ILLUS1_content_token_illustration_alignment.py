"""
ILLUS1 — Content Token × Illustration Type Alignment (Option B)

For each IA3 folio with a known illustration subtype, find which content tokens
are significantly over/underrepresented vs the full-corpus baseline.
Goal: build a vocabulary–illustration mapping table as a first step toward decoding.

Tests:
1. Chi-square / log-likelihood ratio for over-representation per illus type
2. Top 15 content tokens per illustration type (enrichment > 2×)
3. Cross-illustration type token overlap (Jaccard)
4. Section-level vocabulary comparison as background model
5. Candidate "Rosetta" tokens: those with high enrichment AND morphological structure

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import chi2_contingency, fisher_exact
from scipy.special import xlogy

# ─── Load corpus ───────────────────────────────────────────────────────────────
df = pd.read_csv("D1_corpus/corpus_tokens.csv")

# ─── IA3 folio illustration type map ───────────────────────────────────────────
IA3_PROFILES = {
    'f1v':  'botanical-single',
    'f15v': 'botanical-single',
    'f20r': 'botanical-single',
    'f25v': 'botanical-single',
    'f33v': 'botanical-single',
    'f40v': 'botanical-single',
    'f46v': 'botanical-single',
    'f55v': 'botanical-single',
    'f65v': 'botanical-single',
    'f75r': 'balneological-pool',
    'f77r': 'balneological-pool',
    'f79r': 'balneological-pool',
    'f68r1': 'astronomical-radial',
    'f68r2': 'astronomical-radial',
    'f68r3': 'astronomical-radial',
    'f85r2': 'cosmological-foldout',
    'f86v4': 'cosmological-foldout',
    'f103r': 'pharmaceutical-jar',
    'f107r': 'pharmaceutical-jar',
    'f116v': 'text-only',
}

# ─── Structural token sets (to filter them out for content token analysis) ─────
STRUCTURAL_PATH = "P1_structural/p1_1_cluster_frequencies.csv"
struct_df = pd.read_csv(STRUCTURAL_PATH)
STRUCTURAL_TOKENS = set(struct_df['cluster'].tolist())

# ─── Label corpus tokens ────────────────────────────────────────────────────────
df['illus_type'] = df['folio_id'].map(IA3_PROFILES)
df['is_structural'] = df['token'].isin(STRUCTURAL_TOKENS)
df['is_content'] = ~df['is_structural']

# Content tokens only
content = df[df['is_content']].copy()

# IA3 subset
ia3_content = content[content['illus_type'].notna()].copy()

illus_types = sorted(ia3_content['illus_type'].unique())
print(f"IA3 folios: {ia3_content['folio_id'].nunique()} folios")
print(f"IA3 content tokens: {len(ia3_content):,}")
print(f"Illustration types: {illus_types}")
print()
for it in illus_types:
    sub = ia3_content[ia3_content['illus_type'] == it]
    print(f"  {it:30s}: {sub['folio_id'].nunique()} folios, {len(sub):,} tokens")

# ─── 1. Token enrichment per illustration type ──────────────────────────────────
print("\n" + "="*65)
print("TOKEN ENRICHMENT BY ILLUSTRATION TYPE (vs full corpus baseline)")
print("="*65)

# Baseline: token frequency in full content corpus
baseline_counts = content['token'].value_counts()
baseline_total = len(content)

enriched = {}  # illus_type → list of (token, obs, exp, enrichment, p_fisher)

for it in illus_types:
    sub = ia3_content[ia3_content['illus_type'] == it]
    sub_total = len(sub)
    sub_counts = sub['token'].value_counts()

    hits = []
    for token, obs in sub_counts.items():
        if obs < 3:
            continue
        base_rate = baseline_counts.get(token, 0) / baseline_total
        exp = base_rate * sub_total
        if exp < 0.5:
            continue
        enrichment = obs / exp if exp > 0 else 0
        # Fisher exact test: 2×2 table
        a = obs
        b = sub_total - obs
        c = int(baseline_counts.get(token, 0)) - obs
        d = baseline_total - sub_total - c
        if c < 0 or d < 0:
            continue
        _, p = fisher_exact([[a, b], [max(c, 0), max(d, 0)]], alternative='greater')
        hits.append((token, obs, round(exp, 1), round(enrichment, 2), round(p, 5)))

    # Sort by enrichment
    hits.sort(key=lambda x: (-x[3], x[4]))
    enriched[it] = hits

    print(f"\n{it.upper()} (n={sub_total} tokens):")
    print(f"  {'Token':<15} {'Obs':>5} {'Exp':>6} {'Enrich':>8} {'p':>9}")
    print("  " + "-"*50)
    for token, obs, exp, enr, p in hits[:15]:
        star = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
        print(f"  {token:<15} {obs:>5} {exp:>6.1f} {enr:>7.1f}×  {p:>8.5f} {star}")

# ─── 2. Top enriched tokens with morphological profile ────────────────────────
print("\n" + "="*65)
print("CANDIDATE ROSETTA TOKENS (enrichment > 3×, p < 0.05)")
print("="*65)

rosetta = []
for it, hits in enriched.items():
    for token, obs, exp, enr, p in hits:
        if enr >= 3.0 and p < 0.05:
            # Morphological profile
            has_dy = token.endswith('dy') or token.endswith('edy') or token.endswith('ody')
            has_ain = 'ain' in token or 'ai!n' in token
            has_ch = token.startswith('ch') or 'ch' in token[1:]
            has_sh = token.startswith('sh') or 'sh' in token[1:]
            length = len(token)
            rosetta.append({
                'illus_type': it,
                'token': token,
                'obs': obs,
                'exp': exp,
                'enrichment': enr,
                'p': p,
                'has_dy': has_dy,
                'has_ain': has_ain,
                'length': length,
            })

rosetta_df = pd.DataFrame(rosetta)
if len(rosetta_df) > 0:
    print(f"\nFound {len(rosetta_df)} Rosetta candidates:")
    print(rosetta_df.to_string(index=False))
else:
    print("No tokens with enrichment > 3× and p < 0.05 found.")

# ─── 3. Cross-illustration Jaccard overlap ─────────────────────────────────────
print("\n" + "="*65)
print("CROSS-ILLUSTRATION TYPE JACCARD SIMILARITY")
print("="*65)

# Vocabulary sets (tokens appearing ≥2× in each type)
illus_vocabs = {}
for it in illus_types:
    sub = ia3_content[ia3_content['illus_type'] == it]
    counts = sub['token'].value_counts()
    illus_vocabs[it] = set(counts[counts >= 2].index)
    print(f"  {it:30s}: {len(illus_vocabs[it])} types (≥2×)")

print("\nJaccard similarity matrix:")
header = "  " + "".join(f"{it[:10]:>12}" for it in illus_types)
print(header)
for it1 in illus_types:
    row = f"  {it1[:10]:12}"
    for it2 in illus_types:
        v1, v2 = illus_vocabs[it1], illus_vocabs[it2]
        j = len(v1 & v2) / len(v1 | v2) if v1 | v2 else 0
        row += f"  {j:.3f}    "
    print(row)

# ─── 4. Section-level comparison (expanded baseline) ──────────────────────────
print("\n" + "="*65)
print("SECTION-LEVEL TOKEN ENRICHMENT COMPARISON")
print("="*65)

# Map IA3 illustration types to sections
ILLUS_TO_SECTION = {
    'botanical-single': 'H',
    'balneological-pool': 'B',
    'astronomical-radial': 'A',
    'cosmological-foldout': 'C',
    'pharmaceutical-jar': 'P',
    'text-only': 'T',
}

print("\nFor each illus type, compare top enriched tokens against the full section vocabulary:")
for it, sec in ILLUS_TO_SECTION.items():
    if it not in enriched:
        continue
    top_tokens = [tok for tok, obs, exp, enr, p in enriched[it][:10] if p < 0.05]
    if not top_tokens:
        continue
    # Check what fraction also appear in the same section at higher-than-median rate
    sec_content = content[content['section'] == sec]
    sec_total = len(sec_content)
    sec_counts = sec_content['token'].value_counts()
    print(f"\n  {it} (section {sec}) top tokens also elevated in section?")
    for tok in top_tokens:
        sec_rate = sec_counts.get(tok, 0) / sec_total if sec_total > 0 else 0
        base_rate = baseline_counts.get(tok, 0) / baseline_total
        ratio = sec_rate / base_rate if base_rate > 0 else 0
        print(f"    {tok:<15}: sec-rate={sec_rate*1000:.2f}‰, baseline={base_rate*1000:.2f}‰, "
              f"ratio={ratio:.1f}×")

# ─── 5. Morphological signature by illustration type ──────────────────────────
print("\n" + "="*65)
print("MORPHOLOGICAL SIGNATURE BY ILLUSTRATION TYPE")
print("="*65)

def morph_profile(tokens):
    """Return morphological profile dict for a list of tokens."""
    n = len(tokens)
    return {
        'pct_dy_suffix': sum(1 for t in tokens if t.endswith('dy') or t.endswith('edy')) / n,
        'pct_ain':       sum(1 for t in tokens if 'ain' in t or 'ai!n' in t) / n,
        'pct_ch':        sum(1 for t in tokens if 'ch' in t) / n,
        'pct_sh':        sum(1 for t in tokens if 'sh' in t) / n,
        'pct_ol_al':     sum(1 for t in tokens if t in ('ol','al','or','ar')) / n,
        'mean_length':   np.mean([len(t) for t in tokens]),
        'n_hapax':       sum(1 for t in tokens if baseline_counts.get(t, 0) == 1),
    }

print(f"\n  {'Illus type':<25} {'%dy':>6} {'%ain':>6} {'%ch':>5} {'%sh':>5} {'mean_len':>9}")
print("  " + "-"*65)
baseline_tokens = content['token'].tolist()
bprof = morph_profile(baseline_tokens)
print(f"  {'BASELINE (full corpus)':<25} {bprof['pct_dy_suffix']*100:>5.1f}% "
      f"{bprof['pct_ain']*100:>5.1f}% {bprof['pct_ch']*100:>4.1f}% "
      f"{bprof['pct_sh']*100:>4.1f}% {bprof['mean_length']:>8.2f}")
for it in illus_types:
    sub_toks = ia3_content[ia3_content['illus_type'] == it]['token'].tolist()
    if not sub_toks:
        continue
    p = morph_profile(sub_toks)
    print(f"  {it:<25} {p['pct_dy_suffix']*100:>5.1f}% "
          f"{p['pct_ain']*100:>5.1f}% {p['pct_ch']*100:>4.1f}% "
          f"{p['pct_sh']*100:>4.1f}% {p['mean_length']:>8.2f}")

# ─── 6. Save Rosetta table ─────────────────────────────────────────────────────
output = {
    'illus_types': illus_types,
    'enriched_tokens_per_type': {
        it: [(tok, obs, exp, enr, p)
             for tok, obs, exp, enr, p in hits[:20]]
        for it, hits in enriched.items()
    },
    'rosetta_candidates': rosetta,
    'jaccard_matrix': {
        it1: {it2: round(len(illus_vocabs.get(it1,set()) & illus_vocabs.get(it2,set())) /
                         len(illus_vocabs.get(it1,set()) | illus_vocabs.get(it2,set())), 3)
              for it2 in illus_types}
        for it1 in illus_types
    },
}
with open('ILLUS1_content_token_illustration_results.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

print("\nSaved: ILLUS1_content_token_illustration_results.json")
