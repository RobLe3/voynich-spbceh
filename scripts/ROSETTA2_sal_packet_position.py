"""
ROSETTA2 — sal Packet-Internal Position Analysis

Questions:
1. What packet-internal position does `sal` occupy (early/mid/late)?
2. Is sal consistently in entity-subject slot (first R4 in payload)?
3. What tokens immediately precede and follow sal (bigram context)?
4. How does sal compare to calibration tokens (qol, daiin, oly)?
5. Does the sal-family (sal, saly, salar, sal!) collectively show position bias?
6. Does sal appear near R1 (packet start) or R2 (packet end)?
7. What is sal's section breakdown and folio distribution?

Method:
- Reconstruct packets from paragraph-level role sequences
- Assign each token within a packet a relative position (0.0 = first token, 1.0 = last token)
- Compare sal's mean relative position with calibration tokens
- Test position bias with t-test (null: mean = 0.5, i.e., no positional preference)

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import ttest_1samp, fisher_exact, mannwhitneyu

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("../data/corpus_tokens.csv")
roles_df = pd.read_csv("../results/p1_1_cluster_frequencies.csv")

# Build token → role mapping
role_map = dict(zip(roles_df['cluster'], roles_df['role']))

# Assign roles to corpus tokens
df['role'] = df['token'].map(role_map).fillna('CONTENT')

R1_TOKENS = set(roles_df[roles_df['role'] == 'INIT']['cluster'])
R2_TOKENS = set(roles_df[roles_df['role'] == 'CLOSE']['cluster'])
R6_TOKENS = set(roles_df[roles_df['role'] == 'REF']['cluster'])

TARGET = 'sal'
SAL_FAMILY = {'sal', 'sal!', 'saly', 'salar', 'saldy', 'salkeedy', 'saldam', 'salal', 'salo'}
CALIBRATION = ['qol', 'daiin', 'ol', 'aiin', 'chedy', 'shedy']

print("=" * 70)
print("ROSETTA2 — sal Packet-Internal Position Analysis")
print("=" * 70)

# ── 1. Basic section distribution ─────────────────────────────────────────────
print("\n1. SAL SECTION DISTRIBUTION")
print("-" * 40)
sal_df = df[df['token'] == TARGET].copy()
total_by_section = df.groupby('section').size()
sal_by_section = sal_df.groupby('section').size()
baseline_rates = (sal_by_section / total_by_section).fillna(0)
overall_rate = len(sal_df) / len(df)

print(f"  Total `sal` occurrences: {len(sal_df)}")
print(f"  Overall corpus rate: {overall_rate:.4f} ({overall_rate*100:.2f}%)")
print(f"\n  {'Section':<10} {'n_sal':>6} {'n_total':>8} {'rate':>8} {'enrichment':>12}")
print("  " + "-" * 50)
for sec in sorted(total_by_section.index):
    n_sal = sal_by_section.get(sec, 0)
    n_total = total_by_section[sec]
    rate = n_sal / n_total
    enrich = rate / overall_rate if overall_rate > 0 else 0
    print(f"  {sec:<10} {n_sal:>6} {n_total:>8} {rate:>8.4f} {enrich:>10.2f}×")

_b_sal   = sal_by_section.get('B', 0)
_b_total = total_by_section.get('B', 1)
_b_rate  = _b_sal / _b_total if _b_total > 0 else 0
sal_B_enrichment = _b_rate / overall_rate if overall_rate > 0 else None

# ── 2. Reconstruct packets within paragraphs ──────────────────────────────────
print("\n\n2. PACKET RECONSTRUCTION & sal POSITION WITHIN PACKETS")
print("-" * 60)

# Sort corpus by folio, paragraph, token_index
df_sorted = df.sort_values(['folio_id', 'paragraph_id', 'token_index']).copy()

# For each paragraph, extract R1→payload→R2 sequences
packets = []  # list of dicts: {folio, para, section, tokens, roles, positions}

for (folio, para_id), grp in df_sorted.groupby(['folio_id', 'paragraph_id']):
    toks = grp['token'].tolist()
    tok_roles = grp['role'].tolist()
    section = grp['section'].iloc[0]

    # Slide through looking for R1...R2 spans
    i = 0
    while i < len(toks):
        if tok_roles[i] == 'INIT':
            # Found R1 start — scan forward for R2
            j = i + 1
            while j < len(toks) and tok_roles[j] != 'CLOSE':
                j += 1
            if j < len(toks) and tok_roles[j] == 'CLOSE':
                # Found complete packet R1[i]..R2[j]
                payload_toks = toks[i+1:j]  # between R1 and R2
                payload_roles = tok_roles[i+1:j]
                packets.append({
                    'folio': folio,
                    'para_id': para_id,
                    'section': section,
                    'r1': toks[i],
                    'r2': toks[j],
                    'payload': payload_toks,
                    'payload_roles': payload_roles,
                    'payload_len': len(payload_toks)
                })
                i = j + 1
            else:
                i += 1
        else:
            i += 1

print(f"  Complete packets reconstructed: {len(packets)}")
packets_with_payload = [p for p in packets if p['payload_len'] > 0]
print(f"  Packets with non-empty payload: {len(packets_with_payload)}")

# ── 3. sal position within packet payloads ────────────────────────────────────
print("\n\n3. sal RELATIVE POSITION WITHIN PACKET PAYLOADS")
print("-" * 60)

def get_positions_in_packets(token_set, packets, mode='exact'):
    """Get relative positions of token(s) within packet payloads."""
    positions = []
    packet_contexts = []
    for p in packets:
        if p['payload_len'] == 0:
            continue
        payload = p['payload']
        for idx, tok in enumerate(payload):
            if (mode == 'exact' and tok in token_set) or \
               (mode == 'prefix' and any(tok.startswith(pref) for pref in token_set)):
                rel_pos = idx / (p['payload_len'] - 1) if p['payload_len'] > 1 else 0.5
                positions.append(rel_pos)
                packet_contexts.append({
                    'folio': p['folio'],
                    'section': p['section'],
                    'token': tok,
                    'rel_pos': rel_pos,
                    'payload': payload,
                    'payload_len': p['payload_len'],
                    'r1': p['r1'],
                    'r2': p['r2']
                })
    return positions, packet_contexts

sal_positions, sal_contexts = get_positions_in_packets({TARGET}, packets)
sal_family_positions, _ = get_positions_in_packets(SAL_FAMILY, packets)

print(f"\n  `sal` found in {len(sal_positions)} packet payloads")
if sal_positions:
    mean_pos = np.mean(sal_positions)
    std_pos = np.std(sal_positions)
    t_stat, p_val = ttest_1samp(sal_positions, 0.5)
    print(f"  Mean relative position: {mean_pos:.3f} (0.0=first, 1.0=last)")
    print(f"  Std deviation: {std_pos:.3f}")
    print(f"  t-test vs 0.5 (no bias): t={t_stat:.3f}, p={p_val:.4f}")

    # Quartile breakdown
    early = sum(1 for p in sal_positions if p < 0.33)
    mid   = sum(1 for p in sal_positions if 0.33 <= p <= 0.67)
    late  = sum(1 for p in sal_positions if p > 0.67)
    print(f"\n  Position distribution:")
    print(f"    Early (0–33%):  {early:3d} ({early/len(sal_positions)*100:.1f}%)")
    print(f"    Mid   (33–67%): {mid:3d} ({mid/len(sal_positions)*100:.1f}%)")
    print(f"    Late  (67–100%): {late:3d} ({late/len(sal_positions)*100:.1f}%)")

print(f"\n  sal-FAMILY (n={len(sal_family_positions)}) mean position: "
      f"{np.mean(sal_family_positions):.3f}" if sal_family_positions else "  sal-family: no packets")

# ── 4. Calibration comparison ─────────────────────────────────────────────────
print("\n\n4. CALIBRATION: POSITION COMPARISON ACROSS CANDIDATE TOKENS")
print("-" * 60)
print(f"\n  {'Token':<15} {'n_in_pkts':>10} {'mean_pos':>10} {'p_vs_0.5':>10} {'interpretation':>20}")
print("  " + "-" * 70)

all_token_positions = {}
for tok in [TARGET] + CALIBRATION:
    positions, _ = get_positions_in_packets({tok}, packets)
    if len(positions) >= 5:
        mean_p = np.mean(positions)
        _, p_val = ttest_1samp(positions, 0.5)
        if mean_p < 0.35:
            interp = 'EARLY (entity-lead)'
        elif mean_p > 0.65:
            interp = 'LATE (entity-tail)'
        else:
            interp = 'CENTRAL (no bias)'
        sig = '***' if p_val < 0.001 else ('**' if p_val < 0.01 else ('*' if p_val < 0.05 else 'ns'))
        print(f"  {tok:<15} {len(positions):>10} {mean_p:>10.3f} {p_val:>8.4f} {sig}  {interp}")
        all_token_positions[tok] = positions
    else:
        print(f"  {tok:<15} {len(positions):>10}  {'<5 obs — skip':>30}")

# ── 5. Bigram context: what immediately precedes/follows sal? ─────────────────
print("\n\n5. BIGRAM CONTEXT: IMMEDIATE NEIGHBORS OF sal")
print("-" * 60)

df_sorted2 = df.sort_values(['folio_id', 'paragraph_id', 'token_index']).copy()
df_sorted2['prev_tok'] = df_sorted2.groupby(['folio_id', 'paragraph_id'])['token'].shift(1)
df_sorted2['next_tok'] = df_sorted2.groupby(['folio_id', 'paragraph_id'])['token'].shift(-1)
df_sorted2['prev_role'] = df_sorted2.groupby(['folio_id', 'paragraph_id'])['role'].shift(1)
df_sorted2['next_role'] = df_sorted2.groupby(['folio_id', 'paragraph_id'])['role'].shift(-1)

sal_bigram = df_sorted2[df_sorted2['token'] == TARGET].copy()

print(f"\n  n={len(sal_bigram)} sal occurrences with bigram context\n")

prev_toks = sal_bigram['prev_tok'].dropna().value_counts().head(10)
next_toks = sal_bigram['next_tok'].dropna().value_counts().head(10)
prev_roles = sal_bigram['prev_role'].dropna().value_counts()
next_roles = sal_bigram['next_role'].dropna().value_counts()

print("  PRECEDING TOKENS (top 10):")
for tok, n in prev_toks.items():
    role = role_map.get(tok, 'CONTENT')
    print(f"    {tok:<20} n={n:3d}  [{role}]")

print("\n  FOLLOWING TOKENS (top 10):")
for tok, n in next_toks.items():
    role = role_map.get(tok, 'CONTENT')
    print(f"    {tok:<20} n={n:3d}  [{role}]")

print("\n  PRECEDING ROLE DISTRIBUTION:")
for role, n in prev_roles.items():
    print(f"    {role:<15} n={n}")

print("\n  FOLLOWING ROLE DISTRIBUTION:")
for role, n in next_roles.items():
    print(f"    {role:<15} n={n}")

# ── 6. Section B only — detailed packet listing ───────────────────────────────
print("\n\n6. FULL PACKET LISTING: sal IN BALNEOLOGICAL SECTION")
print("-" * 60)

b_sal_contexts = [c for c in sal_contexts if c['section'] == 'B']
print(f"\n  {len(b_sal_contexts)} sal occurrences inside packets in section B:\n")

for ctx in b_sal_contexts:
    payload_annotated = []
    for tok in ctx['payload']:
        role = role_map.get(tok, 'CONTENT')
        if tok == TARGET:
            payload_annotated.append(f"**{tok}**")
        elif role in ('INIT','CLOSE','REF'):
            payload_annotated.append(f"[{tok}]")
        else:
            payload_annotated.append(tok)
    payload_str = ' '.join(payload_annotated)
    print(f"  {ctx['folio']:8s} pos={ctx['rel_pos']:.2f}  "
          f"{ctx['r1']} | {payload_str} | {ctx['r2']}")

# ── 7. sal vs NOT-sal packet-payload enrichment ───────────────────────────────
print("\n\n7. sal PACKET-PAYLOAD ENRICHMENT (replication of PILOT3 method)")
print("-" * 60)

# Total corpus token count
n_total = len(df)
# How many are in packet payloads?
payload_token_set = set()
packet_payload_tokens = []
for p in packets:
    for tok in p['payload']:
        packet_payload_tokens.append(tok)

n_in_payload = len(packet_payload_tokens)
payload_rate = n_in_payload / n_total
sal_in_payload = packet_payload_tokens.count(TARGET)
sal_total = len(sal_df)
sal_payload_rate = sal_in_payload / sal_total if sal_total > 0 else 0
sal_enrichment = sal_payload_rate / payload_rate if payload_rate > 0 else 0

print(f"\n  Corpus tokens in packet payloads: {n_in_payload} / {n_total} ({payload_rate*100:.1f}%)")
print(f"  sal in packet payloads: {sal_in_payload} / {sal_total} ({sal_payload_rate*100:.1f}%)")
print(f"  sal payload enrichment: {sal_enrichment:.2f}×")

# Calibration: qol should be ~1.39×, ol ~1.41×
for tok in ['qol', 'ol', 'daiin', 'chedy']:
    tok_total = (df['token'] == tok).sum()
    tok_in_payload = packet_payload_tokens.count(tok)
    if tok_total > 0:
        tok_rate = tok_in_payload / tok_total
        enrich = tok_rate / payload_rate if payload_rate > 0 else 0
        print(f"  {tok:<15} payload enrichment: {enrich:.2f}×  "
              f"(n_payload={tok_in_payload}, n_total={tok_total})")

# ── 8. Folio distribution of sal in section B ────────────────────────────────
print("\n\n8. sal FOLIO DISTRIBUTION IN BALNEOLOGICAL SECTION")
print("-" * 60)

b_sal_df = sal_df[sal_df['section'] == 'B']
folio_counts = b_sal_df['folio_id'].value_counts().sort_index()
print(f"\n  {len(folio_counts)} folios with sal in section B:")
for folio, n in folio_counts.items():
    print(f"    {folio}: n={n}")

# ── 9. Morphological family enrichment ───────────────────────────────────────
print("\n\n9. sal MORPHOLOGICAL FAMILY — COMBINED ANALYSIS")
print("-" * 60)

sal_fam_df = df[df['token'].isin(SAL_FAMILY)]
print(f"\n  sal-family tokens ({', '.join(sorted(SAL_FAMILY))}):")
print(f"  Total occurrences: {len(sal_fam_df)}")
for tok in sorted(SAL_FAMILY):
    n = (df['token'] == tok).sum()
    if n > 0:
        secs = df[df['token'] == tok]['section'].value_counts().to_dict()
        print(f"    {tok:<15} n={n:3d}  {secs}")

fam_by_section = sal_fam_df.groupby('section').size()
print(f"\n  Family section distribution:")
for sec in sorted(total_by_section.index):
    n_fam = fam_by_section.get(sec, 0)
    n_total_sec = total_by_section[sec]
    rate = n_fam / n_total_sec
    enrich = rate / (len(sal_fam_df) / n_total)
    print(f"    {sec}: n={n_fam:3d} / {n_total_sec:5d}  ({rate*100:.2f}%)  enrich={enrich:.2f}×")

# ── 10. Save results ──────────────────────────────────────────────────────────
results = {
    'sal_total': int(sal_total),
    'sal_section_distribution': sal_by_section.to_dict(),
    'n_packets_reconstructed': len(packets),
    'sal_in_payload_n': int(sal_in_payload),
    'sal_payload_enrichment': float(sal_enrichment),
    'sal_positions_in_packets': sal_positions,
    'sal_mean_position': float(np.mean(sal_positions)) if sal_positions else None,
    'sal_position_p_value': float(ttest_1samp(sal_positions, 0.5)[1]) if len(sal_positions) >= 2 else None,
    'sal_family_members': sorted(SAL_FAMILY),
    'sal_family_total': int(len(sal_fam_df)),
    'top_preceding_tokens': prev_toks.to_dict(),
    'top_following_tokens': next_toks.to_dict(),
    'preceding_role_distribution': prev_roles.to_dict(),
    'following_role_distribution': next_roles.to_dict(),
    'sal_B_section_enrichment': float(sal_B_enrichment) if sal_B_enrichment else None,
}

with open('../results/ROSETTA2_sal_packet_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n\nSaved: ROSETTA2_sal_packet_results.json")
print("\n" + "="*70)
print("ROSETTA2 COMPLETE")
print("="*70)
