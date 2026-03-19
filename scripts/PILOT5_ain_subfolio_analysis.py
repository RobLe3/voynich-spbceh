"""
PILOT5 — -ain Suffix Sub-Folio Analysis

Goal: Map -ain family tokens to sub-folio structure more finely than PILOT2.
PILOT2 tested: does dominant -ain token encode zodiac SIGN? → REFUTED (2/7 consistency)
PILOT5 tests: does -ain token vary within a folio (by paragraph/line), and
              is there a systematic line-position or paragraph-position pattern?

Questions:
1. Within a single folio, does the dominant -ain token vary by paragraph?
2. Is -ain token frequency concentrated in specific line positions (line-initial vs medial)?
3. Do -ain tokens appear preferentially near R1 (INIT) or R2 (CLOSE) tokens?
4. What is the -ain token's packet-internal position (entity-slot)?
5. Are there -ain tokens that are EXCLUSIVE to individual folios (folio-unique entities)?
6. What role does the -ain suffix play morphologically (is it a suffix on content stems)?

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import fisher_exact, ttest_1samp

df = pd.read_csv("../data/corpus_tokens.csv")
roles_df = pd.read_csv("../results/p1_1_cluster_frequencies.csv")
role_map = dict(zip(roles_df['cluster'], roles_df['role']))
df['role'] = df['token'].map(role_map).fillna('CONTENT')

# Stars section folios
STARS_SECTION = 'S'
stars_df = df[df['section'] == STARS_SECTION].copy()

print("=" * 70)
print("PILOT5 — -ain Suffix Sub-Folio Analysis (Stars Section)")
print("=" * 70)
print(f"\nStars section tokens: {len(stars_df)}")
print(f"Stars section folios: {stars_df['folio_id'].nunique()}")

# ── 1. Identify -ain family tokens ──────────────────────────────────────────
def is_ain_token(tok):
    return tok.endswith('ain') or tok.endswith('ai!n') or tok.endswith('aiin') or \
           tok.endswith('aiiin') or tok.endswith('ai!in')

ain_tokens_df = stars_df[stars_df['token'].apply(is_ain_token)].copy()
print(f"\n-ain family tokens in Stars section: {len(ain_tokens_df)}")
print(f"-ain types: {ain_tokens_df['token'].nunique()}")

print("\n\n1. TOP -ain TOKENS IN STARS SECTION")
print("-" * 50)
ain_counts = ain_tokens_df['token'].value_counts()
total_stars = len(stars_df)
print(f"\n  {'Token':<20} {'n':>6} {'%_stars':>8} {'n_folios':>10}")
print("  " + "-" * 50)
for tok, n in ain_counts.head(20).items():
    n_folios = ain_tokens_df[ain_tokens_df['token']==tok]['folio_id'].nunique()
    pct = n / total_stars * 100
    print(f"  {tok:<20} {n:>6} {pct:>7.3f}% {n_folios:>10}")

# ── 2. Per-folio dominant -ain token ────────────────────────────────────────
print("\n\n2. PER-FOLIO DOMINANT -ain TOKEN (Stars section)")
print("-" * 60)

folio_ain = defaultdict(Counter)
for _, row in ain_tokens_df.iterrows():
    folio_ain[row['folio_id']][row['token']] += 1

folio_order = sorted(folio_ain.keys())
print(f"\n  {'Folio':<10} {'Dom -ain token':<22} {'n':>4} {'total_ain':>10} {'dom%':>8}")
print("  " + "-" * 60)
for folio in folio_order:
    counts = folio_ain[folio]
    total_ain_folio = sum(counts.values())
    if not counts:
        continue
    dom_tok, dom_n = counts.most_common(1)[0]
    dom_pct = dom_n / total_ain_folio * 100
    print(f"  {folio:<10} {dom_tok:<22} {dom_n:>4} {total_ain_folio:>10} {dom_pct:>7.1f}%")

# ── 3. Within-folio variability: does dominant -ain vary by PARAGRAPH? ───────
print("\n\n3. WITHIN-FOLIO -ain VARIABILITY BY PARAGRAPH")
print("-" * 60)

# For each folio, get dominant -ain by paragraph
folio_para_ain = defaultdict(lambda: defaultdict(Counter))
for _, row in ain_tokens_df.iterrows():
    folio_para_ain[row['folio_id']][row['paragraph_id']][row['token']] += 1

print(f"\n  Folios with multiple paragraphs having -ain tokens:")
for folio in folio_order:
    para_data = folio_para_ain[folio]
    if len(para_data) < 2:
        continue
    dominant_per_para = {}
    for para_id, counts in para_data.items():
        if counts:
            dominant_per_para[para_id] = counts.most_common(1)[0][0]
    unique_dominants = len(set(dominant_per_para.values()))
    all_same = unique_dominants == 1
    status = 'CONSISTENT' if all_same else 'VARIES'
    print(f"  {folio:<10}: {len(dominant_per_para)} paragraphs, "
          f"{unique_dominants} distinct dominant tokens [{status}]")
    if not all_same:
        for para_id, tok in sorted(dominant_per_para.items()):
            print(f"    para {para_id}: {tok}")

# ── 4. -ain token packet-internal position ───────────────────────────────────
print("\n\n4. -ain TOKEN PACKET-INTERNAL POSITION (Stars section)")
print("-" * 60)

df_sorted = df.sort_values(['folio_id','paragraph_id','token_index']).copy()
# Reconstruct packets in Stars section
s_packets = []
for (folio, para_id), grp in df_sorted.groupby(['folio_id','paragraph_id']):
    if grp['section'].iloc[0] != STARS_SECTION:
        continue
    toks = grp['token'].tolist()
    tok_roles = grp['role'].tolist()
    i = 0
    while i < len(toks):
        if tok_roles[i] == 'INIT':
            j = i + 1
            while j < len(toks) and tok_roles[j] != 'CLOSE':
                j += 1
            if j < len(toks):
                payload = toks[i+1:j]
                s_packets.append({'folio': folio, 'payload': payload, 'payload_len': len(payload)})
            i = j+1 if j < len(toks) else i+1
        else:
            i += 1

# Find -ain tokens in packet payloads
ain_packet_positions = []
ain_in_packets_by_type = defaultdict(list)
for p in s_packets:
    for idx, tok in enumerate(p['payload']):
        if is_ain_token(tok):
            rel_pos = idx / (p['payload_len']-1) if p['payload_len'] > 1 else 0.5
            ain_packet_positions.append(rel_pos)
            ain_in_packets_by_type[tok].append(rel_pos)

print(f"\n  Stars packets reconstructed: {len(s_packets)}")
print(f"  -ain occurrences inside packets: {len(ain_packet_positions)}")
if ain_packet_positions:
    mean_p = np.mean(ain_packet_positions)
    _, p_val = ttest_1samp(ain_packet_positions, 0.5)
    print(f"  Mean relative position: {mean_p:.3f}")
    print(f"  t-test vs 0.5: p={p_val:.4f}")

    early = sum(1 for p in ain_packet_positions if p < 0.33)
    mid   = sum(1 for p in ain_packet_positions if 0.33 <= p <= 0.67)
    late  = sum(1 for p in ain_packet_positions if p > 0.67)
    print(f"\n  Position distribution:")
    print(f"    Early (0–33%):  {early} ({early/len(ain_packet_positions)*100:.1f}%)")
    print(f"    Mid   (33–67%): {mid} ({mid/len(ain_packet_positions)*100:.1f}%)")
    print(f"    Late  (67–100%): {late} ({late/len(ain_packet_positions)*100:.1f}%)")

# Top -ain types by packet position
print(f"\n  -ain types with ≥3 packet occurrences:")
print(f"  {'Token':<20} {'n_pkts':>8} {'mean_pos':>10} {'p':>10}")
for tok, positions in sorted(ain_in_packets_by_type.items(), key=lambda x: -len(x[1])):
    if len(positions) < 3: continue
    mean_p = np.mean(positions)
    _, p_val = ttest_1samp(positions, 0.5) if len(positions) >= 5 else (None, None)
    p_str = f"{p_val:.4f}" if p_val is not None else "n<5"
    print(f"  {tok:<20} {len(positions):>8} {mean_p:>10.3f} {p_str:>10}")

# ── 5. Folio-unique -ain types ──────────────────────────────────────────────
print("\n\n5. FOLIO-UNIQUE -ain TYPES (appear in only 1 Stars folio)")
print("-" * 60)

ain_folio_set = defaultdict(set)
for _, row in ain_tokens_df.iterrows():
    ain_folio_set[row['token']].add(row['folio_id'])

unique_types = [(tok, list(folios)[0], len(ain_tokens_df[ain_tokens_df['token']==tok]))
                for tok, folios in ain_folio_set.items() if len(folios) == 1]
unique_types.sort(key=lambda x: -x[2])

print(f"\n  Folio-unique -ain types: {len(unique_types)} / {ain_tokens_df['token'].nunique()} total types")
print(f"\n  {'Token':<22} {'Folio':<12} {'n':<6}")
print("  " + "-" * 45)
for tok, folio, n in unique_types[:25]:
    print(f"  {tok:<22} {folio:<12} {n}")

# ── 6. Stem analysis: what comes BEFORE -ain suffix? ────────────────────────
print("\n\n6. MORPHOLOGICAL STEM ANALYSIS: CONSONANTS PRECEDING -ain")
print("-" * 60)

def get_stem(tok):
    """Extract consonant stem before -ain/-aiin/-ai!n suffix."""
    for suffix in ['aiiin', 'aiin', 'ai!in', 'ai!n', 'ain']:
        if tok.endswith(suffix):
            return tok[:-len(suffix)]
    return None

stem_counts = Counter()
for tok, n in ain_counts.items():
    stem = get_stem(tok)
    if stem is not None:
        stem_counts[stem] += n

print(f"\n  Stars -ain stems (n≥3):")
print(f"  {'Stem':<20} {'n':>6}  Interpretation")
print("  " + "-" * 60)
for stem, n in stem_counts.most_common(25):
    if n < 3: break
    # Simple consonant analysis
    cons = ''.join(c for c in stem if c not in 'aeiou!?')
    print(f"  {stem:<20} {n:>6}  cons=[{cons}]")

# ── 7. -ain bigram context in Stars ─────────────────────────────────────────
print("\n\n7. BIGRAM CONTEXT: WHAT PRECEDES -ain TOKENS IN STARS SECTION?")
print("-" * 60)

df_s = df_sorted[df_sorted['section'] == STARS_SECTION].copy()
df_s['prev_tok'] = df_s.groupby(['folio_id','paragraph_id'])['token'].shift(1)
df_s['next_tok'] = df_s.groupby(['folio_id','paragraph_id'])['token'].shift(-1)
df_s['prev_role'] = df_s.groupby(['folio_id','paragraph_id'])['role'].shift(1)
df_s['next_role'] = df_s.groupby(['folio_id','paragraph_id'])['role'].shift(-1)

ain_s = df_s[df_s['token'].apply(is_ain_token)].copy()

prev_role = ain_s['prev_role'].dropna().value_counts()
next_role = ain_s['next_role'].dropna().value_counts()
prev_tok = ain_s['prev_tok'].dropna().value_counts().head(10)
next_tok = ain_s['next_tok'].dropna().value_counts().head(10)

print(f"\n  Stars -ain preceding role distribution:")
for role, n in prev_role.items():
    print(f"    {role:<15} n={n}")

print(f"\n  Stars -ain following role distribution:")
for role, n in next_role.items():
    print(f"    {role:<15} n={n}")

print(f"\n  Top preceding tokens:")
for tok, n in prev_tok.items():
    role = role_map.get(tok, 'CONTENT')
    print(f"    {tok:<20} n={n}  [{role}]")

print(f"\n  Top following tokens:")
for tok, n in next_tok.items():
    role = role_map.get(tok, 'CONTENT')
    print(f"    {tok:<20} n={n}  [{role}]")

# ── 8. Save results ───────────────────────────────────────────────────────────
results = {
    'stars_ain_total': int(len(ain_tokens_df)),
    'stars_ain_types': int(ain_tokens_df['token'].nunique()),
    'folio_dominant_ain': {f: c.most_common(1)[0] for f, c in folio_ain.items() if c},
    'n_folio_unique_types': len(unique_types),
    'ain_packet_positions_n': len(ain_packet_positions),
    'ain_mean_packet_position': float(np.mean(ain_packet_positions)) if ain_packet_positions else None,
    'top_stems': stem_counts.most_common(10),
    'preceding_role_distribution': prev_role.to_dict(),
    'following_role_distribution': next_role.to_dict(),
}
with open('../results/PILOT5_ain_subfolio_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\n\nSaved: PILOT5_ain_subfolio_results.json")
print("\n" + "="*70)
print("PILOT5 COMPLETE")
print("="*70)
