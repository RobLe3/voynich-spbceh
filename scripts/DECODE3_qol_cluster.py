"""
DECODE3 — Lead 3: `qol` in Balneological — Hebrew kol / Arabic kull (all/every)?

Tests:
1. Full line listing of qol in section B with context
2. What immediately precedes/follows qol? (quantifier → should precede content nouns)
3. Compare qol context B vs S vs other sections
4. Test: does qol + [content-token] produce semantically coherent clusters?
5. Compare qol, kal, okol, qokeol — are these variants of the same root?
6. If qol = "all/every": it should precede content tokens, not structural ones
7. Cross-check with sal: do sal and qol appear on the same lines?

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import fisher_exact

df = pd.read_csv("D1_corpus/corpus_tokens.csv")
struct_df = pd.read_csv("P1_structural/p1_1_cluster_frequencies.csv")
STRUCT = set(struct_df['cluster'].tolist())

TARGET = 'qol'
VARIANTS = ['kal', 'okol', 'qokeol', 'ol', 'kol']   # potential root variants
SECTIONS = ['H','A','B','P','C','Z','S','T']

df_sorted = df.sort_values(['folio_id','line_id','token_index'])
df_sorted['prev'] = df_sorted.groupby(['folio_id','line_id'])['token'].shift(1)
df_sorted['next'] = df_sorted.groupby(['folio_id','line_id'])['token'].shift(-1)
df_sorted['prev2'] = df_sorted.groupby(['folio_id','line_id'])['token'].shift(2)
df_sorted['next2'] = df_sorted.groupby(['folio_id','line_id'])['token'].shift(-2)

qol_rows = df_sorted[df_sorted['token'] == TARGET].copy()

print(f"'{TARGET}': {len(qol_rows)} total occurrences")
print("Section distribution:")
for s in SECTIONS:
    n = (qol_rows['section'] == s).sum()
    pct = n / len(qol_rows) * 100
    print(f"  {s}: {n:3d}  ({pct:.1f}%)")

# ── 1. Full line listing in section B ─────────────────────────────────────────
print("\n" + "="*65)
print(f"1. ALL '{TARGET}' OCCURRENCES IN SECTION B (with line context)")
print("="*65)

lines = df.groupby(['folio_id','line_id'])['token'].apply(list).reset_index()
lines.columns = ['folio_id','line_id','tokens']
lines['section'] = df.groupby(['folio_id','line_id'])['section'].first().values

qol_b_lines = lines[(lines['tokens'].apply(lambda t: TARGET in t)) & (lines['section'] == 'B')]
print(f"\n{len(qol_b_lines)} lines with '{TARGET}' in section B:\n")
for _, row in qol_b_lines.iterrows():
    toks = row['tokens']
    annotated = []
    for t in toks:
        if t == TARGET:
            annotated.append(f'**{t}**')
        elif t in STRUCT:
            annotated.append(f'[{t}]')
        else:
            annotated.append(t)
    print(f"  {row['folio_id']:8s}: {' '.join(annotated)}")

# ── 2. Immediate bigram context by section ────────────────────────────────────
print("\n" + "="*65)
print(f"2. BIGRAM CONTEXT: WHAT PRECEDES/FOLLOWS '{TARGET}'?")
print("="*65)

for sec in ['B','S','H','A']:
    sub = qol_rows[qol_rows['section'] == sec]
    if len(sub) == 0: continue
    prev_c = sub['prev'].dropna().value_counts()
    next_c = sub['next'].dropna().value_counts()
    print(f"\n  Section {sec} (n={len(sub)}):")
    print(f"    Preceding: " + ', '.join(f"{t}({'S' if t in STRUCT else 'c'}:{n})" for t,n in prev_c.head(6).items()))
    print(f"    Following: " + ', '.join(f"{t}({'S' if t in STRUCT else 'c'}:{n})" for t,n in next_c.head(6).items()))

# ── 3. Structural vs content context ──────────────────────────────────────────
print("\n" + "="*65)
print(f"3. DOES '{TARGET}' PRECEDE CONTENT OR STRUCTURAL TOKENS?")
print("="*65)

# If qol = quantifier "all/every", it should PRECEDE content tokens
# If qol = structural function word, it should appear near structural tokens
for sec in ['B','S','H']:
    sub = qol_rows[qol_rows['section'] == sec]
    if len(sub) == 0: continue
    next_toks = sub['next'].dropna()
    n_struct_next = next_toks.isin(STRUCT).sum()
    n_content_next = (~next_toks.isin(STRUCT)).sum()
    prev_toks = sub['prev'].dropna()
    n_struct_prev = prev_toks.isin(STRUCT).sum()
    n_content_prev = (~prev_toks.isin(STRUCT)).sum()
    print(f"\n  Section {sec}: follows structural={n_struct_prev}, follows content={n_content_prev}")
    print(f"           precedes structural={n_struct_next}, precedes content={n_content_next}")

# ── 4. qol + content-noun clusters in B ───────────────────────────────────────
print("\n" + "="*65)
print(f"4. MOST COMMON [qol + CONTENT_TOKEN] PAIRS IN SECTION B")
print("="*65)

b_qol = qol_rows[qol_rows['section'] == 'B']
pairs_b = []
for _, row in b_qol.iterrows():
    nxt = row['next']
    if pd.notna(nxt) and nxt not in STRUCT:
        pairs_b.append(nxt)
pair_counts_b = Counter(pairs_b)
print(f"\n  Top content tokens following qol in section B:")
for tok, n in pair_counts_b.most_common(15):
    print(f"    qol + {tok:<15} n={n}")

# ── 5. Root variant comparison: qol, kal, okol, ol ────────────────────────────
print("\n" + "="*65)
print(f"5. ROOT VARIANT COMPARISON: qol / kal / okol / ol")
print("="*65)

# Check each variant's section distribution and role
for var in [TARGET] + VARIANTS:
    var_rows = df[df['token'] == var]
    if len(var_rows) == 0: continue
    is_struct = var in STRUCT
    sec_dist = var_rows['section'].value_counts()
    top_secs = ', '.join(f"{s}={c}" for s,c in sec_dist.head(3).items())
    n_total = len(var_rows)
    print(f"  {var:<10} n={n_total:4d}  role={'STRUCT' if is_struct else 'content'}  sections: {top_secs}")

# Shared section profile? Compute correlation
print(f"\n  Section profile correlation (all sections):")
variant_profiles = {}
for var in [TARGET] + VARIANTS:
    var_rows = df[df['token'] == var]
    if len(var_rows) == 0: continue
    profile = [var_rows[var_rows['section']==s].shape[0] / max(len(var_rows),1) for s in SECTIONS]
    variant_profiles[var] = profile

# Pairwise correlation
vars_present = list(variant_profiles.keys())
for i, v1 in enumerate(vars_present):
    for j, v2 in enumerate(vars_present):
        if j <= i: continue
        p1, p2 = np.array(variant_profiles[v1]), np.array(variant_profiles[v2])
        if p1.std() > 0 and p2.std() > 0:
            corr = np.corrcoef(p1, p2)[0,1]
            print(f"    {v1} vs {v2}: r={corr:.3f}")

# ── 6. Quantifier hypothesis test ─────────────────────────────────────────────
print("\n" + "="*65)
print(f"6. QUANTIFIER HYPOTHESIS: qol BEFORE CONTENT NOUNS IN B")
print("="*65)

# If qol = "all/every" (quantifier), it predicts:
# A: qol is followed by content tokens more than structural tokens
# B: the content token following qol varies widely (it quantifies many things)
# C: qol is NOT followed by qol or other quantifiers

b_qol_next = b_qol['next'].dropna()
n_content = (~b_qol_next.isin(STRUCT)).sum()
n_struct = b_qol_next.isin(STRUCT).sum()
unique_content = b_qol_next[~b_qol_next.isin(STRUCT)].nunique()

print(f"\n  qol in B: {len(b_qol)} occurrences")
print(f"  Followed by content token: {n_content} ({n_content/len(b_qol)*100:.0f}%)")
print(f"  Followed by structural token: {n_struct} ({n_struct/len(b_qol)*100:.0f}%)")
print(f"  Unique content tokens following qol in B: {unique_content}")
print(f"  → {'HIGH DIVERSITY (consistent with quantifier)' if unique_content > 5 else 'LOW DIVERSITY (inconsistent with quantifier)'}")

# ── 7. qol + sal co-occurrence ────────────────────────────────────────────────
print("\n" + "="*65)
print("7. qol + sal CROSS-OCCURRENCE (salt water hypothesis)")
print("="*65)

lines_with_both = lines[lines['tokens'].apply(lambda t: 'qol' in t and 'sal' in t)]
lines_with_both_B = lines_with_both[lines_with_both['section'] == 'B']
print(f"\n  Lines containing both qol AND sal:")
print(f"    All sections: {len(lines_with_both)}")
print(f"    Section B:    {len(lines_with_both_B)}")
if len(lines_with_both_B) > 0:
    print(f"\n  Section B lines with both:")
    for _, row in lines_with_both_B.iterrows():
        annotated = ['**'+t+'**' if t in ('qol','sal') else ('['+t+']' if t in STRUCT else t) for t in row['tokens']]
        print(f"    {row['folio_id']:8s}: {' '.join(annotated)}")
else:
    print("  → qol and sal do NOT commonly appear on the same line")

# ── 8. Overall verdict ────────────────────────────────────────────────────────
print("\n" + "="*65)
print("OVERALL VERDICT SUMMARY")
print("="*65)

# Compute key stats for summary
b_count = (qol_rows['section'] == 'B').sum()
total_b_content = df[(df['section']=='B') & (~df['token'].isin(STRUCT))].shape[0]
b_rate = b_count / total_b_content * 1000

# Capture the qol-ol correlation specifically
qol_ol_r = None
for tok in ['ol']:
    p1 = variant_profiles.get('qol')
    p2 = variant_profiles.get(tok)
    if p1 is not None and p2 is not None:
        qol_ol_r = float(np.corrcoef(p1, p2)[0, 1])

results = {
    'qol_total': int(len(qol_rows)),
    'qol_B_count': int(b_count),
    'qol_B_rate_per1000': round(b_rate, 2),
    'qol_B_lines': int(len(qol_b_lines)),
    'content_following_B': int(n_content),
    'struct_following_B': int(n_struct),
    'unique_content_following_B': int(unique_content),
    'lines_both_qol_sal': int(len(lines_with_both)),
    'lines_both_qol_sal_B': int(len(lines_with_both_B)),
    'qol_ol_pearson_r': qol_ol_r,
}
with open('DECODE3_qol_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved: DECODE3_qol_results.json")
