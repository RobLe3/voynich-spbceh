"""
DECODE1 — Lead 1: `sal` = Latin sal (salt) co-occurrence verification

Tests:
1. What co-occurs with `sal` on the same line? (bi/trigram context)
2. Does `sal` + `qol` or `sal` + `oly` appear more than chance?
3. Full line listing for all `sal` occurrences in section B
4. Compare sal context B vs S vs H
5. Does sal form a recurring "bath ingredient" cluster with oly/qol/olor?

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import fisher_exact, mannwhitneyu

df = pd.read_csv("D1_corpus/corpus_tokens.csv")
struct_df = pd.read_csv("P1_structural/p1_1_cluster_frequencies.csv")
STRUCT = set(struct_df['cluster'].tolist())

TARGET = 'sal'
CANDIDATES = ['qol', 'oly', 'olor', 'ol', 'daiin', 'aiin', 'cheedy', 'shedy']
SECTIONS = ['H','A','B','P','C','Z','S','T']

# ── Build line-level token sets ──────────────────────────────────────────────
lines = df.groupby(['folio_id','line_id'])['token'].apply(list).reset_index()
lines.columns = ['folio_id','line_id','tokens']
lines['section'] = df.groupby(['folio_id','line_id'])['section'].first().values

sal_lines = lines[lines['tokens'].apply(lambda toks: TARGET in toks)].copy()
print(f"Lines containing '{TARGET}': {len(sal_lines)} / {len(lines)} total lines")
print(f"Section distribution:")
for s in SECTIONS:
    n = (sal_lines['section'] == s).sum()
    pct = n / len(sal_lines) * 100 if len(sal_lines) > 0 else 0
    print(f"  {s}: {n:3d}  ({pct:.1f}%)")

# ── 1. Co-occurrence on same line ─────────────────────────────────────────────
print("\n" + "="*65)
print(f"1. SAME-LINE CO-OCCURRENCE WITH '{TARGET}'")
print("="*65)

cooccur = Counter()
for _, row in sal_lines.iterrows():
    toks = set(row['tokens']) - {TARGET}
    for t in toks:
        cooccur[t] += 1

# Baseline: how often does each candidate appear in ANY line?
all_tok_in_lines = Counter()
for _, row in lines.iterrows():
    for t in set(row['tokens']):
        all_tok_in_lines[t] += 1

n_lines = len(lines)
n_sal_lines = len(sal_lines)

print(f"\n{'Token':<15} {'co-occur':>9} {'expected':>9} {'enrichment':>11} {'p_fisher':>10}")
print("-"*60)
for tok, co_n in cooccur.most_common(20):
    base_rate = all_tok_in_lines.get(tok, 0) / n_lines
    exp = base_rate * n_sal_lines
    enrich = co_n / exp if exp > 0 else 0
    # Fisher exact: sal-line with tok / without tok vs non-sal-line with tok / without
    a = co_n
    b = n_sal_lines - co_n
    c = all_tok_in_lines.get(tok, 0) - co_n
    d = n_lines - n_sal_lines - max(c, 0)
    _, p = fisher_exact([[a, b], [max(c,0), max(d,0)]], alternative='greater')
    flag = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
    role = '[STRUCT]' if tok in STRUCT else ''
    print(f"  {tok:<13} {co_n:>8}  {exp:>8.1f}  {enrich:>9.2f}×  {p:>9.5f} {flag} {role}")

# ── 2. Specific co-occurrence with candidate water/oil terms ──────────────────
print("\n" + "="*65)
print(f"2. SPECIFIC CO-OCCURRENCE: {TARGET} + BATH-TERM CANDIDATES")
print("="*65)

for cand in CANDIDATES:
    both = sal_lines[sal_lines['tokens'].apply(lambda t: cand in t)]
    n_both = len(both)
    base_rate_cand = all_tok_in_lines.get(cand, 0) / n_lines
    exp = base_rate_cand * n_sal_lines
    enrich = n_both / exp if exp > 0 else 0
    a, b = n_both, n_sal_lines - n_both
    c = max(all_tok_in_lines.get(cand, 0) - n_both, 0)
    d = max(n_lines - n_sal_lines - c, 0)
    _, p = fisher_exact([[a, b], [c, d]], alternative='greater')
    role = '[STRUCT]' if cand in STRUCT else ''
    print(f"  sal + {cand:<10}: n={n_both:3d}, exp={exp:.1f}, enrich={enrich:.2f}×, p={p:.5f} {'***' if p<0.001 else ('**' if p<0.01 else ('*' if p<0.05 else ''))} {role}")

# ── 3. Full line listing for section B ────────────────────────────────────────
print("\n" + "="*65)
print(f"3. ALL '{TARGET}' LINES IN SECTION B (BALNEOLOGICAL)")
print("="*65)

b_sal = sal_lines[sal_lines['section'] == 'B'].copy()
print(f"\n{len(b_sal)} lines with '{TARGET}' in section B:\n")
for _, row in b_sal.iterrows():
    toks = row['tokens']
    pos = toks.index(TARGET) if TARGET in toks else -1
    # Mark structural tokens
    annotated = ['['+t+']' if t in STRUCT else t for t in toks]
    line_str = ' '.join(annotated)
    print(f"  {row['folio_id']:8s} {row['line_id']:12s}: {line_str}")

# ── 4. Compare sal context B vs S vs H ───────────────────────────────────────
print("\n" + "="*65)
print(f"4. BIGRAM CONTEXT: WHAT IMMEDIATELY PRECEDES/FOLLOWS '{TARGET}'?")
print("="*65)

df_sorted = df.sort_values(['folio_id','line_id','token_index'])
df_sorted['prev'] = df_sorted.groupby(['folio_id','line_id'])['token'].shift(1)
df_sorted['next'] = df_sorted.groupby(['folio_id','line_id'])['token'].shift(-1)

sal_ctx = df_sorted[df_sorted['token'] == TARGET].copy()

for sec in ['B','S','H']:
    sub = sal_ctx[sal_ctx['section'] == sec]
    if len(sub) == 0: continue
    prev_counts = sub['prev'].dropna().value_counts().head(5)
    next_counts = sub['next'].dropna().value_counts().head(5)
    print(f"\n  Section {sec} (n={len(sub)}):")
    print(f"    Preceding: " + ', '.join(f"{t}({n})" for t,n in prev_counts.items()))
    print(f"    Following: " + ', '.join(f"{t}({n})" for t,n in next_counts.items()))

# ── 5. sal + qol + oly cluster — do they share lines? ─────────────────────────
print("\n" + "="*65)
print("5. BATH INGREDIENT CLUSTER: sal + qol + oly SHARED LINES")
print("="*65)

cluster_toks = ['sal', 'qol', 'oly', 'olor']
for t1 in cluster_toks:
    for t2 in cluster_toks:
        if t1 >= t2: continue
        both = lines[lines['tokens'].apply(lambda t: t1 in t and t2 in t)]
        b_both = both[both['section'] == 'B']
        print(f"  {t1} + {t2}: {len(both):3d} shared lines total, {len(b_both):2d} in section B")

# ── 6. Summary verdict ────────────────────────────────────────────────────────
print("\n" + "="*65)
print("VERDICT: sal = Latin sal (salt)?")
print("="*65)
# Check if qol is the top co-occurring term
top_cooccur = cooccur.most_common(5)
qol_rank = next((i+1 for i,(t,_) in enumerate(cooccur.most_common()) if t == 'qol'), None)
oly_rank  = next((i+1 for i,(t,_) in enumerate(cooccur.most_common()) if t == 'oly'), None)
print(f"\n  qol co-occurrence rank with sal: #{qol_rank}")
print(f"  oly co-occurrence rank with sal: #{oly_rank}")
print(f"  Top 5 co-occurring tokens: {[(t,n) for t,n in top_cooccur]}")

results = {
    'sal_lines': int(len(sal_lines)),
    'top_cooccur': [(t, int(n)) for t,n in cooccur.most_common(10)],
    'qol_cooccur_rank': qol_rank,
    'oly_cooccur_rank': oly_rank,
}
with open('DECODE1_sal_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved: DECODE1_sal_results.json")
