"""
PILOT3 — qol/ol Inner-Packet Doublet Test
Phase 2 Step 6

Tests whether qol appears inside packets at elevated rate relative to shuffled baseline.
If qol = inner-packet function word (content-layer doublet of structural ol):
  → qol should appear between R1 and R2 tokens (inside packets) more than chance
  → qol should NOT appear at paragraph boundaries
  → qol + ol on the same paragraph: more than chance?

Also tests kal, kol variants.

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import permutation_test, mannwhitneyu
import random

random.seed(42)
np.random.seed(42)

df = pd.read_csv("D1_corpus/corpus_tokens.csv")
struct_df = pd.read_csv("P1_structural/p1_1_cluster_frequencies.csv")
STRUCT = set(struct_df['cluster'].tolist())
role_map = dict(zip(struct_df['cluster'], struct_df['role']))

LAYER2_CANDIDATES = ['qol', 'kal', 'kol', 'okol']
TARGET = 'qol'
STRUCTURAL_OL = 'ol'  # R6 token

print("="*70)
print("PILOT3: qol/ol Inner-Packet Doublet Test")
print("="*70)

# ── 1. Packet detection: find all [R1 ... R2] spans ────────────────────────
df_sorted = df.sort_values(['folio_id', 'paragraph_id', 'line_id', 'token_index'])

print("\n1. PACKET DETECTION")
print("="*70)

packets = []
para_groups = df_sorted.groupby(['folio_id', 'paragraph_id'])

for (folio, para), grp in para_groups:
    toks = grp['token'].tolist()
    sections = grp['section'].tolist()
    section = sections[0] if sections else '?'
    n = len(toks)
    i = 0
    while i < n:
        if role_map.get(toks[i]) == 'INIT':
            # find next CLOSE
            j = i + 1
            while j < n and role_map.get(toks[j]) != 'CLOSE':
                j += 1
            if j < n and role_map.get(toks[j]) == 'CLOSE':
                packet_tokens = toks[i:j+1]
                payload = toks[i+1:j]  # between R1 and R2
                packets.append({
                    'folio': folio, 'para': para, 'section': section,
                    'start': i, 'end': j, 'length': j-i+1,
                    'r1': toks[i], 'r2': toks[j],
                    'payload': payload,
                    'has_qol': TARGET in payload,
                    'has_ol': STRUCTURAL_OL in payload,
                    'has_qol_ol_both': TARGET in payload and STRUCTURAL_OL in payload,
                })
                i = j + 1
            else:
                i += 1
        else:
            i += 1

print(f"Total complete packets detected: {len(packets)}")
packets_with_qol = [p for p in packets if p['has_qol']]
packets_with_ol = [p for p in packets if p['has_ol']]
packets_with_both = [p for p in packets if p['has_qol_ol_both']]

print(f"Packets containing qol: {len(packets_with_qol)} ({len(packets_with_qol)/max(len(packets),1)*100:.1f}%)")
print(f"Packets containing ol (structural): {len(packets_with_ol)} ({len(packets_with_ol)/max(len(packets),1)*100:.1f}%)")
print(f"Packets containing both qol + ol: {len(packets_with_both)}")

# ── 2. Position of qol within packets ──────────────────────────────────────
print("\n2. qol POSITION WITHIN PACKETS")
print("="*70)

qol_positions_relative = []  # relative position (0=start, 1=end of payload)
for p in packets_with_qol:
    payload = p['payload']
    if TARGET in payload:
        idx = payload.index(TARGET)
        rel = idx / max(len(payload)-1, 1) if len(payload) > 1 else 0.5
        qol_positions_relative.append(rel)

if qol_positions_relative:
    print(f"\nqol relative position in payload (0=start, 1=end):")
    print(f"  Mean: {np.mean(qol_positions_relative):.3f}")
    print(f"  Median: {np.median(qol_positions_relative):.3f}")
    print(f"  Uniform expectation: 0.500")
    # Test: is qol biased toward start or end?
    from scipy.stats import ttest_1samp
    t, p_val = ttest_1samp(qol_positions_relative, 0.5)
    print(f"  t-test vs 0.5: t={t:.3f}, p={p_val:.4f}")
    print(f"  → qol {'biased toward START' if np.mean(qol_positions_relative)<0.45 else 'biased toward END' if np.mean(qol_positions_relative)>0.55 else 'CENTRAL (no bias)'}")

# ── 3. Is qol inside packets MORE than expected by chance? ─────────────────
print("\n3. WITHIN-PACKET RATE vs SHUFFLED BASELINE")
print("="*70)

# Compute qol occurrence rate inside vs outside packets
all_packet_tokens = set()
packet_payload_positions = set()
for i, p in enumerate(packets):
    grp = df_sorted.groupby(['folio_id','paragraph_id']).get_group((p['folio'], p['para']))
    indices = list(grp.index)
    for offset in range(p['start']+1, p['end']):  # +1/-1 to exclude R1/R2
        if offset < len(indices):
            packet_payload_positions.add(indices[offset])

total_payload_tokens = len(packet_payload_positions)
qol_df = df_sorted[df_sorted['token'] == TARGET]
qol_in_payload = sum(1 for idx in qol_df.index if idx in packet_payload_positions)
qol_total = len(qol_df)
qol_outside = qol_total - qol_in_payload

expected_in_payload = qol_total * (total_payload_tokens / max(len(df_sorted), 1))

print(f"\nTotal corpus tokens: {len(df_sorted)}")
print(f"Tokens inside packet payloads: {total_payload_tokens} ({total_payload_tokens/len(df_sorted)*100:.1f}%)")
print(f"qol total: {qol_total}")
print(f"qol inside packet payloads: {qol_in_payload}")
print(f"qol outside packets: {qol_outside}")
print(f"Expected inside (if random): {expected_in_payload:.1f}")
if expected_in_payload > 0:
    enrichment = qol_in_payload / expected_in_payload
    print(f"Enrichment ratio: {enrichment:.2f}×")
    print(f"→ qol is {'ELEVATED' if enrichment>1.2 else 'DEPLETED' if enrichment<0.8 else 'at baseline'} inside packet payloads")

# ── 4. Section breakdown of qol in packets ─────────────────────────────────
print("\n4. qol-CONTAINING PACKETS BY SECTION")
print("="*70)

section_counts = Counter(p['section'] for p in packets_with_qol)
for sec, n in sorted(section_counts.items(), key=lambda x: -x[1]):
    print(f"  Section {sec}: {n} packets with qol")

# ── 5. qol vs ol co-occurrence at paragraph level ──────────────────────────
print("\n5. qol + ol SAME-PARAGRAPH CO-OCCURRENCE")
print("="*70)

para_tokens = df.groupby(['folio_id','paragraph_id'])['token'].apply(list)
paras_with_qol = sum(1 for toks in para_tokens if TARGET in toks)
paras_with_ol = sum(1 for toks in para_tokens if STRUCTURAL_OL in toks)
paras_with_both = sum(1 for toks in para_tokens if TARGET in toks and STRUCTURAL_OL in toks)
total_paras = len(para_tokens)

# Fisher exact
from scipy.stats import fisher_exact
table = [[paras_with_both, paras_with_qol - paras_with_both],
         [paras_with_ol - paras_with_both, total_paras - paras_with_qol - paras_with_ol + paras_with_both]]
odds, p_fisher = fisher_exact(table, alternative='greater')

print(f"\nTotal paragraphs: {total_paras}")
print(f"Paragraphs with qol: {paras_with_qol}")
print(f"Paragraphs with ol (structural): {paras_with_ol}")
print(f"Paragraphs with BOTH: {paras_with_both}")
print(f"Fisher exact (one-tailed, greater): OR={odds:.3f}, p={p_fisher:.4f}")
if p_fisher < 0.05:
    print(f"→ qol and ol co-occur at SIGNIFICANTLY ELEVATED rate in same paragraphs (p={p_fisher:.4f})")
else:
    print(f"→ qol/ol paragraph co-occurrence not significantly elevated (p={p_fisher:.4f})")

# ── 6. Variant comparison inside packets ───────────────────────────────────
print("\n6. LAYER 2 VARIANTS — WITHIN-PACKET RATE COMPARISON")
print("="*70)
print(f"\n{'Token':<10} {'total':>6} {'in_payload':>12} {'rate':>8} {'vs_baseline':>12}")
print("-"*55)
for tok in LAYER2_CANDIDATES:
    tok_rows = df_sorted[df_sorted['token'] == tok]
    tok_in = sum(1 for idx in tok_rows.index if idx in packet_payload_positions)
    tok_total = len(tok_rows)
    rate = tok_in / max(tok_total, 1)
    baseline = total_payload_tokens / len(df_sorted)
    vs_b = rate / baseline if baseline > 0 else 0
    print(f"  {tok:<10} {tok_total:>6}  {tok_in:>10}  {rate:>8.3f}  {vs_b:>10.2f}×")

# Also structural ol for comparison
tok_rows = df_sorted[df_sorted['token'] == STRUCTURAL_OL]
tok_in = sum(1 for idx in tok_rows.index if idx in packet_payload_positions)
tok_total = len(tok_rows)
rate = tok_in / max(tok_total, 1)
baseline = total_payload_tokens / len(df_sorted)
vs_b = rate / baseline if baseline > 0 else 0
print(f"  {'ol (struct)':<10} {tok_total:>6}  {tok_in:>10}  {rate:>8.3f}  {vs_b:>10.2f}× [reference]")

# ── Summary ─────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("VERDICT SUMMARY")
print("="*70)

results = {
    'total_packets': len(packets),
    'packets_with_qol': len(packets_with_qol),
    'packets_with_ol': len(packets_with_ol),
    'packets_with_both': len(packets_with_both),
    'qol_total': qol_total,
    'qol_in_payload': qol_in_payload,
    'qol_expected_in_payload': round(expected_in_payload, 2),
    'qol_payload_enrichment': round(qol_in_payload / max(expected_in_payload, 0.001), 3),
    'qol_ol_fisher_p': round(p_fisher, 4),
    'qol_ol_fisher_or': round(odds, 3),
    'qol_mean_relative_position': round(np.mean(qol_positions_relative), 3) if qol_positions_relative else None,
    'total_paragraphs': total_paras,
    'paras_with_both_qol_ol': paras_with_both,
}

with open('PILOT3_qol_ol_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nPackets detected: {len(packets)}")
print(f"qol within-packet enrichment: {results['qol_payload_enrichment']:.2f}×")
print(f"qol+ol paragraph co-occurrence: p={p_fisher:.4f}")
print(f"\nConclusion: qol behaves as {'an INNER-PACKET function word (elevated inside payloads)' if results['qol_payload_enrichment'] > 1.2 else 'NOT preferentially inside packets — Layer 2 status uncertain'}")
print("\nSaved: PILOT3_qol_ol_results.json")
