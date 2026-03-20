"""
PILOT4 — Balneological Packet Structure Analysis

Questions:
1. Does section B have a preferred R1 (INIT) token? (qokain hypothesis)
2. Does section B have a preferred R2 (CLOSE) token? (shedy vs chedy)
3. What tokens occupy the first-payload slot (entity-subject position) in B packets?
4. How does B packet internal structure differ from other sections?
5. What is the co-occurrence structure of top B-enriched tokens?
6. Are there recurring sub-packet templates (R1 + first_payload + R2 triplets)?

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import chi2_contingency, fisher_exact

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("../data/corpus_tokens.csv")
roles_df = pd.read_csv("../results/p1_1_cluster_frequencies.csv")
role_map = dict(zip(roles_df['cluster'], roles_df['role']))
df['role'] = df['token'].map(role_map).fillna('CONTENT')

SECTIONS = ['H', 'A', 'B', 'P', 'S']
TARGET_SECTION = 'B'

print("=" * 70)
print("PILOT4 — Balneological Packet Structure Analysis")
print("=" * 70)

# ── Reconstruct packets (full corpus, section-tagged) ────────────────────────
df_sorted = df.sort_values(['folio_id', 'paragraph_id', 'token_index']).copy()

packets = []
for (folio, para_id), grp in df_sorted.groupby(['folio_id', 'paragraph_id']):
    toks = grp['token'].tolist()
    tok_roles = grp['role'].tolist()
    section = grp['section'].iloc[0]
    i = 0
    while i < len(toks):
        if tok_roles[i] == 'INIT':
            j = i + 1
            while j < len(toks) and tok_roles[j] != 'CLOSE':
                j += 1
            if j < len(toks) and tok_roles[j] == 'CLOSE':
                payload = toks[i+1:j]
                payload_roles = tok_roles[i+1:j]
                packets.append({
                    'folio': folio,
                    'para_id': para_id,
                    'section': section,
                    'r1': toks[i],
                    'r2': toks[j],
                    'payload': payload,
                    'payload_roles': payload_roles,
                    'payload_len': len(payload),
                    'first_payload': payload[0] if payload else None,
                    'last_payload': payload[-1] if payload else None,
                })
                i = j + 1
            else:
                i += 1
        else:
            i += 1

print(f"\n  Total packets reconstructed: {len(packets)}")
for sec in SECTIONS:
    n = sum(1 for p in packets if p['section'] == sec)
    print(f"    Section {sec}: {n} packets")

# ── 1. Preferred R1 token by section ─────────────────────────────────────────
print("\n\n1. R1 (INIT) TOKEN DISTRIBUTION BY SECTION")
print("-" * 60)

for sec in SECTIONS:
    sec_pkts = [p for p in packets if p['section'] == sec]
    if not sec_pkts:
        continue
    r1_counts = Counter(p['r1'] for p in sec_pkts)
    total = len(sec_pkts)
    print(f"\n  Section {sec} ({total} packets):")
    for tok, n in r1_counts.most_common(8):
        pct = n / total * 100
        print(f"    {tok:<20} {n:4d} ({pct:5.1f}%)")

# ── 2. Preferred R2 (CLOSE) token by section ─────────────────────────────────
print("\n\n2. R2 (CLOSE) TOKEN DISTRIBUTION BY SECTION")
print("-" * 60)

for sec in SECTIONS:
    sec_pkts = [p for p in packets if p['section'] == sec]
    if not sec_pkts:
        continue
    r2_counts = Counter(p['r2'] for p in sec_pkts)
    total = len(sec_pkts)
    print(f"\n  Section {sec} ({total} packets):")
    for tok, n in r2_counts.most_common(8):
        pct = n / total * 100
        print(f"    {tok:<20} {n:4d} ({pct:5.1f}%)")

# ── 3. First-payload token (entity-subject slot) by section ──────────────────
print("\n\n3. FIRST-PAYLOAD TOKEN (ENTITY-SUBJECT SLOT) BY SECTION")
print("-" * 60)

for sec in SECTIONS:
    sec_pkts = [p for p in packets if p['section'] == sec and p['payload_len'] > 0]
    if not sec_pkts:
        continue
    first_counts = Counter(p['first_payload'] for p in sec_pkts)
    total = len(sec_pkts)
    print(f"\n  Section {sec} ({total} packets with payload):")
    for tok, n in first_counts.most_common(10):
        pct = n / total * 100
        role = role_map.get(tok, 'CONTENT')
        print(f"    {tok:<20} {n:4d} ({pct:5.1f}%)  [{role}]")

# ── 4. B-section: is first-payload slot different from rest? ─────────────────
print("\n\n4. SECTION B FIRST-PAYLOAD: FREQUENCY VS REST OF CORPUS")
print("-" * 60)

b_first = Counter(p['first_payload'] for p in packets
                  if p['section'] == 'B' and p['payload_len'] > 0)
other_first = Counter(p['first_payload'] for p in packets
                      if p['section'] != 'B' and p['payload_len'] > 0)
n_b = sum(b_first.values())
n_other = sum(other_first.values())
all_first_toks = set(b_first.keys()) | set(other_first.keys())

print(f"\n  B first-payload tokens: {n_b} total")
print(f"  Other sections first-payload tokens: {n_other} total")
print(f"\n  {'Token':<20} {'n_B':>6} {'n_other':>8} {'B_rate':>8} {'OR':>8} {'p_fisher':>10}")
print("  " + "-" * 65)

enrichments = []
for tok in all_first_toks:
    n_b_tok = b_first.get(tok, 0)
    n_other_tok = other_first.get(tok, 0)
    if n_b_tok + n_other_tok < 3:
        continue
    a, b_val = n_b_tok, n_b - n_b_tok
    c, d = n_other_tok, n_other - n_other_tok
    OR = (a * d) / (b_val * c) if (b_val * c > 0) else float('inf')
    _, p = fisher_exact([[a, b_val], [c, d]], alternative='greater')
    enrichments.append((tok, n_b_tok, n_other_tok, a/n_b if n_b>0 else 0, OR, p))

enrichments.sort(key=lambda x: -x[4])
for tok, nb, no, rate, OR, p in enrichments[:15]:
    sig = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
    print(f"  {tok:<20} {nb:>6} {no:>8} {rate:>8.3f} {OR:>8.2f} {p:>9.5f} {sig}")

# ── 5. qokain-initiated packets: what is their internal structure? ────────────
print("\n\n5. qokain-INITIATED PACKET STRUCTURE (section B focus)")
print("-" * 60)

qokain_pkts = [p for p in packets if p['r1'] == 'qokain']
b_qokain_pkts = [p for p in qokain_pkts if p['section'] == 'B']
other_qokain_pkts = [p for p in qokain_pkts if p['section'] != 'B']

print(f"\n  Total qokain-initiated packets: {len(qokain_pkts)}")
print(f"  In section B: {len(b_qokain_pkts)}")
print(f"  In other sections: {len(other_qokain_pkts)}")

# What R2 closes qokain packets in B?
if b_qokain_pkts:
    r2_after_qokain = Counter(p['r2'] for p in b_qokain_pkts)
    print(f"\n  R2 tokens that close qokain packets in B:")
    for tok, n in r2_after_qokain.most_common():
        print(f"    {tok:<20} n={n}")

    # First-payload in qokain packets in B
    first_in_qokain = Counter(p['first_payload'] for p in b_qokain_pkts if p['payload_len'] > 0)
    print(f"\n  First-payload tokens in qokain+B packets:")
    for tok, n in first_in_qokain.most_common(10):
        role = role_map.get(tok, 'CONTENT')
        print(f"    {tok:<20} n={n}  [{role}]")

    # Full packet listing for B qokain packets (short ones)
    short_pkts = [p for p in b_qokain_pkts if 1 <= p['payload_len'] <= 8]
    print(f"\n  Short qokain+B packets (payload ≤8 tokens), n={len(short_pkts)}:")
    for p in short_pkts[:15]:
        payload_str = ' '.join(p['payload'])
        print(f"    {p['folio']:8s}  {p['r1']} | {payload_str} | {p['r2']}")

# ── 6. shedy vs chedy as R2 in section B ─────────────────────────────────────
print("\n\n6. shedy vs chedy AS SECTION-B CLOSE MARKERS")
print("-" * 60)

for r2_tok in ['shedy', 'chedy', 'shey', 'chey', 'lchedy']:
    pkts_with = [p for p in packets if p['r2'] == r2_tok]
    n_total = len(pkts_with)
    n_b = sum(1 for p in pkts_with if p['section'] == 'B')
    n_h = sum(1 for p in pkts_with if p['section'] == 'H')
    n_s = sum(1 for p in pkts_with if p['section'] == 'S')
    if n_total == 0: continue
    print(f"\n  R2={r2_tok} (n={n_total}): B={n_b}({n_b/n_total*100:.0f}%), "
          f"H={n_h}({n_h/n_total*100:.0f}%), S={n_s}({n_s/n_total*100:.0f}%)")
    # What R1 pairs with this R2?
    r1_for_r2 = Counter(p['r1'] for p in pkts_with[:])
    top_r1 = r1_for_r2.most_common(5)
    print(f"    Top R1 partners: " + ', '.join(f"{t}({n})" for t,n in top_r1))

# ── 7. Recurring packet templates (R1 + first_payload + R2) ──────────────────
print("\n\n7. RECURRING PACKET TEMPLATES: R1 + FIRST_PAYLOAD + R2")
print("-" * 60)

template_counts = Counter()
for p in packets:
    if p['payload_len'] > 0:
        template = (p['r1'], p['first_payload'], p['r2'])
        template_counts[template] += 1

print("\n  Top 20 recurring templates (R1, first_payload, R2):")
print(f"  {'R1':<20} {'First_payload':<20} {'R2':<15} {'n':>5} {'sections'}")
print("  " + "-" * 80)
for (r1, fp, r2), n in template_counts.most_common(20):
    # Which sections?
    secs = Counter(p['section'] for p in packets
                   if p['r1'] == r1 and p['first_payload'] == fp and p['r2'] == r2)
    sec_str = ', '.join(f"{s}:{c}" for s,c in secs.most_common())
    print(f"  {r1:<20} {fp:<20} {r2:<15} {n:>5}  [{sec_str}]")

# ── T3. INIT-bleed rates by section ──────────────────────────────────────────
init_bleed_by_section = {}
for _sec in ['B', 'S', 'H', 'A', 'P']:
    _sec_pkts = [p for p in packets if p['section'] == _sec]
    if _sec_pkts:
        _n_init_first = sum(1 for p in _sec_pkts
                            if p['payload_roles'] and p['payload_roles'][0] == 'INIT')
        init_bleed_by_section[_sec] = {
            'n_packets': len(_sec_pkts),
            'n_init_first': _n_init_first,
            'rate': _n_init_first / len(_sec_pkts),
        }

# ── T2. Nested packet test ────────────────────────────────────────────────────
_b_with_payload = [p for p in packets if p['section'] == 'B' and p['payload_len'] > 0]
_b_init_first   = [p for p in _b_with_payload
                   if p['payload_roles'] and p['payload_roles'][0] == 'INIT']
nested_n_init_first_B = len(_b_init_first)
nested_n_sub_close_B  = sum(1 for p in _b_init_first if 'CLOSE' in p['payload_roles'])

# ── 8. Save summary results ───────────────────────────────────────────────────
b_pkts = [p for p in packets if p['section'] == 'B']
b_r1 = Counter(p['r1'] for p in b_pkts)
b_r2 = Counter(p['r2'] for p in b_pkts)
b_first_payload = Counter(p['first_payload'] for p in b_pkts if p['payload_len'] > 0)

_qol_enr = next(((OR, p) for t, nb, no, _, OR, p in enrichments if t == 'qol'), (None, None))

results = {
    'total_packets': len(packets),
    'b_packets': len(b_pkts),
    'b_top_r1': b_r1.most_common(5),
    'b_top_r2': b_r2.most_common(5),
    'b_top_first_payload': b_first_payload.most_common(10),
    'qokain_b_packets': len(b_qokain_pkts),
    'top_b_enriched_first_payload': [(t, nb, no, OR) for t, nb, no, _, OR, p in enrichments[:10]],
    'qol_first_payload_OR':  float(_qol_enr[0]) if _qol_enr[0] is not None else None,
    'qol_first_payload_p':   float(_qol_enr[1]) if _qol_enr[1] is not None else None,
    # T2 — nested packet test
    'nested_n_init_first_B':       nested_n_init_first_B,
    'nested_n_sub_close_B':        nested_n_sub_close_B,
    # T3 — INIT-bleed by section
    'init_bleed_by_section':       {sec: {'n_packets': v['n_packets'],
                                          'n_init_first': v['n_init_first'],
                                          'rate': round(v['rate'], 4)}
                                    for sec, v in init_bleed_by_section.items()},
}

with open('../results/PILOT4_balneo_packet_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\n\nSaved: PILOT4_balneo_packet_results.json")
print("\n" + "="*70)
print("PILOT4 COMPLETE")
print("="*70)
