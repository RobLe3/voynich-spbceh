"""
ROSETTA3c — qotaiin Positional Analysis in Stars Packets + Consistent FSA Baseline

Uses ROSETTA2-consistent packet reconstruction (role_map from cluster_frequencies.csv).

Questions:
1. Does qotaiin occupy a consistent structural slot in Stars-section packets?
2. What is the pre-R2 baseline for ALL tokens in B-section packets (consistent method)?
3. Does sal's pre-R2 rate stand out relative to sol and other sl-tokens?
4. Positional analysis for top 10 Balneological payload tokens.
5. lkaiin positional analysis in Stars packets — EARLY or neutral?
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import ttest_1samp, mannwhitneyu
from pathlib import Path

# ── Load data ──────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results"

df = pd.read_csv(DATA_DIR / "corpus_tokens.csv")
roles_df = pd.read_csv(RESULTS_DIR / "p1_1_cluster_frequencies.csv")

# Role mapping from cluster analysis (consistent with ROSETTA2)
role_map = dict(zip(roles_df['cluster'], roles_df['role']))
df['role'] = df['token'].map(role_map).fillna('CONTENT')

R1_TOKENS = set(roles_df[roles_df['role'] == 'INIT']['cluster'])
R2_TOKENS = set(roles_df[roles_df['role'] == 'CLOSE']['cluster'])

print(f"R1 (INIT) tokens: {len(R1_TOKENS)} — {sorted(R1_TOKENS)[:8]}...")
print(f"R2 (CLOSE) tokens: {len(R2_TOKENS)} — {sorted(R2_TOKENS)[:8]}...")
print(f"Corpus: {len(df)} tokens")

# ── Packet reconstruction (ROSETTA2-consistent method) ─────────────────────────
def reconstruct_packets_for_section(section_code):
    """Reconstruct packets for a given section using role_map."""
    df_sec = df[df['section'] == section_code].sort_values(
        ['folio_id', 'paragraph_id', 'token_index']
    ).copy()

    packets = []
    for (folio, para_id), grp in df_sec.groupby(['folio_id', 'paragraph_id'], sort=False):
        tokens_list = grp['token'].tolist()
        roles_list = grp['role'].tolist()
        i = 0
        while i < len(tokens_list):
            tok = tokens_list[i]
            if tok in R1_TOKENS:
                j = i + 1
                while j < len(tokens_list) and tokens_list[j] not in R2_TOKENS:
                    j += 1
                if j < len(tokens_list):
                    payload = tokens_list[i+1:j]
                    packets.append({
                        'folio': folio,
                        'para': para_id,
                        'section': section_code,
                        'init': tok,
                        'payload': payload,
                        'close': tokens_list[j],
                        'payload_len': len(payload),
                    })
                    i = j + 1
                else:
                    i += 1
            else:
                i += 1
    return packets

# ============================================================
# 1. PACKET COUNTS BY SECTION (validation)
# ============================================================
print("\n\n1. PACKET COUNTS BY SECTION (ROSETTA2-consistent)")
print("=" * 60)

all_packets = {}
total_across_sections = 0
for sec in ['S', 'B', 'H', 'C', 'T', 'Z', 'F', 'P']:
    pkts = reconstruct_packets_for_section(sec)
    all_packets[sec] = pkts
    total_across_sections += len(pkts)
    sec_tokens = len(df[df['section'] == sec])
    print(f"  Section {sec}: {len(pkts)} packets, {sec_tokens} tokens")

print(f"  Total: {total_across_sections} packets")
print(f"  (ROSETTA2 reference: 897 packets total)")

# ============================================================
# 2. QOTAIIN POSITIONAL ANALYSIS IN STARS PACKETS
# ============================================================
print("\n\n2. QOTAIIN POSITIONAL ANALYSIS IN STARS PACKETS")
print("=" * 60)

stars_packets = all_packets.get('S', [])
print(f"  Stars section: {len(stars_packets)} packets")

TARGET = 'qotaiin'
target_positions = []
target_packets = []

for pkt in stars_packets:
    payload = pkt['payload']
    n = len(payload)
    for j, t in enumerate(payload):
        if t == TARGET:
            rel_pos = j / (n - 1) if n > 1 else 0.5
            target_positions.append(rel_pos)
            target_packets.append({**pkt, 'pos': rel_pos, 'idx': j, 'n': n})

print(f"  qotaiin occurrences in Stars payload: {len(target_positions)}")

if target_positions:
    mean_pos = np.mean(target_positions)
    t_stat, p_val = ttest_1samp(target_positions, 0.5)
    bias = "EARLY" if mean_pos < 0.45 else ("LATE" if mean_pos > 0.55 else "CENTRAL")
    print(f"  Mean position: {mean_pos:.3f} (0=first, 1=last in payload)")
    print(f"  t-test vs 0.5: t={t_stat:.3f}, p={p_val:.4f}")
    print(f"  Positional bias: {bias}")
    if p_val < 0.05:
        print(f"  → SIGNIFICANT: qotaiin is {bias}-biased in Stars packets")
    else:
        print(f"  → NOT significant (p >= 0.05) — no consistent positional slot")

    print(f"\n  All qotaiin packet occurrences in Stars:")
    for rec in target_packets:
        payload_str = ' '.join(
            f'[{t}]' if t == TARGET else t for t in rec['payload']
        )
        print(f"    {rec['folio']} pos={rec['pos']:.2f} ({rec['idx']}/{rec['n']-1}): "
              f"{rec['init']} | {payload_str[:80]}... | {rec['close']}")

# Compare to calibration tokens in Stars
print(f"\n  Calibration — Stars packet positions for top tokens:")
calibration_tokens = ['qokain', 'laiin', 'aiin', 'daiin', 'okaiin', 'lkaiin', 'qotaiin']
for cal_tok in calibration_tokens:
    positions = []
    for pkt in stars_packets:
        payload = pkt['payload']
        n = len(payload)
        for j, t in enumerate(payload):
            if t == cal_tok:
                rel_pos = j / (n - 1) if n > 1 else 0.5
                positions.append(rel_pos)
    if positions:
        mean_pos = np.mean(positions)
        t_stat, p_val = ttest_1samp(positions, 0.5) if len(positions) > 1 else (0, 1)
        sig = '*' if p_val < 0.05 else ' '
        bias = "EARLY" if mean_pos < 0.45 else ("LATE" if mean_pos > 0.55 else "CENTRAL")
        print(f"    {cal_tok:15s}: n={len(positions):3d} mean={mean_pos:.3f} "
              f"p={p_val:.4f}{sig} → {bias}")

# ============================================================
# 3. LKAIIN POSITIONAL ANALYSIS IN STARS PACKETS
# ============================================================
print("\n\n3. LKAIIN POSITIONAL ANALYSIS IN STARS PACKETS")
print("=" * 60)

LKAIIN = 'lkaiin'
lkaiin_positions = []
lkaiin_packets = []

for pkt in stars_packets:
    payload = pkt['payload']
    n = len(payload)
    for j, t in enumerate(payload):
        if t == LKAIIN:
            rel_pos = j / (n - 1) if n > 1 else 0.5
            lkaiin_positions.append(rel_pos)
            lkaiin_packets.append({**pkt, 'pos': rel_pos, 'idx': j, 'n': n})

print(f"  lkaiin occurrences in Stars payload: {len(lkaiin_positions)}")
if lkaiin_positions:
    mean_pos = np.mean(lkaiin_positions)
    t_stat, p_val = ttest_1samp(lkaiin_positions, 0.5) if len(lkaiin_positions) > 1 else (0, 1)
    bias = "EARLY" if mean_pos < 0.45 else ("LATE" if mean_pos > 0.55 else "CENTRAL")
    print(f"  Mean position: {mean_pos:.3f}, t={t_stat:.3f}, p={p_val:.4f}")
    print(f"  Positional bias: {bias}")
    sig_note = "SIGNIFICANT" if p_val < 0.05 else "NOT significant"
    print(f"  → {sig_note}")

# lkaiin section breakdown
print(f"\n  lkaiin section breakdown (cross-check):")
lkaiin_all = df[df['token'] == LKAIIN]
print(f"  Total corpus: {len(lkaiin_all)}")
for sec, grp in lkaiin_all.groupby('section'):
    pct = len(grp) / len(lkaiin_all) * 100
    print(f"    Section {sec}: {len(grp)} ({pct:.1f}%)")

# ============================================================
# 4. SAL TERMINAL RE-TEST (consistent FSA method)
# ============================================================
print("\n\n4. SAL TERMINAL RE-TEST — Consistent FSA Baseline")
print("=" * 60)

balneo_packets = all_packets.get('B', [])
print(f"  B-section packets: {len(balneo_packets)}")

# Collect all payload positions across B packets
pre_r2_counts = Counter()
payload_counts = Counter()

for pkt in balneo_packets:
    payload = pkt['payload']
    if not payload:
        continue
    for tok in payload:
        payload_counts[tok] += 1
    pre_r2_counts[payload[-1]] += 1  # last token immediately before R2

# Compute pre-R2 rates for tokens with >= 5 payload occurrences
pre_r2_rates = {}
for tok, cnt_pre in pre_r2_counts.items():
    cnt_total = payload_counts[tok]
    if cnt_total >= 5:
        pre_r2_rates[tok] = {
            'token': tok,
            'count_pre_r2': cnt_pre,
            'count_in_payload': cnt_total,
            'pre_r2_rate': cnt_pre / cnt_total
        }

all_rates_list = sorted(pre_r2_rates.values(), key=lambda x: -x['pre_r2_rate'])

baseline_rates = [v['pre_r2_rate'] for v in pre_r2_rates.values()]
baseline_mean = np.mean(baseline_rates)
baseline_p90 = np.percentile(baseline_rates, 90)
baseline_p95 = np.percentile(baseline_rates, 95)

print(f"\n  Total payload tokens analyzed: {sum(payload_counts.values())}")
print(f"  Unique tokens (freq >= 5): {len(pre_r2_rates)}")
print(f"  Baseline mean pre-R2 rate: {baseline_mean:.3f}")
print(f"  Baseline p90: {baseline_p90:.3f}")
print(f"  Baseline p95: {baseline_p95:.3f}")

print(f"\n  Top 25 by pre-R2 rate:")
print(f"  {'Token':15s} {'pre-R2':6s} {'total':6s} {'rate':8s} {'note'}")
for data in all_rates_list[:25]:
    tok = data['token']
    note = ''
    if tok == 'sal':
        note = '<-- SAL'
    elif tok.startswith('sol'):
        note = '<-- sol-family'
    elif tok in {'ol', 'al', 'or', 'ar'}:
        note = '<-- R6 structural'
    elif tok in R1_TOKENS:
        note = '<-- INIT'
    print(f"  {tok:15s} {data['count_pre_r2']:6d} {data['count_in_payload']:6d} "
          f"{data['pre_r2_rate']:8.3f}  {note}")

# sal vs sol specifically
sal_data = pre_r2_rates.get('sal')
sol_data = pre_r2_rates.get('sol')
print(f"\n  SAL vs SOL comparison:")
if sal_data:
    sal_pctile = sum(1 for r in baseline_rates if r > sal_data['pre_r2_rate']) / len(baseline_rates)
    print(f"  sal: {sal_data['pre_r2_rate']:.3f} ({sal_data['count_pre_r2']}/{sal_data['count_in_payload']}) — top {sal_pctile*100:.0f}%")
    print(f"  sal vs baseline mean: {sal_data['pre_r2_rate']/baseline_mean:.2f}×")
    print(f"  sal vs p90: {'ABOVE' if sal_data['pre_r2_rate'] > baseline_p90 else 'BELOW'}")
else:
    print(f"  sal: not in payload (freq < 5)")
if sol_data:
    sol_pctile = sum(1 for r in baseline_rates if r > sol_data['pre_r2_rate']) / len(baseline_rates)
    print(f"  sol: {sol_data['pre_r2_rate']:.3f} ({sol_data['count_pre_r2']}/{sol_data['count_in_payload']}) — top {sol_pctile*100:.0f}%")
else:
    print(f"  sol: not in payload (freq < 5)")

# Sal-family together
sal_family = {tok for tok in payload_counts if tok.startswith('sal')}
print(f"\n  sl-family tokens in B payload: {sorted(sal_family)}")
for tok in sorted(sal_family):
    if tok in pre_r2_rates:
        d = pre_r2_rates[tok]
        print(f"  {tok:15s} rate={d['pre_r2_rate']:.3f} ({d['count_pre_r2']}/{d['count_in_payload']})")
    elif payload_counts.get(tok, 0) > 0:
        print(f"  {tok:15s} n_payload={payload_counts[tok]} (below freq threshold)")

# ============================================================
# 5. TOP-10 BALNEOLOGICAL PAYLOAD TOKENS — POSITIONAL BIAS
# ============================================================
print("\n\n5. TOP-10 BALNEOLOGICAL PAYLOAD TOKENS — POSITIONAL BIAS")
print("=" * 60)

# Collect positions for all tokens in B-packet payloads
token_positions_B = defaultdict(list)
for pkt in balneo_packets:
    payload = pkt['payload']
    n = len(payload)
    for j, t in enumerate(payload):
        rel_pos = j / (n - 1) if n > 1 else 0.5
        token_positions_B[t].append(rel_pos)

# Analyze top 20 by payload frequency
top_B_tokens = [tok for tok, _ in Counter(payload_counts).most_common(20)]
print(f"  {'Token':15s} {'n':5s} {'mean':6s} {'p':7s} {'bias':8s}")
print(f"  {'-'*15} {'-'*5} {'-'*6} {'-'*7} {'-'*8}")
results_by_token = {}
for tok in top_B_tokens:
    positions = token_positions_B.get(tok, [])
    if len(positions) < 5:
        continue
    mean_pos = np.mean(positions)
    t_stat, p_val = ttest_1samp(positions, 0.5)
    bias = "EARLY" if (mean_pos < 0.45 and p_val < 0.05) else \
           ("LATE" if (mean_pos > 0.55 and p_val < 0.05) else "CENTRAL")
    sig = '*' if p_val < 0.05 else ' '
    role = role_map.get(tok, 'CONTENT')
    print(f"  {tok:15s} {len(positions):5d} {mean_pos:6.3f} {p_val:7.4f}{sig} {bias:8s} [{role}]")
    results_by_token[tok] = {
        'n': len(positions), 'mean_pos': mean_pos, 'p': p_val, 'bias': bias
    }

# ============================================================
# 6. QOTAIIN SECTION BREAKDOWN AND FOLIO DISTRIBUTION
# ============================================================
print("\n\n6. QOTAIIN CORPUS PROFILE")
print("=" * 60)

qotaiin_df = df[df['token'] == 'qotaiin']
print(f"  Total qotaiin occurrences: {len(qotaiin_df)}")
print(f"  Section breakdown:")
total = len(qotaiin_df)
for sec, grp in qotaiin_df.groupby('section'):
    pct = len(grp) / total * 100
    print(f"    {sec}: {len(grp)} ({pct:.1f}%)")

print(f"\n  Folio distribution (top 10):")
for folio, grp in sorted(qotaiin_df.groupby('folio_id'),
                          key=lambda x: -len(x[1]))[:10]:
    print(f"    {folio}: {len(grp)}")

# Qotaiin positional analysis across ALL sections
print(f"\n  qotaiin positional bias by section (within packet payloads):")
for sec in ['S', 'B', 'H', 'C']:
    pkts = all_packets.get(sec, [])
    positions = []
    for pkt in pkts:
        payload = pkt['payload']
        n = len(payload)
        for j, t in enumerate(payload):
            if t == 'qotaiin':
                positions.append(j / (n - 1) if n > 1 else 0.5)
    if len(positions) >= 3:
        mean_pos = np.mean(positions)
        t_stat, p_val = ttest_1samp(positions, 0.5) if len(positions) > 1 else (0, 1)
        bias = "EARLY" if mean_pos < 0.45 else ("LATE" if mean_pos > 0.55 else "CENTRAL")
        sig = '*' if p_val < 0.05 else ' '
        print(f"    Section {sec}: n={len(positions):3d} mean={mean_pos:.3f} "
              f"p={p_val:.4f}{sig} → {bias}")
    elif positions:
        print(f"    Section {sec}: n={len(positions)} (too few for t-test)")

# ============================================================
# SAVE RESULTS
# ============================================================

output = {
    'packet_counts': {sec: len(pkts) for sec, pkts in all_packets.items()},
    'total_packets': total_across_sections,
    'qotaiin_stars': {
        'n': len(target_positions),
        'mean_position': float(np.mean(target_positions)) if target_positions else None,
        'p_vs_0.5': float(ttest_1samp(target_positions, 0.5)[1]) if len(target_positions) > 1 else None,
    },
    'lkaiin_stars': {
        'n': len(lkaiin_positions),
        'mean_position': float(np.mean(lkaiin_positions)) if lkaiin_positions else None,
        'p_vs_0.5': float(ttest_1samp(lkaiin_positions, 0.5)[1]) if len(lkaiin_positions) > 1 else None,
    },
    'sal_terminal': {
        'pre_r2_rate': sal_data['pre_r2_rate'] if sal_data else None,
        'count_pre_r2': sal_data['count_pre_r2'] if sal_data else None,
        'count_in_payload': sal_data['count_in_payload'] if sal_data else None,
        'baseline_mean': float(baseline_mean),
        'baseline_p90': float(baseline_p90),
        'baseline_p95': float(baseline_p95),
    },
    'top_B_positional_bias': results_by_token,
}

with open(RESULTS_DIR / "ROSETTA3c_qotaiin_positional_results.json", 'w') as f:
    json.dump(output, f, indent=2)

print("\n\nSaved: ROSETTA3c_qotaiin_positional_results.json")
print("\n" + "=" * 60)
print("ROSETTA3c COMPLETE")
print("=" * 60)
